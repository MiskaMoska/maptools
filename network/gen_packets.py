import os 
import struct
import random
os.chdir('.')

DW = 34

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

with open('send_pool.bin','w') as f:
    for i in range(10000):
        a = int.from_bytes(struct.pack("f",random.random()),'little')
        f.write('01'+str(dec2bin(a,bit_wide=32))+'\n')