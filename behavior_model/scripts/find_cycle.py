'''
Given a CDG, find all multicast dependency cycles
A type: multicast dependency
V type: contention dependency
H type: serial dependency
'''
import sys
import rewrite as rw
from matplotlib import pyplot as plt
import networkx as nx
from copy import deepcopy
from build_cdg import CDG,SID,IS_CONTENT,IS_UNICAST,W,H


file_name = "/mnt/c/git/nvcim-comm/behavior_model/scripts/cycle_log"

G = nx.MultiDiGraph()
OCP = dict()
CYCLES = []

#----------------------------------------------------------------------------------------------------
# Functions to draw cycles
#----------------------------------------------------------------------------------------------------
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
    edge_label = dict()
    G=nx.MultiDiGraph()
    for i in range(W):
        for j in range(H):
            for k in range(len(legal_node)):
                G.add_node(f"{i}_{j}_"+legal_node[k])
                pos[f"{i}_{j}_"+legal_node[k]]=(legal_xpos[k]+5*i,-(legal_ypos[k]+5*j))

    G.add_edges_from(cycle)
    for i in range(len(cycle)-1):
        edge_label[cycle[i]] = i
    return G,pos,edge_label


#----------------------------------------------------------------------------------------------------
# Functions to find cycles
#----------------------------------------------------------------------------------------------------
def popp(lst:list):
    lst.pop()
    return lst

def log_out(dep_chain:list,ocp:dict,f):
    print("find one")
    CYCLES.append(deepcopy(dep_chain))
    f.write("find a cycle:"+str(dep_chain)+"\n")
    occupied_list = []
    for k in ocp.keys():
        if ocp[k]:
            occupied_list.append(ocp[k])
    f.write("occupation:"+str(occupied_list)+"\n")


def DFS(G:nx.MultiDiGraph,start_edge,cur_edge,dep_chain:list,ocp:dict,f,last_dep="A"):

    # f.write(str(dep_chain)+"\n")

    if cur_edge == start_edge:
        log_out(dep_chain,ocp,f)
        return
    
    elif cur_edge in popp(dep_chain):
        dep_chain.append(cur_edge)
        return
    dep_chain.append(cur_edge)

    # find A type dependency
    if last_dep != "A" and not IS_UNICAST[cur_edge[0]]:
        if G.out_degree(cur_edge[0]) > 1:
            for e in G.out_edges(cur_edge[0]):
                assert len(SID[cur_edge]) > 0, "error: current multicast edge has no stream id"
                for id in SID[cur_edge]:
                    if e != cur_edge and id in SID[e]: # for every other multicast edge with the same stream id
                        dep_chain.append(e)
                        DFS(G,start_edge,e,dep_chain,ocp,f,last_dep="A")
                        dep_chain.pop()

    # find V type dependency
    if last_dep != "V" and IS_CONTENT[cur_edge[1]]:
        if G.in_degree(cur_edge[1]) > 1:
            if ocp[cur_edge[1]] == False: # not occupied
                for e in G.in_edges(cur_edge[1]):
                    if e != cur_edge: # for every other content edge
                        ocp[cur_edge[1]] = e # occupy
                        dep_chain.append(e)
                        DFS(G,start_edge,e,dep_chain,ocp,f,last_dep="V")
                        ocp[cur_edge[1]] = False # release
                        dep_chain.pop()
            else: #occupied
                dep_chain.append(ocp[cur_edge[1]])
                DFS(G,start_edge,ocp[cur_edge[1]],dep_chain,ocp,f,last_dep="V")
                dep_chain.pop()

    # find H type dependency
    if G.out_degree(cur_edge[1]) > 0:
        for e in G.out_edges(cur_edge[1]):
            dep_chain.append(e)
            DFS(G,start_edge,e,dep_chain,ocp,f,last_dep="H")
            dep_chain.pop()
    return


def search(G:nx.MultiDiGraph,ocp:dict,f):
    for n in G.nodes():
        if G.in_degree(n) > 1 and IS_CONTENT[n]: # contention node
            for de in G.in_edges(n):
                for se in G.in_edges(n):
                    ocp[n] = se
                    if de != se:
                        print("start searching at:",se,de)
                        DFS(G,se,de,[se,de],ocp,f,last_dep="V")
                    ocp[n] = False

if __name__ == "__main__":
    for n in CDG.nodes():
        OCP[n] = False

    with open(file_name,'w') as f:
        search(CDG,OCP,f)
        # OCP['3_1_cw_o'] = ('3_1_ce_i', '3_1_cw_o')
        # DFS(CDG,('3_1_ce_i', '3_1_cw_o'), ('3_1_cl_i', '3_1_cw_o'),[('3_1_ce_i', '3_1_cw_o'), ('3_1_cl_i', '3_1_cw_o')],OCP,f,last_dep="V")
    print(f"self-defined algorithm find {len(CYCLES)} cycle(s)")
    if rw.find_cycle(CDG) != False:
        print(f"graph-loop algorithm find cycle(s)")
    else:
        print(f"graph-loop algorithm find no cycle")

    # find critical nodes begin
    # critical_nodes = []
    # for cycle in CYCLES:
    #     for edge in cycle:
    #         critical_nodes.append([])
    #         if edge[0][-4:] == 'cl_o':
    #             if edge[0][:-5] not in critical_nodes[-1]:
    #                 critical_nodes[-1].append(edge[0][:-5])

    # for item in critical_nodes:
    #     if len(item) > 0:
    #         print(item)
    # find critical nodes begin

    # draw cycles begin
    cnt = 0
    for cycle in CYCLES:
        cnt += 1
        plt.figure(figsize=(10,11))
        plot_routers()
        G,pos,el = construct_cdg(cycle)
        nx.draw(G, pos, node_size = 20,width=1, arrowsize=10,node_color='black',edge_color='red',arrowstyle='-|>')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=el,font_size=7,font_color='blue',bbox=dict(alpha=0))
        plt.savefig(f'/mnt/c/git/nvcim-comm/behavior_model/cycle_img/img_'+str(cnt)+'jpg',
            dpi=400,bbox_inches='tight')
        print(f"Finished saving {cnt} image")
        # plt.show()
    # draw cycles end

