from typing import Callable, List
from maptools.core import (
    CTG, ACG, DLEMethod, 
    PhysicalTile, CIR2PhyIdxMap, DLEMethod
)
from abc import ABCMeta, abstractmethod
from random import shuffle
from maptools.nlrt.encoding import LayoutPatternCode

class BaseDLE(Callable, metaclass=ABCMeta):
    '''
    Base Class for Deterministic Layout Engine
    '''
    def __init__(self, lpc: LayoutPatternCode) -> None:
        super().__init__()
        self.lpc = lpc
        self.noc_w = lpc.noc_w
        self.noc_h = lpc.noc_h
        self.cluster_list = lpc.cluster_list

    def __call__(self) -> LayoutPatternCode:
        return self._map_tiles()

    @abstractmethod
    def generate_path(self) -> List[int]: ...
        
    def _map_tiles(self) -> LayoutPatternCode:
        map_dict = {}
        path = self.generate_path()

        base = 0
        for cidx, num in enumerate(self.cluster_list):
            id_list = list(range(num))
            shuffle(id_list)
            for i, tidx in enumerate(id_list):
                map_dict[(cidx, tidx)] = path[base + i]
            base += num

        self.lpc.map = map_dict.copy()
        return self.lpc

    def reset(self) -> None: ...
        

class ReversesDLE(BaseDLE):

    def generate_path(self) -> List[int]:
        path = []
        for i in range(self.noc_h):
            for j in range(self.noc_w):
                idx = ((i+1) * self.noc_w-j-1 
                    if i % 2 else i*self.noc_w+j)
                path.append(idx)

        return path


class ZigzagDLE(BaseDLE):

    def generate_path(self) -> List[int]:
        path = []
        for i in range(self.noc_h):
            for j in range(self.noc_w):
                path.append(j+i*self.noc_w)
        
        return path


__DLE_ACCESS_TABLE__ = {
    DLEMethod.REVERSE_S         :ReversesDLE,
    DLEMethod.ZIGZAG            :ZigzagDLE
}