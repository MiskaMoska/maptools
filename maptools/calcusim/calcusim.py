import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import pickle
from copy import deepcopy
from typing import List, Dict, Optional, Tuple, Any, Union, Callable, Literal
from functools import wraps, cached_property
from maptools.core import CTG, OperatorGraph, QuantConfig, DeviceParams, ROOT_DIR
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
        _y = torch.clamp(_y, -1024, 1023)
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


class _Xbar(nn.Module):

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

        rebuild_pads(self.conv_pads)
        rebuild_pads(self.pool_pads)

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

            # only for xbar with gather in dataflow
            # add quantization converting from input to output, return a int8
            if self.quantize:
                x = torch.round(x * self.ai_scale / self.ao_scale)
                x = torch.clamp(x, -128, 127)

        if self.is_act:
            assert self.act_mode == 'Relu', (
                f"activation mode must be Relu, but got {self.act_mode}")
            x = F.relu(x)

            # only for xbar with activation (relu)
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
        host_graph: OperatorGraph, 
        params: DeviceParams,
        **kwargs: Any
    ) -> None:
        '''
        Parameters
        ----------
        ctg : CTG
            communication trace graph
        
        params : DeviceParams
            from `OnnxConverter.param_dict`

        kwargs : Dict
            mapname : str = 'newmap'
                Map name

        Key Members
        -----------
        self.res_dict : Dict[Union[str, Tuple], Dict[str, Optional[torch.Tensor]]]
            Stores the intermediate results of each xbar
            A dictionary with logical xbar as keys and result dictionary as values
            Where the result dictionary has keys in `OBSERVE_VARS`
        '''
        super().__init__()
        self.ctg = ctg
        self.params = params
        self.mapname: str = 'newmap'
        self.quantize: bool = False
        self.observe: bool = False
        self.physical: bool = False
        self.__dict__.update(kwargs)
        if self.physical and not self.quantize:
            raise AssertionError ("to use physical CIMU, quantize must be enabled")
        self.obj_dict: Dict[Any, Union[_Xbar, torch.Tensor]] = dict()
        self._build_device_task()
        self._build_host_task(host_graph)
        self.res_dict: Dict[Union[str, Tuple], Dict[str, Optional[torch.Tensor]]] = dict()

    def _build_device_task(self) -> None:
        for node in self.ctg.node_names:

            if self.ctg.is_comm(node): # is comm
                self.obj_dict[node] = 0
                
            else: # is xbar
                cfg = self.ctg.get_xbar_config(node)
                kwargs = get_xbar_kwargs(cfg, self.params)
                is_merge = False
                is_gather = False
                for pred in self.ctg.preds(node):
                    if self.ctg.is_merge_comm(pred):
                        is_merge = True
                    if self.ctg.is_gather_comm(pred):
                        is_gather = True
                self.obj_dict[node] = _Xbar(
                    is_merge=is_merge, 
                    is_gather=is_gather,
                    quantize=self.quantize,
                    physical=self.physical,
                    observe = self.observe,
                    **kwargs
                )

    def _build_host_task(self, host_graph: OperatorGraph) -> None:
        self.host_task = HostTask(host_graph)

    def _arrage_output(self, y: List[Tuple]) -> torch.Tensor:
        y.sort(key=lambda x : x[0])
        return torch.cat([v[1] for v in y], dim=1)

    def cuda(self) -> None:
        '''
        This method is implemented particularly to support cuda acceleration.
        For example, to enable cuda acceleration, use:
        >>> model = CalcuSim(*args, **kwargs)
        >>> model.cuda()
        cuda acceleration is default to be disabled when the CalcuSim obejct is initialized.
        '''
        self.host_task.cuda()
        for node in self.obj_dict.keys():
            if self.ctg.is_xbar(node):
                self.obj_dict[node].cuda()

    def empty_data_cache(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for comm in self.ctg.comms:
                self.obj_dict[comm] = 0
            return func(self, *args, **kwargs)
        return wrapper

    @empty_data_cache
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        assert isinstance(x, torch.Tensor), f"input should be torch.Tensor, but got {type(x)}"
        assert len(x.shape) == 4, f"input dimension should be 4 [N, C, H, W], but got {len(x.shape)}"
        print('Launching CalcuSim ....')
        print('Quantization ' + ('Enabled' if self.quantize else 'Disabled'))
        y = []

        #quantizing before performing device task
        if self.quantize:
            x = torch.round(torch.divide(x, self.ctg.input_quant_config.input_scale))
            x = torch.clamp(x, -128, 127)

        # device task
        for node in self.ctg.xbars:
            # get input data
            cast_in, merge_in, gather_in = None, None, None
            if self.ctg.is_head_xbar(node):
                cast_in = x
            else:
                if self.ctg.has_cast_in(node):
                    cast_in = self.obj_dict[self.ctg.cast_pred_comm(node)]
                if self.ctg.has_merge_in(node):
                    merge_in = self.obj_dict[self.ctg.merge_pred_comm(node)]
                if self.ctg.has_gather_in(node):
                    gather_in = self.obj_dict[self.ctg.gather_pred_comm(node)]
            
            # perform xbar execution
            temp_y = self.obj_dict[node](cast_in, merge_in, gather_in)
            
            # store output data
            if self.ctg.is_tail_xbar(node):
                y.append((node[1], temp_y))

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

        device_output = self._arrage_output(y)
        self.res_dict['output'] = device_output # the output of device task

        # dequantizing before performing host task
        if self.quantize:
            device_output = torch.mul(device_output, self.ctg.output_quant_config.output_scale)
        print('Finished Device Task')

        # host task
        host_output = self.host_task(device_output)
        print('Finished Host Task')
        print('Finished CalcuSim')
        return host_output
    
    def save_results(self, file_name: str = 'results'):
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'calcusim')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        file_dir = os.path.join(save_dir, file_name+'.pkl')
        with open(file_dir,'wb') as f:
            pickle.dump(self.res_dict, f)
        print(f"\nintermediate results written to {file_dir}")