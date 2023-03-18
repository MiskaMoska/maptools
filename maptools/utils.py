import os
import pickle
from typing import List, Tuple
import networkx as nx

__all__ = [
    'is_subseq',
    'build_mesh',
    'get_map'
]

def is_subseq(a: List, b: List) -> bool:
    '''
    This function judges if is the susequence of b, where a must be a 2-element list.
    '''
    for i in range(len(b)-1):
        if a[0] == b[i]:
            if b[i+1] == a[1]:
                return True
    return False

def build_mesh(eager_nodes: List[Tuple[int, int]]) -> nx.Graph:
    '''
    This function returns a mesh graph from given range of nodes.
    This function is designed for constructing steiner tree for cast routing plan.
    '''
    xs, ys = zip(*eager_nodes)
    sx = min(xs)
    dx = max(xs)
    sy = min(ys)
    dy = max(ys)
    g = nx.Graph()
    for x in range(sx, dx+1):
        for y in range(sy, dy):
            g.add_edge((x,y),(x,y+1))
    for y in range(sy, dy+1):
        for x in range(sx, dx):
            g.add_edge((x,y),(x+1,y))
    return g

def get_map(mapname: str = 'newmap') -> None:
    root_dir = os.environ['NVCIM_HOME']
    file_dir = os.path.join(root_dir, 'mapsave', mapname, 'params.pkl')
    with open(file_dir, 'rb') as f:
        params = pickle.load(f)
    file_dir = os.path.join(root_dir, 'mapsave', mapname, 'mapinfo.pkl')
    with open(file_dir, 'rb') as f:
        mapinfo = pickle.load(f)
    return params, mapinfo
