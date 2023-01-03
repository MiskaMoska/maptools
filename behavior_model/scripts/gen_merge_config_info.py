'''
Generate merge network config info in "merge_network_config.svh"
'''

import networkx as nx
from merge_path_config import *

MG = nx.MultiDiGraph()

for x in range(W):
    for y in range(H):
        MG.add_node((x,y))

MG.add_edges_from(Paths)

for node in MG.nodes():
    print(MG.out_degree())