import os

__all__ = ['gen_top_network']

def gen_top_network(root_dir, w, h, flees):
    containt = ""
    containt += '''`include "params.svh"
`include "network_config.svh"

module network(
    input       wire                        clk,
    input       wire                        rstn,

    //stab port
    input       wire        [`DW-1:0]       data_i_stab,
    input       wire                        valid_i_stab,
    output      wire                        ready_o_stab,
'''
    for i in range(len(flees[0])):
        containt +=f'''
    //flee{i} port
    output      wire        [`DW-1:0]       data_o_flee{i},
    output      wire                        valid_o_flee{i},
    input       wire                        ready_i_flee{i},
'''

    for i in range(w):
        for j in range(h):
            containt += f'''
    input       wire        [`DW-1:0]       cast_data_i_{i}_{j},
    input       wire                        cast_valid_i_{i}_{j},
    output      wire                        cast_ready_o_{i}_{j},

    output      wire        [`DW-1:0]       cast_data_o_{i}_{j},
    output      wire                        cast_valid_o_{i}_{j},
    input       wire                        cast_ready_i_{i}_{j},
'''
    for i in range(w):
        for j in range(h):
            containt += f'''
    input       wire        [`DW-1:0]       merge_data_i_{i}_{j},
    input       wire                        merge_valid_i_{i}_{j},
    output      wire                        merge_ready_o_{i}_{j},

    output      wire        [`DW-1:0]       merge_data_o_{i}_{j},
    output      wire                        merge_valid_o_{i}_{j},
    input       wire                        merge_ready_i_{i}_{j},'''

    for i in range(w):
        for j in range(h):
            containt += f'''
    input       wire        [`DW-1:0]       gather_data_i_{i}_{j},
    input       wire                        gather_valid_i_{i}_{j},
    output      wire                        gather_ready_o_{i}_{j},

    output      wire        [`DW-1:0]       gather_data_o_{i}_{j},
    output      wire                        gather_valid_o_{i}_{j},
    input       wire                        gather_ready_i_{i}_{j},'''

    containt = containt.rstrip(',')
    containt += '\n);'
    containt += '''
wire [`DW-1:0] data_stab;
wire valid_stab, ready_stab;
''' 
    for i in range(len(flees[0])):
        containt += f'''
wire [`DW-1:0] data_flee{i};
wire valid_flee{i}, ready_flee{i};
'''

    containt += '''
wire [`DW-1:0] data_i_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], data_o_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], data_i_merge_nw[`NOC_WIDTH][`NOC_HEIGHT], data_o_merge_nw[`NOC_WIDTH][`NOC_HEIGHT], data_i_gather_nw[`NOC_WIDTH][`NOC_HEIGHT], data_o_gather_nw[`NOC_WIDTH][`NOC_HEIGHT];
wire valid_i_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], valid_o_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], valid_i_merge_nw[`NOC_WIDTH][`NOC_HEIGHT], valid_o_merge_nw[`NOC_WIDTH][`NOC_HEIGHT], valid_i_gather_nw[`NOC_WIDTH][`NOC_HEIGHT], valid_o_gather_nw[`NOC_WIDTH][`NOC_HEIGHT];
wire ready_i_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], ready_o_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], ready_i_merge_nw[`NOC_WIDTH][`NOC_HEIGHT], ready_o_merge_nw[`NOC_WIDTH][`NOC_HEIGHT], ready_i_gather_nw[`NOC_WIDTH][`NOC_HEIGHT], ready_o_gather_nw[`NOC_WIDTH][`NOC_HEIGHT];

wire credit_upd[`NOC_WIDTH][`NOC_HEIGHT];
'''

    containt += '''
// from stab port to network
converter #(
    .out                            (1),
    .sid                            (1023)
)converter_stab(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_pe                     (valid_i_stab),
    .data_i_pe                      (data_i_stab),
    .ready_o_pe                     (ready_o_stab),
    .valid_o_pe                     (),
    .data_o_pe                      (),
    .ready_i_pe                     (1'b0),
    .valid_i_nw                     (1'b0),
    .data_i_nw                      ({(`DW){1'b0}}),
    .ready_o_nw                     (),
    .valid_o_nw                     (valid_stab),
    .data_o_nw                      (data_stab),
    .ready_i_nw                     (ready_stab)
);
'''
    for i in range(len(flees[0])):
        containt += f'''
// from flee{i} port to outside
converter #(
    .out                            (0),
    .sid                            (1022)
)converter_flee{i}(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_pe                     (1'b0),'''+'''
    .data_i_pe                      ({(`DW){1'b0}}),'''+f'''
    .ready_o_pe                     (),
    .valid_o_pe                     (valid_o_flee{i}),
    .data_o_pe                      (data_o_flee{i}),
    .ready_i_pe                     (ready_i_flee{i}),
    .valid_i_nw                     (valid_flee{i}),
    .data_i_nw                      (data_flee{i}),
    .ready_o_nw                     (ready_flee{i}),
    .valid_o_nw                     (),
    .data_o_nw                      (),
    .ready_i_nw                     (1'b0)
);
'''
    containt += '''
cast_network cast_nw(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_cast_nw),
    .valid_i                        (valid_i_cast_nw),
    .ready_o                        (ready_o_cast_nw),
    .data_o                         (data_o_cast_nw),
    .valid_o                        (valid_o_cast_nw),
    .ready_i                        (ready_i_cast_nw),
    .data_i_stab                    (data_stab),
    .valid_i_stab                   (valid_stab),
    .ready_o_stab                   (ready_stab),
    .data_o_flee0                   (data_flee0),
    .valid_o_flee0                  (valid_flee0),
    .ready_i_flee0                  (ready_flee0),
    .data_o_flee1                   (data_flee1),
    .valid_o_flee1                  (valid_flee1),
    .ready_i_flee1                  (ready_flee1),
    .credit_upd                     (credit_upd)
);                 

merge_network merge_nw(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_merge_nw),
    .valid_i                        (valid_i_merge_nw),
    .ready_o                        (ready_o_merge_nw),
    .data_o                         (data_o_merge_nw),
    .valid_o                        (valid_o_merge_nw),
    .ready_i                        (ready_i_merge_nw)
);

gather_network merge_nw(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_gather_nw),
    .valid_i                        (valid_i_gather_nw),
    .ready_o                        (ready_o_gather_nw),
    .data_o                         (data_o_gather_nw),
    .valid_o                        (valid_o_gather_nw),
    .ready_i                        (ready_i_gather_nw)
);\n
'''
    for i in range(w):
        for j in range(h):
            containt += f'''
network_interface #(
    .cast_out                       (cast_out_{i}_{j}),
    .gather_out                     (gather_out_{i}_{j}),
    .cast_sid                       (cast_sid_{i}_{j}),
    .gather_sid                     (gather_sid_{i}_{j})
)ni_{i}_{j}(
    .clk                            (clk),
    .rstn                           (rstn),

    .valid_i_cast_nw                (valid_o_cast_nw[{i}][{j}]),
    .data_i_cast_nw                 (data_o_cast_nw[{i}][{j}]),
    .ready_o_cast_nw                (ready_i_cast_nw[{i}][{j}]),
    .valid_o_cast_nw                (valid_i_cast_nw[{i}][{j}]),
    .data_o_cast_nw                 (data_i_cast_nw[{i}][{j}]),
    .ready_i_cast_nw                (ready_o_cast_nw[{i}][{j}]),

    .valid_i_gather_nw              (valid_o_gather_nw[{i}][{j}]),
    .data_i_gather_nw               (data_o_gather_nw[{i}][{j}]),
    .ready_o_gather_nw              (ready_i_gather_nw[{i}][{j}]),
    .valid_o_gather_nw              (valid_i_gather_nw[{i}][{j}]),
    .data_o_gather_nw               (data_i_gather_nw[{i}][{j}]),
    .ready_i_gather_nw              (ready_o_gather_nw[{i}][{j}]),
    
    .valid_i_merge_nw               (valid_o_merge_nw[{i}][{j}]),
    .data_i_merge_nw                (data_o_merge_nw[{i}][{j}]),
    .ready_o_merge_nw               (ready_i_merge_nw[{i}][{j}]),
    .valid_o_merge_nw               (valid_i_merge_nw[{i}][{j}]),
    .data_o_merge_nw                (data_i_merge_nw[{i}][{j}]),
    .ready_i_merge_nw               (ready_o_merge_nw[{i}][{j}]),

    .valid_i_cast_pe                (cast_valid_i_{i}_{j}),
    .data_i_cast_pe                 (cast_data_i_{i}_{j}),
    .ready_o_cast_pe                (cast_ready_o_{i}_{j}),
    .valid_o_cast_pe                (cast_valid_o_{i}_{j}),
    .data_o_cast_pe                 (cast_data_o_{i}_{j}),
    .ready_i_cast_pe                (cast_ready_i_{i}_{j}),

    .valid_i_merge_pe               (merge_valid_i_{i}_{j}),
    .data_i_merge_pe                (merge_data_i_{i}_{j}),
    .ready_o_merge_pe               (merge_ready_o_{i}_{j}),
    .valid_o_merge_pe               (merge_valid_o_{i}_{j}),
    .data_o_merge_pe                (merge_data_o_{i}_{j}),
    .ready_i_merge_pe               (merge_ready_i_{i}_{j}),

    .valid_i_gather_pe              (gather_valid_i_{i}_{j}),
    .data_i_gather_pe               (gather_data_i_{i}_{j}),
    .ready_o_gather_pe              (gather_ready_o_{i}_{j}),
    .valid_o_gather_pe              (gather_valid_o_{i}_{j}),
    .data_o_gather_pe               (gather_data_o_{i}_{j}),
    .ready_i_gather_pe              (gather_ready_i_{i}_{j}),

    .credit_upd                     (credit_upd[{i}][{j}])
);\n\n'''
    containt += "endmodule"
    save_dir = os.path.join(root_dir, 'network', 'rtl', 'generated')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_dir = os.path.join(save_dir, 'network.sv')

    with open(file_dir,"w") as my_file:
        my_file.write("{0}\n".format(containt))
        my_file.flush()
        my_file.close()
    
    print(f"top network has been written to: {file_dir}")