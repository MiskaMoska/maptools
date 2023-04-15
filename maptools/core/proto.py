from enum import Enum

__all__ = [
    'QuantConfig',
    'NNModelArch'
]

class QuantConfig(object):

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def __str__(self) -> str:
        ret = '[ QuantConfig Object ]\n'
        for k, v in self.__dict__.items():
            ret += '%-20s%s\n' % (k, v)
        return ret + '\n'


class NNModelArch(Enum):
    VGG             = 0
    RESNET          = 1
    GOOGLENET       = 2
    YOLO_V3         = 3

