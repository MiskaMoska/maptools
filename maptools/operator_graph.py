'''
TODO support more model structures
'''
import os
import sys
import networkx as nx
from graphviz import Digraph as GDG
from typing import Any, List, Dict, Tuple, Optional, Generator
from maptools.maptype import OperatorConfig
from functools import cached_property
from maptools.core.proto import QuantConfig
from copy import deepcopy 

__all__ = ['OperatorGraph']

class OperatorGraph(object):

    def __init__(
        self, 
        graph: nx.MultiDiGraph, 
        dicts: Dict[str, OperatorConfig], 
        arch: str
        ) -> None:
        '''
        Operater graph for graph division, fusion, and optimization
        '''
        self.graph = deepcopy(graph)
        self.dicts = deepcopy(dicts)
        self.arch = arch
        self.quantize = False

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
        for e in self.graph.edges:
            yield e

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

    def in_degree(self, node: str) -> int:
        return self.graph.in_degree(node)

    def config(self, node: str) -> OperatorConfig:
        return self.dicts[node]

    def pred(self, node: str) -> str:
        # Get node's only predecessor
        preds = list(self.graph.predecessors(node))
        assert len(preds) == 1, "Multi predecessors of activation node"
        return preds[0]

    def op_type(self, node: str) -> str:
        # Get node's op_type
        return self.dicts[node]['op_type']

    def exten_op_type(self, node: str, suffix: str) -> None:
        # Extend node's op_type
        self.dicts[node]['op_type'] += suffix

    def add_attr_to_node(self, node: str, key: Any, attr: Any) -> None:
        assert node in self.dicts, f"node {node} not exist in operator graph"
        self.dicts[node][key] = attr

    def cut_graph(self) -> None:
        # Remove all layers after the last AveragePool
        _to_rmv = []
        sort = list(nx.topological_sort(self.graph))
        sort.reverse()
        for i,n in enumerate(sort):
            if self.op_type(n) in ['GlobalAveragePool','AveragePool']:
                _to_rmv = sort[:i+1]
                break
        self.graph.remove_nodes_from(_to_rmv)

    def dispatch_graph(self, op_type: str) -> Tuple:
        '''
        Dispatch the operator graph into host graph and device graph
        The division line is the first `op_type` typed operation from behind
        The division operation is dispatched to host graph
        Usually the division operation type is chosen as GlobalAveragePool
        '''
        sort = list(nx.topological_sort(self.graph))
        sort.reverse()
        device_dicts = deepcopy(self.dicts)
        host_dicts = {}
        host_nodes = []
        for n in sort:
            host_dicts[n] = device_dicts.pop(n)
            host_nodes.append(n)
            if self.op_type(n) == op_type:
                assert self.graph.in_degree(n) == 1 and self.graph.out_degree(n) == 1, (
                    f"the division operation '{op_type}' has multiple predeccessors or successors")
                host_pure_graph = self.graph.subgraph(host_nodes)
                host_graph = OperatorGraph(host_pure_graph, host_dicts, None)
                device_pure_graph = deepcopy(self.graph)
                device_pure_graph.remove_nodes_from(host_nodes)
                device_graph = OperatorGraph(device_pure_graph,device_dicts, None)
                return host_graph, device_graph
        assert True, f"error when dispatching: the origin graph has no operation node typed '{op_type}'"

    def _fuse_operator(self, snode: str, dnode: str) -> None:
        # Fuse one operator to another
        tmp = deepcopy(self.dicts[snode])
        tmp.pop('op_type')
        self.dicts[dnode].update(tmp)

    def fuse_act(self) -> None:
        # Fuse act to its predecessor
        ns2rmv, es2add, ks2rmv = [], [], []
        for n in self.graph.nodes:
            if self.op_type(n) in ['Relu','PRelu','HardSigmoid']: # current node is act
                pred_type = self.op_type(self.pred(n))
                assert pred_type in ['Conv','Add'], \
                    f"the predecessor of an activation node must be Conv or Add rather than {pred_type}"
                self.exten_op_type(self.pred(n), '-Act') # fuse relu will change the op-type of the predecessor
                self._fuse_operator(n, self.pred(n))
                ks2rmv.append(n)
                succs = list(self.graph.successors(n)) # successors of act
                es = [(self.pred(n), node) for node in succs] # edges to be added 
                ns2rmv.append(n)
                es2add += es
        for k in ks2rmv:
            self.dicts.pop(k)
        self.graph.remove_nodes_from(ns2rmv)
        self.graph.add_edges_from(es2add)
    
    def fuse_pool(self) -> None:
        # Fuse pool to its predecessor
        ns2rmv, es2add, ks2rmv = [], [], []
        for n in self.graph.nodes:
            if self.op_type(n) in ['MaxPool','AveragePool']: # current node is pool
                pred_type = self.op_type(self.pred(n))
                if self.arch in ['resnet']:
                    assert pred_type in ['Conv','Conv-Act'], \
                        f"the predecessor of an window pool node must conrtains Conv rather than {pred_type}"
                if pred_type not in ['Conv','Conv-Act']: # for non-resnet archs
                    continue
                self.exten_op_type(self.pred(n), '-Pool') # fuse pool will change the op-type of the predecessor
                self._fuse_operator(n, self.pred(n))
                succs = list(self.graph.successors(n)) # successors of pool
                es = [(self.pred(n), node) for node in succs] # edges to be added 
                ns2rmv.append(n)
                ks2rmv.append(n)
                es2add += es
        for k in ks2rmv:
            self.dicts.pop(k)
        self.graph.remove_nodes_from(ns2rmv)
        self.graph.add_edges_from(es2add)

    def head_pool(self,head_type: str) -> None:
        # Put pool ahead of add or concat
        ns2rmv, es2rmv, es2add, ks2rmv = [], [], [], []
        for n in self.graph.nodes:
            if self.op_type(n) in ['MaxPool','AveragePool','GlobalAveragePool']: 
                pred_type = self.op_type(self.pred(n))
                if pred_type == head_type: # need to put pool ahead
                    ns2rmv.append(n)
                    ks2rmv.append(n)
                    conc = self.pred(n)
                    pool_succs = list(self.graph.successors(n))
                    conc_preds = list(self.graph.predecessors(conc))
                    ns2rmv.append(n) # remove pool
                    for succ in pool_succs:
                        es2add.append((conc,succ))
                    for i,pred in enumerate(conc_preds):
                        new_pool = n + f'_head_{i}'
                        es2add.append((pred,new_pool))
                        es2add.append((new_pool,conc))
                        es2rmv.append((pred,conc))
                        self.dicts[new_pool] = deepcopy(self.dicts[n])
        for k in ks2rmv:
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
                if self.op_type(n) in ['Add','Add-Act']:
                    nf = False
                    preds = list(self.graph.predecessors(n))
                    assert len(preds) == 2, "more than 2 branches to add"
                    d_pred = preds[0]
                    s_pred = preds[1]
                    if preds[0] in trunk and preds[1] in trunk: # direct bypass, both in trunk
                        if nx.has_path(self.graph,preds[0],preds[1]):
                            d_pred, s_pred = s_pred, d_pred
                    else: # indirect bypass, one in trunk, not the other
                        if s_pred in trunk:
                            d_pred, s_pred = s_pred, d_pred
                    succs = self.graph.successors(n)
                    self.graph.remove_node(n)
                    self.graph.add_edge(s_pred,d_pred)
                    for succ in succs:
                        self.graph.add_edge(d_pred,succ)
                    self.exten_op_type(d_pred, '-'+self.op_type(n))
                    self._fuse_operator(n, d_pred)
                    self.dicts.pop(n)
                    break
            if nf:
                break

    def regu_pool(self) -> None:
        # Regularize remain pools
        for n in self.graph.nodes:
            if self.op_type(n) in ['MaxPool','AveragePool','GlobalAveragePool']:
                print("existing remain pools")
                sys.exit()

    def _check_size(self) -> None:
        '''
        Some onnx models have incorrect convolution or pooling pads information.
        This method checks these incorrections and regularizes them.

        However, some incorrections cannot be regularized, for example: 
        1. the `conv_output_size` does not match `pool_input_size` in the same operator.
        2. the calculated `output_size` does not match onnx recorded `output_size`.
        3. the `conv_input size` still does not match `conv_output_size` though pads are corrected.
        Encountering these incorrections will trigger assertion failure.

        Make sure to call this method after finishing opterator-graph-converting.
        '''
        for node in self.nodes:
            config = self.config(node)
            if 'Conv' in config['op_type']:
                cks = config['conv_kernel_size']
                cpads = config['conv_pads']
                cstrs = config['conv_strides']
                cifs = config['conv_input_size']
                cofs = config['conv_output_size']
                self._regu_size(cifs, cofs, cks, cpads, cstrs)
                self.dicts[node]['conv_pads'] = cpads
                
                if 'Pool' in config['op_type']:
                    pks = config['pool_kernel_size']
                    ppads = config['pool_pads']
                    pstrs = config['pool_strides']
                    pifs = config['pool_input_size']
                    pofs = config['pool_output_size']
                    assert cofs == pifs, \
                        f"conv_output_size {cofs} not match pool_input_size {pifs}"
                    self._regu_size(pifs, pofs, pks, ppads, pstrs)
                    self.dicts[node]['pool_pads'] = ppads

    def _regu_size(
        self, 
        ifs: List[int], 
        ofs: List[int], 
        ks: List[int], 
        pads: List[int], 
        strs: List[int]
    ) -> None:
        '''
        pads : List[int]
            `pads` is referenced, after performing this method, 
            `pads` can be modified to accomodate the feature map size
        '''
        def regu_one_dim(dim: int) -> None:
            while True:
                remain = ifs[dim] + pads[0+dim] + pads[2+dim]
                remain -= max([ks[dim], strs[dim]])
                size_o = remain // strs[dim] + 1
                if size_o < ofs[dim]:
                    pads[2-dim] += 1
                elif size_o == ofs[dim]:
                    break
                else:
                    print(f'''
                        calculated output size {size_o} larger than onnx output size {ofs[dim]}
                        input_size: {ifs[dim]}, kernel_size: {ks[dim]},
                        strides: {strs[dim]}, pads: {[pads[0+dim], pads[2+dim]]}
                        need to decrease pads
                    ''')
            extra = remain % strs[dim]
            if extra != 0:
                print('starting correcting one size ....')
                assert extra <= pads[2-dim], \
                    "extra pixels larger than onnx outside (right and down) pads, cannot perform correction"
                for i in range(extra):
                    pads[2-dim] -= 1

        for i in range(2):
            regu_one_dim(i)
        
    def plot_graph(self, save_dir) -> None:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
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
        dot.view(cleanup=True, directory=save_dir)
        print(f"graph saved to {save_dir}")
