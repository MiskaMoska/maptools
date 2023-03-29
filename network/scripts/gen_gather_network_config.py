import os
from maptools import dec2bin

__all__ = ['gen_gather_network_config']

def get_fcdn(w, h, dn_list):
    data = 0
    for n in dn_list:
        i = n[0] + n[1] * w
        data += 2**i
    return dec2bin(data, bit_wide=w*h)

def gen_gather_network_config(root_dir, w, h, gather_fc, packetlen):
    save_dir = os.path.join(root_dir, 'network', 'config', 'network_config')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_dir = os.path.join(save_dir, 'gather_network_config.svh')
    containt = '''
`ifndef __GATHER_NETWORK_CONFIG_SVH_
`define __GATHER_NETWORK_CONFIG_SVH_
    '''
    n = w * h
    for i in range(w):
        for j in range(h):
            # west flow control is for the (0, 0) xbar
            is_fc = 0
            fcdn = 0
            pktlen = 0
            if (i, j) in gather_fc: # is flow control source node
                is_fc = 1
                fcdn = get_fcdn(w, h, gather_fc[(i, j)])
                pktlen = packetlen
            containt += "\nlocalparam isFC_list_"+str(i)+"_"+str(j)+"[`CN] = '{%d,0,0,0,0};\n" % (is_fc)
            containt += "localparam [`NOC_WIDTH*`NOC_HEIGHT-1:0] FCdn_list_"+str(i)+"_"+str(j)+"[`CN] = '{"+str(n)+f"'b{fcdn},"+str(n)+"'b0,"+str(n)+"'b0,"+str(n)+"'b0,"+str(n)+"'b0};\n"
            containt += "localparam int FCpl_list_"+str(i)+"_"+str(j)+"[`CN] = '{%d,0,0,0,0};\n" % (pktlen)
            rt_files = []
            for m in range(5):
                file = os.path.join(root_dir, 'network', 'config', 'routing_tables', f'gather_{i}_{j}_{m}')
                file = '"'+file+'"'
                rt_files.append(file)
            containt += '''localparam string gather_rt_file_list_'''+str(i)+'''_'''+str(j)+'''[`CN] = '{'''+rt_files[0]+''','''+rt_files[1]+''','''+rt_files[2]+''','''+rt_files[3]+''','''+rt_files[4]+'''};\n'''
    containt += '''
`endif'''
    with open(file_dir,"w") as my_file:
        my_file.write("{0}\n".format(containt))
        my_file.flush()
        my_file.close()
    
    print(f"gather network configuration info has been written to: {file_dir}")