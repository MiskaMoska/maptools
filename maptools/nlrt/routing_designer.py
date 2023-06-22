from maptools.core import CTG, ACG, DREMethod
from maptools.core.typing import *
from typing import List, Dict, Tuple, Any, Optional
from maptools.nlrt.layout_designer import LayoutResult
from maptools.nlrt.encoding import RoutingPatternCode
from maptools.nlrt.algorithm import RoutingSimulatedAnnealing
from maptools.nlrt.routing_result import RoutingResult
from maptools.nlrt.dre import __DRE_ACCESS_TABLE__

class RoutingDesigner(object):

    def __init__(
        self, 
        ctg: CTG, 
        acg: ACG, 
        layout: LayoutResult,
        dre: Optional[DREMethod] = None,
        **kwargs
    ) -> None:
        '''
        Tile-NoC Routing Designer
        Determines the routing paths for each communication connection.

        Parameter
        ---------
        ctg: CTG
            Communication Trace Graph of the AI task.

        acg: ACG
            Architecture Characterization Graph of the NoC.

        layout: LayoutResult
            layout result from `LayoutDesigner`.

        dre: Optional[DREMethod]
            To specify the Deterministic Routing Engine.
            When `dre` is None, the optimization algorithm is default to be enabled
            to search for the best routing pattern.
            When `dre` is not None, it must be one of the predefined DREs, and the 
            optimization algorithm is disabled, while the task of routing is handed 
            over to the specified DRE.

        dummy_sa: bool
            never accept worse solutions while running SA algorithm.
            this option is only for OLE, for DLE, this option will be neglected.
        '''
        self.noc_w = acg.w
        self.noc_h = acg.h
        self.layout = layout
        self.rpc = RoutingPatternCode(ctg, acg, layout)
        self.configs = kwargs
        self._init_routing_engine(dre, **kwargs)

    def _init_routing_engine(self, dre: Optional[DREMethod], **kwargs) -> None:
        if dre is not None: # use determininstic routing engine
            self.routing_engine = __DRE_ACCESS_TABLE__[dre](self.rpc)

        else: # use optimization routing engine
            self.routing_engine = RoutingSimulatedAnnealing(
                self.obj_func, 
                self.rpc,
                T_max=1e-2, 
                T_min=1e-10, 
                L=10, 
                max_stay_counter=500,
                silent=False,
                **kwargs
            )

    def obj_func(self, x: RoutingPatternCode) -> float:
        '''
        Objective function for optimization algorithms.
        the function is implemented here rather than in algorithm classes
        because the function is generic for all algorithms (such as SA and GA),
        and it needs global variables in `RoutingDesigner` to execute. 
        '''
        x.decode() # this step is necessary
        freq_dict = {}

        for path in x.path_dict.values():
            for edge in path:
                if edge not in freq_dict:
                    freq_dict[edge] = 0
                freq_dict[edge] += 1
        
        conflicts = list(freq_dict.values())
        return (sum(conflicts) / len(conflicts)) * max(conflicts)
        # return (sum(conflicts) - len(conflicts))/50
        # return max(conflicts)

    def run_routing(self) -> None:
        self.rpc = self.routing_engine()

    def reset(self) -> None:
        self.routing_engine.reset()

    @property
    def routing_result(self) -> RoutingResult:
        self.rpc.decode()
        return RoutingResult(self.layout, self.rpc, **self.configs)
