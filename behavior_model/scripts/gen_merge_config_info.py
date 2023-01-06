'''
Generate merge network config info in "merge_network_config.svh"
'''

import networkx as nx
from merge_path_config import *

def dec2bin(dec_num, bit_wide=16):    
    _, bin_num_abs = bin(dec_num).split('b')    
    if len(bin_num_abs) > bit_wide:        
        raise ValueError   
    else:        
        if dec_num >= 0:            
            bin_num = bin_num_abs.rjust(bit_wide, '0')        
        else:            
            _, bin_num = bin(2**bit_wide + dec_num).split('b')    
    return bin_num 

MG = nx.MultiDiGraph()

for x in range(W):
    for y in range(H):
        MG.add_node((x,y))

MG.add_edges_from(Paths)

nodes = list(MG.nodes())
input_mask = []
output_sel = []

for node in nodes:
    x = node[0]
    y = node[1]
    neighbor_node = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    cur_input_mask = 0
    for i,pre_node in enumerate(neighbor_node):
        if (pre_node,node) in MG.in_edges(node):
            cur_input_mask += 2**(i+1)

    cur_output_sel = 0
    if MG.out_degree(node) == 0: # is merge node
        cur_output_sel = 1
    else: # not merge node
        cur_input_mask += 1
        for j,post_node in enumerate(neighbor_node):
            if (node,post_node) in MG.out_edges(node):
                cur_output_sel = 2**(j+1)
                break

    input_mask.append(dec2bin(cur_input_mask,bit_wide=5))
    output_sel.append(dec2bin(cur_output_sel,bit_wide=5))

for i in range(len(nodes)):
    x = nodes[i][0]
    y = nodes[i][1]
    print("localparam input_mask_"+str(x)+"_"+str(y)+" = 5'b"+str(input_mask[i])+";")
    print("localparam output_sel_"+str(x)+"_"+str(y)+" = 5'b"+str(output_sel[i])+";")

