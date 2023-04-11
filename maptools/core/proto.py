
__all__ = ['QuantConfig']

class QuantConfig(object):

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)