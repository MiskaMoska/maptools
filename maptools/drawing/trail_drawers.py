import os
import networkx as nx
from matplotlib import pyplot as plt
from typing import Dict, List, Optional, Tuple
from maptools.core import ROOT_DIR, RouterPort
from maptools.nlrt import RoutingTrail

__all__ = [
    'build_graph',
    'draw_routers',
    'draw_cast_trails',
    'draw_merge_trails'
]

# parameter settings
link_len = 5.5
node_size = 20
arrow_size = 10
dpi = 500

def build_graph(w: int, h: int) -> Tuple[nx.MultiDiGraph, Dict[Tuple, Tuple]]:
    graph = nx.MultiDiGraph()
    legal_node = [
        RouterPort.WEST_I, 
        RouterPort.WEST_O, 
        RouterPort.EAST_I, 
        RouterPort.EAST_O, 
        RouterPort.NORTH_I, 
        RouterPort.NORTH_O, 
        RouterPort.SOUTH_I, 
        RouterPort.SOUTH_O, 
        RouterPort.LOCAL_I, 
        RouterPort.LOCAL_O
    ]
    legal_xpos = [0,0,4,4,1,2,2,1,3.33+0.5,2.67+0.5]
    legal_ypos = [2,1,1,2,0,0,4,4,2.67+0.5,3.33+0.5]
    pos = dict()
    for i in range(w):
        for j in range(h):
            for k in range(len(legal_node)):
                graph.add_node((i, j, legal_node[k]))
                pos[(i, j, legal_node[k])] = (
                    legal_xpos[k]+link_len*i,
                    -(legal_ypos[k]+link_len*j)
                )
    return graph, pos

def draw_routers(w: int, h: int) -> None:
    for i in range(w):
        for j in range(h):
            plt.plot(
                [0+i*link_len, 0+i*link_len],
                [-0-j*link_len, -4-j*link_len],
                color='black',
                linewidth=1
            )
            plt.plot(
                [0+i*link_len, 3+i*link_len],
                [-4-j*link_len, -4-j*link_len],
                color='black',
                linewidth=1
            )
            plt.plot(
                [3+i*link_len, 4+i*link_len],
                [-4-j*link_len, -3-j*link_len],
                color='black',
                linewidth=1
            )
            plt.plot(
                [4+i*link_len, 4+i*link_len],
                [-3-j*link_len, -0-j*link_len],
                color='black',
                linewidth=1
            )
            plt.plot(
                [4+i*link_len, 0+i*link_len],
                [-0-j*link_len, -0-j*link_len],
                color='black',
                linewidth=1
            )

def draw_cast_trails(cast_trails: List[RoutingTrail], mapname: str = 'newmap') -> None:
    '''
    This function draws cast trails
    '''
    save_dir = os.path.join(ROOT_DIR, 'mapsave', mapname, 'routing')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_dir = os.path.join(save_dir, 'cast_trails.png')

    w, h = cast_trails[0].w, cast_trails[0].h
    plt.figure(figsize=(w, h))
    draw_routers(w, h)
    cast_graph, pos = build_graph(w, h)
    for trail in cast_trails:
        cast_graph.add_edges_from(trail.cast_transitions)
        cast_graph.add_edges_from(trail.links)
    
    nx.draw(
        cast_graph, 
        pos, 
        node_size=node_size, 
        width=1, 
        arrowsize=arrow_size, 
        node_color='black',
        edge_color='red',
        arrowstyle='-|>'
    )

    plt.savefig(
        file_dir,
        dpi=dpi, 
        bbox_inches='tight'
    )

    print(f"image saved to {file_dir}")


def draw_merge_trails(merge_trails: List[RoutingTrail], mapname: str = 'newmap') -> None:
    '''
    This function draws merge trails
    '''
    save_dir = os.path.join(ROOT_DIR, 'mapsave', mapname, 'routing')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_dir = os.path.join(save_dir, 'merge_trails.png')

    w, h = merge_trails[0].w, merge_trails[0].h
    plt.figure(figsize=(w, h))
    draw_routers(w, h)
    merge_graph, pos = build_graph(w, h)
    for trail in merge_trails:
        merge_graph.add_edges_from(trail.merge_transitions)
        merge_graph.add_edges_from(trail.links)

    nx.draw(
        merge_graph, 
        pos, 
        node_size=node_size, 
        width=1, 
        arrowsize=arrow_size, 
        node_color='black',
        edge_color='blue',
        arrowstyle='-|>'
    )

    plt.savefig(
        file_dir,
        dpi=dpi, 
        bbox_inches='tight'
    )
    
    print(f"image saved to {file_dir}")
