import torch
from enum import Enum
from typing import Optional

__all__ = [
    'OperatorQuantConfig',
    'TileQuantConfig',
    'NNModelArch',
    'DLEMethod',
    'DREMethod'
]

class OperatorQuantConfig(object):

    def __init__(self, **kwargs) -> None:
        self.op_type: str
        self.input_bits: int
        self.input_scale: float
        self.output_bits: int
        self.output_scale: float
        self.weight_bits: Optional[torch.Tensor]
        self.weight_scale: Optional[torch.Tensor]
        self.__dict__.update(kwargs)

    def __str__(self) -> str:
        ret = '[ OperatorQuantConfig Object ]\n'
        for k, v in self.__dict__.items():
            ret += '%-20s%s\n' % (k, v)
        return ret + '\n'


class TileQuantConfig(object):

    def __init__(self, **kwargs) -> None:
        self.op_type: str
        self.i_scale: float # tile input scale
        self.o_scale: float # tile output scale
        self.ci_scale: float # conv input scale
        self.co_scale: float # conv output scale
        self.si_scale: Optional[float] # sum input scale
        self.so_scale: Optional[float] # sum output scale
        self.ai_scale: Optional[float] # act input scale
        self.so_scale: Optional[float] # act output scale
        self.ctrans: torch.Tensor # conv transfer factor
        self.strans: Optional[float] # sum transfer factor
        self.atrans: Optional[float] # act transfer factor
        self.ctrans_i: torch.Tensor # conv transfer factor integer part
        self.ctrans_s: torch.Tensor # conv transfer factor shift part
        self.strans_i: Optional[int] # sum transfer factor integer part
        self.strans_s: Optional[int] # sum transfer factor shift part
        self.atrans_i: Optional[int] # act transfer factor integer part
        self.atrans_s: Optional[int] # act transfer factor shift part
        self.__dict__.update(kwargs)

    def __str__(self) -> str:
        ret = '[ TileQuantConfig Object ]\n'
        for k, v in self.__dict__.items():
            ret += '%-20s%s\n' % (k, v)
        return ret + '\n'


class NNModelArch(Enum):
    VGG          = 0
    RESNET       = 1
    GOOGLENET    = 2
    YOLO_V3      = 3
    SQUEEZENET   = 4


class DLEMethod(Enum):
    REVERSE_S = 0


class DREMethod(Enum):
    DYXY = 0
    RPM = 1
    OCR = 2
