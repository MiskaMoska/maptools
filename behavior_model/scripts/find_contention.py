'''
Find contention nodes where more than one cast stream share the same output port
The streams that participate in the contention should be End-to-End flow controlled to avoid message-dependent-dedalocks
'''
import networkx as nx
from build_cdg import CDG,IS_CONTENT

for n in CDG.nodes():
    if CDG.in_degree(n) > 1:
        if IS_CONTENT[n]:
            print(f"contention at node {n}")
