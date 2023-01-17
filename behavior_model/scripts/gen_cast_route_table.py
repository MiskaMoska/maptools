'''
Generate cast network routing table
Run this script under ./behavior_model/scripts
'''
import os
from cast_path_config import *

file_dir = '/mnt/c/git/NVCIM-COMM/behavior_model/test_virtual_vgg16/config/'
file_name = 'cast_rt_'

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

os.chdir(file_dir)
os.system('rm -rf cast_rt_*')
#----------------------------------------------------------------------------------
#Comment this segement before running to filter out valid rt config files 
for x in range(W):
    for y in range(H):
        for ip in range(5):
            file = file_dir + file_name + str(x) + '_' + str(y) + '_' + str(ip)
            os.system('touch '+file)
#---------------------------------------------------------------------------------- 

keys = PATH_DICT.keys()

for key in keys:
    print('\n\n'+80*'-')
    print('router_pos:',key[0],key[1])
    local_dict = dict() 
    for path in PATH_DICT[key]:
        if path[0] not in local_dict.keys():
            local_dict[path[0]] = []
        local_dict[path[0]].append((path[1],path[2]))
    for input_port in local_dict.keys():
        print('\n')
        print('input_port:',input_port)
        input_dict = dict()
        for op_id in local_dict[input_port]:
            print(op_id)
            if op_id[1] not in input_dict.keys():
                input_dict[op_id[1]] = 0
            input_dict[op_id[1]] += 2**op_id[0]
        for id in input_dict.keys():
            file = file_dir + file_name + str(key[0]) + '_' + str(key[1]) + '_' + str(input_port)
            with open(file, 'a') as f:
                f.write(str(dec2bin(input_dict[id], bit_wide=5))+str(dec2bin(id, bit_wide=SID_WIDTH))+"\n")
                f.flush()
