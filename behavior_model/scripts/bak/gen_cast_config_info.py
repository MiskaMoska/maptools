W = 5
H = 11
dir_name = "test_no_contention"

for x in range(W):
    for y in range(H):
        print("localparam isUBM_list_"+str(x)+"_"+str(y)+"[`CN] = '{0,0,0,0,0};")

for x in range(W):
    for y in range(H):
        print("localparam isFC_list_"+str(x)+"_"+str(y)+"[`CN] = '{0,0,0,0,0};")

bits = str(W*H)+"'b0"
for x in range(W):
    for y in range(H):
        print("localparam [`NOC_WIDTH*`NOC_HEIGHT-1:0] FCdn_list_"+str(x)+"_"+str(y)+"[`CN] = '{"+bits+","+bits+","+bits+","+bits+","+bits+"};")

for x in range(W):
    for y in range(H):
        print("localparam int FCpl_list_"+str(x)+"_"+str(y)+"[`CN] = '{0,0,0,0,0};")

for x in range(W):
    for y in range(H):
        print('''localparam string rt_file_list_'''+str(x)+"_"+str(y)+'''[`CN] = '{"/mnt/c/git/NVCIM-COMM/behavior_model/'''+dir_name+'''/config/cast_rt_'''+str(x)+"_"+str(y)+'''_0","/mnt/c/git/NVCIM-COMM/behavior_model/'''+dir_name+'''/config/cast_rt_'''+str(x)+"_"+str(y)+'''_1","/mnt/c/git/NVCIM-COMM/behavior_model/'''+dir_name+'''/config/cast_rt_'''+str(x)+"_"+str(y)+'''_2","/mnt/c/git/NVCIM-COMM/behavior_model/'''+dir_name+'''/config/cast_rt_'''+str(x)+"_"+str(y)+'''_3","/mnt/c/git/NVCIM-COMM/behavior_model/'''+dir_name+'''/config/cast_rt_'''+str(x)+"_"+str(y)+'''_4"};''')