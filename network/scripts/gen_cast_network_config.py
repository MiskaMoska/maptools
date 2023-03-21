import os

__all__ = ['gen_cast_network_config']

def gen_cast_network_config(root_dir, w, h):
    save_dir = os.path.join(root_dir, 'network', 'config', 'network_config')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_dir = os.path.join(save_dir, 'cast_network_config.svh')
    containt = '''
`ifndef __CAST_NETWORK_CONFIG_SVH_
`define __CAST_NETWORK_CONFIG_SVH_
    '''
    n = w * h
    for i in range(w):
        for j in range(h):
            containt += "\nlocalparam isUBM_list_"+str(i)+"_"+str(j)+"[`CN] = '{0,0,0,0,0};\n"
            containt += "localparam isFC_list_"+str(i)+"_"+str(j)+"[`CN] = '{0,0,0,0,0};\n"
            containt += "localparam [`NOC_WIDTH*`NOC_HEIGHT-1:0] FCdn_list_"+str(i)+"_"+str(i)+"[`CN] = '{"+str(n)+"'b0,"+str(n)+"'b0,"+str(n)+"'b0,"+str(n)+"'b0,"+str(n)+"'b0};\n"
            containt += "localparam int FCpl_list_"+str(i)+"_"+str(i)+"[`CN] = '{0,0,0,0,0};\n"
            rt_files = []
            for m in range(5):
                file = os.path.join(root_dir, 'network', 'srcs', 'config', 'routing_tables', f'cast_{i}_{j}_{m}')
                file = '"'+file+'"'
                rt_files.append(file)
            containt += '''localparam string rt_file_list_'''+str(i)+'''_'''+str(j)+'''[`CN] = '{'''+rt_files[0]+''','''+rt_files[1]+''','''+rt_files[2]+''','''+rt_files[3]+''','''+rt_files[4]+'''};\n'''
    containt += '''
`endif'''
    with open(file_dir,"w") as my_file:
        my_file.write("{0}\n".format(containt))
        my_file.flush()
        my_file.close()
    
    print(f"cast network configuration info has been written to: {file_dir}")