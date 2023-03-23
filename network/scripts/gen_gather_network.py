import os

__all__ = ['gen_gather_network']

def gen_ports(w, h):
    port_str = '''
//Gather Network
//Width: '''+str(w)+'''
//Height:'''+str(h)+'''
`include "params.svh"
`include "gather_network_config.svh"

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

    port_str += "\n);\n"
    return port_str

def gen_instances(data_width, w, h):
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
                south_in_data = "data_"+str(id+w)+"_to_"+str(id)
                south_in_valid = "valid_"+str(id+w)+"_to_"+str(id)
                south_in_ready = "ready_"+str(id)+"_to_"+str(id+w)

                south_out_data = "data_"+str(id)+"_to_"+str(id+w)
                south_out_valid = "valid_"+str(id)+"_to_"+str(id+w)
                south_out_ready = "ready_"+str(id+w)+"_to_"+str(id)

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
gather_router #(
    .rt_file_list          (gather_rt_file_list_'''+str(j)+'''_'''+str(i)+''')
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
    .north_data_i          ('''+north_in_data+'''),
    .north_valid_i         ('''+north_in_valid+'''),
    .north_ready_o         ('''+north_in_ready+'''),
    .north_data_o          ('''+north_out_data+'''),
    .north_valid_o         ('''+north_out_valid+'''),
    .north_ready_i         ('''+north_out_ready+'''),
    .south_data_i          ('''+south_in_data+'''),
    .south_valid_i         ('''+south_in_valid+'''),
    .south_ready_o         ('''+south_in_ready+'''),
    .south_data_o          ('''+south_out_data+'''),
    .south_valid_o         ('''+south_out_valid+'''),
    .south_ready_i         ('''+south_out_ready+'''),
    .local_data_i          (data_i['''+str(j)+''']['''+str(i)+''']),
    .local_valid_i         (valid_i['''+str(j)+''']['''+str(i)+''']),
    .local_ready_o         (ready_o['''+str(j)+''']['''+str(i)+''']),
    .local_data_o          (data_o['''+str(j)+''']['''+str(i)+''']),
    .local_valid_o         (valid_o['''+str(j)+''']['''+str(i)+''']),
    .local_ready_i         (ready_i['''+str(j)+''']['''+str(i)+'''])
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
wire    [`DW-1:0]   data_'''+str(i+j*w)+'''_to_'''+str(i+(j+1)*w)+''',\tdata_'''+str(i+(j+1)*w)+'''_to_'''+str(i+j*w)+''';
wire                valid_'''+str(i+j*w)+'''_to_'''+str(i+(j+1)*w)+''',\tvalid_'''+str(i+(j+1)*w)+'''_to_'''+str(i+j*w)+''';
wire                ready_'''+str(i+(j+1)*w)+'''_to_'''+str(i+j*w)+''',\tready_'''+str(i+j*w)+'''_to_'''+str(i+(j+1)*w)+''';'''
            wires_str += temp_txt
    wires_str += "\n"
    return wires_str

def gen_gather_network(root_dir, data_width, w, h):
    save_dir = os.path.join(root_dir, 'network', 'rtl', 'generated')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_dir = os.path.join(save_dir, 'gather_network.sv')
    containt = ""
    containt += gen_ports(w, h)
    containt += gen_wires(w, h)
    containt += gen_instances(data_width, w, h)
    containt += "\nendmodule"

    with open(file_dir,"w") as my_file:
        my_file.write("{0}\n".format(containt))
        my_file.flush()
        my_file.close()
    
    print(f"gather network has been written to: {file_dir}")
