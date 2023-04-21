import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import pickle
from copy import deepcopy
from typing import List, Dict, Optional, Tuple, Any, Union, Callable
from functools import wraps, cached_property
from maptools.core import (
    CTG, HostGraph, QuantConfig, 
    ModelParams, ROOT_DIR, PhysicalTile
)
from maptools.calcusim.utils import *
from maptools.host import HostTask

__all__ = ['CalcuSim']

OBSERVE_VARS = {
    'cast_in',
    'merge_in', 
    'gather_in',
    'cast_in_float', 
    'merge_in_float', 
    'gather_in_float',
    'before_pool', 
    'before_pool_float',
    'data_out',
    'data_out_float'
}

def cimu_conv2d(
    x: torch.Tensor,
    weight: torch.Tensor,
    bias: Optional[torch.Tensor] = None,
    stride: Optional[List[int]] = [1, 1]
) -> torch.Tensor:
    x = torch.clamp(x, -128, 127)
    x = x.type(torch.int8)
    y = 0
    for i in range(8):
        _y = F.conv2d(
            ((x >> i) & 1).float(),
            weight,
            stride=stride
        )
        # print("max:%-15dmin:%-15davg_abs:%d"%(int(torch.max(_y)), int(torch.min(_y)), float(torch.mean(torch.abs(_y)))))
        # _y = torch.clamp(_y, -1024, 1023)
        if i == 7: # sign bit
            y += _y*(-pow(2, 7))
        else: # non sign bit
            y += _y*pow(2, i)
    if bias is not None:
        y += bias.view([1, -1, 1, 1])
    return y


class ConvUnit(nn.Module):

    def __init__(
        self, 
        weight: torch.Tensor, 
        bias: torch.Tensor, 
        strides: List[int],
        physical: bool = False
    ) -> None:
        super().__init__()
        self.weight = weight
        self.bias = bias
        self.strides = strides
        self.func = cimu_conv2d if physical else F.conv2d

    def cuda(self):
        self.weight = self.weight.cuda()
        if self.bias is not None:
            self.bias = self.bias.cuda()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.func(x, self.weight, bias=self.bias, stride=self.strides)


class _Tile(nn.Module):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        # for general
        self.conv_pads: Optional[List] = None
        self.conv_weight: Optional[torch.Tensor] = None
        self.conv_bias: Optional[torch.Tensor] = None
        self.conv_strides: Optional[List] = None
        self.pool_mode: Optional[str] = None
        self.pool_pads: Optional[List] = None
        self.pool_kernel_size: Optional[List] = None
        self.pool_strides: Optional[List] = None
        self.act_mode: Optional[str] = None
        self.is_pool: bool = False
        self.is_act: bool = False
        self.is_merge: bool = False
        self.is_gather: bool = False

        # whether to observe data while running
        # enabling this variable will slow down the execution
        self.observe: bool = False 

        # for quantization
        self.merge_node: bool = False
        self.quantize: bool = False
        self.physical: bool = False
        self.ochan_range: Tuple[int, int] = (0, 0)

        self._init_quant_config()
        self.__dict__.update(kwargs)
        if self.quantize: self._init_for_quantization()
        if self.observe: self._init_observe_vars()
        self._init_conv_module()

    def _init_conv_module(self) -> None:
        self._conv = ConvUnit(
            self.conv_weight, 
            self.conv_bias, 
            self.conv_strides, 
            physical=self.physical
        )

    def _init_quant_config(self) -> None:
        for name in ['conv', 'add', 'relu']:
            self.__dict__[name + '_quant_config']: Optional[QuantConfig] = None

    def _init_observe_vars(self) -> None:
        for name in OBSERVE_VARS:
            self.__dict__[name]: Optional[torch.Tensor] = None

    def _init_for_quantization(self) -> None:
        if self.merge_node:
            assert self.conv_quant_config is not None, (
                f"quantize enabled but got no conv_quant_config")
        if self.is_gather:
            assert self.add_quant_config is not None, (
                f"quantize enabled but got no add_quant_config")
            assert self.co_scale == self.ai_scale, (
                f"conv output scale ({self.co_scale}) not add input scale ({self.ai_scale})")
        if self.is_act:
            assert self.relu_quant_config is not None, (
                f"quantize enabled but got no relu_quant_config")

    def cuda(self) -> None:
        self._conv.cuda()
        if self.quantize:
            self.cw_scale = self.cw_scale.cuda()

    @property
    def cw_scale(self) -> torch.Tensor:
        return self.conv_quant_config.weight_scale
    
    @cw_scale.setter
    def cw_scale(self, value: torch.Tensor) -> None:
        self.conv_quant_config.weight_scale = value
    
    @property
    def ci_scale(self) -> float:
        return self.conv_quant_config.input_scale
    
    @property
    def co_scale(self) -> float:
        return self.conv_quant_config.output_scale
    
    @property
    def ai_scale(self) -> float: # should be equal to `self.co_scale`
        return self.add_quant_config.input_scale

    @property
    def ao_scale(self) -> float:
        return self.add_quant_config.output_scale
    
    @property
    def ri_scale(self) -> float:
        return self.relu_quant_config.input_scale
    
    @property
    def ro_scale(self) -> float:
        return self.relu_quant_config.output_scale
    
    @cached_property
    def o_scale(self) -> float:
        scale = self.co_scale
        if self.is_act: scale = self.ro_scale
        elif self.is_gather: scale = self.ao_scale
        return scale
    
    def record_observe_vars(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            if self.quantize and self.observe:
                self.cast_in_float = self.cast_in * self.ci_scale
                if self.is_merge:
                    self.merge_in_float = self.merge_in * self.ci_scale
                if self.is_gather:
                    self.gather_in_float = self.gather_in * self.co_scale
                if self.is_pool: 
                    self.before_pool_float = self.before_pool * self.o_scale
                self.data_out = res
                self.data_out_float = self.data_out * self.o_scale
            return res
        return wrapper

    def _absorb(self, *args: Tuple[torch.Tensor]) -> None:
        self.cast_in = args[0]
        self.merge_in = args[1]
        self.gather_in = args[2]

    @record_observe_vars
    def forward(self, *args: Tuple[torch.Tensor]) -> torch.Tensor:
        self._absorb(*args)
        assert self.cast_in is not None, "cast in data got None"
        x = F.pad(
            self.cast_in, 
            self.conv_pads
        )
        x = self._conv(x)
        
        if self.is_merge:
            assert self.merge_in is not None, "merge in data got None"
            assert x.shape == self.merge_in.shape, (
                f"got x's shape = {x.shape} but merge's shape = {self.merge_in.shape}, cannot merge")
            x = torch.add(x, self.merge_in)

        # only for merge node where a complete sum should appear
        # conv quantization converting from input to output, return a int8
        if self.merge_node and self.quantize:
            weight_scale = self.cw_scale[self.ochan_range[0]:self.ochan_range[1]]
            weight_scale = weight_scale.view([1, -1, 1, 1])
            x = torch.round(x * weight_scale * self.ci_scale / self.co_scale)
            x = torch.clamp(x, -128, 127)

        if self.is_gather:
            assert self.merge_node, f"this is a gather_in node but is not a merge node"
            assert self.gather_in is not None, "gather in data got None"
            assert x.shape == self.gather_in.shape, (
                f"got x's shape = {x.shape} but gather's shape = {self.gather_in.shape}, cannot gather")
            x = torch.add(x, self.gather_in)

            # only for tile with gather in dataflow
            # add quantization converting from input to output, return a int8
            if self.quantize:
                x = torch.round(x * self.ai_scale / self.ao_scale)
                x = torch.clamp(x, -128, 127)

        if self.is_act:
            assert self.act_mode == 'Relu', (
                f"activation mode must be Relu, but got {self.act_mode}")
            x = F.relu(x)

            # only for tile with activation (relu)
            # add quantization converting from input to output, return a int8
            if self.quantize:
                x = torch.round(x * self.ri_scale / self.ro_scale)
                x = torch.clamp(x, -128, 127)

        if self.is_pool:
            if self.observe: self.before_pool = x
            assert self.pool_mode in ['MaxPool', 'AveragePool'], (
                f"got invalid pool mode: {self.pool_mode}")
            x = F.pad(x, self.pool_pads)
            if self.pool_mode == 'MaxPool':
                x = F.max_pool2d(
                    x, 
                    kernel_size = tuple(self.pool_kernel_size),
                    stride = tuple(self.pool_strides)
                )
            elif self.pool_mode == 'AveragePool':
                assert not self.quantize, "quantitized average pooling not supported yet"
                x = F.avg_pool2d(
                    x, 
                    kernel_size = tuple(self.pool_kernel_size),
                    stride = tuple(self.pool_strides)
                )

        return x


class CalcuSim(nn.Module):

    def __init__(
        self, 
        ctg: CTG, 
        host_graph: HostGraph, 
        params: ModelParams,
        **kwargs: Any
    ) -> None:
        '''
        `CalcuSim` is a calculation simulation engine for post-mapping inference.

        The original AI model is deconstructed to some abstract data structures such
        as `HostGraph`, `DeviceGraph`, and `CTG`, but is reconstructed in `CalcuSim` 
        in the format of `torch.nn.Module`.

        `CalcuSim` is composed of two main parts: the host task and the device task.
        The host task is reconstructed as a `HostTask` according to `HostGraph`.
        The device task is reconstructed by multiple tiles executors according to `CTG`.

        Parameters
        ----------
        ctg : CTG
            communication trace graph, obtained from `TileMapper.ctg`
        
        params : ModelParams
            device param dictionary, with operator name as keys and the parameters as
            values, obtained from `OnnxConverter.params`.

        kwargs : Dict
            mapname : str = 'newmap'
                map name

        Examples
        --------
        Users can treat `CalcuSim` as a complete replacement of the torch model.
        For example, if we have an AI model with the format of `torch.nn.Module`, 
        we can perform inference by calling the model object:

        >>> model = .... # my torch model
        >>> x = torch.Tensor(...) # input data
        >>> y = model(x)

        Now suppose we have our torch model exported to an .onnx file and then mapped
        to `CTG` and `HostGraph`, to reconstruct the inference task of the original 
        AI model, we can instantiate a CalcuSim object and call it:

        >>> csim = CalcuSim(...) # instantiate a CalcuSim object
        >>> y = csim(x)

        That means, `CalcuSim` expose the same software interface as the torch model, 
        and we can perform post-mapping infrence as if we are operating the torch model.

        Besides, `CalcuSim` supports cuda acceleration, which can be enabled by calling
        the method `CalcuSim.cuda()`:

        >>> csim.cuda()
        >>> y = csim(x)

        Key Members
        -----------
        self.obj_dict : Dict[Union[PhysicalTile, str], Union[_Tile, torch.Tensor]]
            A dictionary with physical tile id as keys and its corrensponding tile
            executors and values. The tile executors are the submodules of CalcuSim.

        self.res_dict : Dict[Union[str, Tuple], Dict[str, Optional[torch.Tensor]]]
            Stores the intermediate results of each tile.
            A dictionary with logical tile as keys and result dictionary as values
            Where the result dictionary has keys in `OBSERVE_VARS`.
        '''
        super().__init__()
        self.ctg = ctg
        self.host_graph = host_graph
        self.params = params
        self.mapname: str = 'newmap'
        self.quantize: bool = False
        self.observe: bool = False
        self.physical: bool = False
        self.__dict__.update(kwargs)

        if self.physical and not self.quantize:
            raise AssertionError ("to use physical CIMU, quantize must be enabled")
        
        self.obj_dict: Dict[Union[PhysicalTile, str], torch.Tensor] = dict()
        self.res_dict: Dict[Union[PhysicalTile, str], Dict[str, Optional[torch.Tensor]]] = dict()

        self._build_device_task()
        self._build_host_task()

    def _build_device_task(self) -> None:
        for node in self.ctg.node_names:
            if self.ctg.is_comm(node): # is comm
                self.obj_dict[node] = 0
                
            else: # is tile
                cfg = self.ctg.get_tile_config(node)
                kwargs = get_tile_kwargs(cfg, self.params)
                is_merge = False
                is_gather = False
                for pred in self.ctg.preds(node):
                    if self.ctg.is_merge_comm(pred):
                        is_merge = True
                    if self.ctg.is_gather_comm(pred):
                        is_gather = True
                self.obj_dict[node] = _Tile(
                    is_merge=is_merge, 
                    is_gather=is_gather,
                    quantize=self.quantize,
                    physical=self.physical,
                    observe = self.observe,
                    **kwargs
                )

    def _build_host_task(self) -> None:
        self.host_task = HostTask(self.host_graph, self.params)

    def _arrage_output(self, y: List[Tuple]) -> torch.Tensor:
        y.sort(key=lambda x : x[0])
        return torch.cat([v[1] for v in y], dim=1)

    def cuda(self) -> None:
        self.host_task.cuda()
        for node in self.obj_dict.keys():
            if self.ctg.is_tile(node):
                self.obj_dict[node].cuda()

    def empty_device_buffer(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for comm in self.ctg.comms:
                self.obj_dict[comm] = 0
            return func(self, *args, **kwargs)
        return wrapper

    @empty_device_buffer
    def _forward_device_task(self, x: torch.Tensor) -> List[torch.Tensor]:
        assert isinstance(x, torch.Tensor), f"input should be torch.Tensor, but got {type(x)}"
        assert len(x.shape) == 4, f"input dimension should be 4 [N, C, H, W], but got {len(x.shape)}"
        print('Launching CalcuSim ....')
        print('Quantization ' + ('Enabled' if self.quantize else 'Disabled'))

        # to store the raw output
        # the length of `output_list` equals the number of output layers in device task
        # each sublist of `output_list` stores the output of all tiles in one output layer
        # the arrangement of the sublists follows the order of bridge index
        # each member of the sublist is a tuple with the tile output tensor as the second 
        # element and the corresponding region index of the tile as the first element
        output_list = [[]] * self.ctg.output_num

        #quantizing before performing device task
        if self.quantize:
            x = torch.round(torch.divide(x, self.ctg.iqc.input_scale))
            x = torch.clamp(x, -128, 127)

        # device task
        for node in self.ctg.tiles:
            # get input data
            cast_in, merge_in, gather_in = None, None, None
            if self.ctg.is_head_tile(node):
                cast_in = x
            else:
                if self.ctg.has_cast_in(node):
                    cast_in = self.obj_dict[self.ctg.cast_pred_comm(node)]
                if self.ctg.has_merge_in(node):
                    merge_in = self.obj_dict[self.ctg.merge_pred_comm(node)]
                if self.ctg.has_gather_in(node):
                    gather_in = self.obj_dict[self.ctg.gather_pred_comm(node)]
            
            # perform tile execution
            temp_y = self.obj_dict[node](cast_in, merge_in, gather_in)
            
            # store output data
            if self.ctg.is_tail_tile(node):
                bridge_idx = self.ctg.dicts[node]['bridge_idx']
                output_list[bridge_idx].append((node[1], temp_y))

            else:
                if self.ctg.has_cast_out(node):
                    self.obj_dict[self.ctg.cast_succ_comm(node)] = temp_y
                if self.ctg.has_merge_out(node):
                    self.obj_dict[self.ctg.merge_succ_comm(node)] += temp_y
                if self.ctg.has_gather_out(node):
                    self.obj_dict[self.ctg.gather_succ_comm(node)] = temp_y
            
            # collect intermediate results
            # execute only when observing is enabled
            if self.observe:
                res = dict()
                for name in OBSERVE_VARS:
                    res[name] = self.obj_dict[node].__dict__[name]
                self.res_dict[node] = res

        device_output = [self._arrage_output(y) for y in output_list]
        self.res_dict['output'] = device_output # the output of device task

        # dequantizing before performing host task
        if self.quantize:
            device_output = [torch.mul(y, self.ctg.oqc[i].output_scale) for i, y in enumerate(device_output)]
        print('Finished Device Task')
        return device_output

    def _forward_host_task(self, x: List[torch.Tensor]) -> torch.Tensor:
        host_output = self.host_task(x)
        print('Finished Host Task')
        print('Finished CalcuSim')
        return host_output

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self._forward_host_task(self._forward_device_task(x))

    def save_results(self, file_name: str = 'results'):
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'calcusim')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        file_dir = os.path.join(save_dir, file_name+'.pkl')
        with open(file_dir,'wb') as f:
            pickle.dump(self.res_dict, f)
        print(f"\nintermediate results written to {file_dir}")