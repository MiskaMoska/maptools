
__all__ = ['QuantConfig']

class QuantConfig(object):

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def __str__(self) -> str:
        ret = '/ QuantConfig Object /\n'
        for k, v in self.__dict__.items():
            ret += '%-20s%s\n' % (k, v)
        return ret + '\n'
