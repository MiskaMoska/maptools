import os
import sys
import networkx as nx
from copy import deepcopy 
from graphviz import Digraph as GDG
from functools import cached_property
from typing import Any, List, Dict, Tuple, Optional, Generator
from maptools.core.typing import OperatorConfig
from maptools.core.proto import QuantConfig, NNModelArch
from maptools.core.common import ROOT_DIR, TRUNCATE_OPS

__all__ = [
    'OperatorGraph',
    'OriginGraph',
    'HostGraph',
    'DeviceGraph'
]

class OperatorGraph(object):

    def __init__(
        self, 
        graph: nx.MultiDiGraph, 
        dicts: Dict[str, OperatorConfig], 
        arch: NNModelArch,
        quantize: bool
        ) -> None:
        self.graph = deepcopy(graph)
        self.dicts = deepcopy(dicts)
        self.arch = arch
        self.quantize = quantize

    @property
    def trunk(self) -> List[str]:
        # Find and return the nodes in the trunk
        return list(nx.dag_longest_path(self.graph))

    @property
    def node_dicts(self) -> Generator[Dict, None, None]:
        for n in nx.topological_sort(self.graph):
            tmp = {'name':n}
            tmp.update(self.dicts[n])
            yield tmp

    @property
    def nodes(self) -> Generator[str, None, None]:
        yield from nx.topological_sort(self.graph)

    @property
    def egdes(self) -> Generator[Tuple, None, None]:
        yield from self.graph.edges

    @property
    def unique_input(self) -> str:
        return self.trunk[0]
    
    @property
    def unique_output(self) -> str:
        return self.trunk[-1]

    def config(self, node: str) -> OperatorConfig:
        return self.dicts[node]

    def in_degree(self, node: str) -> int:
        return self.graph.in_degree(node)
    
    def out_degree(self, node: str) -> int:
        return self.graph.in_degree(node)

    def preds(self, node: str) -> List[str]:
        return list(self.graph.predecessors(node))

    def succs(self, node: str) -> List[str]:
        return list(self.graph.successors(node))

    def unique_pred(self, node: str) -> str:
        # Get node's unique predecessor
        preds = self.preds(node)
        assert len(preds) == 1, "found multiple predecessors while assuming it to be unique"
        return preds[0]
    
    def unique_succ(self, node: str) -> str:
        # Get node's unique successor
        succs = self.succs(node)
        assert len(succs) == 1, "found multiple successors while assuming it to be unique"
        return succs[0]

    def op_type(self, node: str) -> str:
        # Get node's op_type
        return self.dicts[node]['op_type']

    def _exten_op_type(self, node: str, suffix: str) -> None:
        # Extend node's op_type
        self.dicts[node]['op_type'] += suffix

    def add_attr_to_node(self, node: str, key: Any, attr: Any) -> None:
        assert node in self.dicts, f"node {node} not exist in operator graph"
        self.dicts[node][key] = attr
        
    def plot_graph(self, save_dir: Optional[str] = None) -> None:
        dot = GDG('graph', format='svg')
        shape = 'box3d'
        labelloc = None
        for n in self.graph.nodes:
            dot.node(
                n,
                self.dicts[n]['op_type'], 
                shape=shape,
                labelloc=labelloc,
                fontname='Arial'
            )
        for e in self.graph.edges:
            dot.edge(e[0],e[1])
        if save_dir is None:
            save_dir = os.path.join(ROOT_DIR, 'mapsave', 'operator_graph')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        dot.view(cleanup=True, directory=save_dir)
        print(f"graph saved to {save_dir}")


class OriginGraph(OperatorGraph):

    def _dfs_cut(
        self, 
        graph: nx.MultiDiGraph, 
        host_nodes: List[str], 
        current_node: str
    ) -> None:
        host_nodes.append(current_node)
        for node in graph.predecessors(current_node):
            if self.op_type(node) in TRUNCATE_OPS:
                if graph.in_degree(current_node) > 1 or graph.out_degree(node) > 1:
                    raise AssertionError(
                        f"truncate node {node} must has one-to-one connection with its successor {current_node}")
                graph.remove_edge(node, current_node)
                return
        
        for node in graph.predecessors(current_node):
            self._dfs_cut(graph, host_nodes, node)

    def dispatch_graph(self) -> Tuple['HostGraph', 'DeviceGraph']:
        '''
        Dispatch the operator graph into host graph and device graph
        '''
        host_nodes = []
        device_pure_graph = deepcopy(self.graph)

        self._dfs_cut(device_pure_graph, host_nodes, self.unique_output)
        device_pure_graph.remove_nodes_from(host_nodes)
        host_pure_graph = self.graph.subgraph(host_nodes)
        device_dicts = deepcopy(self.dicts)
        host_dicts = {n: device_dicts.pop(n) for n in host_nodes}

        host_graph = HostGraph(host_pure_graph, host_dicts, self.arch, self.quantize)
        device_graph = DeviceGraph(device_pure_graph, device_dicts, self.arch, self.quantize)

        return host_graph, device_graph


class HostGraph(OperatorGraph): ...


class DeviceGraph(OperatorGraph):

    @cached_property
    def input_output_quant_config(self) -> Optional[Tuple[QuantConfig, QuantConfig]]:
        nodes = list(self.nodes)
        head_node, tail_node = nodes[0], nodes[-1]
        head_config, tail_config = self.config(head_node), self.config(tail_node)

        if self.quantize:
            head_quant_config = head_config['conv_quant_config']
            tail_name = 'conv_'
            if 'Act' in self.op_type(tail_node):
                tail_name = 'add_'
            elif 'Add' in self.op_type(tail_node):
                tail_name = 'relu_'
            tail_quant_config = tail_config[tail_name + 'quant_config']
            return head_quant_config, tail_quant_config
        
    def _fuse_config(self, snode: str, dnode: str) -> None:
        # Fuse one operator to another
        tmp = deepcopy(self.dicts[snode])
        tmp.pop('op_type')
        self.dicts[dnode].update(tmp)

    def fuse_act(self) -> None:
        # Fuse act to its predecessor
        ns2rmv, es2add = [], []
        for n in self.graph.nodes:
            if self.op_type(n) in {'Relu', 'PRelu', 'HardSigmoid'}: # current node is act
                pred_type = self.op_type(self.unique_pred(n))
                assert pred_type in {'Conv', 'Add'}, \
                    f"the predecessor of an activation node must be Conv or Add rather than {pred_type}"
                self._exten_op_type(self.unique_pred(n), '-Act') # fuse relu will change the op-type of the predecessor
                self._fuse_config(n, self.unique_pred(n))
                succs = list(self.succs(n)) # successors of act
                es = [(self.unique_pred(n), node) for node in succs] # edges to be added 
                ns2rmv.append(n)
                es2add += es

        for k in ns2rmv:
            self.dicts.pop(k)
        self.graph.remove_nodes_from(ns2rmv)
        self.graph.add_edges_from(es2add)

    def fuse_resize(self) -> None:
        # Fuse resize to its predecessor
        ns2rmv, es2add = [], []
        for n in self.graph.nodes:
            if self.op_type(n) in {'Resize'}: # current node is resize
                pred_type = self.op_type(self.unique_pred(n))
                assert pred_type in {'Conv', 'Conv-Act'}, (
                    f"the predecessor of an activation node must be Conv or Conv-Act rather than {pred_type}")
                self._exten_op_type(self.unique_pred(n), '-Rsz') # fuse resize will change the op-type of the predecessor
                self._fuse_config(n, self.unique_pred(n))
                succs = list(self.succs(n)) # successors of act
                es = [(self.unique_pred(n), node) for node in succs] # edges to be added 
                ns2rmv.append(n)
                es2add += es

        for k in ns2rmv:
            self.dicts.pop(k)
        self.graph.remove_nodes_from(ns2rmv)
        self.graph.add_edges_from(es2add)

    def remove_concat(self) -> None:
        # Remove concat and genrate concat information
        ns2rmv, es2add = [], []
        for n in self.graph.nodes:
            if self.op_type(n) == 'Concat': # current node is concat
                for pred in self.preds(n):
                    assert 'Conv' in self.op_type(pred), (
                        f"the predecessors of concat must have conv, but got {self.op_type(pred)}")
                    for succ in self.succs(n):
                        assert 'Conv' in self.op_type(succ), (
                            f"the successors of concat must have conv, but got {self.op_type(pred)}")
                        es2add.append((pred, succ))
                ns2rmv.append(n)
        
        for k in ns2rmv:
            self.dicts.pop(k)
        self.graph.remove_nodes_from(ns2rmv)
        self.graph.add_edges_from(es2add)
    
    def fuse_pool(self) -> None:
        # Fuse pool to its predecessor
        ns2rmv, es2add= [], []
        for n in self.graph.nodes:
            if self.op_type(n) in {'MaxPool', 'AveragePool'}: # current node is pool
                pred_type = self.op_type(self.unique_pred(n))
                if self.arch in {NNModelArch.RESNET}:
                    assert pred_type in {'Conv', 'Conv-Act'}, (
                        f"the predecessor of an window pool node must conrtains Conv rather than {pred_type}")
                if pred_type not in {'Conv', 'Conv-Act'}: # for non-resnet archs
                    continue
                self._exten_op_type(self.unique_pred(n), '-Pool') # fuse pool will change the op-type of the predecessor
                self._fuse_config(n, self.unique_pred(n))
                succs = list(self.succs(n)) # successors of pool
                es = [(self.unique_pred(n), node) for node in succs] # edges to be added 
                ns2rmv.append(n)
                es2add += es
                
        for k in ns2rmv:
            self.dicts.pop(k)
        self.graph.remove_nodes_from(ns2rmv)
        self.graph.add_edges_from(es2add)

    def head_pool(self, head_type: str) -> None:
        # Put pool ahead of add or concat
        ns2rmv, es2rmv, es2add = [], [], []
        for n in self.graph.nodes:
            if self.op_type(n) in {'MaxPool', 'AveragePool', 'GlobalAveragePool'}: 
                pred_type = self.op_type(self.unique_pred(n))
                if pred_type == head_type: # need to put pool ahead
                    ns2rmv.append(n)
                    conc = self.unique_pred(n)
                    pool_succs = list(self.succs(n))
                    conc_preds = list(self.preds(conc))
                    ns2rmv.append(n) # remove pool
                    for succ in pool_succs:
                        es2add.append((conc,succ))
                    for i,pred in enumerate(conc_preds):
                        new_pool = n + f'_head_{i}'
                        es2add.append((pred,new_pool))
                        es2add.append((new_pool,conc))
                        es2rmv.append((pred,conc))
                        self.dicts[new_pool] = deepcopy(self.dicts[n])

        for k in ns2rmv:
            self.dicts.pop(k)
        self.graph.remove_nodes_from(ns2rmv)
        self.graph.remove_edges_from(es2rmv)
        self.graph.add_edges_from(es2add)

    def fuse_add(self) -> None:
        # Fuse add to its trunk predecessor
        trunk = self.trunk
        while True:
            nf = True
            for n in self.graph.nodes:
                if self.op_type(n) in {'Add', 'Add-Act'}:
                    nf = False
                    preds = list(self.preds(n))
                    assert len(preds) == 2, "more than 2 branches to add"
                    d_pred = preds[0]
                    s_pred = preds[1]
                    if preds[0] in trunk and preds[1] in trunk: # direct bypass, both in trunk
                        if nx.has_path(self.graph,preds[0],preds[1]):
                            d_pred, s_pred = s_pred, d_pred
                    else: # indirect bypass, one in trunk, not the other
                        if s_pred in trunk:
                            d_pred, s_pred = s_pred, d_pred
                    succs = self.succs(n)
                    self.graph.remove_node(n)
                    self.graph.add_edge(s_pred, d_pred)
                    for succ in succs:
                        self.graph.add_edge(d_pred, succ)
                    self._exten_op_type(d_pred, '-'+self.op_type(n))
                    self._fuse_config(n, d_pred)
                    self.dicts.pop(n)
                    break
            if nf:
                break

    def regu_pool(self) -> None:
        # Regularize remain pools
        for n in self.graph.nodes:
            if self.op_type(n) in {'MaxPool', 'AveragePool', 'GlobalAveragePool'}:
                print("existing remain pools")
                sys.exit()
