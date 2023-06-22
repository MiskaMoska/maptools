import numpy as np
from maptools.core import CTG, ACG, DLEMethod
from graphviz import Graph as ZGraph
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from typing import List, Dict, Tuple, Literal, Optional, Union
from maptools.core.typing import *
from functools import cached_property
from itertools import combinations as comb
from maptools.nlrt.algorithm import LayoutSimulatedAnnealing
from maptools.nlrt.layout_result import LayoutResult
from maptools.nlrt.encoding import LayoutPatternCode
from maptools.nlrt.dle import __DLE_ACCESS_TABLE__

class LayoutDesigner(object):

    def __init__(
        self, 
        ctg: CTG,
        acg: ACG,
        dle: Optional[DLEMethod] = None,
        **kwargs
    ) -> None:
        '''
        Tile-NoC Layout Designer
        Determines the 1-to-1 mapping between logical tile and physical tiles

        Parameter
        ---------
        ctg: CTG
            Communication Trace Graph of the AI task.

        acg: ACG
            Architecture Characterization Graph of the NoC.

        dle: Optional[DLEMethod]
            To specify the Deterministic Layout Engine.
            When `dle` is None, the optimization algorithm is default to be enabled
            to search for the best layout pattern.
            When `dle` is not None, it must be one of the predefined DLEs, and the 
            optimization algorithm is disabled, while the task of layout is handed 
            over to the specified DLE.
        '''
        if len(acg.nodes) < len(ctg.tile_nodes):
            raise ValueError(
                f"need larger NoC with more than {len(ctg.tile_nodes)} nodes")
        
        self.acg_nodes = acg.nodes
        self.lpc = LayoutPatternCode(ctg, acg)
        self.configs = kwargs
        self._init_layout_engine(dle)

    def _init_layout_engine(self, dle: Optional[DLEMethod]) -> None:
        if dle is not None: # use determininstic layout engine
            self.layout_engine = __DLE_ACCESS_TABLE__[dle](self.lpc)

        else: # use optimization layout engine
            self.layout_engine = LayoutSimulatedAnnealing(
                self.obj_func, 
                self.lpc,
                T_max=1e-2, 
                T_min=1e-10, 
                L=10, 
                max_stay_counter=150,
                silent=False  
            )

    @cached_property
    def ptdm(self) -> np.ndarray:
        '''
        Physical Tile Distance Matrix (PTDM)
        '''
        res = np.zeros([len(self.acg_nodes)]*2)
        for i, s in enumerate(self.acg_nodes):
            for j, d in enumerate(self.acg_nodes):

                # using the Manhattan distance
                res[i, j] = abs(s[0] - d[0]) + abs(s[1] - d[1])

        return res

    def obj_func(self, x: LayoutPatternCode) -> float:
        '''
        Objective function for optimization algorithms.
        the function is implemented here rather than in algorithm classes
        because the function is generic for all algorithms (such as SA and GA),
        and it needs global variables in `LayoutDesigner` to execute. 
        '''
        total_dist = 0
        for i, num in enumerate(x.cluster_list):
            for s, d in comb(list(range(num)), 2):
                s_cir, d_cir = (i, s), (i, d)
                s_pidx, d_pidx = x.map[s_cir], x.map[d_cir]
                total_dist += self.ptdm[s_pidx, d_pidx]

        return total_dist

    @property
    def layout_valid(self) -> bool:
        return self.lpc.is_valid

    def run_layout(self) -> None:
        self.lpc = self.layout_engine()
        print(f"layout is valid: {self.lpc.is_valid}")

    def reset(self) -> None:
        self.layout_engine.reset()

    @property
    def layout_result(self) -> 'LayoutResult':
        return LayoutResult(self.lpc, **self.configs)
