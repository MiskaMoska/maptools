'''
A test script to test the optimization of cast communication plan
The object is to reduce contentions of cast communication as much as possible
'''
import networkx as nx
from mapper import Mapper
from mapplot import *

def construct_test_cdg(w,h,cast_paths:dict):
    legal_node = ['cw_i','cw_o','ce_i','ce_o','cv0_i','cv1_i','cv1_o','cv0_o','cl_i','cl_o','mrg']
    G=nx.MultiDiGraph()
    for i in range(w):
        for j in range(h):
            for k in range(len(legal_node)):
                G.add_node(f"{i}_{j}_"+legal_node[k])

    # generate cast inner edges according to cast_paths
    for k,v in cast_paths.items():
        for p in v:
            G.add_edge(f"{k[0]}_{k[1]}_"+translate(p[0],'i'),f"{k[0]}_{k[1]}_"+translate(p[1],'o'))
    return G

def evaluate_contention(G:nx.MultiDiGraph):
    cnt = 0
    for n in G.nodes():
        if G.in_degree(n) > 1:
            cnt += 1
    return cnt

if __name__ == "__main__":
    maper = Mapper(5,11,[1,1,1,1,1,2,2,2,4,4,4,4,4],[1,1,1,1,1,1,1,2,2,2,2,2,2])
    con_accu = 10000
    while True:
        maper.Run_Mapping()
        G = construct_test_cdg(maper.w,maper.h,maper.cast_paths)
        con = evaluate_contention(G)
        if con < con_accu:
            con_accu = con
            print("accumulated_contention_level:",con)
            plt.figure(figsize=(maper.w,maper.h))
            plot_routers(maper.w,maper.h)
            G,pos,el = construct_cdg(maper.w,maper.h,maper.cast_paths,maper.merge_paths)
            ec = get_edge_colors(G)
            nx.draw(G, pos, node_size = 20,width=1, arrowsize=10,node_color='black',edge_color='blue',arrowstyle='-|>')
            plt.savefig(f'/mnt/c/git/nvcim-comm/behavior_model/opt_cast/contention_level_'+str(con_accu),
                            dpi=400,bbox_inches='tight')
            print(f"Finished saving the image")
        if con_accu <= 0:
            print("cast_paths = dict()")
            for k,v in maper.cast_paths.items():
                print(f"cast_paths[{k}]={v}")
            print("merge_paths = [")
            for i in maper.merge_paths:
                print(i,",")
            print("]")
            break
    
