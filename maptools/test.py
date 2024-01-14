import torch
import torch.nn.functional as F
import torch.nn as nn
from typing import Generator
import math
import networkx as nx

class A(nn.Module):

    def __init__(self) -> None:
        super().__init__()
        self.b = nn.Conv2d(31,32,[3,3])
        self.c = nn.Conv2d(32,32,[3,3])
        self.dict = {}
        self.dict['d'] = nn.Conv2d(33,32,[3,3])
        self.dict['e'] = nn.Conv2d(34,32,[3,3])
        for k, v in self.dict.items():
            self.add_module(k, v)

    # def children(self) -> Generator:
    #     yield from iter([self.b, self.c])
    #     yield from self.dict.values()


class Gemm(nn.Module):
    
    def __init__(self, weight: torch.Tensor) -> None:
        super().__init__()
        self.weight = torch.tensor(weight)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.linear(x, self.weight)


class B():

    def __init__(self) -> None:
        self._var = 0
    
    @property
    def var(self):
        return self._var
    
    @var.setter
    def var(self, value):
        self._var = value


def set_precall_method(callee=lambda x:x):
    def precall_method(func):

        def wrapper(*args, **kwargs):
            callee()
            return func(*args, **kwargs)

        return wrapper
    return precall_method


import random
import networkx as nx
from matplotlib import pyplot as plt

w = 5
h = 5
n = 2

outer_dir = 0
inner_dir = 1

nodes = [(x, y) for x in range(w) for y in range(h)]
term_nodes = random.sample(nodes, n)
src_node = random.choice(term_nodes)
xy = list(zip(*term_nodes))

fcn = [min, max]
key = lambda x : x[outer_dir]
min_pos = min(xy[1-outer_dir])
start_layer = [n for n in term_nodes if n[1-outer_dir] == min_pos]
start_node = fcn[inner_dir](start_layer, key=key)

raw_edges = []
cur_node = start_node
remain_nodes = term_nodes.copy()
turn_node = (
    start_node[0] if outer_dir 
    else (0 if inner_dir else w-1),
    start_node[1] if (1-outer_dir) 
    else (0 if inner_dir else h-1)
)
direction = inner_dir

def draw():
    colors = []
    poses = {}
    G = nx.DiGraph()
    for x in range(w):
        for y in range(h):
            G.add_node((x, y))
            poses[(x, y)] = (x*3,-3*y)
            if (x, y) == start_node:
                colors.append('red')
            elif (x, y) in term_nodes:
                colors.append('green')
            else:
                colors.append('black')
    G.add_edges_from(raw_edges)
    nx.draw(G, node_color=colors, with_labels=True, pos=poses)
    plt.show()

while True:
    if cur_node in remain_nodes:
        remain_nodes.remove(cur_node)

    if len(remain_nodes) == 0:
        break

    print("cur_node:", cur_node, "turn_node:", turn_node)
    if cur_node == turn_node:
        nxt_node = (
            cur_node[0] + outer_dir, 
            cur_node[1] + 1-outer_dir
        )
        if outer_dir == 0:
            turn_node = (w-1-turn_node[0], turn_node[1]+1)
        else:
            turn_node = (turn_node[0]+1, h-1-turn_node[1])
        direction = 1- direction
        print("new_turn_node: ", turn_node)
        print("nxt_node: ", nxt_node)
    
    else:
        nxt_node = (
            cur_node[0] + (1-outer_dir) 
            *(-1 if direction else 1),
            cur_node[1] + outer_dir 
            *(-1 if direction else 1)
        )

    raw_edges.append((cur_node, nxt_node))
    cur_node = nxt_node

# ############################################################
# graph = nx.Graph()
# graph.add_edges_from(raw_edges)

# direction = inner_dir
# for i in range(min(xy[1]), max(xy[1])):
#     now = (1-direction) * (w-1)
#     while True:
#         if ((now, i+1) not in term_nodes) and (
#             (now, i) not in term_nodes):
#             graph.remove_edge((now, i), (now, i+1))
#             # print("layer: ", i, "now: ", now)
#             nxt = now + (1 if direction else -1)
#             graph.remove_edge((now, i), (nxt, i))
#             graph.remove_edge((now, i+1), (nxt, i+1))
#             graph.add_edge((nxt, i), (nxt, i+1))
#             now = nxt
#         else:
#             break
#     direction = 1 - direction

# digraph: nx.DiGraph = nx.bfs_tree(graph, src_node)
# raw_edges = list(digraph.edges)

############################################################
graph = nx.Graph()
graph.add_edges_from(raw_edges)

def tup2(a, b):
    return (a, b) if outer_dir else (b, a)

direction = inner_dir
for i in range(min(xy[1-outer_dir]), max(xy[1-outer_dir])):
    now = (1-direction) * ((h if outer_dir else w) - 1)
    while True:
        if (tup2(i+1, now) not in term_nodes) and (
            tup2(i, now) not in term_nodes):
            if graph.has_edge(tup2(i-1, now), tup2(i, now)) and (
                all(n[1-outer_dir] != i for n in term_nodes)) and (
                all(n[1-outer_dir] != i+1 for n in term_nodes)):
                break
            graph.remove_edge(tup2(i, now), tup2(i+1, now))
            print("layer: ", i, "now: ", now)
            nxt = now + (1 if direction else -1)
            graph.remove_edge(tup2(i, now), tup2(i, nxt))
            graph.remove_edge(tup2(i+1, now), tup2(i+1, nxt))
            graph.add_edge(tup2(i, nxt), tup2(i+1, nxt))
            now = nxt
        else:
            break
    direction = 1 - direction

digraph: nx.DiGraph = nx.bfs_tree(graph, src_node)
raw_edges = list(digraph.edges)

draw()

# print(raw_edges)









