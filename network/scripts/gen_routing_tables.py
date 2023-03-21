import os
from typing import Dict, Tuple, List
from maptools import dec2bin

__all__ = ['gen_routing_tables']

def gen_routing_tables(root_dir, w, h, config, type):
    '''
    Generate the routing tables to the target folder
    config: can be `NocConfig.cast_config` or `NocConfig.gather_config`
    type: can be 'cast' or 'gather'
    Note that the raw `cast_config` generated from `NocConfig` cannot be
    written to routing tables directly cause stab and flee ports should be 
    added to it later.
    '''
    # prepare clean saving directory
    save_dir = os.path.join(root_dir, 'network', 'config', 'routing_tables')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    rm_files = os.path.join(save_dir, type+'*')
    print(f'removing old {type} routing tables')
    os.system(f'rm -rf {rm_files}')

    for x in range(w):
        for y in range(h):
            for ip in range(5):
                file_dir = os.path.join(save_dir, type+f'_{w}_{y}_{ip}')
                os.system('touch '+ file_dir)

    # save files
    keys = config.keys()
    for key in keys:
        local_dict = dict() 
        for path in config[key]:
            if path[0] not in local_dict.keys():
                local_dict[path[0]] = []
            local_dict[path[0]].append((path[1],path[2]))
        for input_port in local_dict.keys():
            input_dict = dict()
            for op_id in local_dict[input_port]:
                if op_id[1] not in input_dict.keys():
                    input_dict[op_id[1]] = 0
                input_dict[op_id[1]] += 2**op_id[0]
            for id in input_dict.keys():
                file_dir = os.path.join(save_dir, type+f'_{key[0]}_{key[1]}_{input_port}')
                with open(file_dir, 'a') as f:
                    f.write(f'{dec2bin(input_dict[id], bit_wide=5)}{dec2bin(id, bit_wide=10)}\n')
                    f.flush()
    print(f'new {type} routing tables have been written to {save_dir}')