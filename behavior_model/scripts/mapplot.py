'''
Plot the mapping results
'''
from matplotlib import pyplot as plt
import networkx as nx
from mapper import Mapper

def translate(chan_num:int,mode:str):
    if mode == 'i':
        if chan_num == 0:
            return "cl_i"
        elif chan_num == 1:
            return "cw_i"
        elif chan_num == 2:
            return "ce_i"
        elif chan_num == 3:
            return "cv0_i"
        elif chan_num == 4:
            return "cv1_i"
    
    elif mode == 'o':
        if chan_num == 0:
            return "cl_o"
        elif chan_num == 1:
            return "cw_o"
        elif chan_num == 2:
            return "ce_o"
        elif chan_num == 3:
            return "cv0_o"
        elif chan_num == 4:
            return "cv1_o"

def plot_routers(w,h):
    for i in range(w):
        for j in range(h):
            plt.plot([0+i*5,0+i*5],[-0-j*5,-4-j*5],color='black',linewidth=1)
            plt.plot([0+i*5,3+i*5],[-4-j*5,-4-j*5],color='black',linewidth=1)
            plt.plot([3+i*5,4+i*5],[-4-j*5,-3-j*5],color='black',linewidth=1)
            plt.plot([4+i*5,4+i*5],[-3-j*5,-0-j*5],color='black',linewidth=1)
            plt.plot([4+i*5,0+i*5],[-0-j*5,-0-j*5],color='black',linewidth=1)

def try_add_edge(G:nx.MultiDiGraph,e:tuple):
    G.add_edge(e[0],e[1])
    if G.in_degree(e[0]) == 0 and G.out_degree(e[1]) == 0:
        G.remove_edge(e[0],e[1])

def construct_cdg(w,h,cast_paths:dict,merge_paths:list):
    legal_node = ['cw_i','cw_o','ce_i','ce_o','cv0_i','cv1_i','cv1_o','cv0_o','cl_i','cl_o','mrg']
    legal_xpos = [0,0,4,4,1,2,2,1,3.33+0.5,2.67+0.5,4.5]
    legal_ypos = [2,1,1,2,0,0,4,4,2.67+0.5,3.33+0.5,4.5]
    pos = dict()
    G=nx.MultiDiGraph()
    for i in range(w):
        for j in range(h):
            for k in range(len(legal_node)):
                G.add_node(f"{i}_{j}_"+legal_node[k])
                pos[f"{i}_{j}_"+legal_node[k]]=(legal_xpos[k]+5*i,-(legal_ypos[k]+5*j))

    # generate cast inner edges according to cast_paths
    for k,v in cast_paths.items():
        for p in v:
            G.add_edge(f"{k[0]}_{k[1]}_"+translate(p[0],'i'),f"{k[0]}_{k[1]}_"+translate(p[1],'o'))
    
    # generate merge edges according to merge_paths
    for p in merge_paths:
        G.add_edge(f"{p[0][0]}_{p[0][1]}_"+'mrg',f"{p[1][0]}_{p[1][1]}_"+'mrg')
    
    # generate cast-merge joint edges
    for i in range(w):
        for j in range(h):
            if G.out_degree(f"{i}_{j}_mrg") == 0: 
                if G.in_degree(f"{i}_{j}_cl_o") > 0: # the current node is a caster
                    G.add_edge(f"{i}_{j}_cl_o",f"{i}_{j}_cl_i")
                    G.add_edge(f"{i}_{j}_mrg",f"{i}_{j}_cl_i")
            else: # the current node is not a caster
                G.add_edge(f"{i}_{j}_cl_o",f"{i}_{j}_mrg")

    # generate cast neighbor edges
    for i in range(w-1):
        for j in range(h):
            try_add_edge(G,(f"{i}_{j}_ce_o",f"{i+1}_{j}_cw_i"))
            try_add_edge(G,(f"{i+1}_{j}_cw_o",f"{i}_{j}_ce_i"))

    for i in range(w):
        for j in range(h-1):
            try_add_edge(G,(f"{i}_{j}_cv0_o",f"{i}_{j+1}_cv0_i"))
            try_add_edge(G,(f"{i}_{j}_cv1_o",f"{i}_{j+1}_cv1_i"))
    return G,pos

def get_edge_colors(G:nx.MultiDiGraph):
    edge_color = []
    for e in G.edges():
        if 'mrg' in e[0] or 'mrg' in e[1]:
            edge_color.append('blue')
        else:
            edge_color.append('red')
    return edge_color


if __name__ == "__main__":
    file_name = "/mnt/c/git/nvcim-comm/behavior_model/scripts/cycle_log"
    maper = Mapper(8,7,[1,1,1,1,1,2,2,2,4,4,4,4,4],[1,1,1,1,1,1,1,2,2,2,2,2,2])
    maper.Run_Mapping()
    plt.figure(figsize=(maper.w,maper.h))
    plot_routers(maper.w,maper.h)
    G,pos,el = construct_cdg(maper.w,maper.h,maper.cast_paths,maper.merge_paths)
    ec = get_edge_colors(G)
    nx.draw(G, pos, node_size = 20,width=1, arrowsize=10,node_color='black',edge_color='blue',arrowstyle='-|>')
    # nx.draw_networkx_edge_labels(G,pos,edge_labels=el,font_size=7,font_color='blue',bbox=dict(alpha=0))
    plt.show()