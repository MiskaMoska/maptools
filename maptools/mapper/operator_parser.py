import onnx
import numpy as np
from typing import Dict, List, Tuple
from functools import wraps
from maptools.core import OperatorConfig, ModelParams
import onnx.numpy_helper as onh

__all__ = ['__PARSER_ACCESS_TABLE__']

class BaseOperatorParser(object):

    processed_nodes = 0 

    def __init__(
        self, 
        node: onnx.NodeProto, 
        node_name: str, # the node.name may have duplicates, so all nodes are renamed outsides
        graph: onnx.GraphProto, 
        params: ModelParams
    ) -> None:
        if not isinstance(node, onnx.NodeProto):
            raise TypeError(
                f"parser need a {onnx.NodeProto} to proccess, but got a {type(node)}")
        if not isinstance(graph, onnx.GraphProto):
            raise TypeError(
                f"parser need a {onnx.GraphProto} to proccess, but got a {type(graph)}")
        self.node = node
        self.node_name = node_name
        self.graph = graph
        self.params = params

    def __call__(self) -> OperatorConfig:
        return self.process()

    def _get_variable(self, name: str) -> onnx.TensorProto:
        for var in self.graph.initializer:
            if var.name == name:
                return var
        raise RuntimeError(f"cannot find variable named {name}")

    @staticmethod
    def _get_data_dims(name: str, graph: onnx.GraphProto) -> List[int]:
        for tensor in graph.value_info:
            if tensor.name == name:
                dim = tensor.type.tensor_type.shape.dim
                return [d.dim_value for d in dim]
        dim = graph.input[0].type.tensor_type.shape.dim # not found in value_info, then it must be input
        return [d.dim_value for d in dim]

    def _get_io_size(self, node: onnx.NodeProto) -> Tuple[List[int], List[int]]:
        # get input and output size
        name = node.input[0]
        i_dims = self._get_data_dims(name, self.graph)
        name = node.output[0]
        o_dims = self._get_data_dims(name, self.graph)
        return list(i_dims[-2:]), list(o_dims[-2:])
    
    @staticmethod
    def assert_kernel_padding(kernel_shape: List[int], padding: List[int]) -> None:
        if kernel_shape is None or padding is None:
            return
        
        if (kernel_shape[0] <= padding[0]) or (
            kernel_shape[0] <= padding[2]) or (
            kernel_shape[1] <= padding[1]) or (
            kernel_shape[1] <= padding[3]
        ):
            raise AssertionError(
                f"kernel_shape {kernel_shape} must be larger than padding {padding}")

    def echo_invoke(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            print(f"Parsing Onnx Operator: {self.node_name} using Parser: {type(self)}")
            return func(self, *args, **kwargs)
        return wrapper

    @echo_invoke
    def process(self) -> OperatorConfig:
        self.config = {}
        self.config['name'] = self.node_name
        self.config['op_type'] = self.node.op_type
        self.processed_nodes += 1
        return self.config


class ConvParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        size_i, size_o = self._get_io_size(self.node)
        self.config['conv_input_size'] = size_i # input feature map size without pads
        self.config['conv_output_size'] = size_o # output feature map size without pads
        self.config['conv_pads'] = [0]*4 # some conv operators have no conv_pads

        kernel_shape, padding = None, None

        for at in self.node.attribute:
            if at.name == 'dilations':
                assert list(at.ints) == [1, 1], (
                    f"conv_dilations must be [1, 1], but got {at.ints}")
            elif at.name == 'group':
                assert at.i == 1, f"conv_group must be 1, but got {at.i}"
            elif at.name == 'kernel_shape':
                self.config['conv_kernel_size'] = list(at.ints)
                kernel_shape = list(at.ints)
            elif at.name == 'pads':
                self.config['conv_pads'] = list(at.ints)
                padding = list(at.ints)
            elif at.name == 'strides':
                self.config['conv_strides'] = list(at.ints)
        
        self.assert_kernel_padding(kernel_shape, padding)

        weight = self._get_variable(self.node.input[1]) # input[1] should be weight
        bias = None
        if len(self.node.input) > 2: # if has bias
            bias = self._get_variable(self.node.input[2]) # input[2] should be weight

        # save convolution weights
        name = self.node_name + '_conv_weight'
        self.config['conv_weight'] = name
        self.params[name] = onh.to_array(weight)

        # save convolution bias
        name = self.node_name + '_conv_bias'
        self.config['conv_bias'] = name
        self.params[name] = None if bias is None else onh.to_array(bias)

        self.config['conv_num_ichan'] = weight.dims[1] # input channel number
        self.config['conv_num_ochan'] = weight.dims[0] # output channel number

        return self.config


class PoolParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        size_i, size_o = self._get_io_size(self.node)
        self.config['pool_input_size'] = size_i # input feature map size without pads
        self.config['pool_output_size'] = size_o # output feature map size without pads
        self.config['pool_mode'] = self.node.op_type

        kernel_shape, padding = None, None

        for at in self.node.attribute:
            if at.name == 'ceil_mode':
                self.config['pool_ceil_mode'] = at.i
            elif at.name == 'kernel_shape':
                self.config['pool_kernel_size'] = list(at.ints)
                kernel_shape = list(at.ints)
            elif at.name == 'pads':
                self.config['pool_pads'] = list(at.ints)
                padding = list(at.ints)
            elif at.name == 'strides':
                self.config['pool_strides'] = list(at.ints)

        self.assert_kernel_padding(kernel_shape, padding)
        
        return self.config


class GemmParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        weight = self._get_variable(self.node.input[1]) # input[1] should be weight
        if len(self.node.input[2]): # if has bias
            bias = self._get_variable(self.node.input[2]) # input[2] should be weight
        else: bias = np.zeros(weight.dims[0])

        # save gemm weights
        name = self.node_name + '_gemm_weight'
        self.config['gemm_weight'] = name
        self.params[name] = onh.to_array(weight) 

        # save gemm bias
        name = self.node_name + '_gemm_bias'
        self.config['gemm_bias'] = name
        self.params[name] = None if bias is None else onh.to_array(bias)

        self.config['gemm_len_inv'] = weight.dims[1] # input vector length
        self.config['gemm_len_outv'] = weight.dims[0] # output vector length

        return self.config


class ActParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        size_i, _ = self._get_io_size(self.node)
        self.config['act_input_size'] = size_i
        self.config['act_mode'] = self.node.op_type 
        for at in self.node.attribute:
            if at.name == 'alpha':
                self.config['act_alpha'] = at.f
        
        return self.config


class ResizeParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        scales = onh.to_array(self._get_variable(self.node.input[-1]))
        assert scales.shape[0] == 4, (f"resize scales must be a 4-element array")
        assert scales[0] * scales[1] == 1, (
            f"resize scales on batch and channels must be 1, but got {scales}")
        assert scales[2].is_integer() and scales[3].is_integer(), (
            f"resize scales[2:4] must be int, but got {type(scales[2])}, {type(scales[3])}")
        assert scales[2] * scales[3] >= 1, (
            f"resize portion must be no less than 1, but got: {scales[2] * scales[3]}")
        self.config['resize_scales'] = scales.astype(np.int8)

        return self.config


class FlattenParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        for at in self.node.attribute:
            if at.name == 'axis':
                self.config['flatten_axis'] = at.i
        
        return self.config


class ReshapeParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        shape = self._get_variable(self.node.input[1])
        self.config['reshape_shape'] = onh.to_array(shape).tolist()

        return self.config


class TransposeParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        for at in self.node.attribute:
            if at.name == 'perm':
                self.config['transpose_perm'] = list(at.ints)

        return self.config


__PARSER_ACCESS_TABLE__ = {
    'Conv'                  : ConvParser,
    'Gemm'                  : GemmParser,
    'MaxPool'               : PoolParser,
    'AveragePool'           : PoolParser,
    'GlobalAveragePool'     : PoolParser,
    'Relu'                  : ActParser,
    'PRelu'                 : ActParser,
    'LeakyRelu'             : ActParser,
    'HardSigmoid'           : ActParser,
    'Resize'                : ResizeParser,
    'Flatten'               : FlattenParser,
    'Reshape'               : ReshapeParser,
    'Transpose'             : TransposeParser,
    'Add'                   : BaseOperatorParser,
    'Concat'                : BaseOperatorParser
}