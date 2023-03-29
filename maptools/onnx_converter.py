'''
# // TODO need to provide the size info (W x H) of the intermidiate data (size info is restored after onnx-sim)
# // TODO need to support multi-style paddings in inception (there is no Pads any more in onnx-simplified model)
TODO need to support reduce mean in mnasnet
TODO need to support sigmoid in efficientnet
TODO need to support global average pool and fc layer
'''
import os
import sys
import pickle
import onnx
import onnx.numpy_helper as onh
import networkx as nx
from typing import Any, List, Dict, Tuple, Optional, Generator
from graphviz import Digraph
from copy import deepcopy 
import numpy as np
from maptools.operator_graph import *

__all__ = ['OnnxConverter']

class OnnxConverter(object):

    valid_ops = ['Conv','Mul','Add','Relu','PRelu','MaxPool','AveragePool','GlobalAveragePool','HardSigmoid','Flatten','Gemm','Concat','Softmax']
    valid_archs = ['vgg','resnet','googlenet','squeezenet']
    merge_ops = ['Mul','Add','Concat']

    def __init__(self, model: onnx.ModelProto, *args, **kwargs) -> None:
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
        >>> oc.run_conversion()

        The conversion results are located in OnnxConverter.og
        >>> og: OperationGraph = oc.og

        Or you can get the seperate results from OnnxConverter.op_graph and OnnxConverter.op_dicts:
        >>> op_graph: nx.MultiDiGraph = oc.op_graph
        >>> op_dicts: Dict[str, Dict] = oc.op_dicts

        Parameters
        -------------
        model : onnx.ModelProto
            The onnx model must be simplified model, run `onnxsim model.onnx model_sim.onnx` to simplify the model.
            It's better to preview the model structure using netron before running OnnxConverter.

        kwargs : Dict
            arch : str = 'resnet'
                The architecture of the model (or backbone).
                The arch must be one of OnnxConverter.valid_archs.

            root_dir : str = os.environ.get('NVCIM_HOME')
                The root directory of the project.

            mapname : str = 'newmap'
                Map name

        Key Members
        -----------
        self.param_dict : Dict[str, np.ndarray]
            A dictionary with tensor name as keys and numpy array as values.
            Stores the parameters of the model.
        '''
        self.model = model
        self.arch = 'resnet'
        self.root_dir = os.environ.get('NVCIM_HOME')
        self.mapname = 'newmap'
        self.__dict__.update(kwargs)
        self.param_dict: Dict[str, np.ndarray] = dict() 
        assert self.arch in OnnxConverter.valid_archs,\
                    f"unsupported model arch: {self.arch}"

    @staticmethod
    def _is_merge_node(node: onnx.NodeProto) -> bool:
        return True if node.op_type in OnnxConverter.merge_ops else False

    @staticmethod
    def _get_node_attr(node: onnx.NodeProto, name: str) -> Optional[onnx.AttributeProto]:
        for at in node.attribute:
            if at.name == name:
                return at

    @staticmethod
    def _get_data_dims(name: str, graph: onnx.GraphProto) -> List[int]:
        for tensor in graph.value_info:
            if tensor.name == name:
                dim = tensor.type.tensor_type.shape.dim
                return [d.dim_value for d in dim]
        dim = graph.input[0].type.tensor_type.shape.dim # not found in value_info, then it must be input
        return [d.dim_value for d in dim]
    
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

    def _get_io_size(self, node: onnx.NodeProto) -> Tuple[List[int], List[int]]:
        # get input and output size
        name = node.input[0]
        i_dims = self._get_data_dims(name,self.model.graph)
        name = node.output[0]
        o_dims = self._get_data_dims(name,self.model.graph)
        return list(i_dims[-2:]), list(o_dims[-2:])

    def _complete_conv_info(self, node: onnx.NodeProto, d: Dict) -> None:
        size_i, size_o = self._get_io_size(node)
        d['conv_input_size'] = size_i
        d['conv_output_size'] = size_o
        for at in node.attribute:
            if at.name == 'dilations':
                assert list(at.ints) == [1, 1],\
                        f"conv_dilations must be [1, 1], but got {at.ints}"
            elif at.name == 'group':
                assert at.i == 1,\
                        f"conv_group must be 1, but got {at.i}"
            elif at.name == 'kernel_shape':
                d['conv_kernel_size'] = list(at.ints)
            elif at.name == 'pads':
                d['conv_pads'] = list(at.ints)
            elif at.name == 'strides':
                d['conv_strides'] = list(at.ints)

        weight = self._get_tensor(node.input[1]) # input[1] should be weight
        bias = None
        if len(node.input[2]): # if has bias
            bias = self._get_tensor(node.input[2]) # input[2] should be weight

        # save convolution weights
        name = node.name + '_conv_weight'
        d['conv_weight'] = name
        self.param_dict[name] = onh.to_array(weight)

        # save convolution bias
        name = node.name + '_conv_bias'
        d['conv_bias'] = name
        self.param_dict[name] = onh.to_array(bias)

        d['conv_num_ichan'] = weight.dims[1] # input channel number
        d['conv_num_ochan'] = weight.dims[0] # output channel number

    def _complete_pool_info(self, node: onnx.NodeProto, d: Dict) -> None:
        size_i, size_o = self._get_io_size(node)
        d['pool_input_size'] = size_i
        d['pool_output_size'] = size_o
        d['pool_mode'] = node.op_type
        for at in node.attribute:
            if at.name == 'ceil_mode':
                d['pool_ceil_mode'] = at.i
            elif at.name == 'kernel_shape':
                d['pool_kernel_size'] = list(at.ints)
            elif at.name == 'pads':
                d['pool_pads'] = list(at.ints)
            elif at.name == 'strides':
                d['pool_strides'] = list(at.ints)

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

        if self._is_conv(node.op_type):
            self._complete_conv_info(node, d)
        elif self._is_pool(node.op_type): 
            self._complete_pool_info(node, d)
        elif self._is_gemm(node.op_type):
            self._complete_gemm_info(node, d)
        elif self._is_act(node.op_type):
            self._complete_act_info(node, d)
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
        og._fuse_act() 
        og._fuse_pool()
        og._regu_pool()
        og._fuse_add()

    def __googlenet(self, og: OperatorGraph) -> None:
        og._cut_graph()
        og._fuse_act()
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
        self.og._check_size()
        self.op_graph = self.og.graph
        self.op_dicts = self.og.dicts

    def run_conversion(self) -> None:
        self.construct_raw_graph()
        self.construct_op_graph()

    def save_params(self) -> None:
        save_dir = os.path.join(self.root_dir, 'mapsave', self.mapname)
        file_dir = os.path.join(save_dir, 'params.pkl')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        with open(file_dir, 'wb') as f:
            pickle.dump(self.param_dict, f)
        print(f"parameters of the model has been written to: {file_dir}")

    def _print_dict(self, dicts: Dict[str, Dict]) -> None:
        for v in dicts.values():
            print('\n'+'-'*20)
            print(f"op_type:{v['op_type']}")
            for k1 in v.keys():
                if k1 != 'op_type':
                    print(k1)

    def print_raw_dict(self) -> None:
        self._print_dict(self.raw_dicts)

    def print_op_dict(self) -> None:
        self._print_dict(self.op_dicts)

    def _plot_graph(self, graph: nx.MultiDiGraph, dicts: Dict) -> None:
        name = 'raw_graph' if dicts is self.raw_dicts else 'op_graph'
        save_dir = os.path.join(self.root_dir, 'mapsave', self.mapname, name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        dot = Digraph('graph')
        shape = 'box3d'
        labelloc = None
        for n in graph.nodes:
            dot.node(n,dicts[n]['op_type'],shape=shape,labelloc=labelloc,fontname='Arial')
        for e in graph.edges:
            dot.edge(e[0],e[1])
        dot.view(cleanup=True, directory=save_dir, )
        print(f"graph saved to {save_dir}")

    def plot_raw_graph(self) -> None:
        self._plot_graph(self.raw_graph, self.raw_dicts)

    def plot_op_graph(self) -> None:
        self._plot_graph(self.op_graph, self.op_dicts)



