import os
from maptools import dec2bin

__all__ = ['gen_cast_network_config']

def get_fcdn(w, h, dn_list):
    data = 0
    for n in dn_list:
        i = n[0] + n[1] * w
        data += 2**i
    return dec2bin(data, bit_wide=w*h)

def gen_cast_network_config(root_dir, w, h, cast_fc, packetlen):
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
            # west flow control is for the (0, 0) xbar
            local_is_fc, west_is_fc = 0, 0
            local_fcdn, west_fcdn = 0, 0
            local_pktlen, west_pktlen = 0, 0
            if (i, j) in cast_fc: # is flow control source node
                local_is_fc = 1
                local_fcdn = get_fcdn(w, h, cast_fc[(i, j)])
                local_pktlen = packetlen
            if (i, j) == (0, 0): # is (0, 0) xbar
                west_is_fc = 1
                west_fcdn = get_fcdn(w, h, [(0, 0)]) # only fc with the first xbar (first layer)
                west_pktlen = packetlen
            containt += "\nlocalparam isUBM_list_"+str(i)+"_"+str(j)+"[`CN] = '{1,1,1,1,1};\n"
            containt += "localparam isFC_list_"+str(i)+"_"+str(j)+"[`CN] = '{%d,%d,0,0,0};\n" % (local_is_fc, west_is_fc)
            containt += "localparam [`NOC_WIDTH*`NOC_HEIGHT-1:0] FCdn_list_"+str(i)+"_"+str(j)+"[`CN] = '{"+str(n)+f"'b{local_fcdn},"+str(n)+f"'b{west_fcdn},"+str(n)+"'b0,"+str(n)+"'b0,"+str(n)+"'b0};\n"
            containt += "localparam int FCpl_list_"+str(i)+"_"+str(j)+"[`CN] = '{%d,%d,0,0,0};\n" % (local_pktlen, west_pktlen)
            rt_files = []
            for m in range(5):
                file = os.path.join(root_dir, 'network', 'config', 'routing_tables', f'cast_{i}_{j}_{m}')
                file = '"'+file+'"'
                rt_files.append(file)
            containt += '''localparam string cast_rt_file_list_'''+str(i)+'''_'''+str(j)+'''[`CN] = '{'''+rt_files[0]+''','''+rt_files[1]+''','''+rt_files[2]+''','''+rt_files[3]+''','''+rt_files[4]+'''};\n'''
    containt += '''
`endif'''
    with open(file_dir,"w") as my_file:
        my_file.write("{0}\n".format(containt))
        my_file.flush()
        my_file.close()
    
    print(f"cast network configuration info has been written to: {file_dir}")