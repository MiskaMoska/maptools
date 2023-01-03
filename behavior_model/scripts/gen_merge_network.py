'''
Generate cast network system verilog file
'''
DATA_WIDTH = 16
NETWORK_WIDTH = 3
NETWORK_HEIGHT = 3

file_name = "/mnt/c/git/NVCIM-COMM/behavior_model/srcs/merge_network.sv"

def gen_ports(w,h):
    port_str = '''//Merge Network
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
    output      wire                            ready_o[`NOC_WIDTH][`NOC_HEIGHT],

    output      wire        [`DW-1:0]           data_o[`NOC_WIDTH][`NOC_HEIGHT],
    output      wire                            valid_o[`NOC_WIDTH][`NOC_HEIGHT],
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
                north_data_in = '    data_i_'+str(j)+'_'+str(i)+'[3] = data_o_'+str(j)+'_'+str(i+1)+'[4];\n'
                north_valid_in = '    valid_i_'+str(j)+'_'+str(i)+'[3] = valid_o_'+str(j)+'_'+str(i+1)+'[4];\n'
                north_ready_in = '    ready_i_'+str(j)+'_'+str(i)+'[3] = ready_o_'+str(j)+'_'+str(i+1)+'[4];\n'
            sigs += north_data_in + north_valid_in + north_ready_in 

            '''
            generate south port signals
            '''
            if i == 0: #south boundary
                south_data_in = ''
                south_valid_in = ''
                south_ready_in = ''
            else:
                south_data_in = '    data_i_'+str(j)+'_'+str(i)+'[4] = data_o_'+str(j)+'_'+str(i-1)+'[3];\n'
                south_valid_in = '    valid_i_'+str(j)+'_'+str(i)+'[4] = valid_o_'+str(j)+'_'+str(i-1)+'[3];\n'
                south_ready_in = '    ready_i_'+str(j)+'_'+str(i)+'[4] = ready_o_'+str(j)+'_'+str(i-1)+'[3];\n'
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
            local_data_in = '    data_i_'+str(j)+'_'+str(i)+'[0] = data_o_['+str(j)+']['+str(i)+'];\n'
            local_valid_in = '    valid_i_'+str(j)+'_'+str(i)+'[0] = valid_o_['+str(j)+']['+str(i)+'];\n'
            local_ready_in = '    ready_i_'+str(j)+'_'+str(i)+'[0] = ready_o_['+str(j)+']['+str(i)+'];\n'
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


def gen_verilog_file():
    containt = ""
    containt += gen_ports(NETWORK_WIDTH,NETWORK_HEIGHT)
    containt += gen_wires(NETWORK_WIDTH,NETWORK_HEIGHT)
    containt += gen_instances(DATA_WIDTH,NETWORK_WIDTH,NETWORK_HEIGHT)
    containt += "\nendmodule"

    with open(file_name,"w") as my_file:
        my_file.write("{0}\n".format(containt))
        my_file.flush()
        my_file.close()

    print("Text has been written into:",file_name)



if __name__ == "__main__":
    gen_verilog_file()