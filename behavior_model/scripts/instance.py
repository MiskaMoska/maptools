import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib import patches
from networkx import simple_cycles

W = 7
H = 8

def plot_routers():
    for i in range(W):
        for j in range(H):
            plt.plot([0+i*5,0+i*5],[-0-j*5,-4-j*5],color='black',linewidth=1)
            plt.plot([0+i*5,3+i*5],[-4-j*5,-4-j*5],color='black',linewidth=1)
            plt.plot([3+i*5,4+i*5],[-4-j*5,-3-j*5],color='black',linewidth=1)
            plt.plot([4+i*5,4+i*5],[-3-j*5,-0-j*5],color='black',linewidth=1)
            plt.plot([4+i*5,0+i*5],[-0-j*5,-0-j*5],color='black',linewidth=1)

def construct_cdg(cycle:list):
    legal_node = ['cw_i','cw_o','ce_i','ce_o','cv0_i','cv1_i','cv1_o','cv0_o','cl_i','cl_o','mrg']
    legal_xpos = [0,0,4,4,1,2,2,1,3.33+0.5,2.67+0.5,4.5]
    legal_ypos = [2,1,1,2,0,0,4,4,2.67+0.5,3.33+0.5,4.5]
    pos = dict()
    G=nx.MultiDiGraph()
    for i in range(W):
        for j in range(H):
            for k in range(len(legal_node)):
                G.add_node(f"{i}_{j}_"+legal_node[k])
                pos[f"{i}_{j}_"+legal_node[k]]=(legal_xpos[k]+5*i,-(legal_ypos[k]+5*j))
    G.add_edges_from(cycle)
    return G,pos

if __name__ == "__main__":
    plot_routers()
    G,pos = construct_cdg()
    nx.draw(G, pos, node_size = 40,width=1, arrowsize=10,node_color='black',edge_color='darkblue',arrowstyle='-|>')
    plt.show()

