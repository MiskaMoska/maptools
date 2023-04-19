import onnx
import numpy as np
from abc import ABCMeta, abstractmethod
from typing import Dict, List, Tuple
from maptools.core import OperatorConfig, DeviceParams
import onnx.numpy_helper as onh

__all__ = ['__PARSER_ACCESS_TABLE__']

class BaseOperatorParser(object):

    def __init__(
        self, 
        node: onnx.NodeProto, 
        graph: onnx.GraphProto, 
        param_dict: DeviceParams
    ) -> None:
        if not isinstance(node, onnx.NodeProto):
            raise TypeError(
                f"shaper need a {onnx.NodeProto} to proccess, but got a {type(node)}")
        if not isinstance(graph, onnx.GraphProto):
            raise TypeError(
                f"shaper need a {onnx.GraphProto} to proccess, but got a {type(graph)}")
        self.node = node
        self.graph = graph
        self.param_dict = param_dict

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

    def process(self) -> OperatorConfig:
        self.config = {}
        self.config['name'] = self.node.name
        self.config['op_type'] = self.node.op_type
        return self.config


class ConvParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        size_i, size_o = self._get_io_size(self.node)
        self.config['conv_input_size'] = size_i
        self.config['conv_output_size'] = size_o
        self.config['conv_pads'] = [0]*4 # some conv operators have no conv_pads

        for at in self.node.attribute:
            if at.name == 'dilations':
                assert list(at.ints) == [1, 1], (
                    f"conv_dilations must be [1, 1], but got {at.ints}")
            elif at.name == 'group':
                assert at.i == 1, f"conv_group must be 1, but got {at.i}"
            elif at.name == 'kernel_shape':
                self.config['conv_kernel_size'] = list(at.ints)
            elif at.name == 'pads':
                self.config['conv_pads'] = list(at.ints)
            elif at.name == 'strides':
                self.config['conv_strides'] = list(at.ints)

        weight = self._get_variable(self.node.input[1]) # input[1] should be weight
        bias = None
        if len(self.node.input) > 2: # if has bias
            bias = self._get_variable(self.node.input[2]) # input[2] should be weight

        # save convolution weights
        name = self.node.name + '_conv_weight'
        self.config['conv_weight'] = name
        self.param_dict[name] = onh.to_array(weight)

        # save convolution bias
        name = self.node.name + '_conv_bias'
        self.config['conv_bias'] = name
        self.param_dict[name] = None if bias is None else onh.to_array(bias)

        self.config['conv_num_ichan'] = weight.dims[1] # input channel number
        self.config['conv_num_ochan'] = weight.dims[0] # output channel number

        return self.config


class PoolParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        size_i, size_o = self._get_io_size(self.node)
        self.config['pool_input_size'] = size_i
        self.config['pool_output_size'] = size_o
        self.config['pool_mode'] = self.node.op_type

        for at in self.node.attribute:
            if at.name == 'ceil_mode':
                self.config['pool_ceil_mode'] = at.i
            elif at.name == 'kernel_shape':
                self.config['pool_kernel_size'] = list(at.ints)
            elif at.name == 'pads':
                self.config['pool_pads'] = list(at.ints)
            elif at.name == 'strides':
                self.config['pool_strides'] = list(at.ints)

        return self.config


class GemmParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        weight = onh.to_array(self._get_variable(self.node.input[1])) # input[1] should be weight
        if len(self.node.input[2]): # if has bias
            bias = onh.to_array(self._get_variable(self.node.input[2])) # input[2] should be weight
        else: bias = np.zeros(weight.dims[0])

        self.config['gemm_weight'] = weight
        self.config['gemm_bias'] = bias
        self.config['gemm_len_inv'] = weight.shape[1] # input vector length
        self.config['gemm_len_outv'] = weight.shape[0] # output vector length

        return self.config


class ActParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        self.config['act_mode'] = self.node.op_type 
        for at in self.node.attribute:
            if at.name == 'alpha':
                self.config['act_alpha'] = at.f
        
        return self.config


class ResizeParser(BaseOperatorParser):

    def process(self) -> OperatorConfig:
        super().process()
        scales = onh.to_array(self._get_variable(self.node.input[1]))
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
    'HardSigmoid'           : ActParser,
    'Resize'                : ResizeParser,
    'Flatten'               : FlattenParser,
    'Reshape'               : ReshapeParser,
    'Transpose'             : TransposeParser,
    'Add'                   : BaseOperatorParser,
    'Concat'                : BaseOperatorParser
}