'''
# // TODO need to provide the size info (W x H) of the intermidiate data (size info is restored after onnx-sim)
# // TODO need to support multi-style paddings in inception (there is no Pads any more in onnx-simplified model)
TODO need to support reduce mean in mnasnet
TODO need to support sigmoid in efficientnet
'''

import sys
import onnx
import onnx.numpy_helper as onh
import networkx as nx
from typing import Any, List, Dict, Tuple, Optional, Generator
from graphviz import Digraph
from copy import deepcopy 

__all__ = ['OnnxConverter']

class OperatorGraph(object):

    valid_ops = ['Conv','Conv-Pool','Pool','Conv-Add','Conv-Pool-Add','Pool-Add','GlobalPool','Add','Mul','Concat']

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
        tmp.pop('input_dims')
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


class OnnxConverter(object):

    valid_ops = ['Conv','Mul','Add','Relu','PRelu','MaxPool','AveragePool','GlobalAveragePool','HardSigmoid','Flatten','Gemm','Concat','Softmax']
    valid_archs = ['vgg','resnet','googlenet','squeezenet']
    merge_ops = ['Mul','Add','Concat']

    def __init__(self, model: onnx.ModelProto, arch: str = 'resnet') -> None:
        '''
        Convert Onnx to NVCIM intermediate representation which will be fed to TileMapper and NocMapper.
        About supported op_type:
            The supported onnx op_types are listed in OnnxConverter.valid_ops. Note that:
            1. Sigmoid is not supported cause it is not hardware-friendly.
            2. Reshape is not supported. If you want to transform a [1, N, 1, 1] tensor to [1, N], always use Flatten instead of Reshape.
            3. Seperate Pad is not supported. Please fuse pad to other opts like Conv or Pool.
            4. Dropout is not supported.
        
        About the supported archs:
            The supported archs are listed in OnnxConverter.valid_archs. Note that:
            1. ResNet must have a GlobalAveragePool layer before the linear layer, 
               ResNet must have only 2 branches to merge

        Examples
        -------------
        >>> model = onnx.load("googlenet.onnx")
        >>> oc = OnnxConverter(model,arch='googlenet)
        >>> oc.Run_Conversion()

        The conversion results are located in OnnxConverter.og
        >>> og: OperationGraph = oc.og

        Or you can get the seperate results from OnnxConverter.op_graph and OnnxConverter.op_dicts:
        >>> op_graph: nx.MultiDiGraph = oc.op_graph
        >>> op_dicts: Dict[str,Dict] = oc.op_dicts

        Parameters
        -------------
        model : onnx.ModelProto
            The onnx model must be simplified model, run `onnxsim model.onnx model_sim.onnx` to simplify the model.
            It's better to preview the model structure using netron before running OnnxConverter.

        arch : str
            The architecture of the model (or backbone).
            The arch must be one of OnnxConverter.valid_archs.
        '''
        assert arch in OnnxConverter.valid_archs, f"unsupported model arch: {arch}"
        self.model = model
        self.arch = arch

    @staticmethod
    def _is_merge_node(node: onnx.NodeProto) -> bool:
        return True if node.op_type in OnnxConverter.merge_ops else False

    @staticmethod
    def _get_node_attr(node: onnx.NodeProto, name: str) -> onnx.AttributeProto:
        for at in node.attribute:
            if at.name == name:
                return at

    @staticmethod
    def _get_data_dims(name: str, graph: onnx.GraphProto) -> Tuple[int]:
        for tensor in graph.value_info:
            if tensor.name == name:
                dim = tensor.type.tensor_type.shape.dim
                return tuple([d.dim_value for d in dim])
        dim = graph.input[0].type.tensor_type.shape.dim # not found in value_info, then it must be input
        return tuple([d.dim_value for d in dim])
    
    @staticmethod
    def _is_conv(type: str) -> bool:
        return True if type in ['Conv'] else False

    @staticmethod
    def _is_gemm(type: str) -> bool:
        return True if type in ['Gemm'] else False

    @staticmethod
    def _is_pool(type: str) -> bool:
        return True if type in ['MaxPool','AveragePool','GlobalAveragePool'] else False

    @staticmethod
    def _is_act(type: str) -> bool:
        return True if type in ['Relu','PRelu','HardSigmoid'] else False

    def _get_tensor(self, name: str) -> onnx.TensorProto:
        for tensor in self.model.graph.initializer:
            if tensor.name == name:
                return tensor
        print(f"cannot find tensor named {name}")
        sys.exit()

    def _verify_op_type(self, node: onnx.NodeProto) -> None:
        assert node.op_type in self.valid_ops, f"unsupported op type: {node.op_type}"
        if node.op_type in ['Concat, Flatten']:
            assert self._get_node_attr(node,'axis') == 1, f"axis must be 1 at op type: {node.op_type}" 

    def _complete_conv_info(self, node: onnx.NodeProto, d: Dict) -> None:
        for at in node.attribute:
            if at.name == 'dilations':
                d['conv_dilations'] = at.ints
            elif at.name == 'group':
                d['conv_group'] = at.i
            elif at.name == 'kernel_shape':
                d['conv_kernel_size'] = at.ints
            elif at.name == 'pads':
                d['conv_pads'] = at.ints
            elif at.name == 'strides':
                d['conv_strides'] = at.ints

        weight = self._get_tensor(node.input[1]) # input[1] should be weight
        bias = None
        if len(node.input[2]): # if has bias
            bias = self._get_tensor(node.input[2]) # input[2] should be weight
        d['conv_weight'] = onh.to_array(weight)
        d['conv_bias'] = onh.to_array(bias)
        d['conv_num_inchan'] = weight.dims[1] # input channel number
        d['conv_num_outchan'] = weight.dims[0] # output channel number

    def _complete_pool_info(self, node: onnx.NodeProto, d: Dict) -> None:
        d['pool_mode'] = node.op_type
        for at in node.attribute:
            if at.name == 'ceil_mode':
                d['pool_ceil_mode'] = at.i
            elif at.name == 'kernel_shape':
                d['pool_kernel_size'] = at.ints
            elif at.name == 'pads':
                d['pool_pads'] = at.ints
            elif at.name == 'strides':
                d['pool_strides'] = at.ints

    def _complete_gemm_info(self, node: onnx.NodeProto, d: Dict) -> None:
        weight = self._get_tensor(node.input[1]) # input[1] should be weight
        bias = None
        if len(node.input[2]): # if has bias
            bias = self._get_tensor(node.input[2]) # input[2] should be weight
        d['fc_weight'] = onh.to_array(weight)
        d['fc_bias'] = onh.to_array(bias)
        d['fc_len_inv'] = weight.dims[1] # input vector length
        d['fc_len_outv'] = weight.dims[0] # output vector length

    def _complete_act_info(self, node: onnx.NodeProto, d: Dict) -> None:
        d['act_mode'] = node.op_type 
        for at in node.attribute:
            if at.name == 'alpha':
                d['act_alpha'] = at.f

    def _construct_raw_dict(self, node: onnx.NodeProto) -> Dict:
        d = dict()
        d['op_type'] = node.op_type
        name = node.input[0]
        dims = self._get_data_dims(name,self.model.graph)
        d['input_dims'] = dims

        if self._is_conv(node.op_type):
            self._complete_conv_info(node,d)
        elif self._is_pool(node.op_type): 
            self._complete_pool_info(node,d)
        elif self._is_gemm(node.op_type):
            self._complete_gemm_info(node,d)
        elif self._is_act(node.op_type):
            self._complete_act_info(node,d)
        return d

    def _remove_data_nodes(self) -> None:
        '''
        Remove data nodes in raw bipartite graph.
        features:
        1. opt nodes has multi(>=1) inputs and single output
        2. data nodes has single input and multi(>=1) outputs
        '''
        for n in self.data_nodes:
            inputs = list(self.raw_graph.predecessors(n))
            outputs = list(self.raw_graph.successors(n))
            self.raw_graph.remove_node(n)
            if len(inputs) > 0 and len(outputs) > 0: # not input data nor output data
                assert len(inputs) == 1, "ERROR: data node has multiple inputs" # feature 2
                for output in outputs:
                    self.raw_graph.add_edge(inputs[0],output)

    def construct_raw_graph(self) -> None:
        '''
        Construct raw compute graph where each node is an onnx opt
        '''
        self.raw_graph = nx.MultiDiGraph() # bipartite graph
        self.compute_nodes = []
        self.data_nodes = []
        self.raw_dicts = dict() # key: name, value: info dict

        for n in self.model.graph.node:
            now_node = n.name
            self.compute_nodes.append(now_node+'_o')
            self._verify_op_type(n) # verify if the op type is supported

            if self._is_merge_node(n): # multi inputs
                for pred_node in n.input:
                    self.data_nodes.append(pred_node+'_d')
                    self.raw_graph.add_edge(pred_node+'_d',now_node+'_o')
    
            else: # only one input
                self.data_nodes.append(n.input[0]+'_d')
                self.raw_graph.add_edge(n.input[0]+'_d',now_node+'_o')

            succ_node = n.output[0] # there is always one output
            self.data_nodes.append(succ_node+'_d')
            self.raw_graph.add_edge(now_node+'_o',succ_node+'_d')
            self.raw_dicts[now_node+'_o'] = self._construct_raw_dict(n)

        self.data_nodes = list(set(self.data_nodes))
        self._remove_data_nodes()

    def __resnet(self, og: OperatorGraph) -> None:
        og._cut_graph()
        og._fuse_relu() 
        og._fuse_pool()
        og._regu_pool()
        og._fuse_add()

    def __googlenet(self, og: OperatorGraph) -> None:
        og._cut_graph()
        og._fuse_relu()
        og._head_pool('Concat')
        og._fuse_pool()
        og._regu_pool()

    def construct_op_graph(self) -> None:
        '''
        Construct opt compute graph where each node is a nvcim opt
        '''
        self.og = OperatorGraph(self.raw_graph,self.raw_dicts,self.arch) 
        if self.arch == 'resnet':
            self.__resnet(self.og)
        elif self.arch == 'googlenet':
            self.__googlenet(self.og)
        self.op_graph = self.og.graph
        self.op_dicts = self.og.dicts

    def run_conversion(self) -> None:
        self.construct_raw_graph()
        self.construct_op_graph()

    def _print_dict(self, dicts: Dict[str, Dict]) -> None:
        for v in dicts.values():
            print("\n"+"-"*20)
            print(f"op_type:{v['op_type']}")
            for k1 in v.keys():
                if k1 != 'op_type':
                    print(k1)

    def print_raw_dict(self) -> None:
        self._print_dict(self.raw_dicts)

    def print_op_dict(self) -> None:
        self._print_dict(self.op_dicts)

    def _plot_graph(self, graph: nx.MultiDiGraph, dicts: Dict) -> None:
        dot = Digraph('graph')
        shape = 'box3d'
        labelloc = None
        for n in graph.nodes:
            dot.node(n,dicts[n]['op_type'],shape=shape,labelloc=labelloc,fontname='Arial')
        for e in graph.edges:
            dot.edge(e[0],e[1])
        dot.view()

    def plot_raw_graph(self) -> None:
        self._plot_graph(self.raw_graph, self.raw_dicts)

    def plot_op_graph(self) -> None:
        self._plot_graph(self.op_graph, self.op_dicts)

if __name__ == "__main__":
    model = onnx.load("../models/simp-resnet50.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    oc.plot_op_graph()
    # oc.print_op_dict()
    # print(type(oc.og.nodes))



