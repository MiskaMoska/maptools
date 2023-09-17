import torch
import itertools as it
import networkx as nx
import random
from matplotlib import pyplot as plt

N = 100
M = 50
K = 4

while(True):
    objs = list(range(N))
    m = random.randint(1, M)
    G_list = []
    max_conflict = 0
    for i in range(m):
        k_obj = random.randint(1, K)
        max_conflict = max(max_conflict, k_obj)
        nodes = random.sample(objs, k_obj)
        local_G = nx.complete_graph(nodes)
        G_list.append(local_G)
        # local_D = nx.greedy_color(local_G)
        # nx.draw(local_G)
        # num = len(set(local_D.values()))
        # plt.show()
        
    G = nx.compose_all(G_list)
    d = nx.greedy_color(G)
    max_vc = len(set(d.values()))
    print(max_conflict, max_vc)
    if max_conflict != max_vc:
        break
    # nx.draw(G)




