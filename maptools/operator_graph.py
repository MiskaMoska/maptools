'''
TODO fuse pool to conv-add, now only support fusing pool to conv
but actually there are rarely this kind of structure in resnet
'''
import sys
import networkx as nx
from typing import Any, List, Dict, Tuple, Optional, Generator
from copy import deepcopy 

__all__ = ['OperatorGraph']

class OperatorGraph(object):

    valid_ops = ['Conv','Conv-Pool','Pool','Conv-Add','GlobalPool','Add','Mul','Concat']

    def __init__(self, graph: nx.MultiDiGraph, dicts: Dict[str, Dict], arch: str) -> None:
        '''
        Operater graph for graph division, fusion, and optimization
        '''
        self.graph = deepcopy(graph)
        self.dicts = deepcopy(dicts)
        self.arch = arch

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
        for n in self.graph.nodes:
            yield n

    @property
    def egdes(self) -> Generator[Tuple, None, None]:
        for e in self.graph.edges:
            yield e

    def in_degree(self, node: str) -> int:
        return self.graph.in_degree(node)

    def info(self, node: str) -> Dict:
        return self.dicts[node]

    def pred(self, node: str) -> str:
        # Get node's only predecessor
        preds = list(self.graph.predecessors(node))
        assert len(preds) == 1, "Multi predecessors of activation node"
        return preds[0]

    def op_type(self, node: str) -> str:
        # Get node's op_type
        return self.dicts[node]['op_type']

    def set_op_type(self, node: str, type: str) -> None:
        # Set node's op_type
        self.dicts[node]['op_type'] = type

    def _cut_graph(self) -> None:
        # Remove all layers after the last AveragePool
        _to_rmv = []
        sort = list(nx.topological_sort(self.graph))
        sort.reverse()
        for i,n in enumerate(sort):
            if self.op_type(n) in ['GlobalAveragePool','AveragePool']:
                _to_rmv = sort[:i+1]
                break
        self.graph.remove_nodes_from(_to_rmv)

    def _fuse_dict(self, snode: str, dnode: str) -> None:
        # Fuse dict to another's
        tmp = deepcopy(self.dicts[snode])
        tmp.pop('op_type')
        self.dicts[dnode].update(tmp)

    def _fuse_relu(self) -> None:
        # Fuse act to its predecessor
        ns2rmv = []
        es2add = []
        ks2rmv = []
        for n in self.graph.nodes:
            if self.op_type(n) in ['Relu','PRelu','HardSigmoid']: # current node is act
                pred_type = self.op_type(self.pred(n))
                assert pred_type in ['Conv','Add'], \
                    f"the predecessor of an activation node must be Conv or Add rather than {pred_type}"
                self._fuse_dict(n,self.pred(n))
                ks2rmv.append(n)
                succs = list(self.graph.successors(n)) # successors of act
                es = [(self.pred(n), node) for node in succs] # edges to be added 
                ns2rmv.append(n)
                es2add += es
        for k in ks2rmv:
            self.dicts.pop(k)
        self.graph.remove_nodes_from(ns2rmv)
        self.graph.add_edges_from(es2add)
    
    def _fuse_pool(self) -> None:
        # Fuse pool to its predecessor
        ns2rmv = []
        es2add = []
        ks2rmv = []
        for n in self.graph.nodes:
            if self.op_type(n) in ['MaxPool','AveragePool']: # current node is pool
                pred_type = self.op_type(self.pred(n))
                if self.arch in ['resnet']:
                    assert pred_type in ['Conv'], \
                        f"the predecessor of an window pool node must be Conv rather than {pred_type}"
                if pred_type not in ['Conv']: # for non-resnet archs
                    continue
                self.set_op_type(self.pred(n),'Conv-Pool') # fuse pool will change the op-type of the predecessor
                self._fuse_dict(n,self.pred(n))
                succs = list(self.graph.successors(n)) # successors of pool
                es = [(self.pred(n), node) for node in succs] # edges to be added 
                ns2rmv.append(n)
                ks2rmv.append(n)
                es2add += es
        for k in ks2rmv:
            self.dicts.pop(k)
        self.graph.remove_nodes_from(ns2rmv)
        self.graph.add_edges_from(es2add)

    def _head_pool(self,head_type: str) -> None:
        # Put pool ahead of add or concat
        ns2rmv = []
        es2rmv = []
        es2add = []
        ks2rmv = []
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

    def _regu_pool(self) -> None:
        # Regularize remain pools
        for n in self.graph.nodes:
            if self.op_type(n) in ['MaxPool','AveragePool','GlobalAveragePool']:
                self.set_op_type(n,'Pool')

    def _fuse_add(self) -> None:
        # Fuse add to its trunk predecessor
        trunk = self.trunk
        while True:
            nf = True
            for n in self.graph.nodes:
                if self.op_type(n) == 'Add':
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
                    self.set_op_type(d_pred,self.op_type(d_pred)+'-Add')
                    self.dicts.pop(n)
                    break
            if nf:
                break
    
    def _check_size(self) -> None:
        '''
        Some onnx models have incorrect convolution or pooling pads information.
        This method checks these incorrections and regularizes them.

        However, some incorrections cannot be regularized, for example: 
        1. the `conv_output_size` does not match `pool_input_size` in the same operator.
        2. the calculated `output_size` does not match onnx recorded `output_size`.
        3. the `conv_input size` still does not match `conv_output_size` though pads are corrected.
        Encountering these incorrections will trigger assertion failure.

        Always make sure to call this method after finishing opterator-graph-converting.
        '''
        for node in self.nodes:
            info = self.info(node)
            if 'Conv' in info['op_type']:
                cks = info['conv_kernel_size']
                cpads = info['conv_pads']
                cstrs = info['conv_strides']
                cifs = info['conv_input_size']
                cofs = info['conv_output_size']
                self.__regu_size(cifs, cofs, cks, cpads, cstrs)
                self.dicts[node]['conv_pads'] = cpads
                
                if 'Pool' in info['op_type']:
                    pks = info['pool_kernel_size']
                    ppads = info['pool_pads']
                    pstrs = info['pool_strides']
                    pifs = info['pool_input_size']
                    pofs = info['pool_output_size']
                    assert cofs == pifs, \
                        f"conv_output_size {cofs} not match pool_input_size {pifs}"
                    self.__regu_size(pifs, pofs, pks, ppads, pstrs)
                    self.dicts[node]['pool_pads'] = ppads

    def __regu_size(self, ifs: List[int], ofs: List[int], 
                    ks: List[int], pads: List[int], strs: List[int]) -> None:
        '''
        pads : List[int]
            `pads` is referenced, after performing this method, 
            `pads` can be modified to accomodate the feature map size
        '''
        def __regu_one_dim(dim: int) -> None:
            while True:
                remain = ifs[dim] + pads[0+dim] + pads[2+dim]
                remain -= max([ks[dim], strs[dim]])
                size_o = remain // strs[dim] + 1
                if size_o < ofs[dim]:
                    pads[0+dim] += 1
                elif size_o == ofs[dim]:
                    break
                else:
                    print(f'''
                            calcuelated output size {size_o} larger than onnx output size {ofs[dim]}
                            input_size: {ifs[dim]}, kernel_size: {ks[dim]},
                            strides: {strs[dim]}, pads: {[pads[0+dim], pads[2+dim]]}
                            need to decrease pads
                    ''')
                # assert size_o == ofs[dim], \
                #     f'''
                #         calcuelated output size {size_o} not match onnx output size {ofs[dim]}
                #         input_size: {ifs[dim]}, kernel_size: {ks[dim]},
                #         strides: {strs[dim]}, pads: {[pads[0+dim], pads[2+dim]]}
                #     '''
            extra = remain % strs[dim]
            if extra != 0:
                print('starting correcting one size ....')
                assert extra <= pads[0+dim] + pads[2+dim], \
                    "extra pixels larger than onnx pads, cannot perform correction"
                for i in range(extra):
                    if pads[0+dim] > 0:
                        pads[0+dim] -= 1
                    else:
                        pads[2+dim] -= 1    

        for i in range(2):
            __regu_one_dim(i)


