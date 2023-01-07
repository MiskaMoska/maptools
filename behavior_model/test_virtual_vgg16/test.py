dn_node = [(1,2),(2,2),(5,2),(6,2)] # stream 9
dn_node = [(3,2),(4,2)] # stream 8
dn_node = [(1,1),(2,1),(3,1)] # stream 7
dn_node = [(0,5),(1,5),(3,5),(4,5)] # stream 14
dn_node = [(3,4),(4,4),(5,5),(6,5)] # stream 13
dn_node = [(3,7),(4,7),(5,7),(6,7)] # stream 17
dn_node = [(3,6),(4,6),(5,6),(6,6)] # stream 16

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

data = 0
for i in dn_node:
    id = i[1]*7+i[0]
    data += 2**id

for i in range(7):
    for j in range(8):
        print('localparam string rt_file_list_'+str(i)+'_'+str(j)+'[`CN] = \'{"/mnt/c/git/NVCIM-COMM/behavior_model/test_virtual_vgg16/config/cast_rt_'+str(i)+'_'+str(j)+'_0","/mnt/c/git/NVCIM-COMM/behavior_model/test_virtual_vgg16/config/cast_rt_'+str(i)+'_'+str(j)+'_1","/mnt/c/git/NVCIM-COMM/behavior_model/test_virtual_vgg16/config/cast_rt_'+str(i)+'_'+str(j)+'_2","/mnt/c/git/NVCIM-COMM/behavior_model/test_virtual_vgg16/config/cast_rt_'+str(i)+'_'+str(j)+'_3","/mnt/c/git/NVCIM-COMM/behavior_model/test_virtual_vgg16/config/cast_rt_'+str(i)+'_'+str(j)+'_4"};''')