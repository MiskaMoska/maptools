import os

__all__ = ['gen_system']

def gen_system(root_dir, w, h, flees):
    save_dir = os.path.join(root_dir, 'network', 'test')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_dir = os.path.join(save_dir, 'system.sv')
    containt = ""
    containt += '''`include "params.svh"
`include "network_config.svh"

module system (
    input       wire                            clk,
    input       wire                            rstn,

    input       wire        [`DW-1:0]           data_i_stab,
    input       wire                            valid_i_stab,
    output      wire                            ready_o_stab,
'''
    for idx in range(len(flees[0])):
        containt += f'''
    output      wire        [`DW-1:0]           data_o_flee{idx},
    output      wire                            valid_o_flee{idx},
    input       wire                            ready_i_flee{idx},'''
    containt = containt.rstrip(',') + '\n);\n'
    containt += '''
wire [`DW-1:0] cast_gather_data_pe_2_nw[`NOC_WIDTH][`NOC_HEIGHT], merge_data_pe_2_nw[`NOC_WIDTH][`NOC_HEIGHT], cast_data_nw_2_pe[`NOC_WIDTH][`NOC_HEIGHT], merge_data_nw_2_pe[`NOC_WIDTH][`NOC_HEIGHT], gather_data_nw_2_pe[`NOC_WIDTH][`NOC_HEIGHT];
wire  cast_gather_valid_pe_2_nw[`NOC_WIDTH][`NOC_HEIGHT], merge_valid_pe_2_nw[`NOC_WIDTH][`NOC_HEIGHT], cast_valid_nw_2_pe[`NOC_WIDTH][`NOC_HEIGHT], merge_valid_nw_2_pe[`NOC_WIDTH][`NOC_HEIGHT], gather_valid_nw_2_pe[`NOC_WIDTH][`NOC_HEIGHT];
wire  cast_ready_pe_2_nw[`NOC_WIDTH][`NOC_HEIGHT], merge_ready_pe_2_nw[`NOC_WIDTH][`NOC_HEIGHT], gather_ready_pe_2_nw[`NOC_WIDTH][`NOC_HEIGHT], merge_ready_nw_2_pe[`NOC_WIDTH][`NOC_HEIGHT], cast_gather_ready_nw_2_pe[`NOC_WIDTH][`NOC_HEIGHT];

wire [31:0] cast_credit_upd[`NOC_WIDTH][`NOC_HEIGHT];
wire [31:0] gather_credit_upd[`NOC_WIDTH][`NOC_HEIGHT];

network nw(
    .clk                                               (clk),
    .rstn                                              (rstn),
    .data_i_stab                                       (data_i_stab),
    .valid_i_stab                                      (valid_i_stab),
    .ready_o_stab                                      (ready_o_stab),'''

    for i in range(len(flees[0])):
        containt += f'''
    .data_o_flee{i}                                      (data_o_flee{i}),
    .valid_o_flee{i}                                     (valid_o_flee{i}),
    .ready_i_flee{i}                                     (ready_i_flee{i}),'''

    for i in range(w):
        for j in range(h): 
            containt += f'''
    .cast_gather_data_i_{i}_{j}                        (cast_gather_data_pe_2_nw[{i}][{j}]),
    .cast_gather_valid_i_{i}_{j}                       (cast_gather_valid_pe_2_nw[{i}][{j}]),
    .cast_gather_ready_o_{i}_{j}                       (cast_gather_ready_nw_2_pe[{i}][{j}]),
    .merge_data_i_{i}_{j}                              (merge_data_pe_2_nw[{i}][{j}]),
    .merge_valid_i_{i}_{j}                             (merge_valid_pe_2_nw[{i}][{j}]),
    .merge_ready_o_{i}_{j}                             (merge_ready_nw_2_pe[{i}][{j}]),

    .cast_data_o_{i}_{j}                               (cast_data_nw_2_pe[{i}][{j}]),
    .cast_valid_o_{i}_{j}                              (cast_valid_nw_2_pe[{i}][{j}]),
    .cast_ready_i_{i}_{j}                              (cast_ready_pe_2_nw[{i}][{j}]),
    .merge_data_o_{i}_{j}                              (merge_data_nw_2_pe[{i}][{j}]),
    .merge_valid_o_{i}_{j}                             (merge_valid_nw_2_pe[{i}][{j}]),
    .merge_ready_i_{i}_{j}                             (merge_ready_pe_2_nw[{i}][{j}]),
    .gather_data_o_{i}_{j}                             (gather_data_nw_2_pe[{i}][{j}]),
    .gather_valid_o_{i}_{j}                            (gather_valid_nw_2_pe[{i}][{j}]),
    .gather_ready_i_{i}_{j}                            (gather_ready_pe_2_nw[{i}][{j}]),'''

    containt += '''
    .cast_credit_upd                                   (cast_credit_upd),
    .gather_credit_upd                                 (gather_credit_upd)
    '''
    containt += '\n);\n'

    for i in range(w):
        for j in range(h):
            containt += f'''
virtual_pe #(
    .cast_out                                          (cast_out_{i}_{j}),
    .merge_in                                          (merge_in_{i}_{j}),
    .merge_out                                         (merge_out_{i}_{j}),
    .gather_in                                         (gather_in_{i}_{j}),
    .gather_out                                        (gather_out_{i}_{j}),
    .x                                                 ({i}),
    .y                                                 ({j})
)vpe_{i}_{j}(
    .clk                                               (clk),
    .rstn                                              (rstn),
    .cast_data_i                                       (cast_data_nw_2_pe[{i}][{j}]),
    .cast_valid_i                                      (cast_valid_nw_2_pe[{i}][{j}]),
    .cast_ready_o                                      (cast_ready_pe_2_nw[{i}][{j}]),
    .cast_gather_data_o                                (cast_gather_data_pe_2_nw[{i}][{j}]),
    .cast_gather_valid_o                               (cast_gather_valid_pe_2_nw[{i}][{j}]),
    .cast_gather_ready_i                               (cast_gather_ready_nw_2_pe[{i}][{j}]),
    .merge_data_i                                      (merge_data_nw_2_pe[{i}][{j}]),
    .merge_valid_i                                     (merge_valid_nw_2_pe[{i}][{j}]),
    .merge_ready_o                                     (merge_ready_pe_2_nw[{i}][{j}]),
    .merge_data_o                                      (merge_data_pe_2_nw[{i}][{j}]),
    .merge_valid_o                                     (merge_valid_pe_2_nw[{i}][{j}]),
    .merge_ready_i                                     (merge_ready_nw_2_pe[{i}][{j}]),
    .gather_data_i                                     (gather_data_nw_2_pe[{i}][{j}]),
    .gather_valid_i                                    (gather_valid_nw_2_pe[{i}][{j}]),
    .gather_ready_o                                    (gather_ready_pe_2_nw[{i}][{j}]),
    .cast_credit_upd                                   (cast_credit_upd[{i}][{j}]),
    .gather_credit_upd                                 (gather_credit_upd[{i}][{j}])
);\n\n'''
    containt += "endmodule"
    with open(file_dir,"w") as my_file:
        my_file.write("{0}\n".format(containt))
        my_file.flush()
        my_file.close()
    
    print(f"test system has been written to: {file_dir}")