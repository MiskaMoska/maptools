import os
from maptools.core import CTG, ACG, ROOT_DIR
from maptools.core.typing import *
from graphviz import Graph as ZGraph
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from typing import List, Dict, Tuple, Literal
from maptools.nlrt.encoding import LayoutPatternCode

class LayoutResult(object):

    def __init__(self, lpc: LayoutPatternCode, **kwargs) -> None:
        self.noc_w = lpc.noc_w
        self.noc_h = lpc.noc_h
        self.map = lpc.map
        self.log_dict = lpc.log_dict
        self.phy_dict = lpc.phy_dict

        self.mapname = 'newmap'
        self.__dict__.update(kwargs)
        self._prepare_tile_color()

        self.l2p_map = {
            self.log_dict[cir]:  self.phy_dict[self.map[cir]] 
            for cir in self.map.keys()
        }
        
    def __getitem__(self, log_tile: LogicalTile) -> PhysicalTile:
        return self.l2p_map[log_tile]

    def _prepare_tile_color(self) -> None:
        dark_colors = [
            color for _, color in mcolors.CSS4_COLORS.items()
            if all(c <= 0.7 for c in mcolors.to_rgb(color))
        ]
        k = len(self.map) // len(dark_colors) + 1
        self.colors = (dark_colors * k)[:len(self.map)]
    
    def draw(self, engine: Literal['fdp', 'mplt'] = 'fdp') -> None:
        # draw through matplotlib
        if engine == 'mplt': 
            plt.figure(figsize=(self.noc_w, self.noc_h))
            for cir, pidx in self.map.items():
                phytile = self.phy_dict[pidx]
                self._draw_tile_mplt(phytile, cir[0], self.colors[cir[0]])

            plt.show()

        # draw through graphviz fdp
        elif engine == 'fdp':
            save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'layout')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            fdp = ZGraph('layout', engine='fdp', format='pdf')
            self.draw_fdp(fdp)
            fdp.render(cleanup=True, directory=save_dir, view=False)
        
            print(f"layout graph saved to {save_dir}")

    @staticmethod
    def _draw_tile_mplt(
        phytile: PhysicalTile, 
        cid: int, 
        color: str
    ) -> None:
        w = 0.8
        x, y = phytile
        y = -y
        linewidth = 4

        plt.plot([x,x+w], [y,y], color=color, linewidth=linewidth)
        plt.plot([x+w,x+w], [y,y+w], color=color, linewidth=linewidth)
        plt.plot([x+w,x], [y+w,y+w], color=color, linewidth=linewidth)
        plt.plot([x,x], [y+w,y], color=color, linewidth=linewidth)
        
        plt.text(
            x + w/2, y + w/2,
            'C'+str(cid),
            fontsize=15,
            verticalalignment='center', 
            horizontalalignment='center', 
            color=color,
            fontweight='bold'
        )

    def draw_fdp(
        self, fdp: ZGraph,
        mode: Literal['point', 'square_s', 'square_l'] = 'square_l'
    ) -> None:
        dist = 1.8 if mode == 'square_s' else 1
        drawed_set = set()

        # draw the mapped tiles
        for cir, pidx in self.map.items():
            phytile = self.phy_dict[pidx]
            pos = f'{phytile[0] * dist},{-phytile[1] * dist}!'
            drawed_set.add(phytile)
            self._draw_one_node(fdp, cir, phytile, pos, mode=mode)
        
        # draw the rest of the tiles that has not been mapped to
        for phytile in self.phy_dict.values():
            if phytile not in drawed_set:
                pos = f'{phytile[0] * dist},{-phytile[1] * dist}!'
                self._draw_one_node(fdp, None, phytile, pos, mode=mode, passive=True)

    def _draw_one_node(
        self, fdp: ZGraph, *args,
        mode: Literal['point', 'square_s', 'square_l'] = 'square_l',
        passive: bool = False
    ) -> None:
        cir, phytile, pos, *_ = args
        if mode == 'point':
            fdp.node(
                str(phytile), 
                '',
                pos=pos,
                shape='point',
                width='0.24',
                height='0.24'
            )

        elif mode == 'square_s':
            fdp.node(
                str(phytile), 
                'X' if passive else f'C{cir[0]}', 
                color='grey' if passive else self.colors[cir[0]],
                fontcolor='grey' if passive else self.colors[cir[0]],
                pos=pos,
                shape='square',
                width='1',
                penwidth='5',
                fontsize='24',
                fontname='Arial'
            )
            
        elif mode == 'square_l':
            fdp.node(
                str(phytile), 
                'X' if passive else f'C{cir[0]}', 
                color='grey' if passive else self.colors[cir[0]],
                fontcolor='grey' if passive else self.colors[cir[0]],
                pos=pos,
                shape='square',
                width='0.8',
                penwidth='5',
                fontsize='24',
                fontname='Arial'
            )
