import networkx as nx
from cast_path_config import PATH_DICT as cast_paths
from merge_path_config import Paths as merge_paths

W = 7
H = 8

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

CDG = nx.MultiDiGraph()
SID = dict() # store the stream id of each edge in CDG
nodes = ['cw_i','cw_o','ce_i','ce_o','cv0_i','cv0_o','cv1_i','cv1_o','cl_i','cl_o'] 

# generate cast nodes
for i in range(W):
    for j in range(H):
        for n in nodes:
            CDG.add_node(f"{i}_{j}_"+n)

# generate cast transfer edges according to cast_paths
for k in cast_paths.keys():
    x = k[0]
    y = k[1]
    for path in cast_paths[k]:
        i_chan_name = translate(path[0],'i')
        o_chan_name = translate(path[1],'o')
        sn = f"{x}_{y}_"+i_chan_name
        dn = f"{x}_{y}_"+o_chan_name
        CDG.add_edge(sn,dn)
        if (sn,dn) not in SID.keys():
            SID[(sn,dn)] = []
        SID[(sn,dn)].append(path[2])

# generate cast neighbor edges
for i in range(W-1):
    for j in range(H):
        CDG.add_edge(f"{i}_{j}_ce_o",f"{i+1}_{j}_cw_i")
        CDG.add_edge(f"{i+1}_{j}_cw_o",f"{i}_{j}_ce_i")

for i in range(W):
    for j in range(H-1):
        CDG.add_edge(f"{i}_{j}_cv0_o",f"{i}_{j+1}_cv0_i")
        CDG.add_edge(f"{i}_{j}_cv1_o",f"{i}_{j+1}_cv1_i")

# generate merge nodes
for i in range(W):
    for j in range(H):
        CDG.add_node(f"{i}_{j}_mrg")

# generate merge edges according to merge_paths
for path in merge_paths:
    sx = path[0][0]
    sy = path[0][1]
    dx = path[1][0]
    dy = path[1][1]
    CDG.add_edge(f"{sx}_{sy}_mrg",f"{dx}_{dy}_mrg")

# generate 
for i in range(W):
    for j in range(H):
        if CDG.out_degree(f"{i}_{j}_mrg") == 0: #the current node is a caster
            CDG.add_edge(f"{i}_{j}_cl_o",f"{i}_{j}_cl_i")
            CDG.add_edge(f"{i}_{j}_mrg",f"{i}_{j}_cl_i")
        else: # the current node is not a caster
            CDG.add_edge(f"{i}_{j}_cl_o",f"{i}_{j}_mrg")


# for k in SID:
#     print(SID[k])