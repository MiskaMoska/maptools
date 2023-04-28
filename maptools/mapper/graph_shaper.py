'''
device graph shapers
'''
from abc import ABCMeta, abstractmethod
from typing import Callable
from maptools.core import DeviceGraph, NNModelArch

__all__ = ['__SHAPER_ACCESS_TABLE__']

class BaseGraphShaper(Callable, metaclass=ABCMeta):
    
    def __call__(self, graph: DeviceGraph) -> None:
        if not isinstance(graph, DeviceGraph):
            raise TypeError(f"shaper need a {DeviceGraph} to proccess, but got a {type(graph)}")
        self.process(graph)

    @abstractmethod
    def process(self, graph: DeviceGraph) -> None: ...


class ResnetGraphShaper(BaseGraphShaper):

    def process(self, graph: DeviceGraph) -> None:
        graph.fuse_act() 
        graph.fuse_pool()
        graph.regu_pool()
        graph.fuse_add()


class GooglenetGraphShaper(BaseGraphShaper):

    def process(self, graph: DeviceGraph) -> None:
        graph.fuse_act()
        graph.head_pool('Concat')
        graph.fuse_pool()
        graph.regu_pool()
        graph.remove_concat()


class Yolov3GraphShaper(BaseGraphShaper):

    def process(self, graph: DeviceGraph) -> None:
        graph.fuse_act()
        graph.fuse_resize()
        graph.remove_concat()


__SHAPER_ACCESS_TABLE__ = {
    NNModelArch.VGG         : ResnetGraphShaper,
    NNModelArch.RESNET      : ResnetGraphShaper,
    NNModelArch.GOOGLENET   : GooglenetGraphShaper,
    NNModelArch.YOLO_V3     : Yolov3GraphShaper
}