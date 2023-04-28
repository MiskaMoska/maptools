import os

__all__ = ['gen_cast_network']

def is_flee(pos, port, flees):
    if pos in flees[0]:
        idx = flees[0].index(pos)
        if flees[1][idx] == port:
            return True, idx
        return False, None
    return False, None

def gen_ports(w, h, flees):
    port_str = '''
//Cast Network
//Width: '''+str(w)+'''
//Height:'''+str(h)+'''
`include "params.svh"

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
'''
    for idx in range(len(flees[0])):
        port_str += f'''
    output      wire        [`DW-1:0]           data_o_flee{idx},
    output      wire                            valid_o_flee{idx},
    input       wire                            ready_i_flee{idx},
'''
    port_str += '''
    //credit update signal input
    input       wire        [31:0]              credit_upd[`NOC_WIDTH][`NOC_HEIGHT]\n'''
    port_str += "\n);\n\n"
    port_str += '`include "cast_network_config.svh"\n'
    return port_str

def gen_instances(data_width, w, h, flees):
    data_width = str(data_width)
    inst_str = ""
    for j in range(w): 
        for i in range(h): 
            id = w*i+j
            '''
            generate vert0 and vert1 input ports
            '''
            if i == 0: #north boundary
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

            res, idx = is_flee((j, i), 3, flees)
            if res:
                vert0_out_data = f"data_o_flee{idx}"
                vert0_out_valid = f"valid_o_flee{idx}"
                vert0_out_ready = f"ready_i_flee{idx}"

            res, idx = is_flee((j, i), 4, flees)
            if res:
                vert1_out_data = f"data_o_flee{idx}"
                vert1_out_valid = f"valid_o_flee{idx}"
                vert1_out_ready = f"ready_i_flee{idx}"

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

            res, idx = is_flee((j, i), 1, flees)
            if res:
                west_out_data = f"data_o_flee{idx}"
                west_out_valid = f"valid_o_flee{idx}"
                west_out_ready = f"ready_i_flee{idx}"

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

            res, idx = is_flee((j, i), 2, flees)
            if res:
                east_out_data = f"data_o_flee{idx}"
                east_out_valid = f"valid_o_flee{idx}"
                east_out_ready = f"ready_i_flee{idx}"

            router_txt = '''
/*Router '''+str(j)+''','''+str(i)+'''*/    
cast_router #(
    .x_pos                 ('''+str(j)+'''),
    .y_pos                 ('''+str(i)+'''),
    .isUBM_list            (isUBM_list_'''+str(j)+'''_'''+str(i)+'''),
    .isFC_list             (isFC_list_'''+str(j)+'''_'''+str(i)+'''),
    .FCdn_list             (FCdn_list_'''+str(j)+'''_'''+str(i)+'''),
    .FCpl_list             (FCpl_list_'''+str(j)+'''_'''+str(i)+'''),
    .rt_file_list          (cast_rt_file_list_'''+str(j)+'''_'''+str(i)+''')
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

def gen_wires(w, h):
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

def gen_cast_network(root_dir, data_width, w, h, flees):
    save_dir = os.path.join(root_dir, 'network', 'rtl', 'generated')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_dir = os.path.join(save_dir, 'cast_network.sv')
    containt = ""
    containt += gen_ports(w, h, flees)
    containt += gen_wires(w, h)
    containt += gen_instances(data_width, w, h, flees)
    containt += "\nendmodule"

    with open(file_dir,"w") as my_file:
        my_file.write("{0}\n".format(containt))
        my_file.flush()
        my_file.close()
    
    print(f"cast network has been written to: {file_dir}")
