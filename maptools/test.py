import random
import networkx as nx
import numpy as np
from random import shuffle
import json

G = nx.Graph()

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

G.add_edges_from(edges)

g = nx.algorithms.approximation.steiner_tree(G,[(3,0),(2,1),(3,2),(1,2),(0,2)],method='kou')
print(g.edges)
g = nx.dfs_tree(g, source=(2,0))
print(g.edges)

# def _gen_reverse_s(w: int, h: int):
#     '''
#     generate reverse-s path
#     '''
#     rs_path = []
#     for i in range(h):
#         for j in range(w):
#             idx = (i+1)*w-j-1 if i % 2 else i*w+j
#             rs_path.append((idx % w, idx // w))
#     return rs_path

# a = np.array([
# [1,2,3,4],
# [2,3,4,5],
# [5,67,34,2]
# ])
# a[1:3,0:2] *= 0
# print(a)

a = 'abcdef'

a.strip('bcd')

print(a.strip('bcd'))








