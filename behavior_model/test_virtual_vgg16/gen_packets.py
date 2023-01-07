import random
root_path = "/mnt/c/git/NVCIM-COMM/behavior_model/test_virtual_vgg16/"
driver_file_name = "send_pool"

DATA_WIDTH = 16
PACKET_LEN = 16
TOTAL_LEN = 1000
SID_WIDTH = 10 # stream ID data width

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

class packet:
    # create a new random packet
    def __init__(self,size,sid):
        self.payload = []
        self.payload.append("00"+(DATA_WIDTH-2-SID_WIDTH)*"0"+str(dec2bin(sid,bit_wide=SID_WIDTH)))
        for i in range(1,size-1):
            self.payload.append("01" + str(dec2bin(random.randint(0,8000),bit_wide=DATA_WIDTH-2)))
        self.payload.append("11"+(DATA_WIDTH-2)*"1")

if __name__ == "__main__":
    with open(root_path+driver_file_name,'w') as f:
        for i in range(TOTAL_LEN//PACKET_LEN):
            pkt = packet(PACKET_LEN,1023)
            for j in range(len(pkt.payload)):
                f.write(pkt.payload[j]+'\n')
        f.flush()
        