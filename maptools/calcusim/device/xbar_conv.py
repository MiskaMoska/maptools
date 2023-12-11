import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict, Optional, Tuple, Any, Callable
from maptools.core import LogicalTile, TileQuantConfig, XBAR_POWER_PER_1

__all__ = ['XbarConv']

def xbar_conv_bitserial(
    x: torch.Tensor,
    weight: torch.Tensor,
    stride: Optional[List[int]] = [1, 1],
    factor: float = 1,
    tile: LogicalTile = None,
    tqc: TileQuantConfig = None,
    stats: bool = False,
    eval_power: bool = False,
    power_dict: Dict[LogicalTile, Dict[str, float]] = {}
) -> torch.Tensor:
    
    x = torch.clamp(x, tqc.io_min, tqc.io_max)
    x = x.type(torch.int8)
    y = 0

    if stats:
        if tile == (0, 0, 0, 0):
            print('\n'+'-'*70)
            print('\t\tResults Distribution Report')
            print('-'*70)

        print(f'\n--> Tile {tile}')

    for i in range(tqc.io_bits):
        _y = F.conv2d(
            ((x >> i) & 1).float(),
            weight,
            stride=stride
        )

        if not stats: # if not do distribution statistics, enable adc clamp
            if eval_power:
                if tile not in power_dict:
                    power_dict[tile] = {'xbar': 0}
                power_dict[tile]['xbar'] += int(torch.sum(_y)) * XBAR_POWER_PER_1

            _y = torch.clamp(torch.round(_y / factor), tqc.io_min, tqc.io_max) # ivc clamping transfer
            _y = torch.round(_y * factor) # invert transfer

        else: # if do distribution statistics, disable adc clamp and analyze results
            res_range = (int(torch.min(_y)), int(torch.max(_y)))
            res_avg = float(torch.mean(torch.abs(_y)))
            
            print('%-15s%-5s%-8s%-16s%-9s%-10s' % (
                'bit(0 for LSB):'   , i,
                'range:'            , res_range,
                'avg_abs:'          , round(res_avg, 3)    
            ))
        
        if i == tqc.io_bits-1: # sign bit
            y += _y*(-pow(2, i))
        else: # non-sign bit
            y += _y*pow(2, i)
    
    return y


class XbarConv(nn.Module):

    def __init__(
        self, 
        weight: torch.Tensor, 
        strides: List[int],
        physical: bool = False,
        tile: LogicalTile = None,
        tqc: TileQuantConfig = None,
        ivcf: Optional[float] = None,
        first_layer_ivcf: Optional[float] = None,
        stats: bool = False,
        eval_power: bool = False,
        power_dict: Dict[LogicalTile, Dict[str, float]] = {}
    ) -> None:
        super().__init__()
        self.weight = weight
        self.strides = strides
        self.tile = tile
        self.tqc = tqc
        self.physical = physical
        self.stats = stats
        self.eval_power=eval_power
        self.power_dict=power_dict

        # determine ivc transfer factor
        if ivcf is not None:
            if (first_layer_ivcf is not None) and (self.tile == (0, 0, 0, 0)):
                self.factor = first_layer_ivcf
            else:
                self.factor = ivcf
        else: self.factor = 1

    def cuda(self):
        self.weight = self.weight.cuda()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.physical: # use physical cimu
            return xbar_conv_bitserial(
                x, self.weight, 
                stride=self.strides, 
                factor=self.factor,
                tile=self.tile,
                stats=self.stats,
                tqc=self.tqc,
                eval_power=self.eval_power,
                power_dict=self.power_dict
            )
        else: # use pytorch conv2d
            return F.conv2d(
                x, self.weight, 
                bias=None, 
                stride=self.strides,                 
            )