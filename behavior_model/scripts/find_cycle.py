'''
Given an CDG, find all multicast dependency cycles
A type: multicast dependency
V type: contention dependency
H type: serial dependency
'''
import networkx as nx
import sys
from copy import deepcopy
from build_cdg import CDG
from build_cdg import SID

file_name = "/mnt/c/git/nvcim-comm/behavior_model/scripts/cycle2"

G = nx.MultiDiGraph()
OCP = dict()

W = 2
H = 2

def popp(lst:list):
    lst.pop()
    return lst

def log_out(dep_chain:list,ocp:dict,f):
    print("find one")
    f.write("find a cycle:"+str(dep_chain)+"\n")
    occupied_list = []
    for k in ocp.keys():
        if ocp[k]:
            occupied_list.append(ocp[k])
    f.write("occupation:"+str(occupied_list)+"\n")


def DFS(G:nx.MultiDiGraph,start_edge,cur_edge,dep_chain:list,ocp:dict,f,last_dep="A"):

    # print(dep_chain)
    if cur_edge == start_edge:
        log_out(dep_chain,ocp,f)
        return
    
    elif cur_edge in popp(dep_chain):
        dep_chain.append(cur_edge)
        return
    dep_chain.append(cur_edge)

    # find A type dependency
    if last_dep != "A":
        if G.out_degree(cur_edge[0]) > 1:
            for e in G.out_edges(cur_edge[0]):
                assert len(SID[cur_edge]) > 0, "error: current multicast edge has no stream id"
                for id in SID[cur_edge]:
                    if e != cur_edge and SID[e] == id: # for every other multicast edge with the same stream id
                        dep_chain.append(e)
                        DFS(G,start_edge,e,dep_chain,ocp,f,last_dep="A")
                        dep_chain.pop()

    # find V type dependency
    if last_dep != "V":
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


# def search(G:nx.MultiDiGraph,ocp:dict,f):
#     cnt = 0
#     for n in G.nodes():
#         if G.out_degree(n) > 1: # multicast node
#             for se in G.out_edges(n):
#                 for de in G.out_edges(n):
#                     if de != se:
#                         cnt += 1
#                         print(cnt)
#                         DFS(G,se,de,[se,de],ocp,f,last_dep="A")

def search(G:nx.MultiDiGraph,ocp:dict,f):
    for n in G.nodes():
        if G.in_degree(n) > 1: # multicast node
            for de in G.in_edges(n):
                ocp[n] = de
                for se in G.in_edges(n):
                    if de != se:
                        DFS(G,se,de,[se,de],ocp,f,last_dep="V")
                        print("---")
                ocp[n] = False

if __name__ == "__main__":

# if __name__ == "__main__":
#     legal_path = [['left_i','right_o'],['left_i','up_o'],['left_i','down_o'],['right_i','left_o'],['right_i','up_o'],['right_i','down_o'],['up_i','down_o'],['down_i','up_o']]
#     legal_node = ['left_i','left_o','right_i','right_o','up_i','up_o','down_i','down_o']

#     for i in range(W):
#         for j in range(H):
#             rc = []
#             for k in range(len(legal_node)):
#                 G.add_node((i,j,legal_node[k]))
#             for k in range(len(legal_path)):
#                 G.add_edge((i,j,legal_path[k][0]),(i,j,legal_path[k][1]))

#     for i in range(W-1):
#         for j in range(H):
#             G.add_edge((i,j,'right_o'),(i+1,j,'left_i'))
#             G.add_edge((i+1,j,'left_o'),(i,j,'right_i'))

#     for i in range(W):
#         for j in range(H-1):
#             G.add_edge((i,j+1,'up_o'),(i,j,'down_i'))
#             G.add_edge((i,j,'down_o'),(i,j+1,'up_i'))
    for n in CDG.nodes():
        OCP[n] = False

    with open(file_name,'w') as f:
        search(CDG,OCP,f)
