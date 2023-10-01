import math
from maptools.core import ACG, MeshEdge
from maptools.nlrt import RoutingTrail
from typing import Iterable, Dict, Optional, Literal
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, CirclePolygon
import matplotlib.colors as colors
import matplotlib.ticker as ticker


__all__ = ['draw_heatmap']

L = 5 # linke length
R = 0.5 # node radius
LS = 8 # arc link ratio
LW = 5 # link width

def draw_heatmap(
    acg: ACG, 
    trails: Iterable[RoutingTrail],
    maximum: Optional[int] = None,
    mapfunc: Literal['log2', 'sqrt'] = 'log2',
    cmap_name: str = 'coolwarm'
) -> None:
    '''
    This function draws the heatmap which shows the communication load distribution in the NoC

    Parameters
    ----------
    acg: ACG
        Architecture characterization graph.
    
    trails: Iterable[RoutingTrail]
        An iterable collection of routing trails, whitch contains the path and load information.
        Users can pass any trails as he/she likes, so drawing heatmap with a part of connections
        is supported, for example, if you only care about the cast(gather) communication load 
        distribution, you can pass the cast trails only.

    maximum: Optional[int] = None
        The value corresponding to the deepest color

    mapfunc: Literal['log2', 'sqrt'] = 'log2'
        The mapping function for value-color matching.
        This mapping function is used to change the ralation of value-color matching
        from linear to nonlinear to balancing the color distribution.
    '''

    F_FUNC = {
        'log2'  :lambda x: math.log2(x+1),
        'lg'  :lambda x: math.log10(x+1),
        'sqrt'  :lambda x: math.sqrt(x)
    }

    R_FUNC = {
        'log2'  :lambda x: math.pow(2, x)-1,
        'lg'  :lambda x: math.pow(10, x)-1,
        'sqrt'  :lambda x: x**2
    }

    def format_func(x, pos):
        return f'{R_FUNC[mapfunc](x):.2e}'

    w, h = acg.w, acg.h
    load_dict = _init_load_dict(w, h)
    for trail in trails:
        for edge in trail.path:
            load_dict[edge] += trail.load
    
    total_load = sum(load_dict.values())
    nonz_list = [load for load in load_dict.values() if load != 0]
    print('Average load: ', total_load / len(load_dict))
    print('Hotspot ratio: ', total_load/ len(nonz_list))

    for edge, load in load_dict.items():
        # load_dict[edge] = math.log2(load+1)
        load_dict[edge] = F_FUNC[mapfunc](load)
    
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.set_aspect('equal')

    ax.set_xlim(-2, (w-1)*L+2)
    ax.set_ylim(-(h-1)*L-2, 2)

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  
    cmap = plt.cm.get_cmap(cmap_name)

    min_value = min(load_dict.values())
    max_value = max(load_dict.values())

    if maximum is not None:
        maximum = F_FUNC[mapfunc](maximum)
        if max_value < maximum:
            max_value = maximum

        else:
            print("provided maximum value too small")

    norm = colors.Normalize(vmin=min_value, vmax=max_value)

    color_dict = {}
    for element, value in load_dict.items():
        color = cmap(norm(value))
        color_dict[element] = color

    # vertical links
    for x in range(w):
        for y in range(h-1):
            edge1 = ((x, y), (x, y+1))
            edge2 = ((x, y+1), (x, y))

            src = (x*L, -y*L)
            dst = (x*L, (-y-1)*L)

            ctrl1 = (x*L-L/LS, -y*L-L/2)
            ctrl2 = (x*L+L/LS, -y*L-L/2)

            v1 = [src, ctrl1, dst]
            v2 = [src, ctrl2, dst]

            c = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
            path1 = Path(v1, c)
            path2 = Path(v2, c)

            patch1 = PathPatch(
                path1, 
                facecolor='none',
                edgecolor=color_dict[edge1], 
                linewidth=LW
            )

            patch2 = PathPatch(
                path2, 
                facecolor='none',
                edgecolor=color_dict[edge2], 
                linewidth=LW
            )

            ax.add_patch(patch1)
            ax.add_patch(patch2)

    # # horizontal links
    for y in range(h):
        for x in range(w-1):
            edge1 = ((x, y), (x+1, y))
            edge2 = ((x+1, y), (x, y))

            src = (x*L, -y*L)
            dst = ((x+1)*L, -y*L)

            ctrl1 = (x*L+L/2, -y*L-L/LS)
            ctrl2 = (x*L+L/2, -y*L+L/LS)

            v1 = [src, ctrl1, dst]
            v2 = [src, ctrl2, dst]

            c = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
            path1 = Path(v1, c)
            path2 = Path(v2, c)

            patch1 = PathPatch(
                path1, 
                facecolor='none',
                edgecolor=color_dict[edge1], 
                linewidth=LW
            )

            patch2 = PathPatch(
                path2, 
                facecolor='none',
                edgecolor=color_dict[edge2], 
                linewidth=LW
                )
            
            ax.add_patch(patch1)
            ax.add_patch(patch2)

    # routing nodes
    for x in range(w):
        for y in range(h):
            node = CirclePolygon(
                (x*L, -y*L), 
                radius=R, 
                facecolor='black'
                )
            ax.add_patch(node)

    colorbar = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cbar = plt.colorbar(colorbar, ax=ax, shrink=0.8)

    cbar.ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(
            lambda x, pos: 
            format_func(x, pos)
        )
    )

    plt.tight_layout()
    plt.show()


def _init_load_dict(w: int, h: int) -> Dict[MeshEdge, int]:
    load_dict = {}
    for x in range(w):
        for y in range(h-1):
            edge1 = ((x, y), (x, y+1))
            edge2 = ((x, y+1), (x, y))
            load_dict[edge1] = 0
            load_dict[edge2] = 0

    for y in range(h):
        for x in range(w-1):
            edge1 = ((x, y), (x+1, y))
            edge2 = ((x+1, y), (x, y))
            load_dict[edge1] = 0
            load_dict[edge2] = 0
            
    return load_dict
