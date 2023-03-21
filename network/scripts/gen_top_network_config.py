import os

__all__ = ['gen_top_network_config']

def gen_top_network_config(root_dir, config):
    save_dir = os.path.join(root_dir, 'network', 'config', 'network_config')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_dir = os.path.join(save_dir, 'network_config.svh')
    containt = '''
`ifndef __NETWORK_CONFIG_SVH_
`define __NETWORK_CONFIG_SVH_
    '''
    for xbar, cfg in config.items():
        cast_out = int(cfg['cast_out'])
        gather_out = int(cfg['gather_out'])
        merge_in = int(cfg['merge_in'])
        gather_in = int(cfg['gather_in'])
        cast_sid = cfg['cast_sid'] if 'cast_sid' in cfg else 0
        gather_sid = cfg['gather_sid'] if 'gather_sid' in cfg else 0
        containt += f"\nlocalparam cast_out_{xbar[0]}_{xbar[1]} = {cast_out};\n"
        containt += f"localparam gather_out_{xbar[0]}_{xbar[1]} = {gather_out};\n"
        containt += f"localparam merge_in_{xbar[0]}_{xbar[1]} = {merge_in};\n"
        containt += f"localparam gather_in_{xbar[0]}_{xbar[1]} = {gather_in};\n"
        containt += f"localparam cast_sid_{xbar[0]}_{xbar[1]} = {cast_sid};\n"
        containt += f"localparam gather_sid_{xbar[0]}_{xbar[1]} = {gather_sid};\n"

    containt += '''
`endif
'''
    with open(file_dir,"w") as my_file:
        my_file.write("{0}\n".format(containt))
        my_file.flush()
        my_file.close()
    
    print(f"top network configuration info has been written to: {file_dir}")