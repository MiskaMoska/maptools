'''
Configure the hardware network according to cast_paths and merge_paths
---------------------------------------------------------------
1.Generate Cast Network
2.Generate Cast Routing Table
3.Generate Cast Config Info
4.Generate Merge Network
5.Generate Merge Config Info
6.Generate System
7.Generate System Config Info
8.Generate System Header
---------------------------------------------------------------
TODO Only support E2E-FC at local port, not at other ports
'''
import os
import networkx as nx

class Configurator(object):

    def __init__(self,w,h,cast_paths:dict,merge_paths:list,merge_nodes:list,
                    data_width:int=16,e2e_dict:dict=dict(),ubm_nodes:list=[],pool_layers:list=[],
                    root_dir="/mnt/c/git/nvcim-comm/behavior_model/test_auto/"):
        self.w = w
        self.h = h
        self.cast_paths = cast_paths
        self.merge_paths = merge_paths
        self.merge_nodes = merge_nodes
        self.e2e_dict = e2e_dict # for deadlock killing
        self.ubm_nodes = ubm_nodes # for deadlock killing
        self.pool_layers = pool_layers # which layer has 2*2 pooling

        self.__get_flee_ports()
        self.data_width = data_width
        self.root_dir = root_dir
    
    def __get_one_flee_ports(self,mn_pos):
        for op in range(1,5):
            flag = False
            for path in self.cast_paths[mn_pos]:
                if path[1] == op:
                    flag = True
                    break
            if not flag:
                return op
        return 0

    def __get_flee_ports(self):
        '''
        pick out flee ports
        '''
        assert len(self.merge_nodes[-1]) == 2, "the number of last layer's merge nodes must be 2"
        mn0 = self.merge_nodes[-1][0]
        mn1 = self.merge_nodes[-1][1]
        mn0_pos = (mn0 % self.w, mn0 // self.w)
        mn1_pos = (mn1 % self.w, mn1 // self.w)

        mn0_op = self.__get_one_flee_ports(mn0_pos)
        assert mn0_op != 0, "cannot determine the flee port"
        mn1_op = self.__get_one_flee_ports(mn1_pos)
        assert mn1_op != 0, "cannot determine the flee port"

        self.flee0 = (mn0_pos[0],mn0_pos[1],mn0_op)
        self.flee1 = (mn1_pos[0],mn1_pos[1],mn1_op)

    @staticmethod
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

    def Generate_Cast_Network(self):

        file_name = self.root_dir + "cast_network.sv"

        def gen_instances(data_width,w,h):
            data_width = str(data_width)
            inst_str = ""
            for j in range(w): 
                for i in range(h): 
                    id = w*i+j
                    '''
                    generate vert0 and vert1 input ports
                    '''
                    if i == 0: #vert0 and vert1 input ports
                        vert0_in_data = data_width + "'b0"
                        vert0_in_valid = "1'b0"
                        vert0_in_ready = ""

                        vert1_in_data = data_width + "'b0"
                        vert1_in_valid = "1'b0"
                        vert1_in_ready = ""

                    else:
                        vert0_in_data = "data_"+str(id-w)+"_to_"+str(id)+"_v0"
                        vert0_in_valid = "valid_"+str(id-w)+"_to_"+str(id)+"_v0"
                        vert0_in_ready = "ready_"+str(id)+"_to_"+str(id-w)+"_v0"

                        vert1_in_data = "data_"+str(id-w)+"_to_"+str(id)+"_v1"
                        vert1_in_valid = "valid_"+str(id-w)+"_to_"+str(id)+"_v1"
                        vert1_in_ready = "ready_"+str(id)+"_to_"+str(id-w)+"_v1"

                    '''
                    generate vert0 and vert1 output ports
                    '''
                    if i == h-1: #south boundary
                        vert0_out_data = ""
                        vert0_out_valid = ""
                        vert0_out_ready = "1'b0"

                        vert1_out_data = ""
                        vert1_out_valid = ""
                        vert1_out_ready = "1'b0"
                    else:
                        vert0_out_data = "data_"+str(id)+"_to_"+str(id+w)+"_v0"
                        vert0_out_valid = "valid_"+str(id)+"_to_"+str(id+w)+"_v0"
                        vert0_out_ready = "ready_"+str(id+w)+"_to_"+str(id)+"_v0"

                        vert1_out_data = "data_"+str(id)+"_to_"+str(id+w)+"_v1"
                        vert1_out_valid = "valid_"+str(id)+"_to_"+str(id+w)+"_v1"
                        vert1_out_ready = "ready_"+str(id+w)+"_to_"+str(id)+"_v1"

                    if j == self.flee0[0] and i == self.flee0[1] and self.flee0[2] == 3:
                        vert0_out_data = "data_o_flee0"
                        vert0_out_valid = "valid_o_flee0"
                        vert0_out_ready = "ready_i_flee0"

                    if j == self.flee0[0] and i == self.flee0[1] and self.flee0[2] == 4:
                        vert1_out_data = "data_o_flee0"
                        vert1_out_valid = "valid_o_flee0"
                        vert1_out_ready = "ready_i_flee0"

                    if j == self.flee1[0] and i == self.flee1[1] and self.flee1[2] == 3:
                        vert0_out_data = "data_o_flee1"
                        vert0_out_valid = "valid_o_flee1"
                        vert0_out_ready = "ready_i_flee1"

                    if j == self.flee1[0] and i == self.flee1[1] and self.flee1[2] == 4:
                        vert1_out_data = "data_o_flee1"
                        vert1_out_valid = "valid_o_flee1"
                        vert1_out_ready = "ready_i_flee1"

                    '''
                    generate west port signals
                    '''
                    if j == 0: #west boundary
                        if i == 0:
                            west_in_data = "data_i_stab"
                            west_in_valid = "valid_i_stab"
                            west_in_ready = "ready_o_stab"
                        else:
                            west_in_data = data_width + "'b0"
                            west_in_valid = "1'b0"
                            west_in_ready = ""

                        west_out_data = ""
                        west_out_valid = ""
                        west_out_ready = "1'b0"
                    else:
                        west_in_data = "data_"+str(id-1)+"_to_"+str(id)
                        west_in_valid = "valid_"+str(id-1)+"_to_"+str(id)
                        west_in_ready = "ready_"+str(id)+"_to_"+str(id-1)

                        west_out_data = "data_"+str(id)+"_to_"+str(id-1)
                        west_out_valid = "valid_"+str(id)+"_to_"+str(id-1)
                        west_out_ready = "ready_"+str(id-1)+"_to_"+str(id)

                    if j == self.flee0[0] and i == self.flee0[1] and self.flee0[2] == 1:
                        west_out_data = "data_o_flee0"
                        west_out_valid = "valid_o_flee0"
                        west_out_ready = "ready_i_flee0"

                    if j == self.flee1[0] and i == self.flee1[1] and self.flee1[2] == 1:
                        west_out_data = "data_o_flee1"
                        west_out_valid = "valid_o_flee1"
                        west_out_ready = "ready_i_flee1"

                    '''
                    generate east port signals
                    '''
                    if j == w-1: #east boundary
                        east_in_data = data_width + "'b0"
                        east_in_valid = "1'b0"
                        east_in_ready = ""

                        east_out_data = ""
                        east_out_valid = ""
                        east_out_ready = "1'b0"
                    else:
                        east_in_data = "data_"+str(id+1)+"_to_"+str(id)
                        east_in_valid = "valid_"+str(id+1)+"_to_"+str(id)
                        east_in_ready = "ready_"+str(id)+"_to_"+str(id+1)

                        east_out_data = "data_"+str(id)+"_to_"+str(id+1)
                        east_out_valid = "valid_"+str(id)+"_to_"+str(id+1)
                        east_out_ready = "ready_"+str(id+1)+"_to_"+str(id)

                    if j == self.flee0[0] and i == self.flee0[1] and self.flee0[2] == 2:
                        east_out_data = "data_o_flee0"
                        east_out_valid = "valid_o_flee0"
                        east_out_ready = "ready_i_flee0"

                    if j == self.flee1[0] and i == self.flee1[1] and self.flee1[2] == 2:
                        east_out_data = "data_o_flee1"
                        east_out_valid = "valid_o_flee1"
                        east_out_ready = "ready_i_flee1"

                    router_txt = '''
/*Router '''+str(j)+''','''+str(i)+'''*/    
cast_router #(
    .isUBM_list              (isUBM_list_'''+str(j)+'''_'''+str(i)+'''),
    .isFC_list               (isFC_list_'''+str(j)+'''_'''+str(i)+'''),
    .FCdn_list               (FCdn_list_'''+str(j)+'''_'''+str(i)+'''),
    .FCpl_list               (FCpl_list_'''+str(j)+'''_'''+str(i)+'''),
    .rt_file_list            (rt_file_list_'''+str(j)+'''_'''+str(i)+''')
)router_'''+str(j)+'''_'''+str(i)+'''(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           ('''+west_in_data+'''),
    .west_valid_i          ('''+west_in_valid+'''),
    .west_ready_o          ('''+west_in_ready+'''),
    .west_data_o           ('''+west_out_data+'''),
    .west_valid_o          ('''+west_out_valid+'''),
    .west_ready_i          ('''+west_out_ready+'''),
    .east_data_i           ('''+east_in_data+'''),
    .east_valid_i          ('''+east_in_valid+'''),
    .east_ready_o          ('''+east_in_ready+'''),
    .east_data_o           ('''+east_out_data+'''),
    .east_valid_o          ('''+east_out_valid+'''),
    .east_ready_i          ('''+east_out_ready+'''),
    .vert0_data_i          ('''+vert0_in_data+'''),
    .vert0_valid_i         ('''+vert0_in_valid+'''),
    .vert0_ready_o         ('''+vert0_in_ready+'''),
    .vert0_data_o          ('''+vert0_out_data+'''),
    .vert0_valid_o         ('''+vert0_out_valid+'''),
    .vert0_ready_i         ('''+vert0_out_ready+'''),
    .vert1_data_i          ('''+vert1_in_data+'''),
    .vert1_valid_i         ('''+vert1_in_valid+'''),
    .vert1_ready_o         ('''+vert1_in_ready+'''),
    .vert1_data_o          ('''+vert1_out_data+'''),
    .vert1_valid_o         ('''+vert1_out_valid+'''),
    .vert1_ready_i         ('''+vert1_out_ready+'''),
    .local_data_i          (data_i['''+str(j)+''']['''+str(i)+''']),
    .local_valid_i         (valid_i['''+str(j)+''']['''+str(i)+''']),
    .local_ready_o         (ready_o['''+str(j)+''']['''+str(i)+''']),
    .local_data_o          (data_o['''+str(j)+''']['''+str(i)+''']),
    .local_valid_o         (valid_o['''+str(j)+''']['''+str(i)+''']),
    .local_ready_i         (ready_i['''+str(j)+''']['''+str(i)+''']),
    .credit_upd            (credit_upd)
);\n'''
                    inst_str += router_txt
            return inst_str

        def gen_ports(w,h):

            port_str = '''
//Cast Network
//Width: '''+str(w)+'''
//Height:'''+str(h)+'''
`include "params.svh"
`include "cast_network_config.svh"

module cast_network(
    input       wire                            clk,
    input       wire                            rstn,
    '''

            port_str += '''
    //router local ports
    input       wire        [`DW-1:0]           data_i[`NOC_WIDTH][`NOC_HEIGHT],
    input       wire                            valid_i[`NOC_WIDTH][`NOC_HEIGHT],
    output      wire                            ready_o[`NOC_WIDTH][`NOC_HEIGHT],

    output      wire        [`DW-1:0]           data_o[`NOC_WIDTH][`NOC_HEIGHT],
    output      wire                            valid_o[`NOC_WIDTH][`NOC_HEIGHT],
    input       wire                            ready_i[`NOC_WIDTH][`NOC_HEIGHT],'''

            port_str += "\n"
            port_str += '''
    input       wire        [`DW-1:0]           data_i_stab,
    input       wire                            valid_i_stab,
    output      wire                            ready_o_stab,

    output      wire        [`DW-1:0]           data_o_flee0,
    output      wire                            valid_o_flee0,
    input       wire                            ready_i_flee0,

    output      wire        [`DW-1:0]           data_o_flee1,
    output      wire                            valid_o_flee1,
    input       wire                            ready_i_flee1,
'''
            port_str += '''
    //credit update signal input
    input       wire                            credit_upd[`NOC_WIDTH][`NOC_HEIGHT]\n'''
            port_str += ");\n"
            return port_str

        def gen_wires(w,h):

            wires_str = "\n//horizontal signals"
            for i in range(h):
                for j in range(w-1):
                    temp_txt = '''
wire    [`DW-1:0]   data_'''+str(w*i+j)+'''_to_'''+str(w*i+j+1)+''',\tdata_'''+str(w*i+j+1)+'''_to_'''+str(w*i+j)+''';
wire                valid_'''+str(w*i+j)+'''_to_'''+str(w*i+j+1)+''',\tvalid_'''+str(w*i+j+1)+'''_to_'''+str(w*i+j)+''';
wire                ready_'''+str(w*i+j)+'''_to_'''+str(w*i+j+1)+''',\tready_'''+str(w*i+j+1)+'''_to_'''+str(w*i+j)+''';'''
                    wires_str += temp_txt


            wires_str += "\n\n//vertical signals"
            for i in range(w):
                for j in range(h-1):
                    temp_txt = '''
wire    [`DW-1:0]   data_'''+str(i+j*w)+'''_to_'''+str(i+(j+1)*w)+'''_v0,\tdata_'''+str(i+j*w)+'''_to_'''+str(i+(j+1)*w)+'''_v1;
wire                valid_'''+str(i+j*w)+'''_to_'''+str(i+(j+1)*w)+'''_v0,\tvalid_'''+str(i+j*w)+'''_to_'''+str(i+(j+1)*w)+'''_v1;
wire                ready_'''+str(i+(j+1)*w)+'''_to_'''+str(i+j*w)+'''_v0,\tready_'''+str(i+(j+1)*w)+'''_to_'''+str(i+j*w)+'''_v1;'''
                    wires_str += temp_txt
            wires_str += "\n"
            return wires_str

        containt = ""
        containt += gen_ports(self.w,self.h)
        containt += gen_wires(self.w,self.h)
        containt += gen_instances(self.data_width,self.w,self.h)
        containt += "\nendmodule"

        with open(file_name,"w") as my_file:
            my_file.write("{0}\n".format(containt))
            my_file.flush()
            my_file.close()

        print("cast network has been written into:",file_name)

    def complete_cast_paths(self):
        self.cast_paths[(0,0)].append((1,0,1023))
        self.cast_paths[(self.flee0[0],self.flee0[1])].append((0,self.flee0[2],1022))
        self.cast_paths[(self.flee1[0],self.flee1[1])].append((0,self.flee1[2],1022))

    def Generate_Cast_Routing_table(self):
        file_dir = self.root_dir + "config/"
        file_name = 'cast_rt_'
        os.chdir(file_dir)
        os.system('rm -rf cast_rt_*')

        for x in range(self.w):
            for y in range(self.h):
                for ip in range(5):
                    file = file_dir + file_name + str(x) + '_' + str(y) + '_' + str(ip)
                    os.system('touch '+file)

        self.complete_cast_paths()
        keys = self.cast_paths.keys()

        for key in keys:
            # print('\n\n'+80*'-')
            # print('router_pos:',key[0],key[1])
            local_dict = dict() 
            for path in self.cast_paths[key]:
                if path[0] not in local_dict.keys():
                    local_dict[path[0]] = []
                local_dict[path[0]].append((path[1],path[2]))
            for input_port in local_dict.keys():
                # print('\n')
                # print('input_port:',input_port)
                input_dict = dict()
                for op_id in local_dict[input_port]:
                    # print(op_id)
                    if op_id[1] not in input_dict.keys():
                        input_dict[op_id[1]] = 0
                    input_dict[op_id[1]] += 2**op_id[0]
                for id in input_dict.keys():
                    file = file_dir + file_name + str(key[0]) + '_' + str(key[1]) + '_' + str(input_port)
                    with open(file, 'a') as f:
                        f.write(str(self.dec2bin(input_dict[id], bit_wide=5))+str(self.dec2bin(id, bit_wide=10))+"\n")
                        f.flush()
        print("finish generating all cast routing tables")

    def __get_ubm_info(self,x,y):
        local = "1" if f"{x}_{y}_cl_i"  in self.ubm_nodes else "0"
        west  = "1" if f"{x}_{y}_cw_i"  in self.ubm_nodes else "0"
        east  = "1" if f"{x}_{y}_ce_i"  in self.ubm_nodes else "0"
        vert0 = "1" if f"{x}_{y}_cv0_i" in self.ubm_nodes else "0"
        vert1 = "1" if f"{x}_{y}_cv1_i" in self.ubm_nodes else "0"
        return local,west,east,vert0,vert1

    def Generate_Cast_Config_Info(self):
        '''
        Only support E2E-FC at local port, not at other ports
        '''
        file_name = self.root_dir + "cast_network_config.svh"
        containt = ""
        for x in range(self.w):
            for y in range(self.h):
                local,west,east,vert0,vert1 = self.__get_ubm_info(x,y)
                containt += "localparam isUBM_list_"+str(x)+"_"+str(y)+"[`CN] = '{"+local+","+west+","+east+","+vert0+","+vert1+"};\n"

        for x in range(self.w):
            for y in range(self.h):
                m = 1 if (x + y * self.w) in self.e2e_dict.keys() else 0 # is e2e source node or not 
                containt += "localparam isFC_list_"+str(x)+"_"+str(y)+"[`CN] = '{"+str(m)+",0,0,0,0};\n"

        bits = str(self.w*self.h)+"'b0"
        for x in range(self.w):
            for y in range(self.h):
                k = x + y * self.w
                data = 0
                if k in self.e2e_dict.keys():
                    for i in self.e2e_dict[k]:
                        data += 2**i
                    data = Configurator.dec2bin(data,bit_wide=self.w*self.h)
                containt += "localparam [`NOC_WIDTH*`NOC_HEIGHT-1:0] FCdn_list_"+str(x)+"_"+str(y)+"[`CN] = '{"+str(self.w*self.h)+"'b"+str(data)+","+bits+","+bits+","+bits+","+bits+"};\n"

        for x in range(self.w):
            for y in range(self.h):
                m = "`PKT_LEN" if (x + y * self.w) in self.e2e_dict.keys() else "0" # is e2e source node or not 
                containt += "localparam int FCpl_list_"+str(x)+"_"+str(y)+"[`CN] = '{"+m+",0,0,0,0};\n"

        for x in range(self.w):
            for y in range(self.h):
                containt += '''localparam string rt_file_list_'''+str(x)+"_"+str(y)+'''[`CN] = '{"'''+self.root_dir+'''config/cast_rt_'''+str(x)+"_"+str(y)+'''_0","'''+self.root_dir+'''config/cast_rt_'''+str(x)+"_"+str(y)+'''_1","'''+self.root_dir+'''config/cast_rt_'''+str(x)+"_"+str(y)+'''_2","'''+self.root_dir+'''config/cast_rt_'''+str(x)+"_"+str(y)+'''_3","'''+self.root_dir+'''config/cast_rt_'''+str(x)+"_"+str(y)+'''_4"};\n'''

        with open(file_name,"w") as my_file:
            my_file.write("{0}\n".format(containt))
            my_file.flush()
            my_file.close()
        
        print("cast config info has been written into:",file_name)

    def Generate_Merge_Network(self):
        
        file_name = self.root_dir + "merge_network.sv"

        def gen_ports(w,h):
            port_str = '''
//Merge Network
//Width: '''+str(w)+'''
//Height:'''+str(h)+'''
`include "params.svh"
`include "merge_network_config.svh"

module merge_network(
    input       wire                            clk,
    input       wire                            rstn,
    '''

            port_str += '''
    //router local ports
    input       wire        [`DW-1:0]           data_i[`NOC_WIDTH][`NOC_HEIGHT],
    input       wire                            valid_i[`NOC_WIDTH][`NOC_HEIGHT],
    output      reg                             ready_o[`NOC_WIDTH][`NOC_HEIGHT],

    output      reg         [`DW-1:0]           data_o[`NOC_WIDTH][`NOC_HEIGHT],
    output      reg                             valid_o[`NOC_WIDTH][`NOC_HEIGHT],
    input       wire                            ready_i[`NOC_WIDTH][`NOC_HEIGHT]
);'''
            return port_str

        def gen_instances(data_width,w,h):
            data_width = str(data_width)
            inst_str = ""
            for j in range(w): 
                for i in range(h): 
                    id = w*i+j
                    sigs = ''

                    '''
                    generate north port signals
                    '''
                    if i == 0: #north boundary
                        north_data_in = ''
                        north_valid_in = ''
                        north_ready_in = ''
                    else:
                        north_data_in = '    data_i_'+str(j)+'_'+str(i)+'[3] = data_o_'+str(j)+'_'+str(i-1)+'[4];\n'
                        north_valid_in = '    valid_i_'+str(j)+'_'+str(i)+'[3] = valid_o_'+str(j)+'_'+str(i-1)+'[4];\n'
                        north_ready_in = '    ready_i_'+str(j)+'_'+str(i)+'[3] = ready_o_'+str(j)+'_'+str(i-1)+'[4];\n'
                    sigs += north_data_in + north_valid_in + north_ready_in 

                    '''
                    generate south port signals
                    '''
                    if i == h-1: #south boundary
                        south_data_in = ''
                        south_valid_in = ''
                        south_ready_in = ''
                    else:
                        south_data_in = '    data_i_'+str(j)+'_'+str(i)+'[4] = data_o_'+str(j)+'_'+str(i+1)+'[3];\n'
                        south_valid_in = '    valid_i_'+str(j)+'_'+str(i)+'[4] = valid_o_'+str(j)+'_'+str(i+1)+'[3];\n'
                        south_ready_in = '    ready_i_'+str(j)+'_'+str(i)+'[4] = ready_o_'+str(j)+'_'+str(i+1)+'[3];\n'
                    sigs += south_data_in + south_valid_in + south_ready_in

                    '''
                    generate west port signals
                    '''
                    if j == 0: #west boundary
                        west_data_in = ''
                        west_valid_in = ''
                        west_ready_in = ''
                    else:
                        west_data_in = '    data_i_'+str(j)+'_'+str(i)+'[1] = data_o_'+str(j-1)+'_'+str(i)+'[2];\n'
                        west_valid_in = '    valid_i_'+str(j)+'_'+str(i)+'[1] = valid_o_'+str(j-1)+'_'+str(i)+'[2];\n'
                        west_ready_in = '    ready_i_'+str(j)+'_'+str(i)+'[1] = ready_o_'+str(j-1)+'_'+str(i)+'[2];\n'
                    sigs += west_data_in + west_valid_in + west_ready_in

                    '''
                    generate east port signals
                    '''
                    if j == w-1: #east boundary
                        east_data_in = ''
                        east_valid_in = ''
                        east_ready_in = ''
                    else:
                        east_data_in = '    data_i_'+str(j)+'_'+str(i)+'[2] = data_o_'+str(j+1)+'_'+str(i)+'[1];\n'
                        east_valid_in = '    valid_i_'+str(j)+'_'+str(i)+'[2] = valid_o_'+str(j+1)+'_'+str(i)+'[1];\n'
                        east_ready_in = '    ready_i_'+str(j)+'_'+str(i)+'[2] = ready_o_'+str(j+1)+'_'+str(i)+'[1];\n'
                    sigs += east_data_in + east_valid_in + east_ready_in

                    '''
                    generate local port signals
                    '''
                    local_data_in = '    data_i_'+str(j)+'_'+str(i)+'[0] = data_i['+str(j)+']['+str(i)+'];\n'
                    local_valid_in = '    valid_i_'+str(j)+'_'+str(i)+'[0] = valid_i['+str(j)+']['+str(i)+'];\n'
                    local_ready_in = '    ready_i_'+str(j)+'_'+str(i)+'[0] = ready_i['+str(j)+']['+str(i)+'];\n'
                    sigs += local_data_in + local_valid_in + local_ready_in

                    router_txt = '''
/*Router '''+str(j)+''','''+str(i)+'''*/    
merge_router #(
    .input_mask                     (input_mask_'''+str(j)+'''_'''+str(i)+'''),
    .output_sel                     (output_sel_'''+str(j)+'''_'''+str(i)+''')
)router'''+str(id)+'''(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_'''+str(j)+'''_'''+str(i)+'''),
    .valid_i                        (valid_i_'''+str(j)+'''_'''+str(i)+'''),
    .ready_o                        (ready_o_'''+str(j)+'''_'''+str(i)+'''),
    .data_o                         (data_o_'''+str(j)+'''_'''+str(i)+'''),
    .valid_o                        (valid_o_'''+str(j)+'''_'''+str(i)+'''),
    .ready_i                        (ready_i_'''+str(j)+'''_'''+str(i)+''')
);\n'''     
                    router_txt += '''
\nalways@(*) begin
        '''+sigs+'''end\n\n'''
                    inst_str += router_txt
            return inst_str

        def gen_wires(w,h):
            wires_str = ''
            for j in range(w):
                for i in range(h):
                    wires_str += '''
reg [`DW-1:0] data_i_'''+str(j)+'''_'''+str(i)+'''[5];
reg valid_i_'''+str(j)+'''_'''+str(i)+'''[5], ready_i_'''+str(j)+'''_'''+str(i)+'''[5];    
wire [`DW-1:0] data_o_'''+str(j)+'''_'''+str(i)+'''[5];
wire valid_o_'''+str(j)+'''_'''+str(i)+'''[5], ready_o_'''+str(j)+'''_'''+str(i)+'''[5];        
'''
            return wires_str

        def gen_outputs(w,h):
            out_str = "\nalways@(*) begin\n"
            for i in range(w):
                for j in range(h):
                    out_str += "    data_o["+str(i)+"]["+str(j)+"] = data_o_"+str(i)+"_"+str(j)+"[0];\n"
                    out_str += "    valid_o["+str(i)+"]["+str(j)+"] = valid_o_"+str(i)+"_"+str(j)+"[0];\n"
                    out_str += "    ready_o["+str(i)+"]["+str(j)+"] = ready_o_"+str(i)+"_"+str(j)+"[0];\n"
            out_str += "end\n"
            return out_str

        containt = ""
        containt += gen_ports(self.w,self.h)
        containt += gen_wires(self.w,self.h)
        containt += gen_outputs(self.w,self.h)
        containt += gen_instances(self.data_width,self.w,self.h)
        containt += "\nendmodule"

        with open(file_name,"w") as my_file:
            my_file.write("{0}\n".format(containt))
            my_file.flush()
            my_file.close()

        print("merge network has been written into:",file_name)

    def Generate_Merge_Config_Info(self):
        file_name = self.root_dir + "merge_network_config.svh"
        MG = nx.MultiDiGraph()

        for x in range(self.w):
            for y in range(self.h):
                MG.add_node((x,y))

        MG.add_edges_from(self.merge_paths)

        nodes = list(MG.nodes())
        input_mask = []
        output_sel = []

        for node in nodes:
            x = node[0]
            y = node[1]
            neighbor_node = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
            cur_input_mask = 0
            for i,pre_node in enumerate(neighbor_node):
                if (pre_node,node) in MG.in_edges(node):
                    cur_input_mask += 2**(i+1)

            cur_output_sel = 0
            if MG.out_degree(node) == 0: # is merge node
                cur_output_sel = 1
            else: # not merge node
                cur_input_mask += 1
                for j,post_node in enumerate(neighbor_node):
                    if (node,post_node) in MG.out_edges(node):
                        cur_output_sel = 2**(j+1)
                        break

            input_mask.append(self.dec2bin(cur_input_mask,bit_wide=5))
            output_sel.append(self.dec2bin(cur_output_sel,bit_wide=5))

        containt = ""
        for i in range(len(nodes)):
            x = nodes[i][0]
            y = nodes[i][1]
            containt += "localparam input_mask_"+str(x)+"_"+str(y)+" = 5'b"+str(input_mask[i])+";\n"
            containt += "localparam output_sel_"+str(x)+"_"+str(y)+" = 5'b"+str(output_sel[i])+";\n"

        with open(file_name,"w") as my_file:
            my_file.write("{0}\n".format(containt))
            my_file.flush()
            my_file.close()

        print("merge config info has been written into:",file_name)
    
    def Generate_System(self):
        file_name = self.root_dir + "system.sv"
        containt = ""
        containt += '''
`include "params.svh"
`include "system_config.svh"

module system (
    input       wire                            clk,
    input       wire                            rstn,

    input       wire        [`DW-1:0]           data_i_stab,
    input       wire                            valid_i_stab,
    output      wire                            ready_o_stab,

    output      wire        [`DW-1:0]           data_o_flee0,
    output      wire                            valid_o_flee0,
    input       wire                            ready_i_flee0,

    output      wire        [`DW-1:0]           data_o_flee1,
    output      wire                            valid_o_flee1,
    input       wire                            ready_i_flee1  
);

wire [`DW-1:0] cast_data_o[`NOC_WIDTH][`NOC_HEIGHT];
wire cast_valid_o[`NOC_WIDTH][`NOC_HEIGHT],cast_ready_o[`NOC_WIDTH][`NOC_HEIGHT];

wire [`DW-1:0] pe_cast_data_o[`NOC_WIDTH][`NOC_HEIGHT];
wire pe_cast_valid_o[`NOC_WIDTH][`NOC_HEIGHT],pe_cast_ready_o[`NOC_WIDTH][`NOC_HEIGHT];

wire credit_upd[`NOC_WIDTH][`NOC_HEIGHT];

cast_network cast_nw(
    .clk                                               (clk),
    .rstn                                              (rstn),
    .data_i                                            (pe_cast_data_o),
    .valid_i                                           (pe_cast_valid_o),
    .ready_o                                           (cast_ready_o),
    .data_o                                            (cast_data_o),
    .valid_o                                           (cast_valid_o),
    .ready_i                                           (pe_cast_ready_o),
    .data_i_stab                                       (data_i_stab),
    .valid_i_stab                                      (valid_i_stab),
    .ready_o_stab                                      (ready_o_stab),
    .data_o_flee0                                      (data_o_flee0),
    .valid_o_flee0                                     (valid_o_flee0),
    .ready_i_flee0                                     (ready_i_flee0),
    .data_o_flee1                                      (data_o_flee1),
    .valid_o_flee1                                     (valid_o_flee1),
    .ready_i_flee1                                     (ready_i_flee1),
    .credit_upd                                        (credit_upd)
);

wire [`DW-1:0] merge_data_o[`NOC_WIDTH][`NOC_HEIGHT];
wire merge_valid_o[`NOC_WIDTH][`NOC_HEIGHT],merge_ready_o[`NOC_WIDTH][`NOC_HEIGHT];

wire [`DW-1:0] pe_merge_data_o[`NOC_WIDTH][`NOC_HEIGHT];
wire pe_merge_valid_o[`NOC_WIDTH][`NOC_HEIGHT],pe_merge_ready_o[`NOC_WIDTH][`NOC_HEIGHT];

merge_network merge_nw(
    .clk                                            (clk),
    .rstn                                           (rstn),
    .data_i                                         (pe_merge_data_o),
    .valid_i                                        (pe_merge_valid_o),
    .ready_o                                        (merge_ready_o),
    .data_o                                         (merge_data_o),
    .valid_o                                        (merge_valid_o),
    .ready_i                                        (pe_merge_ready_o)
);\n\n'''

        for i in range(self.w):
            for j in range(self.h):
                containt += '''
virtual_pe #(
    .isCaster                    (isCaster_'''+str(i)+'''_'''+str(j)+'''),
    .isPooler                    (isPooler_'''+str(i)+'''_'''+str(j)+'''),
    .stream_id                   (stream_id_'''+str(i)+'''_'''+str(j)+''')
)pe_'''+str(i)+'''_'''+str(j)+'''(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o['''+str(i)+''']['''+str(j)+''']),
    .data_i_cast                 (cast_data_o['''+str(i)+''']['''+str(j)+''']),
    .ready_o_cast                (pe_cast_ready_o['''+str(i)+''']['''+str(j)+''']),
    .valid_o_cast                (pe_cast_valid_o['''+str(i)+''']['''+str(j)+''']),
    .data_o_cast                 (pe_cast_data_o['''+str(i)+''']['''+str(j)+''']),
    .ready_i_cast                (cast_ready_o['''+str(i)+''']['''+str(j)+''']),
    .valid_i_merge               (merge_valid_o['''+str(i)+''']['''+str(j)+''']),
    .data_i_merge                (merge_data_o['''+str(i)+''']['''+str(j)+''']),
    .ready_o_merge               (pe_merge_ready_o['''+str(i)+''']['''+str(j)+''']),
    .valid_o_merge               (pe_merge_valid_o['''+str(i)+''']['''+str(j)+''']),
    .data_o_merge                (pe_merge_data_o['''+str(i)+''']['''+str(j)+''']),
    .ready_i_merge               (merge_ready_o['''+str(i)+''']['''+str(j)+''']),
    .credit_upd                  (credit_upd['''+str(i)+''']['''+str(j)+'''])
);\n\n'''
        containt += "endmodule"

        with open(file_name,"w") as my_file:
            my_file.write("{0}\n".format(containt))
            my_file.flush()
            my_file.close()

        print("system has been written into:",file_name)

    def Generate_System_Config_Info(self):
        file_name = self.root_dir + "system_config.svh"
        isPooler = []
        isCaster = []
        stream_id = []
        keys = list(self.cast_paths.keys())

        for k in keys:
            v = self.cast_paths[k]
            flag = False
            for path in v:
                if path[0] == 0: 
                    flag = True
                    tmp = path[2]
                    break
            if flag:
                isCaster.append(1)
                stream_id.append(tmp)
            else:
                isCaster.append(0)
                stream_id.append(0)
            flag = False
            for i in self.pool_layers:
                if k[0] + k[1] * self.w in self.merge_nodes[i]: # is pool
                    flag = True
                    break
            if flag:
                isPooler.append(1)
            else:
                isPooler.append(0)
        containt = ""
        for i in range(len(keys)):
            containt += f"localparam isPooler_{keys[i][0]}_{keys[i][1]} = {isPooler[i]};\n"
            containt += f"localparam isCaster_{keys[i][0]}_{keys[i][1]} = {isCaster[i]};\n"
            containt += f"localparam stream_id_{keys[i][0]}_{keys[i][1]} = {stream_id[i]};\n"

        with open(file_name,"w") as my_file:
            my_file.write("{0}\n".format(containt))
            my_file.flush()
            my_file.close()

        print("system config info has been written into:",file_name)

    def Generate_System_Header(self):
        file_name = self.root_dir + "params.svh"
        containt = f'''
`ifndef         __PARAMS_SVH__
`define         __PARAMS_SVH__

`define         DW                              16 //data width
`define         CN                              5 //channel number 0:local 1:west 2:east 3:verti0 4:verti1
`define         NOC_WIDTH                       {self.w}
`define         NOC_HEIGHT                      {self.h}

`define         BUFFER_ALLOC                    256
`define         BUFFER_ALLOC_LOG                8

`define         ROUTE_TABLE_DEPTH               16
`define         CAST_ROUTER_BUFFER_DEPTH_LOG    4

`define         PKT_LEN                         16
`define         PKT_LEN_LOG                     4

`define         NUM_POOL_LAYER                  {len(self.pool_layers)}

//packet contents begin

`define         STREAM_ID_H                     9
`define         STREAM_ID_L                     0

`define         PKT_LEN_H                       `STREAM_ID_H+8
`define         PKT_LEN_L                       `STREAM_ID_H+1

//packet contents end

`define         HEAD                            2'b00
`define         BODY                            2'b01
`define         TAIL                            2'b11

`endif'''
        with open(file_name,"w") as my_file:
            my_file.write("{0}\n".format(containt))
            my_file.flush()
            my_file.close()

        print("system header has been written into:",file_name)

    def Run_Configuring(self):
        self.Generate_Cast_Network()
        self.Generate_Cast_Routing_table()
        self.Generate_Cast_Config_Info()
        self.Generate_Merge_Network()
        self.Generate_Merge_Config_Info()
        self.Generate_System()
        self.Generate_System_Config_Info()
        self.Generate_System_Header()