import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict, Optional, Tuple, Any, Callable
from maptools.core import TileQuantConfig, LogicalTile
from maptools.calcusim.device import XbarConv
from copy import deepcopy

__all__ = ['TileTask']

OBSERVE_VARS = {
    'cast_in',
    'merge_in', 
    'gather_in',
    'cast_in_float', 
    'merge_in_float', 
    'gather_in_float',
    'after_xbar',
    'after_xbar_float',
    'before_pool', 
    'before_pool_float',
    'data_out',
    'data_out_float'
}

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
        self.stats: bool = False

        # for power evaluation
        self.eval_power: bool = False
        self.power_dict: Dict[LogicalTile, Dict[str, float]] = {}

        self.__dict__.update(kwargs)
        self._init_conv_module()
        if self.observe: self._init_observe_vars()
        if self.is_resize: self._init_resize_module()

    def _init_conv_module(self) -> None:
        self._conv = XbarConv(
            self.conv_weight,
            self.conv_strides, 
            physical=self.physical,
            tile=self.tile,
            tqc=self.tqc,
            ivcf=self.ivcf,
            first_layer_ivcf=self.first_layer_ivcf,
            stats=self.stats,
            eval_power=self.eval_power,
            power_dict=self.power_dict
        )

    def _init_resize_module(self) -> None:
        factor = (self.resize_scales[2], self.resize_scales[3])
        self._resize = nn.Upsample(scale_factor=factor)

    def _init_observe_vars(self) -> None:
        for name in OBSERVE_VARS:
            self.__dict__[name]: Optional[torch.Tensor] = None

    def cuda(self) -> None:
        self._conv.cuda()
        if self.conv_bias is not None:
            self.conv_bias = self.conv_bias.cuda()
        if self.quantize:
            self.tqc.cuda()
    
    def record_var(self, var: Optional[torch.Tensor], name: str) -> None:
        if self.observe:
            self.__dict__[name] = deepcopy(var)

    def record_input_vars(self, *args: Tuple[Optional[torch.Tensor]]) -> None:
        for i, name in enumerate(['cast_in', 'merge_in', 'gather_in']):
            self.record_var(args[i], name)

    def record_dequant_vars(self) -> None:
        if (not self.observe) or (not self.quantize):
            return 
        
        self.cast_in_float = self.cast_in * self.tqc.i_scale
        self.data_out_float = self.data_out * self.tqc.o_scale
        self.after_xbar_float = self.after_xbar * self.tqc.co_scale

        if self.is_merge: self.merge_in_float = self.merge_in * self.tqc.i_scale
        if self.is_gather: self.gather_in_float = self.gather_in * self.tqc.co_scale
        if self.is_pool: self.before_pool_float = self.before_pool * self.tqc.o_scale

    def forward(self, *args: Tuple[torch.Tensor]) -> torch.Tensor:
        self.record_input_vars(*args)
        assert args[0] is not None, "cast in data got None"

        # ANCHOR padding before convolution
        x = F.pad(
            args[0], 
            self.conv_pads
        )

        # ANCHOR pure convolution
        x = self._conv(x)
        self.record_var(x, 'after_xbar')

        # ANCHOR add bias
        if self.conv_bias is not None:
            x += self.conv_bias.view(1, -1, 1, 1)
        
        # ANCHOR add merge in 
        if self.is_merge:
            assert args[1] is not None, "merge in data got None"
            assert x.shape == args[1].shape, (
                f"got x's shape = {x.shape} but merge's shape = {args[1].shape}, cannot merge")
            x = torch.add(x, args[1])

        # ANCHOR Convolution dequantization
        # only for merge node where a complete sum should appear
        # conv quantization converting from input to output
        if self.merge_node and self.quantize:
            if self.hardtrans:
                ctrans_i = self.tqc.ctrans_i.view([1, -1, 1, 1])
                ctrans_s = self.tqc.ctrans_s.view([1, -1, 1, 1])
                mult = ctrans_i / pow(2, -ctrans_s)
            else: mult = self.tqc.ctrans.view([1, -1, 1, 1])
            x = torch.clamp(torch.round(x * mult), self.tqc.io_min, self.tqc.io_max)

        # ANCHOR add gather in (Add operation)
        if self.is_gather:
            assert self.merge_node, f"this is a gather_in node but is not a merge node"
            assert args[2] is not None, "gather in data got None"
            assert x.shape == args[2].shape, (
                f"got x's shape = {x.shape} but gather's shape = {args[2].shape}, cannot gather")
            x = torch.add(x, args[2])

            # ANCHOR Add dequantization
            # only for tile with gather in dataflow
            # add quantization converting from input to output
            if self.quantize:
                if self.hardtrans: 
                    mult = self.tqc.strans_i / pow(2, -self.tqc.strans_s)
                else: mult = self.tqc.strans
                x = torch.clamp(torch.round(x * mult), self.tqc.io_min, self.tqc.io_max)

        # ANCHOR activation
        if self.is_act:
            assert self.act_mode == 'Relu', (
                f"activation mode must be Relu, but got {self.act_mode}")
            x = F.relu(x)

            # ANCHOR Activation dequantization
            # only for tile with activation (relu)
            # act quantization converting from input to output
            if self.quantize:
                if self.hardtrans:
                    mult = self.tqc.atrans_i / pow(2, -self.tqc.atrans_s)
                else: mult = self.tqc.atrans
                x = torch.clamp(torch.round(x * mult), self.tqc.io_min, self.tqc.io_max)

        # ANCHOR Resize (w/o quantization)
        if self.is_resize:
            x = self._resize(x)

        # ANCHOR Pooling (w/o quantization)
        if self.is_pool:
            self.record_var(x, 'before_pool')
            assert self.pool_mode in ['MaxPool', 'AveragePool'], (
                f"got invalid pool mode: {self.pool_mode}")
            
            # ANCHOR padding before pooling
            x = F.pad(x, self.pool_pads)

            # ANCHOR pure pooling 
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

        self.record_var(x, 'data_out')
        self.record_dequant_vars()

        return x