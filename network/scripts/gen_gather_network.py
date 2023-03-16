import os

__all__ = ['gen_gather_network']

def gen_ports(w, h):
    port_str = '''
//Gather Network
//Width: '''+str(w)+'''
//Height:'''+str(h)+'''
`include "params.svh"
`include "gather_config.svh"

module gather_network(
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
input       wire                            ready_i[`NOC_WIDTH][`NOC_HEIGHT]'''

    port_str += ");\n"
    return port_str

def gen_instances(data_width, w, h, flees):
    data_width = str(data_width)
    inst_str = ""
    for j in range(w): 
        for i in range(h): 
            id = w*i+j
            '''
            generate north ports
            '''
            if i == 0: #north boundary
                north_in_data = data_width + "'b0"
                north_in_valid = "1'b0"
                north_in_ready = ""

                north_out_data = ""
                north_out_valid = ""
                north_out_ready = "1'b0"

            else:
                north_in_data = "data_"+str(id-w)+"_to_"+str(id)
                north_in_valid = "valid_"+str(id-w)+"_to_"+str(id)
                north_in_ready = "ready_"+str(id)+"_to_"+str(id-w)

                north_out_data = "data_"+str(id)+"_to_"+str(id-w)
                north_out_valid = "valid_"+str(id)+"_to_"+str(id-w)
                north_out_ready = "ready_"+str(id-w)+"_to_"+str(id)

            '''
            generate south ports
            '''
            if i == h-1: #south boundary
                south_in_data = data_width + "'b0"
                south_in_valid = "1'b0"
                south_in_ready = ""

                south_out_data = ""
                south_out_valid = ""
                south_out_ready = "1'b0"
            else:
                south_in_data = "data_"+str(id+w)+"_to_"+str(id)+"_v0"
                south_in_valid = "valid_"+str(id+w)+"_to_"+str(id)+"_v0"
                south_in_ready = "ready_"+str(id)+"_to_"+str(id+w)+"_v0"

                south_out_data = "data_"+str(id)+"_to_"+str(id+w)+"_v1"
                south_out_valid = "valid_"+str(id)+"_to_"+str(id+w)+"_v1"
                south_out_ready = "ready_"+str(id+w)+"_to_"+str(id)+"_v1"

            '''
            generate west port signals
            '''
            if j == 0: #west boundary
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
    file_name = os.path.join(root_dir, 'network', 'rtl', 'generated', 'cast_network.sv')
    containt = ""
    containt += gen_ports(w, h, flees)
    containt += gen_wires(w, h)
    containt += gen_instances(data_width, w, h, flees)
    containt += "\nendmodule"

    with open(file_name,"w") as my_file:
        my_file.write("{0}\n".format(containt))
        my_file.flush()
        my_file.close()
    
    print(f"cast_network has been written to: {file_name}")

    return containt
