import torch
from enum import Enum
from typing import List, Optional, Union
from maptools.core.typing import PhysicalTile, MeshEdge

__all__ = [
    'OperatorQuantConfig',
    'TileQuantConfig',
    'NNModelArch',
    'DLEMethod',
    'DREMethod',
    'RouterPort',
    'TrailType'
]

class OperatorQuantConfig(object):

    def __init__(self, **kwargs) -> None:
        # operation type
        self.op_type: str

        # input and output quantization bit number
        self.io_bits: int

        # input and output quantization min value
        self.io_min: int

        # input and output quantization max value
        self.io_max: int

        # input quantization scale (no zero point, default to be symmetrical quantization)
        self.input_scale: float

        # output quantization scale (no zero point, default to be symmetrical quantization)
        self.output_scale: float

        # weight quantization bit number
        self.weight_bits: Optional[torch.Tensor]

        # weight quantization min value
        self.weight_min: Optional[torch.Tensor]

        # weight quantization max value
        self.weight_max: Optional[torch.Tensor]

        # weight quantization scale
        self.weight_scale: Optional[torch.Tensor]

        self.__dict__.update(kwargs)

    def __str__(self) -> str:
        ret = '[ OperatorQuantConfig Object ]\n'
        for k, v in self.__dict__.items():
            ret += '%-20s%s\n' % (k, v)
        return ret + '\n'


class TileQuantConfig(object):

    def __init__(self, **kwargs) -> None:
        # tile operation type
        self.op_type: str

        # tile input and output quantization bit number
        self.io_bits: int

        # tile input and output quantization min value
        self.io_min: int

        # tile input and output quantization max value
        self.io_max: int

        # tile input quantization scale
        self.i_scale: float 

        # tile output quantization scale
        self.o_scale: float 

        # conv input quantization scale
        self.ci_scale: float

        # conv output quantization scale 
        self.co_scale: float 

        # sum input quantization scale
        self.si_scale: Optional[float] 

        # sum output quantization scale
        self.so_scale: Optional[float] 

        # act input quantization scale
        self.ai_scale: Optional[float]

        # act output quantization scale
        self.so_scale: Optional[float] 

        # conv quantization transfer factor
        self.ctrans: torch.Tensor 

        # sum quantization transfer factor
        self.strans: Optional[float]

        # act quantization transfer factor 
        self.atrans: Optional[float] 

        # conv quantization transfer factor integer part
        self.ctrans_i: torch.Tensor 

        # conv quntization transfer factor shift part
        self.ctrans_s: torch.Tensor 

        # sum quntization transfer factor integer part
        self.strans_i: Optional[int] 

        # sum quantization transfer factor shift part
        self.strans_s: Optional[int]

        # act quantization transfer factor integer part
        self.atrans_i: Optional[int] 

        # act quantization transfer factor shift part
        self.atrans_s: Optional[int] 

        self.__dict__.update(kwargs)

    def __str__(self) -> str:
        ret = '[ TileQuantConfig Object ]\n'
        for k, v in self.__dict__.items():
            ret += '%-20s%s\n' % (k, v)
        return ret + '\n'
    
    def cuda(self) -> None:
        self.ctrans = self.ctrans.cuda()
        self.ctrans_i = self.ctrans_i.cuda()
        self.ctrans_s = self.ctrans_s.cuda()


class NNModelArch(Enum):
    VGG             = 0
    RESNET          = 1
    GOOGLENET       = 2
    YOLO_V3         = 3
    SQUEEZENET      = 4


class DLEMethod(Enum):
    REVERSE_S       = 0
    ZIGZAG          = 1


class DREMethod(Enum):
    DYXY            = 0
    RPM             = 1
    OCR             = 2
    SP_RANDOM       = 3 # random single path
    SP_REVERSE_S    = 4 # reverse-S single path

class RouterPort(Enum):
    WEST_I          = 0
    WEST_O          = 1
    EAST_I          = 2
    EAST_O          = 3
    NORTH_I         = 4
    NORTH_O         = 5
    SOUTH_I         = 6
    SOUTH_O         = 7
    LOCAL_I         = 8
    LOCAL_O         = 9

class TrailType(Enum):
    CAST            = 0 # fused both cast and gather data stream
    MERGE           = 1
    