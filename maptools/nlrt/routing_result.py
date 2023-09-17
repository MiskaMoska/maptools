import os
from functools import cached_property
import matplotlib.colors as mcolors
from maptools.core import ROOT_DIR, MeshEdge, Connection, PhysicalTile
from typing import List, Dict, Tuple, Any
from graphviz import Digraph as ZDigraph
from maptools.nlrt.layout_designer import LayoutResult
from maptools.nlrt.encoding import RoutingPatternCode

class RoutingResult(object):
    
    def __init__(self, layout: LayoutResult, rpc: RoutingPatternCode, **kwargs) -> None:
        self._layout = layout
        self._path_dict = rpc.path_dict
        self._src_dict = rpc.src_dict
        self._term_dict = rpc.term_dict

        self.mapname = 'newmap'
        self.__dict__.update(kwargs)
        self._prepare_route_color()

    def __getitem__(self, conn: Connection) -> Dict[Connection, Any]:
        return {
            'term': self._term_dict[conn],
            'src': self._src_dict[conn],
            'path': self._path_dict[conn]
        }
    
    @cached_property
    def connects(self) -> List[Connection]:
        return list(self._path_dict.keys())
    
    def get_layout(self) -> LayoutResult:
        return self._layout
    
    def get_path(self, conn: str) -> List[MeshEdge]:
        return self._path_dict[conn]

    def _prepare_route_color(self) -> None:
        dark_colors = [
            color for _, color in mcolors.CSS4_COLORS.items() 
            if all(c <= 0.6 for c in mcolors.to_rgb(color))
        ]
        k = len(self._path_dict) // len(dark_colors) + 1
        self.colors = (dark_colors * k)[:len(self._path_dict)]

    @property
    def max_conflicts(self) -> int:
        freq_dict = {}
        for path in self._path_dict.values():
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
        self._layout.draw_fdp(fdp, mode='point')

        # draw routing paths
        for i, path in enumerate(self._path_dict.values()):
            for edge in path:
                fdp.edge(
                    str(edge[0]),
                    str(edge[1]),
                    color=self.colors[i],
                    penwidth='3'
                )
        fdp.render(cleanup=True, directory=save_dir, view=False)

        print(f"routing graph saved to {save_dir}")