'''
# // TODO need to provide the size info (W x H) of the intermidiate data (size info is restored after onnx-sim)
# // TODO need to support multi-style paddings in inception (there is no Pads any more in onnx-simplified model)
TODO need to support reduce mean in mnasnet
TODO need to support sigmoid in efficientnet
TODO need to support global average pool and gemm layer
'''
import os
import sys
import pickle
import onnx
from typing import Any, List, Dict, Tuple, Optional, Generator
from maptools.utils import load_quant_to_graph, regularize_pads, recheck_pads
from maptools.mapper.graph_shaper import *
from maptools.mapper.operator_parser import *
from maptools.core import (
    OperatorVariableGraph, OperatorGraph, OriginGraph, 
    HostGraph, DeviceGraph, NNModelArch,
    VALID_OPS, MERGE_OPS, ROOT_DIR, OperatorConfig, ModelParams
)

__all__ = ['OnnxConverter']

class OnnxConverter(object):

    def __init__(self, model: onnx.ModelProto, **kwargs: Any) -> None:
        '''
        Convert Onnx to NVCIM intermediate representation which will be fed to TileMapper and NocMapper.
        About supported op_type:
            The supported onnx op_types are listed in `VALID_OPS`. Note that:
            1. Sigmoid is not supported cause it is not hardware-friendly.
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
        ----------
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
        self.params : ModelParams
            A dictionary with tensor name as keys and numpy array as values.
            Stores the parameters of the model.
        '''
        self._model = model
        self.arch = NNModelArch.RESNET
        self.mapname = 'newmap'
        self.quantize = False
        self.__dict__.update(kwargs)
        assert isinstance(self.arch, NNModelArch), f"unsupported model arch: {self.arch}"

        self.params: ModelParams = dict()
        self.shaper = __SHAPER_ACCESS_TABLE__[self.arch]()

        self.raw_graph: OperatorVariableGraph
        self.origin_graph: OriginGraph
        self.host_graph: HostGraph
        self.device_graph: DeviceGraph

        self.raw_graph = OperatorVariableGraph()

    def _assert_node(self, node: onnx.NodeProto) -> None:
        assert node.op_type in VALID_OPS, f"unsupported op type: {node.op_type}"
        if node.op_type in {'Concat'}:
            for at in node.attribute:
                if at.name == 'axis':
                    assert at.i == 1, f"axis must be 1 for op_type: {node.op_type}" 

        if node.op_type in {'Add', 'Mul'}:
            assert len(node.input) == 2, (
                f"input number of Add and Mul operations must be 2, but got {len(node.input)}")

    def _construct_raw_graph(self) -> None:
        for i, n in enumerate(self._model.graph.node):
            node_name = n.name if n.name != '' else f'{n.op_type}_{i}'
            self.raw_graph.add_operator_node(node_name)
            self._assert_node(n)

            if n.op_type in MERGE_OPS: # multi inputs
                # this step is for adding merge edges whose source nodes are variables
                # and destination node is an operator, it will guarantee the order of 
                # the merge variables, which is necessary for operators like Concat.
                for pred_node in n.input:
                    self.raw_graph.add_variable_node(pred_node+'_d')
                    self.raw_graph.add_edge(pred_node+'_d', node_name)
    
            else: # only one input
                self.raw_graph.add_variable_node(n.input[0]+'_d')
                self.raw_graph.add_edge(n.input[0]+'_d', node_name)

            succ_node = n.output[0] # there is always a unique output
            self.raw_graph.add_variable_node(succ_node+'_d')
            self.raw_graph.add_edge(node_name, succ_node+'_d')

            parser = __PARSER_ACCESS_TABLE__[n.op_type](n, self._model.graph, self.params)
            self.raw_graph.set_operator_config(node_name, parser())

    def insert_quant_info(self) -> None:
        '''
        Insert quantization information to original operation graph
        The device graph is constructed from the original graph,
        so the quantization information will be updated to the device graph
        '''
        quantinfo_path = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'quantinfo.pkl')
        load_quant_to_graph(quantinfo_path, self.origin_graph)

    def construct_origin_graph(self) -> None:
        self._construct_raw_graph()
        self.raw_graph.connect_concats()
        self.origin_graph = self.raw_graph.reduce(quantize=self.quantize)
        regularize_pads(self.origin_graph)
        if self.quantize:
            self.insert_quant_info()

    def construct_host_graph(self) -> None:
        self.host_graph, self.device_graph = (
            self.origin_graph.dispatch_graph(arch=self.arch))

    def construct_device_graph(self) -> None:
        self.shaper(self.device_graph)
        recheck_pads(self.device_graph)

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
            pickle.dump(self.params, f)
        print(f"parameters of the model has been written to: {file_dir}")

    def print_raw_dict(self) -> None:
        self.raw_graph.print_dict()

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