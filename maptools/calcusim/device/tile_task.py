import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict, Optional, Tuple, Any, Callable
from functools import wraps, cached_property
from maptools.core import QuantConfig

__all__ = ['TileTask']

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
        print("max:%-15dmin:%-15davg_abs:%d"%(int(torch.max(_y)), int(torch.min(_y)), float(torch.mean(torch.abs(_y)))))
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


class TileTask(nn.Module):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        # for general
        self.conv_pads: List[int] = None
        self.conv_weight: torch.Tensor = None
        self.conv_bias: Optional[torch.Tensor] = None
        self.conv_strides: List[int] = None
        self.pool_mode: Optional[str] = None
        self.pool_pads: Optional[List] = None
        self.pool_kernel_size: Optional[List[int]] = None
        self.pool_strides: Optional[List[int]] = None
        self.act_mode: Optional[str] = None
        self.resize_scales: List[int] = None
        self.is_pool: bool = False
        self.is_act: bool = False
        self.is_resize: bool = False
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
        if self.is_resize: self._init_resize_module()

    def _init_conv_module(self) -> None:
        self._conv = ConvUnit(
            self.conv_weight, 
            self.conv_bias, 
            self.conv_strides, 
            physical=self.physical
        )

    def _init_resize_module(self) -> None:
        factor = (self.resize_scales[2], self.resize_scales[3])
        self._resize = nn.Upsample(scale_factor=factor)

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

        if self.is_resize:
            x = self._resize(x)

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