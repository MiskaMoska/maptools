import os 
import struct
import random
from maptools import dec2bin

__all__ = ['gen_packets']

def gen_packets(root_dir, data_width, flit_num):
    file_dir = os.path.join(root_dir, 'network', 'test', 'send_pool')
    with open(file_dir,'w') as f:
        for i in range(flit_num):
            a = int.from_bytes(struct.pack("f",random.random()),'little')
            f.write('01'+str(dec2bin(a,bit_wide=data_width-2))+'\n')
    print(f"{flit_num} flits have been written to: {file_dir}")