'''
TODO trunk is harmful to hybrid network structures
'''

import os
import sys
import networkx as nx
from copy import deepcopy 
from graphviz import Digraph as GDG
from functools import cached_property, wraps
from typing import Any, List, Dict, Tuple, Optional, Generator, Callable
from maptools.core.typing import OperatorConfig
from maptools.core.proto import QuantConfig, NNModelArch
from maptools.core.common import ROOT_DIR, TRUNCATE_OPS

__all__ = [
    'OperatorGraph',
    'OriginGraph',
    'HostGraph',
    'DeviceGraph',
    'OperatorVariableGraph'
]

class OperatorGraph(object):

    def __init__(
        self, 
        graph: nx.MultiDiGraph, 
        dicts: Dict[str, OperatorConfig], 
        quantize: bool
    ) -> None:
        self.graph = deepcopy(graph)
        self.dicts = deepcopy(dicts)
        self.quantize = quantize

    @property
    def trunk(self) -> List[str]:
        # Find and return the nodes in the trunk
        return list(nx.dag_longest_path(self.graph))

    @property
    def node_configs(self) -> Generator[Dict, None, None]:
        yield from (self.dicts[n] for n in nx.topological_sort(self.graph))

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

    @cached_property
    def input_num(self) -> int:
        return len([node for node in \
            self.graph.nodes if self.is_input(node)])

    @cached_property
    def output_num(self) -> int:
        return len([node for node in \
            self.graph.nodes if self.is_output(node)])

    def is_input(self, node: str) -> bool:
        return self.graph.in_degree(node) == 0
    
    def is_output(self, node: str) -> bool:
        return self.graph.out_degree(node) == 0

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
        now_node: str,
        marker: List[Any]
    ) -> None:
        host_nodes.append(now_node)
        for pred in graph.predecessors(now_node):
            if self.op_type(pred) in TRUNCATE_OPS:
                assert graph.in_degree(now_node) == 1 and graph.out_degree(pred) == 1, (
                    f"truncate node {pred} must have one-to-one connection with its successor {now_node}")
                
                # record bridge index
                self.dicts[now_node]['bridge_idx'] = len(marker)
                self.dicts[pred]['bridge_idx'] = len(marker)
                marker.append(None)

                # cut graph at truncate node
                graph.remove_edge(pred, now_node)
                return
        
        for pred in graph.predecessors(now_node):
            self._dfs_cut(graph, host_nodes, pred, marker)

    def dispatch_graph(self) -> Tuple['HostGraph', 'DeviceGraph']:
        '''
        Dispatch the operator graph into host graph and device graph
        '''
        host_nodes = []
        device_pure_graph = deepcopy(self.graph)

        self._dfs_cut(device_pure_graph, host_nodes, self.unique_output, [])
        device_pure_graph.remove_nodes_from(host_nodes)
        host_pure_graph = self.graph.subgraph(host_nodes)
        device_dicts = deepcopy(self.dicts)
        host_dicts = {n: device_dicts.pop(n) for n in host_nodes}

        host_graph = HostGraph(host_pure_graph, host_dicts, self.quantize)
        device_graph = DeviceGraph(device_pure_graph, device_dicts, self.quantize)

        return host_graph, device_graph


class HostGraph(OperatorGraph): ...


class DeviceGraph(OperatorGraph):

    @cached_property
    def iqc(self) -> QuantConfig:
        config = self.config(self.unique_input)
        return config['conv_quant_config']
    
    @cached_property
    def oqc(self) -> List[QuantConfig]:
        oqc = [0] * self.output_num
        for node in self.nodes:
            if self.is_output(node):
                config = self.config(node)
                name = 'conv_'
                if 'Act' in self.op_type(node):
                    name = 'add_'
                elif 'Add' in self.op_type(node):
                    name = 'relu_'
                bidx = config['bridge_idx']
                oqc[bidx] = config[name + 'quant_config']
        return oqc

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
        # Fuse one operator's config to another
        tmp = deepcopy(self.dicts[snode])
        tmp.pop('name')
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
                assert pred_type in {'Conv', 'Conv-Act'}, (
                    f"the predecessor of an window pool node must conrtains Conv rather than {pred_type}")
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
                raise RuntimeError("existing remain pools")


class OperatorVariableGraph(object):
    
    def __init__(self) -> None:
        self.graph: nx.MultiDiGraph = nx.MultiDiGraph()
        self.dicts: Dict[str, Any] = {}
        self.operators: List[str] = []
        self.variables: List[str] = []
    
    def is_operator(self, node: str) -> bool:
        return node in self.operators
    
    def is_variable(self, node: str) -> bool:
        return node in self.variables

    def add_node_routine(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args):
            self.graph.add_node(args[0])
            return func(self, *args)
        return wrapper

    @add_node_routine
    def add_operator_node(self, node: str) -> None:
        if node not in self.operators:
            self.operators.append(node)
    
    @add_node_routine
    def add_variable_node(self, node: str) -> None:
        if node not in self.variables:
            self.variables.append(node)

    def add_edge(self, *args, **kwargs) -> None:
        self.graph.add_edge(*args, **kwargs)

    def set_operator_config(self, node: str, config: OperatorConfig) -> None:
        assert self.is_operator(node), (
            f"setting operator config but got non-operator node: {node}")
        self.dicts[node] = config

    def op_type(self, node: str) -> str:
        return self.dicts[node]['op_type']
    
    def op_name(self, node: str) -> str:
        return self.dicts[node]['name']

    def _search_concat_targets(self, now_node: str, targets: List[str]) -> bool:
        if self.is_operator(now_node) and (
            self.op_type(now_node) == 'Conv'): # find a target
            targets.append(now_node)
            return True
        
        flag = False
        for node in self.graph.successors(now_node):
            if self.is_operator(node) and (
                self.op_type(node) == 'Concat'):
                raise AssertionError("continuous concat is not permitted")
            if self._search_concat_targets(node, targets): flag = True
        
        return flag
    
    def _config_concat(self, now_node: str, targets: List[str], marker: List[int]) -> None:
        if self.is_operator(now_node) and (
            self.op_type(now_node) == 'Conv'): # find a source

            # configure concat slots
            if 'concat_slots' not in self.dicts[now_node]:
                self.dicts[now_node]['concat_slots'] = {}
            self.dicts[now_node]['concat_slots'].update(
                {target: len(marker) for target in targets})
            
            # configure block boxes
            num_ochan = self.dicts[now_node]['conv_num_ochan']
            box = (sum(marker), sum(marker) + num_ochan)
            marker.append(num_ochan)
            for target in targets:
                if 'block_boxes' not in self.dicts[target]:
                    self.dicts[target]['block_boxes'] = []
                self.dicts[target]['block_boxes'].append(box)

            print(f"\nconfiguring concat_slots in '{now_node}'")
            print(f"concat index: {len(marker)-1}")
            print(f"concat targets: {targets}")
            print(f"block box: {box}")

            return

        preds = list(self.graph.predecessors(now_node))
        if len(preds) > 1:
            if self.is_operator(now_node): # operator node
                if self.op_type(now_node) == 'Concat': # normal
                    for pred in preds:
                        self._config_concat(pred, targets, marker)
                    return
                if self.op_type(now_node) == 'Add': # for Add, only searh its one predecessor
                    self._config_concat(preds[0], targets, marker)
                    return
            raise AssertionError(
                f"operator {now_node} has multiple predecessors when concat configuring")
        self._config_concat(preds[0], targets, marker)

    def _format_block_boxes(self) -> None:
        for node in self.operators:
            if self.op_type(node) == 'Conv':
                self.dicts[node]['block_nums'] = []
                if 'block_boxes' not in self.dicts[node]:
                    num_ichan = self.dicts[node]['conv_num_ichan']
                    self.dicts[node]['block_boxes'] = [(0, num_ichan)]

    def connect_concats(self) -> None:
        '''
        This method is for concat information configuration, which is a necessary
        step to construct a valid device graph. For concat operators, the concat 
        order is critical, the edge order is guaranteed when self-constructing,
        but the conv operators concerned with the concat operator still know nothing about
        the concat order, this method writes the concat order information directly 
        to the related conv operators through to construct complete concat connection. 

        Always make sure to call this method after finishing self-constructing but 
        before `self.reduce`.
        '''
        for node in self.operators:
            if self.op_type(node) == 'Concat':
                targets = []
                if not self._search_concat_targets(node, targets): continue
                self._config_concat(node, targets, [])
        self._format_block_boxes()

    def reduce(self, **kwargs) -> OriginGraph:
        '''
        The OperatorVariableGraph is naturally a bipartite graph
        which contains both operator nodes and variable nodes.
        This method reduces the graph by removing variable nodes.

        The implementation of this method follows two features in 
        the OperatorVariablGraph graph:
        1. Operator nodes have at least one inputs and a single output.
        2. Variable nodes have single input and at least one outputs.
        '''
        graph = deepcopy(self.graph)
        for n in self.variables:
            inputs = list(graph.predecessors(n))
            outputs = list(graph.successors(n))
            graph.remove_node(n)
            if len(inputs) > 0 and len(outputs) > 0: # not input data nor output data
                assert len(inputs) == 1, (
                    f"error: data node {n} has multiple inputs") # feature 2
                for output in outputs:
                    graph.add_edge(inputs[0], output)

        return OriginGraph(graph, deepcopy(self.dicts), kwargs['quantize'])

    def print_dict(self) -> None:
        for v in self.dicts.values():
            print('\n'+'-'*20)
            print(f"op_type:{v['op_type']}")
            for k1 in v.keys():
                if k1 != 'op_type':
                    print(k1)