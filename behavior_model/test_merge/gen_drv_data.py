DATA_WIDTH = 16
RAM_DEPTH = 32
ram_file = "/mnt/c/git/nvcim-comm/behavior_model/test_merge/send_pool"

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

with open(ram_file,"w") as f:
    for i in range(RAM_DEPTH):
        f.write(dec2bin(i,bit_wide=DATA_WIDTH)+"\n")
    f.flush()
