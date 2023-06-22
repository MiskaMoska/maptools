import os
import matplotlib.colors as mcolors
from maptools.core import ROOT_DIR
from typing import List, Dict, Tuple, Any
from graphviz import Digraph as ZDigraph
from maptools.nlrt.layout_designer import LayoutResult
from maptools.nlrt.encoding import RoutingPatternCode

class RoutingResult(object):
    
    def __init__(self, layout: LayoutResult, rpc: RoutingPatternCode, **kwargs) -> None:
        # self.comms = rpc.comms
        self.layout = layout
        self.path_dict = rpc.path_dict
        # self.src_dict = rpc.src_dict
        # self.sid_dict = rpc.sid_dict

        self.mapname = 'newmap'
        self.__dict__.update(kwargs)
        self._prepare_route_color()

    def __getitem__(self, comm: str) -> Dict[str, Any]:
        return self.path_dict[comm]

    def _prepare_route_color(self) -> None:
        dark_colors = [
            color for _, color in mcolors.CSS4_COLORS.items() 
            if all(c <= 0.6 for c in mcolors.to_rgb(color))
        ]
        k = len(self.path_dict) // len(dark_colors) + 1
        self.colors = (dark_colors * k)[:len(self.path_dict)]

    @property
    def max_conflicts(self) -> int:
        freq_dict = {}
        for path in self.path_dict.values():
            for edge in path:
                if edge not in freq_dict:
                    freq_dict[edge] = 0
                freq_dict[edge] += 1
        
        conflicts = list(freq_dict.values())
        return max(conflicts)

    def draw(self) -> None:
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'routing')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        fdp = ZDigraph('routing', engine='fdp', format='pdf')

        # draw layout tiles
        self.layout.draw_fdp(fdp, mode='point')

        # draw routing paths
        for i, path in enumerate(self.path_dict.values()):
            for edge in path:
                fdp.edge(
                    str(edge[0]),
                    str(edge[1]),
                    color=self.colors[i],
                    penwidth='3'
                )
        fdp.render(cleanup=True, directory=save_dir, view=False)

        print(f"routing graph saved to {save_dir}")