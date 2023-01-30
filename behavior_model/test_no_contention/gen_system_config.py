'''
Generate isCaster and stream_id info to configure the PEs in "system.sv"
The generated info should be written into "system_config.svh"
'''
import sys
sys.path.append("..") 
from scripts.cast_path_config import PATH_DICT

isCaster = []
stream_id = []
keys = list(PATH_DICT.keys())

for k in keys:
    v = PATH_DICT[k]
    flag = False
    for path in v:
        if path[0] == 0: 
            flag = True
            tmp = path[2]
            break
    if flag:
        isCaster.append(1)
        stream_id.append(tmp)
    else:
        isCaster.append(0)
        stream_id.append(0)

for i in range(len(keys)):
    print(f"localparam isCaster_{keys[i][0]}_{keys[i][1]} = {isCaster[i]};")
    print(f"localparam stream_id_{keys[i][0]}_{keys[i][1]} = {stream_id[i]};")