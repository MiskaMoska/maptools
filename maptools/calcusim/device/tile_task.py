import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict, Optional, Tuple, Any, Callable
from maptools.core import TileQuantConfig, LogicalTile

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
    stride: Optional[List[int]] = [1, 1],
    factor: float = 1,
    tile: LogicalTile = None
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

        # ivc clamping transfer
        _y = torch.clamp(torch.round(_y / factor), -128, 127)

        # invert transfer
        _y = torch.round(torch.round(_y * factor))

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
        physical: bool = False,
        tile: LogicalTile = None,
        ivcf: Optional[float] = None,
        first_layer_ivcf: Optional[float] = None
    ) -> None:
        super().__init__()
        self.weight = weight
        self.bias = bias
        self.strides = strides
        self.tile = tile
        self.physical = physical

        # determine ivc transfer factor
        if ivcf is not None:
            if (first_layer_ivcf is not None) and (self.tile == (0, 0, 0, 0)):
                self.factor = first_layer_ivcf
            else:
                self.factor = ivcf
        else: self.factor = 1

    def cuda(self):
        self.weight = self.weight.cuda()
        if self.bias is not None:
            self.bias = self.bias.cuda()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.physical: # use physical cimu
            return cimu_conv2d(
                x, self.weight, 
                bias=self.bias, 
                stride=self.strides, 
                factor=self.factor,
                tile=self.tile
            )
        else: # use pytorch conv2d
            return F.conv2d(
                x, self.weight, 
                bias=self.bias, 
                stride=self.strides,                 
            )


class TileTask(nn.Module):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        # for general
        self.tile: LogicalTile = None
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
        self.quantize: bool = False
        self.tqc: Optional[TileQuantConfig] = None
        self.merge_node: bool = False
        self.physical: bool = False
        self.hardtrans: bool = True
        self.ivcf: Optional[float] = None
        self.first_layer_ivcf: Optional[float] = None

        self.__dict__.update(kwargs)
        self._init_conv_module()
        if self.observe: self._init_observe_vars()
        if self.is_resize: self._init_resize_module()

    def _init_conv_module(self) -> None:
        self._conv = ConvUnit(
            self.conv_weight, 
            self.conv_bias, 
            self.conv_strides, 
            physical=self.physical,
            tile=self.tile,
            ivcf=self.ivcf,
            first_layer_ivcf=self.first_layer_ivcf
        )

    def _init_resize_module(self) -> None:
        factor = (self.resize_scales[2], self.resize_scales[3])
        self._resize = nn.Upsample(scale_factor=factor)

    def _init_observe_vars(self) -> None:
        for name in OBSERVE_VARS:
            self.__dict__[name]: Optional[torch.Tensor] = None

    def cuda(self) -> None:
        self._conv.cuda()
        if self.quantize:
            self.tqc.ctrans = self.tqc.ctrans.cuda()
            self.tqc.ctrans_i = self.tqc.ctrans_i.cuda()
            self.tqc.ctrans_s = self.tqc.ctrans_s.cuda()
    
    def record_observe_vars(self, res: Any) -> None:
        self.cast_in_float = self.cast_in * self.tqc.i_scale
        if self.is_merge:
            self.merge_in_float = self.merge_in * self.tqc.i_scale
        if self.is_gather:
            self.gather_in_float = self.gather_in * self.tqc.co_scale
        if self.is_pool: 
            self.before_pool_float = self.before_pool * self.tqc.o_scale
        self.data_out = res
        self.data_out_float = self.data_out * self.tqc.o_scale

    def _absorb(self, *args: Tuple[torch.Tensor]) -> None:
        self.cast_in = args[0]
        self.merge_in = args[1]
        self.gather_in = args[2]

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
            if self.hardtrans:
                ctrans_i = self.tqc.ctrans_i.view([1, -1, 1, 1])
                ctrans_s = self.tqc.ctrans_s.view([1, -1, 1, 1])
                mult = ctrans_i / pow(2, -ctrans_s)
            else: mult = self.tqc.ctrans.view([1, -1, 1, 1])
            x = torch.clamp(torch.round(x * mult), -128, 127)

        if self.is_gather:
            assert self.merge_node, f"this is a gather_in node but is not a merge node"
            assert self.gather_in is not None, "gather in data got None"
            assert x.shape == self.gather_in.shape, (
                f"got x's shape = {x.shape} but gather's shape = {self.gather_in.shape}, cannot gather")
            x = torch.add(x, self.gather_in)

            # only for tile with gather in dataflow
            # add quantization converting from input to output, return a int8
            if self.quantize:
                if self.hardtrans: 
                    mult = self.tqc.strans_i / pow(2, -self.tqc.strans_s)
                else: mult = self.tqc.strans
                x = torch.clamp(torch.round(x * mult), -128, 127)

        if self.is_act:
            assert self.act_mode == 'Relu', (
                f"activation mode must be Relu, but got {self.act_mode}")
            x = F.relu(x)

            # only for tile with activation (relu)
            # add quantization converting from input to output, return a int8
            if self.quantize:
                if self.hardtrans:
                    mult = self.tqc.atrans_i / pow(2, -self.tqc.atrans_s)
                else: mult = self.tqc.atrans
                x = torch.clamp(torch.round(x * mult), -128, 127)

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
            
        if self.quantize and self.observe:
            self.record_observe_vars(x)

        return x