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
import numpy as np
import networkx as nx
from typing import Any, List, Dict, Tuple, Optional, Generator
from maptools.utils import load_quant_to_graph, regularize_pad_sizes
from maptools.mapper.shaper import *
from maptools.core import (
    OperatorGraph, OriginGraph, HostGraph, DeviceGraph, NNModelArch,
    VALID_OPS, MERGE_OPS, ROOT_DIR, OperatorConfig, DeviceParams
)

__all__ = ['OnnxConverter']

class OnnxConverter(object):

    def __init__(self, model: onnx.ModelProto, **kwargs: Any) -> None:
        '''
        Convert Onnx to NVCIM intermediate representation which will be fed to TileMapper and NocMapper.
        About supported op_type:
            The supported onnx op_types are listed in `VALID_OPS`. Note that:
            1. Sigmoid is not supported cause it is not hardware-friendly.
            2. Reshape is not supported. If you want to transform a [1, N, 1, 1] tensor to [1, N], always use Flatten instead of Reshape.
            3. Seperate Pad is not supported. Please fuse pad to other operations like Conv or Pool.
            4. Dropout is not supported.
        
        About the supported archs:
            The supported archs are listed in `NNModelArch`. Note that:
            1. ResNet must have a GlobalAveragePool layer before the linear layer, 
               ResNet must have only 2 branches to merge

        Examples
        -------------
        >>> model = onnx.load("googlenet.onnx")
        >>> oc = OnnxConverter(model, arch=NNModelArch.GOOGLENET)
        >>> oc.run_conversion()

        The conversion results are located in `OnnxConverter.device_graph` and `OnnxConverter.host_graph`.
        The `device_graph` is the operator graph that should be offloaded onto NVCIM device.
        The `host_graph` is the operator graph deployed on host proccessor.
        >>> dg = oc.device_graph
        >>> hg = oc.host_graph

        Parameters
        -------------
        model : onnx.ModelProto
            The onnx model must be simplified model, run `onnxsim model.onnx model_sim.onnx` to simplify the model.
            It's better to preview the model structure using netron before running OnnxConverter.

        kwargs : Dict
            arch : NNModelArch = NNModelArch.RESNET
                The architecture of the model (or backbone).

            mapname : str = 'newmap'
                Map name

            quantize : bool = True
                whether to include quantization information

        Key Members
        -----------
        self.param_dict : DeviceParams
            A dictionary with tensor name as keys and numpy array as values.
            Stores the parameters of the model.
        '''
        self._model = model
        self.arch = NNModelArch.RESNET
        self.mapname = 'newmap'
        self.quantize = False
        self.__dict__.update(kwargs)
        assert isinstance(self.arch, NNModelArch), f"unsupported model arch: {self.arch}"
        self.shaper: BaseShaper = self._get_shaper()

        self._raw_graph: nx.MultiDiGraph = nx.MultiDiGraph()
        self._raw_dicts: Dict = dict() 
        self._operator_nodes: List[str] = []
        self._variable_nodes: List[str] = []
        self.param_dict: DeviceParams = dict()

        self.origin_graph: OriginGraph
        self.host_graph: HostGraph
        self.device_graph: DeviceGraph

    def _get_shaper(self) -> None:
        return __SHAPER_ACCESS_TABLE__[self.arch]()

    @staticmethod
    def _is_merge_node(node: onnx.NodeProto) -> bool:
        return True if node.op_type in MERGE_OPS else False

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
        return True if type in {'Conv'} else False

    @staticmethod
    def _is_gemm(type: str) -> bool:
        return True if type in {'Gemm'} else False

    @staticmethod
    def _is_pool(type: str) -> bool:
        return True if type in {'MaxPool','AveragePool','GlobalAveragePool'} else False

    @staticmethod
    def _is_act(type: str) -> bool:
        return True if type in {'Relu','PRelu','HardSigmoid'} else False
    
    @staticmethod
    def _is_resize(type: str) -> bool:
        return True if type in {'Resize'} else False

    def _get_variable(self, name: str) -> onnx.TensorProto:
        for var in self._model.graph.initializer:
            if var.name == name:
                return var
        print(f"cannot find variable named {name}")
        sys.exit()

    def _verify_op_type(self, node: onnx.NodeProto) -> None:
        assert node.op_type in VALID_OPS, f"unsupported op type: {node.op_type}"
        if node.op_type in {'Concat, Flatten'}:
            assert self._get_node_attr(node,'axis') == 1, f"axis must be 1 for op_type: {node.op_type}" 

    def _get_io_size(self, node: onnx.NodeProto) -> Tuple[List[int], List[int]]:
        # get input and output size
        name = node.input[0]
        i_dims = self._get_data_dims(name,self._model.graph)
        name = node.output[0]
        o_dims = self._get_data_dims(name,self._model.graph)
        return list(i_dims[-2:]), list(o_dims[-2:])

    def _complete_conv_config(self, node: onnx.NodeProto, d: Dict) -> None:
        size_i, size_o = self._get_io_size(node)
        d['conv_input_size'] = size_i
        d['conv_output_size'] = size_o
        d['conv_pads'] = [0]*4 # some conv operators have no conv_pads

        for at in node.attribute:
            if at.name == 'dilations':
                assert list(at.ints) == [1, 1], (
                    f"conv_dilations must be [1, 1], but got {at.ints}")
            elif at.name == 'group':
                assert at.i == 1, f"conv_group must be 1, but got {at.i}"
            elif at.name == 'kernel_shape':
                d['conv_kernel_size'] = list(at.ints)
            elif at.name == 'pads':
                d['conv_pads'] = list(at.ints)
            elif at.name == 'strides':
                d['conv_strides'] = list(at.ints)

        weight = self._get_variable(node.input[1]) # input[1] should be weight
        bias = None
        if len(node.input) > 2: # if has bias
            bias = self._get_variable(node.input[2]) # input[2] should be weight

        # save convolution weights
        name = node.name + '_conv_weight'
        d['conv_weight'] = name
        self.param_dict[name] = onh.to_array(weight)

        # save convolution bias
        name = node.name + '_conv_bias'
        d['conv_bias'] = name
        self.param_dict[name] = None if bias is None else onh.to_array(bias)

        d['conv_num_ichan'] = weight.dims[1] # input channel number
        d['conv_num_ochan'] = weight.dims[0] # output channel number

    def _complete_pool_config(self, node: onnx.NodeProto, d: Dict) -> None:
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

    def _complete_gemm_config(self, node: onnx.NodeProto, d: Dict) -> None:
        weight = onh.to_array(self._get_variable(node.input[1])) # input[1] should be weight
        if len(node.input[2]): # if has bias
            bias = onh.to_array(self._get_variable(node.input[2])) # input[2] should be weight
        else: bias = np.zeros(weight.dims[0])

        d['fc_weight'] = weight
        d['fc_bias'] = bias
        d['fc_len_inv'] = weight.shape[1] # input vector length
        d['fc_len_outv'] = weight.shape[0] # output vector length

    def _complete_act_config(self, node: onnx.NodeProto, d: Dict) -> None:
        d['act_mode'] = node.op_type 
        for at in node.attribute:
            if at.name == 'alpha':
                d['act_alpha'] = at.f

    def _complete_resize_config(self, node: onnx.NodeProto, d: Dict) -> None:
        scales = onh.to_array(self._get_variable(node.input[1]))
        assert scales.shape[0] == 4, f"resize scales must be a 4-element array"
        assert scales[0] * scales[1] == 1, f"resize scales on batch and channels must be 1, but got {scales}"
        d['resize_scales'] = scales

    def _get_raw_config(self, node: onnx.NodeProto) -> OperatorConfig:
        config = dict()
        config['op_type'] = node.op_type

        if self._is_conv(node.op_type):
            self._complete_conv_config(node, config)

        elif self._is_pool(node.op_type): 
            self._complete_pool_config(node, config)

        elif self._is_gemm(node.op_type):
            self._complete_gemm_config(node, config)

        elif self._is_act(node.op_type):
            self._complete_act_config(node, config)

        elif self._is_resize(node.op_type):
            self._complete_resize_config(node, config)

        return config

    def _remove_data_nodes(self) -> None:
        '''
        This constructed raw graph is naturally a bipartite graph
        which contains both operator nodes and variable nodes.
        This method simplifies the raw graph by removes variable nodes in it.

        The implementation of this method follows two features in the raw graph:
        1. Operator nodes have at least one inputs and a single output.
        2. Variable nodes have single input and at least one outputs.
        '''
        self._variable_nodes = list(set(self._variable_nodes))
        for n in self._variable_nodes:
            inputs = list(self._raw_graph.predecessors(n))
            outputs = list(self._raw_graph.successors(n))
            self._raw_graph.remove_node(n)
            if len(inputs) > 0 and len(outputs) > 0: # not input data nor output data
                assert len(inputs) == 1, f"error: data node {n} has multiple inputs" # feature 2
                for output in outputs:
                    self._raw_graph.add_edge(inputs[0],output)

    def _insert_quant_info(self) -> None:
        '''
        Insert quantization information to original operation graph
        The device graph is constructed from the original graph,
        so the quantization information will be updated to the device graph
        '''
        quantinfo_path = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'quantinfo.pkl')
        load_quant_to_graph(quantinfo_path, self.origin_graph)

    def construct_origin_graph(self) -> None:
        for i, n in enumerate(self._model.graph.node):
            now_node = n.name if n.name != '' else f'{n.op_type}_{i}'
            self._operator_nodes.append(now_node)
            self._verify_op_type(n) # verify if the op type is supported

            if self._is_merge_node(n): # multi inputs
                for pred_node in n.input:
                    self._variable_nodes.append(pred_node+'_d')
                    self._raw_graph.add_edge(pred_node+'_d',now_node)
    
            else: # only one input
                self._variable_nodes.append(n.input[0]+'_d')
                self._raw_graph.add_edge(n.input[0]+'_d', now_node)

            succ_node = n.output[0] # there is always one output
            self._variable_nodes.append(succ_node+'_d')
            self._raw_graph.add_edge(now_node, succ_node+'_d')
            self._raw_dicts[now_node] = self._get_raw_config(n)

        self._remove_data_nodes()
        self.origin_graph = OriginGraph(
            self._raw_graph, 
            self._raw_dicts, 
            self.arch,
            self.quantize
        )
        if self.quantize:
            self._insert_quant_info()

    def construct_host_graph(self) -> None:
        self.host_graph, self.device_graph = self.origin_graph.dispatch_graph()

    def construct_device_graph(self) -> None:
        self.shaper(self.device_graph)
        regularize_pad_sizes(self.device_graph)

    def run_conversion(self) -> None:
        self.construct_origin_graph()
        self.construct_host_graph()
        self.construct_device_graph()

    def save_params(self) -> None:
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname)
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
        self._print_dict(self._raw_dicts)

    def _plot_graph(self, graph: OperatorGraph, name: str) -> None:
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname, name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        graph.plot_graph(save_dir=save_dir)

    def plot_origin_graph(self) -> None:
        self._plot_graph(self.origin_graph, 'origin_graph')

    def plot_host_graph(self) -> None:
        self._plot_graph(self.host_graph, 'host_graph')

    def plot_device_graph(self) -> None:
        self._plot_graph(self.device_graph, 'device_graph')