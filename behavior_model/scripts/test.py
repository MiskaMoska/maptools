import random
import networkx as nx
import numpy as np
from random import shuffle

def Route_DyXY(sx,sy,dx,dy,path:list,sid=0)->list:
    if sx == dx and sy == dy:
        return
    if sx != dx and sy != dy:
        randbit = True if random.random() > 0.5 else False
        if randbit:
            nxt_sx = sx
            nxt_sy = sy + (1 if sy < dy else -1)
        else:
            nxt_sy = sy
            nxt_sx = sx + (1 if sx < dx else -1)
    else:
        if sx == dx:
            nxt_sx = sx
            nxt_sy = sy + (1 if sy < dy else -1)
        elif sy == dy:
            nxt_sy = sy
            nxt_sx = sx + (1 if sx < dx else -1)
    path.append(((sx,sy),(nxt_sx,nxt_sy)))
    Route_DyXY(nxt_sx,nxt_sy,dx,dy,path,sid=sid)

G = nx.MultiDiGraph()

edges = [
    ((2,0),(1,0)),
    ((1,0),(0,0)),
    ((2,0),(3,0)),
    ((2,1),(1,1)),
    ((1,1),(0,1)),
    ((2,1),(3,1)),
    ((2,2),(1,2)),
    ((1,2),(0,2)),
    ((2,2),(3,2)),
    ((0,0),(0,1)),
    ((0,1),(0,2)),
    ((1,0),(1,1)),
    ((1,1),(1,2)),
    ((2,0),(2,1)),
    ((2,1),(2,2)),
    ((3,0),(3,1)),
    ((3,1),(3,2))
]

# G.add_edges_from(edges)

# print(nx.algorithms.approximation.steiner_tree(G,[(3,0),(2,1),(3,2),(1,2),(0,2)]))


def _gen_reverse_s(w: int, h: int):
    '''
    generate reverse-s path
    '''
    rs_path = []
    for i in range(h):
        for j in range(w):
            idx = (i+1)*w-j-1 if i % 2 else i*w+j
            rs_path.append((idx % w, idx // w))
    return rs_path

a = [1,2,3]
print(a.reverse())