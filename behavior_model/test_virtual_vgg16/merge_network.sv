//Merge Network
//Width: 7
//Height:8
`include "params.svh"
`include "merge_network_config.svh"

module merge_network(
    input       wire                            clk,
    input       wire                            rstn,
    
    //router local ports
    input       wire        [`DW-1:0]           data_i[`NOC_WIDTH][`NOC_HEIGHT],
    input       wire                            valid_i[`NOC_WIDTH][`NOC_HEIGHT],
    output      reg                             ready_o[`NOC_WIDTH][`NOC_HEIGHT],

    output      reg         [`DW-1:0]           data_o[`NOC_WIDTH][`NOC_HEIGHT],
    output      reg                             valid_o[`NOC_WIDTH][`NOC_HEIGHT],
    input       wire                            ready_i[`NOC_WIDTH][`NOC_HEIGHT]
);
reg [`DW-1:0] data_i_0_0[5];
reg valid_i_0_0[5], ready_i_0_0[5];    
wire [`DW-1:0] data_o_0_0[5];
wire valid_o_0_0[5], ready_o_0_0[5];        

reg [`DW-1:0] data_i_0_1[5];
reg valid_i_0_1[5], ready_i_0_1[5];    
wire [`DW-1:0] data_o_0_1[5];
wire valid_o_0_1[5], ready_o_0_1[5];        

reg [`DW-1:0] data_i_0_2[5];
reg valid_i_0_2[5], ready_i_0_2[5];    
wire [`DW-1:0] data_o_0_2[5];
wire valid_o_0_2[5], ready_o_0_2[5];        

reg [`DW-1:0] data_i_0_3[5];
reg valid_i_0_3[5], ready_i_0_3[5];    
wire [`DW-1:0] data_o_0_3[5];
wire valid_o_0_3[5], ready_o_0_3[5];        

reg [`DW-1:0] data_i_0_4[5];
reg valid_i_0_4[5], ready_i_0_4[5];    
wire [`DW-1:0] data_o_0_4[5];
wire valid_o_0_4[5], ready_o_0_4[5];        

reg [`DW-1:0] data_i_0_5[5];
reg valid_i_0_5[5], ready_i_0_5[5];    
wire [`DW-1:0] data_o_0_5[5];
wire valid_o_0_5[5], ready_o_0_5[5];        

reg [`DW-1:0] data_i_0_6[5];
reg valid_i_0_6[5], ready_i_0_6[5];    
wire [`DW-1:0] data_o_0_6[5];
wire valid_o_0_6[5], ready_o_0_6[5];        

reg [`DW-1:0] data_i_0_7[5];
reg valid_i_0_7[5], ready_i_0_7[5];    
wire [`DW-1:0] data_o_0_7[5];
wire valid_o_0_7[5], ready_o_0_7[5];        

reg [`DW-1:0] data_i_1_0[5];
reg valid_i_1_0[5], ready_i_1_0[5];    
wire [`DW-1:0] data_o_1_0[5];
wire valid_o_1_0[5], ready_o_1_0[5];        

reg [`DW-1:0] data_i_1_1[5];
reg valid_i_1_1[5], ready_i_1_1[5];    
wire [`DW-1:0] data_o_1_1[5];
wire valid_o_1_1[5], ready_o_1_1[5];        

reg [`DW-1:0] data_i_1_2[5];
reg valid_i_1_2[5], ready_i_1_2[5];    
wire [`DW-1:0] data_o_1_2[5];
wire valid_o_1_2[5], ready_o_1_2[5];        

reg [`DW-1:0] data_i_1_3[5];
reg valid_i_1_3[5], ready_i_1_3[5];    
wire [`DW-1:0] data_o_1_3[5];
wire valid_o_1_3[5], ready_o_1_3[5];        

reg [`DW-1:0] data_i_1_4[5];
reg valid_i_1_4[5], ready_i_1_4[5];    
wire [`DW-1:0] data_o_1_4[5];
wire valid_o_1_4[5], ready_o_1_4[5];        

reg [`DW-1:0] data_i_1_5[5];
reg valid_i_1_5[5], ready_i_1_5[5];    
wire [`DW-1:0] data_o_1_5[5];
wire valid_o_1_5[5], ready_o_1_5[5];        

reg [`DW-1:0] data_i_1_6[5];
reg valid_i_1_6[5], ready_i_1_6[5];    
wire [`DW-1:0] data_o_1_6[5];
wire valid_o_1_6[5], ready_o_1_6[5];        

reg [`DW-1:0] data_i_1_7[5];
reg valid_i_1_7[5], ready_i_1_7[5];    
wire [`DW-1:0] data_o_1_7[5];
wire valid_o_1_7[5], ready_o_1_7[5];        

reg [`DW-1:0] data_i_2_0[5];
reg valid_i_2_0[5], ready_i_2_0[5];    
wire [`DW-1:0] data_o_2_0[5];
wire valid_o_2_0[5], ready_o_2_0[5];        

reg [`DW-1:0] data_i_2_1[5];
reg valid_i_2_1[5], ready_i_2_1[5];    
wire [`DW-1:0] data_o_2_1[5];
wire valid_o_2_1[5], ready_o_2_1[5];        

reg [`DW-1:0] data_i_2_2[5];
reg valid_i_2_2[5], ready_i_2_2[5];    
wire [`DW-1:0] data_o_2_2[5];
wire valid_o_2_2[5], ready_o_2_2[5];        

reg [`DW-1:0] data_i_2_3[5];
reg valid_i_2_3[5], ready_i_2_3[5];    
wire [`DW-1:0] data_o_2_3[5];
wire valid_o_2_3[5], ready_o_2_3[5];        

reg [`DW-1:0] data_i_2_4[5];
reg valid_i_2_4[5], ready_i_2_4[5];    
wire [`DW-1:0] data_o_2_4[5];
wire valid_o_2_4[5], ready_o_2_4[5];        

reg [`DW-1:0] data_i_2_5[5];
reg valid_i_2_5[5], ready_i_2_5[5];    
wire [`DW-1:0] data_o_2_5[5];
wire valid_o_2_5[5], ready_o_2_5[5];        

reg [`DW-1:0] data_i_2_6[5];
reg valid_i_2_6[5], ready_i_2_6[5];    
wire [`DW-1:0] data_o_2_6[5];
wire valid_o_2_6[5], ready_o_2_6[5];        

reg [`DW-1:0] data_i_2_7[5];
reg valid_i_2_7[5], ready_i_2_7[5];    
wire [`DW-1:0] data_o_2_7[5];
wire valid_o_2_7[5], ready_o_2_7[5];        

reg [`DW-1:0] data_i_3_0[5];
reg valid_i_3_0[5], ready_i_3_0[5];    
wire [`DW-1:0] data_o_3_0[5];
wire valid_o_3_0[5], ready_o_3_0[5];        

reg [`DW-1:0] data_i_3_1[5];
reg valid_i_3_1[5], ready_i_3_1[5];    
wire [`DW-1:0] data_o_3_1[5];
wire valid_o_3_1[5], ready_o_3_1[5];        

reg [`DW-1:0] data_i_3_2[5];
reg valid_i_3_2[5], ready_i_3_2[5];    
wire [`DW-1:0] data_o_3_2[5];
wire valid_o_3_2[5], ready_o_3_2[5];        

reg [`DW-1:0] data_i_3_3[5];
reg valid_i_3_3[5], ready_i_3_3[5];    
wire [`DW-1:0] data_o_3_3[5];
wire valid_o_3_3[5], ready_o_3_3[5];        

reg [`DW-1:0] data_i_3_4[5];
reg valid_i_3_4[5], ready_i_3_4[5];    
wire [`DW-1:0] data_o_3_4[5];
wire valid_o_3_4[5], ready_o_3_4[5];        

reg [`DW-1:0] data_i_3_5[5];
reg valid_i_3_5[5], ready_i_3_5[5];    
wire [`DW-1:0] data_o_3_5[5];
wire valid_o_3_5[5], ready_o_3_5[5];        

reg [`DW-1:0] data_i_3_6[5];
reg valid_i_3_6[5], ready_i_3_6[5];    
wire [`DW-1:0] data_o_3_6[5];
wire valid_o_3_6[5], ready_o_3_6[5];        

reg [`DW-1:0] data_i_3_7[5];
reg valid_i_3_7[5], ready_i_3_7[5];    
wire [`DW-1:0] data_o_3_7[5];
wire valid_o_3_7[5], ready_o_3_7[5];        

reg [`DW-1:0] data_i_4_0[5];
reg valid_i_4_0[5], ready_i_4_0[5];    
wire [`DW-1:0] data_o_4_0[5];
wire valid_o_4_0[5], ready_o_4_0[5];        

reg [`DW-1:0] data_i_4_1[5];
reg valid_i_4_1[5], ready_i_4_1[5];    
wire [`DW-1:0] data_o_4_1[5];
wire valid_o_4_1[5], ready_o_4_1[5];        

reg [`DW-1:0] data_i_4_2[5];
reg valid_i_4_2[5], ready_i_4_2[5];    
wire [`DW-1:0] data_o_4_2[5];
wire valid_o_4_2[5], ready_o_4_2[5];        

reg [`DW-1:0] data_i_4_3[5];
reg valid_i_4_3[5], ready_i_4_3[5];    
wire [`DW-1:0] data_o_4_3[5];
wire valid_o_4_3[5], ready_o_4_3[5];        

reg [`DW-1:0] data_i_4_4[5];
reg valid_i_4_4[5], ready_i_4_4[5];    
wire [`DW-1:0] data_o_4_4[5];
wire valid_o_4_4[5], ready_o_4_4[5];        

reg [`DW-1:0] data_i_4_5[5];
reg valid_i_4_5[5], ready_i_4_5[5];    
wire [`DW-1:0] data_o_4_5[5];
wire valid_o_4_5[5], ready_o_4_5[5];        

reg [`DW-1:0] data_i_4_6[5];
reg valid_i_4_6[5], ready_i_4_6[5];    
wire [`DW-1:0] data_o_4_6[5];
wire valid_o_4_6[5], ready_o_4_6[5];        

reg [`DW-1:0] data_i_4_7[5];
reg valid_i_4_7[5], ready_i_4_7[5];    
wire [`DW-1:0] data_o_4_7[5];
wire valid_o_4_7[5], ready_o_4_7[5];        

reg [`DW-1:0] data_i_5_0[5];
reg valid_i_5_0[5], ready_i_5_0[5];    
wire [`DW-1:0] data_o_5_0[5];
wire valid_o_5_0[5], ready_o_5_0[5];        

reg [`DW-1:0] data_i_5_1[5];
reg valid_i_5_1[5], ready_i_5_1[5];    
wire [`DW-1:0] data_o_5_1[5];
wire valid_o_5_1[5], ready_o_5_1[5];        

reg [`DW-1:0] data_i_5_2[5];
reg valid_i_5_2[5], ready_i_5_2[5];    
wire [`DW-1:0] data_o_5_2[5];
wire valid_o_5_2[5], ready_o_5_2[5];        

reg [`DW-1:0] data_i_5_3[5];
reg valid_i_5_3[5], ready_i_5_3[5];    
wire [`DW-1:0] data_o_5_3[5];
wire valid_o_5_3[5], ready_o_5_3[5];        

reg [`DW-1:0] data_i_5_4[5];
reg valid_i_5_4[5], ready_i_5_4[5];    
wire [`DW-1:0] data_o_5_4[5];
wire valid_o_5_4[5], ready_o_5_4[5];        

reg [`DW-1:0] data_i_5_5[5];
reg valid_i_5_5[5], ready_i_5_5[5];    
wire [`DW-1:0] data_o_5_5[5];
wire valid_o_5_5[5], ready_o_5_5[5];        

reg [`DW-1:0] data_i_5_6[5];
reg valid_i_5_6[5], ready_i_5_6[5];    
wire [`DW-1:0] data_o_5_6[5];
wire valid_o_5_6[5], ready_o_5_6[5];        

reg [`DW-1:0] data_i_5_7[5];
reg valid_i_5_7[5], ready_i_5_7[5];    
wire [`DW-1:0] data_o_5_7[5];
wire valid_o_5_7[5], ready_o_5_7[5];        

reg [`DW-1:0] data_i_6_0[5];
reg valid_i_6_0[5], ready_i_6_0[5];    
wire [`DW-1:0] data_o_6_0[5];
wire valid_o_6_0[5], ready_o_6_0[5];        

reg [`DW-1:0] data_i_6_1[5];
reg valid_i_6_1[5], ready_i_6_1[5];    
wire [`DW-1:0] data_o_6_1[5];
wire valid_o_6_1[5], ready_o_6_1[5];        

reg [`DW-1:0] data_i_6_2[5];
reg valid_i_6_2[5], ready_i_6_2[5];    
wire [`DW-1:0] data_o_6_2[5];
wire valid_o_6_2[5], ready_o_6_2[5];        

reg [`DW-1:0] data_i_6_3[5];
reg valid_i_6_3[5], ready_i_6_3[5];    
wire [`DW-1:0] data_o_6_3[5];
wire valid_o_6_3[5], ready_o_6_3[5];        

reg [`DW-1:0] data_i_6_4[5];
reg valid_i_6_4[5], ready_i_6_4[5];    
wire [`DW-1:0] data_o_6_4[5];
wire valid_o_6_4[5], ready_o_6_4[5];        

reg [`DW-1:0] data_i_6_5[5];
reg valid_i_6_5[5], ready_i_6_5[5];    
wire [`DW-1:0] data_o_6_5[5];
wire valid_o_6_5[5], ready_o_6_5[5];        

reg [`DW-1:0] data_i_6_6[5];
reg valid_i_6_6[5], ready_i_6_6[5];    
wire [`DW-1:0] data_o_6_6[5];
wire valid_o_6_6[5], ready_o_6_6[5];        

reg [`DW-1:0] data_i_6_7[5];
reg valid_i_6_7[5], ready_i_6_7[5];    
wire [`DW-1:0] data_o_6_7[5];
wire valid_o_6_7[5], ready_o_6_7[5];        

always@(*) begin
    data_o[0][0] = data_o_0_0[0];
    valid_o[0][0] = valid_o_0_0[0];
    ready_o[0][0] = ready_o_0_0[0];
    data_o[0][1] = data_o_0_1[0];
    valid_o[0][1] = valid_o_0_1[0];
    ready_o[0][1] = ready_o_0_1[0];
    data_o[0][2] = data_o_0_2[0];
    valid_o[0][2] = valid_o_0_2[0];
    ready_o[0][2] = ready_o_0_2[0];
    data_o[0][3] = data_o_0_3[0];
    valid_o[0][3] = valid_o_0_3[0];
    ready_o[0][3] = ready_o_0_3[0];
    data_o[0][4] = data_o_0_4[0];
    valid_o[0][4] = valid_o_0_4[0];
    ready_o[0][4] = ready_o_0_4[0];
    data_o[0][5] = data_o_0_5[0];
    valid_o[0][5] = valid_o_0_5[0];
    ready_o[0][5] = ready_o_0_5[0];
    data_o[0][6] = data_o_0_6[0];
    valid_o[0][6] = valid_o_0_6[0];
    ready_o[0][6] = ready_o_0_6[0];
    data_o[0][7] = data_o_0_7[0];
    valid_o[0][7] = valid_o_0_7[0];
    ready_o[0][7] = ready_o_0_7[0];
    data_o[1][0] = data_o_1_0[0];
    valid_o[1][0] = valid_o_1_0[0];
    ready_o[1][0] = ready_o_1_0[0];
    data_o[1][1] = data_o_1_1[0];
    valid_o[1][1] = valid_o_1_1[0];
    ready_o[1][1] = ready_o_1_1[0];
    data_o[1][2] = data_o_1_2[0];
    valid_o[1][2] = valid_o_1_2[0];
    ready_o[1][2] = ready_o_1_2[0];
    data_o[1][3] = data_o_1_3[0];
    valid_o[1][3] = valid_o_1_3[0];
    ready_o[1][3] = ready_o_1_3[0];
    data_o[1][4] = data_o_1_4[0];
    valid_o[1][4] = valid_o_1_4[0];
    ready_o[1][4] = ready_o_1_4[0];
    data_o[1][5] = data_o_1_5[0];
    valid_o[1][5] = valid_o_1_5[0];
    ready_o[1][5] = ready_o_1_5[0];
    data_o[1][6] = data_o_1_6[0];
    valid_o[1][6] = valid_o_1_6[0];
    ready_o[1][6] = ready_o_1_6[0];
    data_o[1][7] = data_o_1_7[0];
    valid_o[1][7] = valid_o_1_7[0];
    ready_o[1][7] = ready_o_1_7[0];
    data_o[2][0] = data_o_2_0[0];
    valid_o[2][0] = valid_o_2_0[0];
    ready_o[2][0] = ready_o_2_0[0];
    data_o[2][1] = data_o_2_1[0];
    valid_o[2][1] = valid_o_2_1[0];
    ready_o[2][1] = ready_o_2_1[0];
    data_o[2][2] = data_o_2_2[0];
    valid_o[2][2] = valid_o_2_2[0];
    ready_o[2][2] = ready_o_2_2[0];
    data_o[2][3] = data_o_2_3[0];
    valid_o[2][3] = valid_o_2_3[0];
    ready_o[2][3] = ready_o_2_3[0];
    data_o[2][4] = data_o_2_4[0];
    valid_o[2][4] = valid_o_2_4[0];
    ready_o[2][4] = ready_o_2_4[0];
    data_o[2][5] = data_o_2_5[0];
    valid_o[2][5] = valid_o_2_5[0];
    ready_o[2][5] = ready_o_2_5[0];
    data_o[2][6] = data_o_2_6[0];
    valid_o[2][6] = valid_o_2_6[0];
    ready_o[2][6] = ready_o_2_6[0];
    data_o[2][7] = data_o_2_7[0];
    valid_o[2][7] = valid_o_2_7[0];
    ready_o[2][7] = ready_o_2_7[0];
    data_o[3][0] = data_o_3_0[0];
    valid_o[3][0] = valid_o_3_0[0];
    ready_o[3][0] = ready_o_3_0[0];
    data_o[3][1] = data_o_3_1[0];
    valid_o[3][1] = valid_o_3_1[0];
    ready_o[3][1] = ready_o_3_1[0];
    data_o[3][2] = data_o_3_2[0];
    valid_o[3][2] = valid_o_3_2[0];
    ready_o[3][2] = ready_o_3_2[0];
    data_o[3][3] = data_o_3_3[0];
    valid_o[3][3] = valid_o_3_3[0];
    ready_o[3][3] = ready_o_3_3[0];
    data_o[3][4] = data_o_3_4[0];
    valid_o[3][4] = valid_o_3_4[0];
    ready_o[3][4] = ready_o_3_4[0];
    data_o[3][5] = data_o_3_5[0];
    valid_o[3][5] = valid_o_3_5[0];
    ready_o[3][5] = ready_o_3_5[0];
    data_o[3][6] = data_o_3_6[0];
    valid_o[3][6] = valid_o_3_6[0];
    ready_o[3][6] = ready_o_3_6[0];
    data_o[3][7] = data_o_3_7[0];
    valid_o[3][7] = valid_o_3_7[0];
    ready_o[3][7] = ready_o_3_7[0];
    data_o[4][0] = data_o_4_0[0];
    valid_o[4][0] = valid_o_4_0[0];
    ready_o[4][0] = ready_o_4_0[0];
    data_o[4][1] = data_o_4_1[0];
    valid_o[4][1] = valid_o_4_1[0];
    ready_o[4][1] = ready_o_4_1[0];
    data_o[4][2] = data_o_4_2[0];
    valid_o[4][2] = valid_o_4_2[0];
    ready_o[4][2] = ready_o_4_2[0];
    data_o[4][3] = data_o_4_3[0];
    valid_o[4][3] = valid_o_4_3[0];
    ready_o[4][3] = ready_o_4_3[0];
    data_o[4][4] = data_o_4_4[0];
    valid_o[4][4] = valid_o_4_4[0];
    ready_o[4][4] = ready_o_4_4[0];
    data_o[4][5] = data_o_4_5[0];
    valid_o[4][5] = valid_o_4_5[0];
    ready_o[4][5] = ready_o_4_5[0];
    data_o[4][6] = data_o_4_6[0];
    valid_o[4][6] = valid_o_4_6[0];
    ready_o[4][6] = ready_o_4_6[0];
    data_o[4][7] = data_o_4_7[0];
    valid_o[4][7] = valid_o_4_7[0];
    ready_o[4][7] = ready_o_4_7[0];
    data_o[5][0] = data_o_5_0[0];
    valid_o[5][0] = valid_o_5_0[0];
    ready_o[5][0] = ready_o_5_0[0];
    data_o[5][1] = data_o_5_1[0];
    valid_o[5][1] = valid_o_5_1[0];
    ready_o[5][1] = ready_o_5_1[0];
    data_o[5][2] = data_o_5_2[0];
    valid_o[5][2] = valid_o_5_2[0];
    ready_o[5][2] = ready_o_5_2[0];
    data_o[5][3] = data_o_5_3[0];
    valid_o[5][3] = valid_o_5_3[0];
    ready_o[5][3] = ready_o_5_3[0];
    data_o[5][4] = data_o_5_4[0];
    valid_o[5][4] = valid_o_5_4[0];
    ready_o[5][4] = ready_o_5_4[0];
    data_o[5][5] = data_o_5_5[0];
    valid_o[5][5] = valid_o_5_5[0];
    ready_o[5][5] = ready_o_5_5[0];
    data_o[5][6] = data_o_5_6[0];
    valid_o[5][6] = valid_o_5_6[0];
    ready_o[5][6] = ready_o_5_6[0];
    data_o[5][7] = data_o_5_7[0];
    valid_o[5][7] = valid_o_5_7[0];
    ready_o[5][7] = ready_o_5_7[0];
    data_o[6][0] = data_o_6_0[0];
    valid_o[6][0] = valid_o_6_0[0];
    ready_o[6][0] = ready_o_6_0[0];
    data_o[6][1] = data_o_6_1[0];
    valid_o[6][1] = valid_o_6_1[0];
    ready_o[6][1] = ready_o_6_1[0];
    data_o[6][2] = data_o_6_2[0];
    valid_o[6][2] = valid_o_6_2[0];
    ready_o[6][2] = ready_o_6_2[0];
    data_o[6][3] = data_o_6_3[0];
    valid_o[6][3] = valid_o_6_3[0];
    ready_o[6][3] = ready_o_6_3[0];
    data_o[6][4] = data_o_6_4[0];
    valid_o[6][4] = valid_o_6_4[0];
    ready_o[6][4] = ready_o_6_4[0];
    data_o[6][5] = data_o_6_5[0];
    valid_o[6][5] = valid_o_6_5[0];
    ready_o[6][5] = ready_o_6_5[0];
    data_o[6][6] = data_o_6_6[0];
    valid_o[6][6] = valid_o_6_6[0];
    ready_o[6][6] = ready_o_6_6[0];
    data_o[6][7] = data_o_6_7[0];
    valid_o[6][7] = valid_o_6_7[0];
    ready_o[6][7] = ready_o_6_7[0];
end

/*Router 0,0*/    
merge_router #(
    .input_mask                     (input_mask_0_0),
    .output_sel                     (output_sel_0_0)
)router0(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_0_0),
    .valid_i                        (valid_i_0_0),
    .ready_o                        (ready_o_0_0),
    .data_o                         (data_o_0_0),
    .valid_o                        (valid_o_0_0),
    .ready_i                        (ready_i_0_0)
);


always@(*) begin
    data_i_0_0[4] = data_o_0_1[3];
    valid_i_0_0[4] = valid_o_0_1[3];
    ready_i_0_0[4] = ready_o_0_1[3];
    data_i_0_0[2] = data_o_1_0[1];
    valid_i_0_0[2] = valid_o_1_0[1];
    ready_i_0_0[2] = ready_o_1_0[1];
    data_i_0_0[0] = data_i[0][0];
    valid_i_0_0[0] = valid_i[0][0];
    ready_i_0_0[0] = ready_i[0][0];
end


/*Router 0,1*/    
merge_router #(
    .input_mask                     (input_mask_0_1),
    .output_sel                     (output_sel_0_1)
)router7(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_0_1),
    .valid_i                        (valid_i_0_1),
    .ready_o                        (ready_o_0_1),
    .data_o                         (data_o_0_1),
    .valid_o                        (valid_o_0_1),
    .ready_i                        (ready_i_0_1)
);


always@(*) begin
    data_i_0_1[3] = data_o_0_0[4];
    valid_i_0_1[3] = valid_o_0_0[4];
    ready_i_0_1[3] = ready_o_0_0[4];
    data_i_0_1[4] = data_o_0_2[3];
    valid_i_0_1[4] = valid_o_0_2[3];
    ready_i_0_1[4] = ready_o_0_2[3];
    data_i_0_1[2] = data_o_1_1[1];
    valid_i_0_1[2] = valid_o_1_1[1];
    ready_i_0_1[2] = ready_o_1_1[1];
    data_i_0_1[0] = data_i[0][1];
    valid_i_0_1[0] = valid_i[0][1];
    ready_i_0_1[0] = ready_i[0][1];
end


/*Router 0,2*/    
merge_router #(
    .input_mask                     (input_mask_0_2),
    .output_sel                     (output_sel_0_2)
)router14(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_0_2),
    .valid_i                        (valid_i_0_2),
    .ready_o                        (ready_o_0_2),
    .data_o                         (data_o_0_2),
    .valid_o                        (valid_o_0_2),
    .ready_i                        (ready_i_0_2)
);


always@(*) begin
    data_i_0_2[3] = data_o_0_1[4];
    valid_i_0_2[3] = valid_o_0_1[4];
    ready_i_0_2[3] = ready_o_0_1[4];
    data_i_0_2[4] = data_o_0_3[3];
    valid_i_0_2[4] = valid_o_0_3[3];
    ready_i_0_2[4] = ready_o_0_3[3];
    data_i_0_2[2] = data_o_1_2[1];
    valid_i_0_2[2] = valid_o_1_2[1];
    ready_i_0_2[2] = ready_o_1_2[1];
    data_i_0_2[0] = data_i[0][2];
    valid_i_0_2[0] = valid_i[0][2];
    ready_i_0_2[0] = ready_i[0][2];
end


/*Router 0,3*/    
merge_router #(
    .input_mask                     (input_mask_0_3),
    .output_sel                     (output_sel_0_3)
)router21(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_0_3),
    .valid_i                        (valid_i_0_3),
    .ready_o                        (ready_o_0_3),
    .data_o                         (data_o_0_3),
    .valid_o                        (valid_o_0_3),
    .ready_i                        (ready_i_0_3)
);


always@(*) begin
    data_i_0_3[3] = data_o_0_2[4];
    valid_i_0_3[3] = valid_o_0_2[4];
    ready_i_0_3[3] = ready_o_0_2[4];
    data_i_0_3[4] = data_o_0_4[3];
    valid_i_0_3[4] = valid_o_0_4[3];
    ready_i_0_3[4] = ready_o_0_4[3];
    data_i_0_3[2] = data_o_1_3[1];
    valid_i_0_3[2] = valid_o_1_3[1];
    ready_i_0_3[2] = ready_o_1_3[1];
    data_i_0_3[0] = data_i[0][3];
    valid_i_0_3[0] = valid_i[0][3];
    ready_i_0_3[0] = ready_i[0][3];
end


/*Router 0,4*/    
merge_router #(
    .input_mask                     (input_mask_0_4),
    .output_sel                     (output_sel_0_4)
)router28(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_0_4),
    .valid_i                        (valid_i_0_4),
    .ready_o                        (ready_o_0_4),
    .data_o                         (data_o_0_4),
    .valid_o                        (valid_o_0_4),
    .ready_i                        (ready_i_0_4)
);


always@(*) begin
    data_i_0_4[3] = data_o_0_3[4];
    valid_i_0_4[3] = valid_o_0_3[4];
    ready_i_0_4[3] = ready_o_0_3[4];
    data_i_0_4[4] = data_o_0_5[3];
    valid_i_0_4[4] = valid_o_0_5[3];
    ready_i_0_4[4] = ready_o_0_5[3];
    data_i_0_4[2] = data_o_1_4[1];
    valid_i_0_4[2] = valid_o_1_4[1];
    ready_i_0_4[2] = ready_o_1_4[1];
    data_i_0_4[0] = data_i[0][4];
    valid_i_0_4[0] = valid_i[0][4];
    ready_i_0_4[0] = ready_i[0][4];
end


/*Router 0,5*/    
merge_router #(
    .input_mask                     (input_mask_0_5),
    .output_sel                     (output_sel_0_5)
)router35(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_0_5),
    .valid_i                        (valid_i_0_5),
    .ready_o                        (ready_o_0_5),
    .data_o                         (data_o_0_5),
    .valid_o                        (valid_o_0_5),
    .ready_i                        (ready_i_0_5)
);


always@(*) begin
    data_i_0_5[3] = data_o_0_4[4];
    valid_i_0_5[3] = valid_o_0_4[4];
    ready_i_0_5[3] = ready_o_0_4[4];
    data_i_0_5[4] = data_o_0_6[3];
    valid_i_0_5[4] = valid_o_0_6[3];
    ready_i_0_5[4] = ready_o_0_6[3];
    data_i_0_5[2] = data_o_1_5[1];
    valid_i_0_5[2] = valid_o_1_5[1];
    ready_i_0_5[2] = ready_o_1_5[1];
    data_i_0_5[0] = data_i[0][5];
    valid_i_0_5[0] = valid_i[0][5];
    ready_i_0_5[0] = ready_i[0][5];
end


/*Router 0,6*/    
merge_router #(
    .input_mask                     (input_mask_0_6),
    .output_sel                     (output_sel_0_6)
)router42(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_0_6),
    .valid_i                        (valid_i_0_6),
    .ready_o                        (ready_o_0_6),
    .data_o                         (data_o_0_6),
    .valid_o                        (valid_o_0_6),
    .ready_i                        (ready_i_0_6)
);


always@(*) begin
    data_i_0_6[3] = data_o_0_5[4];
    valid_i_0_6[3] = valid_o_0_5[4];
    ready_i_0_6[3] = ready_o_0_5[4];
    data_i_0_6[4] = data_o_0_7[3];
    valid_i_0_6[4] = valid_o_0_7[3];
    ready_i_0_6[4] = ready_o_0_7[3];
    data_i_0_6[2] = data_o_1_6[1];
    valid_i_0_6[2] = valid_o_1_6[1];
    ready_i_0_6[2] = ready_o_1_6[1];
    data_i_0_6[0] = data_i[0][6];
    valid_i_0_6[0] = valid_i[0][6];
    ready_i_0_6[0] = ready_i[0][6];
end


/*Router 0,7*/    
merge_router #(
    .input_mask                     (input_mask_0_7),
    .output_sel                     (output_sel_0_7)
)router49(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_0_7),
    .valid_i                        (valid_i_0_7),
    .ready_o                        (ready_o_0_7),
    .data_o                         (data_o_0_7),
    .valid_o                        (valid_o_0_7),
    .ready_i                        (ready_i_0_7)
);


always@(*) begin
    data_i_0_7[3] = data_o_0_6[4];
    valid_i_0_7[3] = valid_o_0_6[4];
    ready_i_0_7[3] = ready_o_0_6[4];
    data_i_0_7[2] = data_o_1_7[1];
    valid_i_0_7[2] = valid_o_1_7[1];
    ready_i_0_7[2] = ready_o_1_7[1];
    data_i_0_7[0] = data_i[0][7];
    valid_i_0_7[0] = valid_i[0][7];
    ready_i_0_7[0] = ready_i[0][7];
end


/*Router 1,0*/    
merge_router #(
    .input_mask                     (input_mask_1_0),
    .output_sel                     (output_sel_1_0)
)router1(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_1_0),
    .valid_i                        (valid_i_1_0),
    .ready_o                        (ready_o_1_0),
    .data_o                         (data_o_1_0),
    .valid_o                        (valid_o_1_0),
    .ready_i                        (ready_i_1_0)
);


always@(*) begin
    data_i_1_0[4] = data_o_1_1[3];
    valid_i_1_0[4] = valid_o_1_1[3];
    ready_i_1_0[4] = ready_o_1_1[3];
    data_i_1_0[1] = data_o_0_0[2];
    valid_i_1_0[1] = valid_o_0_0[2];
    ready_i_1_0[1] = ready_o_0_0[2];
    data_i_1_0[2] = data_o_2_0[1];
    valid_i_1_0[2] = valid_o_2_0[1];
    ready_i_1_0[2] = ready_o_2_0[1];
    data_i_1_0[0] = data_i[1][0];
    valid_i_1_0[0] = valid_i[1][0];
    ready_i_1_0[0] = ready_i[1][0];
end


/*Router 1,1*/    
merge_router #(
    .input_mask                     (input_mask_1_1),
    .output_sel                     (output_sel_1_1)
)router8(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_1_1),
    .valid_i                        (valid_i_1_1),
    .ready_o                        (ready_o_1_1),
    .data_o                         (data_o_1_1),
    .valid_o                        (valid_o_1_1),
    .ready_i                        (ready_i_1_1)
);


always@(*) begin
    data_i_1_1[3] = data_o_1_0[4];
    valid_i_1_1[3] = valid_o_1_0[4];
    ready_i_1_1[3] = ready_o_1_0[4];
    data_i_1_1[4] = data_o_1_2[3];
    valid_i_1_1[4] = valid_o_1_2[3];
    ready_i_1_1[4] = ready_o_1_2[3];
    data_i_1_1[1] = data_o_0_1[2];
    valid_i_1_1[1] = valid_o_0_1[2];
    ready_i_1_1[1] = ready_o_0_1[2];
    data_i_1_1[2] = data_o_2_1[1];
    valid_i_1_1[2] = valid_o_2_1[1];
    ready_i_1_1[2] = ready_o_2_1[1];
    data_i_1_1[0] = data_i[1][1];
    valid_i_1_1[0] = valid_i[1][1];
    ready_i_1_1[0] = ready_i[1][1];
end


/*Router 1,2*/    
merge_router #(
    .input_mask                     (input_mask_1_2),
    .output_sel                     (output_sel_1_2)
)router15(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_1_2),
    .valid_i                        (valid_i_1_2),
    .ready_o                        (ready_o_1_2),
    .data_o                         (data_o_1_2),
    .valid_o                        (valid_o_1_2),
    .ready_i                        (ready_i_1_2)
);


always@(*) begin
    data_i_1_2[3] = data_o_1_1[4];
    valid_i_1_2[3] = valid_o_1_1[4];
    ready_i_1_2[3] = ready_o_1_1[4];
    data_i_1_2[4] = data_o_1_3[3];
    valid_i_1_2[4] = valid_o_1_3[3];
    ready_i_1_2[4] = ready_o_1_3[3];
    data_i_1_2[1] = data_o_0_2[2];
    valid_i_1_2[1] = valid_o_0_2[2];
    ready_i_1_2[1] = ready_o_0_2[2];
    data_i_1_2[2] = data_o_2_2[1];
    valid_i_1_2[2] = valid_o_2_2[1];
    ready_i_1_2[2] = ready_o_2_2[1];
    data_i_1_2[0] = data_i[1][2];
    valid_i_1_2[0] = valid_i[1][2];
    ready_i_1_2[0] = ready_i[1][2];
end


/*Router 1,3*/    
merge_router #(
    .input_mask                     (input_mask_1_3),
    .output_sel                     (output_sel_1_3)
)router22(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_1_3),
    .valid_i                        (valid_i_1_3),
    .ready_o                        (ready_o_1_3),
    .data_o                         (data_o_1_3),
    .valid_o                        (valid_o_1_3),
    .ready_i                        (ready_i_1_3)
);


always@(*) begin
    data_i_1_3[3] = data_o_1_2[4];
    valid_i_1_3[3] = valid_o_1_2[4];
    ready_i_1_3[3] = ready_o_1_2[4];
    data_i_1_3[4] = data_o_1_4[3];
    valid_i_1_3[4] = valid_o_1_4[3];
    ready_i_1_3[4] = ready_o_1_4[3];
    data_i_1_3[1] = data_o_0_3[2];
    valid_i_1_3[1] = valid_o_0_3[2];
    ready_i_1_3[1] = ready_o_0_3[2];
    data_i_1_3[2] = data_o_2_3[1];
    valid_i_1_3[2] = valid_o_2_3[1];
    ready_i_1_3[2] = ready_o_2_3[1];
    data_i_1_3[0] = data_i[1][3];
    valid_i_1_3[0] = valid_i[1][3];
    ready_i_1_3[0] = ready_i[1][3];
end


/*Router 1,4*/    
merge_router #(
    .input_mask                     (input_mask_1_4),
    .output_sel                     (output_sel_1_4)
)router29(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_1_4),
    .valid_i                        (valid_i_1_4),
    .ready_o                        (ready_o_1_4),
    .data_o                         (data_o_1_4),
    .valid_o                        (valid_o_1_4),
    .ready_i                        (ready_i_1_4)
);


always@(*) begin
    data_i_1_4[3] = data_o_1_3[4];
    valid_i_1_4[3] = valid_o_1_3[4];
    ready_i_1_4[3] = ready_o_1_3[4];
    data_i_1_4[4] = data_o_1_5[3];
    valid_i_1_4[4] = valid_o_1_5[3];
    ready_i_1_4[4] = ready_o_1_5[3];
    data_i_1_4[1] = data_o_0_4[2];
    valid_i_1_4[1] = valid_o_0_4[2];
    ready_i_1_4[1] = ready_o_0_4[2];
    data_i_1_4[2] = data_o_2_4[1];
    valid_i_1_4[2] = valid_o_2_4[1];
    ready_i_1_4[2] = ready_o_2_4[1];
    data_i_1_4[0] = data_i[1][4];
    valid_i_1_4[0] = valid_i[1][4];
    ready_i_1_4[0] = ready_i[1][4];
end


/*Router 1,5*/    
merge_router #(
    .input_mask                     (input_mask_1_5),
    .output_sel                     (output_sel_1_5)
)router36(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_1_5),
    .valid_i                        (valid_i_1_5),
    .ready_o                        (ready_o_1_5),
    .data_o                         (data_o_1_5),
    .valid_o                        (valid_o_1_5),
    .ready_i                        (ready_i_1_5)
);


always@(*) begin
    data_i_1_5[3] = data_o_1_4[4];
    valid_i_1_5[3] = valid_o_1_4[4];
    ready_i_1_5[3] = ready_o_1_4[4];
    data_i_1_5[4] = data_o_1_6[3];
    valid_i_1_5[4] = valid_o_1_6[3];
    ready_i_1_5[4] = ready_o_1_6[3];
    data_i_1_5[1] = data_o_0_5[2];
    valid_i_1_5[1] = valid_o_0_5[2];
    ready_i_1_5[1] = ready_o_0_5[2];
    data_i_1_5[2] = data_o_2_5[1];
    valid_i_1_5[2] = valid_o_2_5[1];
    ready_i_1_5[2] = ready_o_2_5[1];
    data_i_1_5[0] = data_i[1][5];
    valid_i_1_5[0] = valid_i[1][5];
    ready_i_1_5[0] = ready_i[1][5];
end


/*Router 1,6*/    
merge_router #(
    .input_mask                     (input_mask_1_6),
    .output_sel                     (output_sel_1_6)
)router43(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_1_6),
    .valid_i                        (valid_i_1_6),
    .ready_o                        (ready_o_1_6),
    .data_o                         (data_o_1_6),
    .valid_o                        (valid_o_1_6),
    .ready_i                        (ready_i_1_6)
);


always@(*) begin
    data_i_1_6[3] = data_o_1_5[4];
    valid_i_1_6[3] = valid_o_1_5[4];
    ready_i_1_6[3] = ready_o_1_5[4];
    data_i_1_6[4] = data_o_1_7[3];
    valid_i_1_6[4] = valid_o_1_7[3];
    ready_i_1_6[4] = ready_o_1_7[3];
    data_i_1_6[1] = data_o_0_6[2];
    valid_i_1_6[1] = valid_o_0_6[2];
    ready_i_1_6[1] = ready_o_0_6[2];
    data_i_1_6[2] = data_o_2_6[1];
    valid_i_1_6[2] = valid_o_2_6[1];
    ready_i_1_6[2] = ready_o_2_6[1];
    data_i_1_6[0] = data_i[1][6];
    valid_i_1_6[0] = valid_i[1][6];
    ready_i_1_6[0] = ready_i[1][6];
end


/*Router 1,7*/    
merge_router #(
    .input_mask                     (input_mask_1_7),
    .output_sel                     (output_sel_1_7)
)router50(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_1_7),
    .valid_i                        (valid_i_1_7),
    .ready_o                        (ready_o_1_7),
    .data_o                         (data_o_1_7),
    .valid_o                        (valid_o_1_7),
    .ready_i                        (ready_i_1_7)
);


always@(*) begin
    data_i_1_7[3] = data_o_1_6[4];
    valid_i_1_7[3] = valid_o_1_6[4];
    ready_i_1_7[3] = ready_o_1_6[4];
    data_i_1_7[1] = data_o_0_7[2];
    valid_i_1_7[1] = valid_o_0_7[2];
    ready_i_1_7[1] = ready_o_0_7[2];
    data_i_1_7[2] = data_o_2_7[1];
    valid_i_1_7[2] = valid_o_2_7[1];
    ready_i_1_7[2] = ready_o_2_7[1];
    data_i_1_7[0] = data_i[1][7];
    valid_i_1_7[0] = valid_i[1][7];
    ready_i_1_7[0] = ready_i[1][7];
end


/*Router 2,0*/    
merge_router #(
    .input_mask                     (input_mask_2_0),
    .output_sel                     (output_sel_2_0)
)router2(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_2_0),
    .valid_i                        (valid_i_2_0),
    .ready_o                        (ready_o_2_0),
    .data_o                         (data_o_2_0),
    .valid_o                        (valid_o_2_0),
    .ready_i                        (ready_i_2_0)
);


always@(*) begin
    data_i_2_0[4] = data_o_2_1[3];
    valid_i_2_0[4] = valid_o_2_1[3];
    ready_i_2_0[4] = ready_o_2_1[3];
    data_i_2_0[1] = data_o_1_0[2];
    valid_i_2_0[1] = valid_o_1_0[2];
    ready_i_2_0[1] = ready_o_1_0[2];
    data_i_2_0[2] = data_o_3_0[1];
    valid_i_2_0[2] = valid_o_3_0[1];
    ready_i_2_0[2] = ready_o_3_0[1];
    data_i_2_0[0] = data_i[2][0];
    valid_i_2_0[0] = valid_i[2][0];
    ready_i_2_0[0] = ready_i[2][0];
end


/*Router 2,1*/    
merge_router #(
    .input_mask                     (input_mask_2_1),
    .output_sel                     (output_sel_2_1)
)router9(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_2_1),
    .valid_i                        (valid_i_2_1),
    .ready_o                        (ready_o_2_1),
    .data_o                         (data_o_2_1),
    .valid_o                        (valid_o_2_1),
    .ready_i                        (ready_i_2_1)
);


always@(*) begin
    data_i_2_1[3] = data_o_2_0[4];
    valid_i_2_1[3] = valid_o_2_0[4];
    ready_i_2_1[3] = ready_o_2_0[4];
    data_i_2_1[4] = data_o_2_2[3];
    valid_i_2_1[4] = valid_o_2_2[3];
    ready_i_2_1[4] = ready_o_2_2[3];
    data_i_2_1[1] = data_o_1_1[2];
    valid_i_2_1[1] = valid_o_1_1[2];
    ready_i_2_1[1] = ready_o_1_1[2];
    data_i_2_1[2] = data_o_3_1[1];
    valid_i_2_1[2] = valid_o_3_1[1];
    ready_i_2_1[2] = ready_o_3_1[1];
    data_i_2_1[0] = data_i[2][1];
    valid_i_2_1[0] = valid_i[2][1];
    ready_i_2_1[0] = ready_i[2][1];
end


/*Router 2,2*/    
merge_router #(
    .input_mask                     (input_mask_2_2),
    .output_sel                     (output_sel_2_2)
)router16(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_2_2),
    .valid_i                        (valid_i_2_2),
    .ready_o                        (ready_o_2_2),
    .data_o                         (data_o_2_2),
    .valid_o                        (valid_o_2_2),
    .ready_i                        (ready_i_2_2)
);


always@(*) begin
    data_i_2_2[3] = data_o_2_1[4];
    valid_i_2_2[3] = valid_o_2_1[4];
    ready_i_2_2[3] = ready_o_2_1[4];
    data_i_2_2[4] = data_o_2_3[3];
    valid_i_2_2[4] = valid_o_2_3[3];
    ready_i_2_2[4] = ready_o_2_3[3];
    data_i_2_2[1] = data_o_1_2[2];
    valid_i_2_2[1] = valid_o_1_2[2];
    ready_i_2_2[1] = ready_o_1_2[2];
    data_i_2_2[2] = data_o_3_2[1];
    valid_i_2_2[2] = valid_o_3_2[1];
    ready_i_2_2[2] = ready_o_3_2[1];
    data_i_2_2[0] = data_i[2][2];
    valid_i_2_2[0] = valid_i[2][2];
    ready_i_2_2[0] = ready_i[2][2];
end


/*Router 2,3*/    
merge_router #(
    .input_mask                     (input_mask_2_3),
    .output_sel                     (output_sel_2_3)
)router23(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_2_3),
    .valid_i                        (valid_i_2_3),
    .ready_o                        (ready_o_2_3),
    .data_o                         (data_o_2_3),
    .valid_o                        (valid_o_2_3),
    .ready_i                        (ready_i_2_3)
);


always@(*) begin
    data_i_2_3[3] = data_o_2_2[4];
    valid_i_2_3[3] = valid_o_2_2[4];
    ready_i_2_3[3] = ready_o_2_2[4];
    data_i_2_3[4] = data_o_2_4[3];
    valid_i_2_3[4] = valid_o_2_4[3];
    ready_i_2_3[4] = ready_o_2_4[3];
    data_i_2_3[1] = data_o_1_3[2];
    valid_i_2_3[1] = valid_o_1_3[2];
    ready_i_2_3[1] = ready_o_1_3[2];
    data_i_2_3[2] = data_o_3_3[1];
    valid_i_2_3[2] = valid_o_3_3[1];
    ready_i_2_3[2] = ready_o_3_3[1];
    data_i_2_3[0] = data_i[2][3];
    valid_i_2_3[0] = valid_i[2][3];
    ready_i_2_3[0] = ready_i[2][3];
end


/*Router 2,4*/    
merge_router #(
    .input_mask                     (input_mask_2_4),
    .output_sel                     (output_sel_2_4)
)router30(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_2_4),
    .valid_i                        (valid_i_2_4),
    .ready_o                        (ready_o_2_4),
    .data_o                         (data_o_2_4),
    .valid_o                        (valid_o_2_4),
    .ready_i                        (ready_i_2_4)
);


always@(*) begin
    data_i_2_4[3] = data_o_2_3[4];
    valid_i_2_4[3] = valid_o_2_3[4];
    ready_i_2_4[3] = ready_o_2_3[4];
    data_i_2_4[4] = data_o_2_5[3];
    valid_i_2_4[4] = valid_o_2_5[3];
    ready_i_2_4[4] = ready_o_2_5[3];
    data_i_2_4[1] = data_o_1_4[2];
    valid_i_2_4[1] = valid_o_1_4[2];
    ready_i_2_4[1] = ready_o_1_4[2];
    data_i_2_4[2] = data_o_3_4[1];
    valid_i_2_4[2] = valid_o_3_4[1];
    ready_i_2_4[2] = ready_o_3_4[1];
    data_i_2_4[0] = data_i[2][4];
    valid_i_2_4[0] = valid_i[2][4];
    ready_i_2_4[0] = ready_i[2][4];
end


/*Router 2,5*/    
merge_router #(
    .input_mask                     (input_mask_2_5),
    .output_sel                     (output_sel_2_5)
)router37(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_2_5),
    .valid_i                        (valid_i_2_5),
    .ready_o                        (ready_o_2_5),
    .data_o                         (data_o_2_5),
    .valid_o                        (valid_o_2_5),
    .ready_i                        (ready_i_2_5)
);


always@(*) begin
    data_i_2_5[3] = data_o_2_4[4];
    valid_i_2_5[3] = valid_o_2_4[4];
    ready_i_2_5[3] = ready_o_2_4[4];
    data_i_2_5[4] = data_o_2_6[3];
    valid_i_2_5[4] = valid_o_2_6[3];
    ready_i_2_5[4] = ready_o_2_6[3];
    data_i_2_5[1] = data_o_1_5[2];
    valid_i_2_5[1] = valid_o_1_5[2];
    ready_i_2_5[1] = ready_o_1_5[2];
    data_i_2_5[2] = data_o_3_5[1];
    valid_i_2_5[2] = valid_o_3_5[1];
    ready_i_2_5[2] = ready_o_3_5[1];
    data_i_2_5[0] = data_i[2][5];
    valid_i_2_5[0] = valid_i[2][5];
    ready_i_2_5[0] = ready_i[2][5];
end


/*Router 2,6*/    
merge_router #(
    .input_mask                     (input_mask_2_6),
    .output_sel                     (output_sel_2_6)
)router44(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_2_6),
    .valid_i                        (valid_i_2_6),
    .ready_o                        (ready_o_2_6),
    .data_o                         (data_o_2_6),
    .valid_o                        (valid_o_2_6),
    .ready_i                        (ready_i_2_6)
);


always@(*) begin
    data_i_2_6[3] = data_o_2_5[4];
    valid_i_2_6[3] = valid_o_2_5[4];
    ready_i_2_6[3] = ready_o_2_5[4];
    data_i_2_6[4] = data_o_2_7[3];
    valid_i_2_6[4] = valid_o_2_7[3];
    ready_i_2_6[4] = ready_o_2_7[3];
    data_i_2_6[1] = data_o_1_6[2];
    valid_i_2_6[1] = valid_o_1_6[2];
    ready_i_2_6[1] = ready_o_1_6[2];
    data_i_2_6[2] = data_o_3_6[1];
    valid_i_2_6[2] = valid_o_3_6[1];
    ready_i_2_6[2] = ready_o_3_6[1];
    data_i_2_6[0] = data_i[2][6];
    valid_i_2_6[0] = valid_i[2][6];
    ready_i_2_6[0] = ready_i[2][6];
end


/*Router 2,7*/    
merge_router #(
    .input_mask                     (input_mask_2_7),
    .output_sel                     (output_sel_2_7)
)router51(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_2_7),
    .valid_i                        (valid_i_2_7),
    .ready_o                        (ready_o_2_7),
    .data_o                         (data_o_2_7),
    .valid_o                        (valid_o_2_7),
    .ready_i                        (ready_i_2_7)
);


always@(*) begin
    data_i_2_7[3] = data_o_2_6[4];
    valid_i_2_7[3] = valid_o_2_6[4];
    ready_i_2_7[3] = ready_o_2_6[4];
    data_i_2_7[1] = data_o_1_7[2];
    valid_i_2_7[1] = valid_o_1_7[2];
    ready_i_2_7[1] = ready_o_1_7[2];
    data_i_2_7[2] = data_o_3_7[1];
    valid_i_2_7[2] = valid_o_3_7[1];
    ready_i_2_7[2] = ready_o_3_7[1];
    data_i_2_7[0] = data_i[2][7];
    valid_i_2_7[0] = valid_i[2][7];
    ready_i_2_7[0] = ready_i[2][7];
end


/*Router 3,0*/    
merge_router #(
    .input_mask                     (input_mask_3_0),
    .output_sel                     (output_sel_3_0)
)router3(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_3_0),
    .valid_i                        (valid_i_3_0),
    .ready_o                        (ready_o_3_0),
    .data_o                         (data_o_3_0),
    .valid_o                        (valid_o_3_0),
    .ready_i                        (ready_i_3_0)
);


always@(*) begin
    data_i_3_0[4] = data_o_3_1[3];
    valid_i_3_0[4] = valid_o_3_1[3];
    ready_i_3_0[4] = ready_o_3_1[3];
    data_i_3_0[1] = data_o_2_0[2];
    valid_i_3_0[1] = valid_o_2_0[2];
    ready_i_3_0[1] = ready_o_2_0[2];
    data_i_3_0[2] = data_o_4_0[1];
    valid_i_3_0[2] = valid_o_4_0[1];
    ready_i_3_0[2] = ready_o_4_0[1];
    data_i_3_0[0] = data_i[3][0];
    valid_i_3_0[0] = valid_i[3][0];
    ready_i_3_0[0] = ready_i[3][0];
end


/*Router 3,1*/    
merge_router #(
    .input_mask                     (input_mask_3_1),
    .output_sel                     (output_sel_3_1)
)router10(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_3_1),
    .valid_i                        (valid_i_3_1),
    .ready_o                        (ready_o_3_1),
    .data_o                         (data_o_3_1),
    .valid_o                        (valid_o_3_1),
    .ready_i                        (ready_i_3_1)
);


always@(*) begin
    data_i_3_1[3] = data_o_3_0[4];
    valid_i_3_1[3] = valid_o_3_0[4];
    ready_i_3_1[3] = ready_o_3_0[4];
    data_i_3_1[4] = data_o_3_2[3];
    valid_i_3_1[4] = valid_o_3_2[3];
    ready_i_3_1[4] = ready_o_3_2[3];
    data_i_3_1[1] = data_o_2_1[2];
    valid_i_3_1[1] = valid_o_2_1[2];
    ready_i_3_1[1] = ready_o_2_1[2];
    data_i_3_1[2] = data_o_4_1[1];
    valid_i_3_1[2] = valid_o_4_1[1];
    ready_i_3_1[2] = ready_o_4_1[1];
    data_i_3_1[0] = data_i[3][1];
    valid_i_3_1[0] = valid_i[3][1];
    ready_i_3_1[0] = ready_i[3][1];
end


/*Router 3,2*/    
merge_router #(
    .input_mask                     (input_mask_3_2),
    .output_sel                     (output_sel_3_2)
)router17(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_3_2),
    .valid_i                        (valid_i_3_2),
    .ready_o                        (ready_o_3_2),
    .data_o                         (data_o_3_2),
    .valid_o                        (valid_o_3_2),
    .ready_i                        (ready_i_3_2)
);


always@(*) begin
    data_i_3_2[3] = data_o_3_1[4];
    valid_i_3_2[3] = valid_o_3_1[4];
    ready_i_3_2[3] = ready_o_3_1[4];
    data_i_3_2[4] = data_o_3_3[3];
    valid_i_3_2[4] = valid_o_3_3[3];
    ready_i_3_2[4] = ready_o_3_3[3];
    data_i_3_2[1] = data_o_2_2[2];
    valid_i_3_2[1] = valid_o_2_2[2];
    ready_i_3_2[1] = ready_o_2_2[2];
    data_i_3_2[2] = data_o_4_2[1];
    valid_i_3_2[2] = valid_o_4_2[1];
    ready_i_3_2[2] = ready_o_4_2[1];
    data_i_3_2[0] = data_i[3][2];
    valid_i_3_2[0] = valid_i[3][2];
    ready_i_3_2[0] = ready_i[3][2];
end


/*Router 3,3*/    
merge_router #(
    .input_mask                     (input_mask_3_3),
    .output_sel                     (output_sel_3_3)
)router24(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_3_3),
    .valid_i                        (valid_i_3_3),
    .ready_o                        (ready_o_3_3),
    .data_o                         (data_o_3_3),
    .valid_o                        (valid_o_3_3),
    .ready_i                        (ready_i_3_3)
);


always@(*) begin
    data_i_3_3[3] = data_o_3_2[4];
    valid_i_3_3[3] = valid_o_3_2[4];
    ready_i_3_3[3] = ready_o_3_2[4];
    data_i_3_3[4] = data_o_3_4[3];
    valid_i_3_3[4] = valid_o_3_4[3];
    ready_i_3_3[4] = ready_o_3_4[3];
    data_i_3_3[1] = data_o_2_3[2];
    valid_i_3_3[1] = valid_o_2_3[2];
    ready_i_3_3[1] = ready_o_2_3[2];
    data_i_3_3[2] = data_o_4_3[1];
    valid_i_3_3[2] = valid_o_4_3[1];
    ready_i_3_3[2] = ready_o_4_3[1];
    data_i_3_3[0] = data_i[3][3];
    valid_i_3_3[0] = valid_i[3][3];
    ready_i_3_3[0] = ready_i[3][3];
end


/*Router 3,4*/    
merge_router #(
    .input_mask                     (input_mask_3_4),
    .output_sel                     (output_sel_3_4)
)router31(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_3_4),
    .valid_i                        (valid_i_3_4),
    .ready_o                        (ready_o_3_4),
    .data_o                         (data_o_3_4),
    .valid_o                        (valid_o_3_4),
    .ready_i                        (ready_i_3_4)
);


always@(*) begin
    data_i_3_4[3] = data_o_3_3[4];
    valid_i_3_4[3] = valid_o_3_3[4];
    ready_i_3_4[3] = ready_o_3_3[4];
    data_i_3_4[4] = data_o_3_5[3];
    valid_i_3_4[4] = valid_o_3_5[3];
    ready_i_3_4[4] = ready_o_3_5[3];
    data_i_3_4[1] = data_o_2_4[2];
    valid_i_3_4[1] = valid_o_2_4[2];
    ready_i_3_4[1] = ready_o_2_4[2];
    data_i_3_4[2] = data_o_4_4[1];
    valid_i_3_4[2] = valid_o_4_4[1];
    ready_i_3_4[2] = ready_o_4_4[1];
    data_i_3_4[0] = data_i[3][4];
    valid_i_3_4[0] = valid_i[3][4];
    ready_i_3_4[0] = ready_i[3][4];
end


/*Router 3,5*/    
merge_router #(
    .input_mask                     (input_mask_3_5),
    .output_sel                     (output_sel_3_5)
)router38(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_3_5),
    .valid_i                        (valid_i_3_5),
    .ready_o                        (ready_o_3_5),
    .data_o                         (data_o_3_5),
    .valid_o                        (valid_o_3_5),
    .ready_i                        (ready_i_3_5)
);


always@(*) begin
    data_i_3_5[3] = data_o_3_4[4];
    valid_i_3_5[3] = valid_o_3_4[4];
    ready_i_3_5[3] = ready_o_3_4[4];
    data_i_3_5[4] = data_o_3_6[3];
    valid_i_3_5[4] = valid_o_3_6[3];
    ready_i_3_5[4] = ready_o_3_6[3];
    data_i_3_5[1] = data_o_2_5[2];
    valid_i_3_5[1] = valid_o_2_5[2];
    ready_i_3_5[1] = ready_o_2_5[2];
    data_i_3_5[2] = data_o_4_5[1];
    valid_i_3_5[2] = valid_o_4_5[1];
    ready_i_3_5[2] = ready_o_4_5[1];
    data_i_3_5[0] = data_i[3][5];
    valid_i_3_5[0] = valid_i[3][5];
    ready_i_3_5[0] = ready_i[3][5];
end


/*Router 3,6*/    
merge_router #(
    .input_mask                     (input_mask_3_6),
    .output_sel                     (output_sel_3_6)
)router45(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_3_6),
    .valid_i                        (valid_i_3_6),
    .ready_o                        (ready_o_3_6),
    .data_o                         (data_o_3_6),
    .valid_o                        (valid_o_3_6),
    .ready_i                        (ready_i_3_6)
);


always@(*) begin
    data_i_3_6[3] = data_o_3_5[4];
    valid_i_3_6[3] = valid_o_3_5[4];
    ready_i_3_6[3] = ready_o_3_5[4];
    data_i_3_6[4] = data_o_3_7[3];
    valid_i_3_6[4] = valid_o_3_7[3];
    ready_i_3_6[4] = ready_o_3_7[3];
    data_i_3_6[1] = data_o_2_6[2];
    valid_i_3_6[1] = valid_o_2_6[2];
    ready_i_3_6[1] = ready_o_2_6[2];
    data_i_3_6[2] = data_o_4_6[1];
    valid_i_3_6[2] = valid_o_4_6[1];
    ready_i_3_6[2] = ready_o_4_6[1];
    data_i_3_6[0] = data_i[3][6];
    valid_i_3_6[0] = valid_i[3][6];
    ready_i_3_6[0] = ready_i[3][6];
end


/*Router 3,7*/    
merge_router #(
    .input_mask                     (input_mask_3_7),
    .output_sel                     (output_sel_3_7)
)router52(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_3_7),
    .valid_i                        (valid_i_3_7),
    .ready_o                        (ready_o_3_7),
    .data_o                         (data_o_3_7),
    .valid_o                        (valid_o_3_7),
    .ready_i                        (ready_i_3_7)
);


always@(*) begin
    data_i_3_7[3] = data_o_3_6[4];
    valid_i_3_7[3] = valid_o_3_6[4];
    ready_i_3_7[3] = ready_o_3_6[4];
    data_i_3_7[1] = data_o_2_7[2];
    valid_i_3_7[1] = valid_o_2_7[2];
    ready_i_3_7[1] = ready_o_2_7[2];
    data_i_3_7[2] = data_o_4_7[1];
    valid_i_3_7[2] = valid_o_4_7[1];
    ready_i_3_7[2] = ready_o_4_7[1];
    data_i_3_7[0] = data_i[3][7];
    valid_i_3_7[0] = valid_i[3][7];
    ready_i_3_7[0] = ready_i[3][7];
end


/*Router 4,0*/    
merge_router #(
    .input_mask                     (input_mask_4_0),
    .output_sel                     (output_sel_4_0)
)router4(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_4_0),
    .valid_i                        (valid_i_4_0),
    .ready_o                        (ready_o_4_0),
    .data_o                         (data_o_4_0),
    .valid_o                        (valid_o_4_0),
    .ready_i                        (ready_i_4_0)
);


always@(*) begin
    data_i_4_0[4] = data_o_4_1[3];
    valid_i_4_0[4] = valid_o_4_1[3];
    ready_i_4_0[4] = ready_o_4_1[3];
    data_i_4_0[1] = data_o_3_0[2];
    valid_i_4_0[1] = valid_o_3_0[2];
    ready_i_4_0[1] = ready_o_3_0[2];
    data_i_4_0[2] = data_o_5_0[1];
    valid_i_4_0[2] = valid_o_5_0[1];
    ready_i_4_0[2] = ready_o_5_0[1];
    data_i_4_0[0] = data_i[4][0];
    valid_i_4_0[0] = valid_i[4][0];
    ready_i_4_0[0] = ready_i[4][0];
end


/*Router 4,1*/    
merge_router #(
    .input_mask                     (input_mask_4_1),
    .output_sel                     (output_sel_4_1)
)router11(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_4_1),
    .valid_i                        (valid_i_4_1),
    .ready_o                        (ready_o_4_1),
    .data_o                         (data_o_4_1),
    .valid_o                        (valid_o_4_1),
    .ready_i                        (ready_i_4_1)
);


always@(*) begin
    data_i_4_1[3] = data_o_4_0[4];
    valid_i_4_1[3] = valid_o_4_0[4];
    ready_i_4_1[3] = ready_o_4_0[4];
    data_i_4_1[4] = data_o_4_2[3];
    valid_i_4_1[4] = valid_o_4_2[3];
    ready_i_4_1[4] = ready_o_4_2[3];
    data_i_4_1[1] = data_o_3_1[2];
    valid_i_4_1[1] = valid_o_3_1[2];
    ready_i_4_1[1] = ready_o_3_1[2];
    data_i_4_1[2] = data_o_5_1[1];
    valid_i_4_1[2] = valid_o_5_1[1];
    ready_i_4_1[2] = ready_o_5_1[1];
    data_i_4_1[0] = data_i[4][1];
    valid_i_4_1[0] = valid_i[4][1];
    ready_i_4_1[0] = ready_i[4][1];
end


/*Router 4,2*/    
merge_router #(
    .input_mask                     (input_mask_4_2),
    .output_sel                     (output_sel_4_2)
)router18(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_4_2),
    .valid_i                        (valid_i_4_2),
    .ready_o                        (ready_o_4_2),
    .data_o                         (data_o_4_2),
    .valid_o                        (valid_o_4_2),
    .ready_i                        (ready_i_4_2)
);


always@(*) begin
    data_i_4_2[3] = data_o_4_1[4];
    valid_i_4_2[3] = valid_o_4_1[4];
    ready_i_4_2[3] = ready_o_4_1[4];
    data_i_4_2[4] = data_o_4_3[3];
    valid_i_4_2[4] = valid_o_4_3[3];
    ready_i_4_2[4] = ready_o_4_3[3];
    data_i_4_2[1] = data_o_3_2[2];
    valid_i_4_2[1] = valid_o_3_2[2];
    ready_i_4_2[1] = ready_o_3_2[2];
    data_i_4_2[2] = data_o_5_2[1];
    valid_i_4_2[2] = valid_o_5_2[1];
    ready_i_4_2[2] = ready_o_5_2[1];
    data_i_4_2[0] = data_i[4][2];
    valid_i_4_2[0] = valid_i[4][2];
    ready_i_4_2[0] = ready_i[4][2];
end


/*Router 4,3*/    
merge_router #(
    .input_mask                     (input_mask_4_3),
    .output_sel                     (output_sel_4_3)
)router25(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_4_3),
    .valid_i                        (valid_i_4_3),
    .ready_o                        (ready_o_4_3),
    .data_o                         (data_o_4_3),
    .valid_o                        (valid_o_4_3),
    .ready_i                        (ready_i_4_3)
);


always@(*) begin
    data_i_4_3[3] = data_o_4_2[4];
    valid_i_4_3[3] = valid_o_4_2[4];
    ready_i_4_3[3] = ready_o_4_2[4];
    data_i_4_3[4] = data_o_4_4[3];
    valid_i_4_3[4] = valid_o_4_4[3];
    ready_i_4_3[4] = ready_o_4_4[3];
    data_i_4_3[1] = data_o_3_3[2];
    valid_i_4_3[1] = valid_o_3_3[2];
    ready_i_4_3[1] = ready_o_3_3[2];
    data_i_4_3[2] = data_o_5_3[1];
    valid_i_4_3[2] = valid_o_5_3[1];
    ready_i_4_3[2] = ready_o_5_3[1];
    data_i_4_3[0] = data_i[4][3];
    valid_i_4_3[0] = valid_i[4][3];
    ready_i_4_3[0] = ready_i[4][3];
end


/*Router 4,4*/    
merge_router #(
    .input_mask                     (input_mask_4_4),
    .output_sel                     (output_sel_4_4)
)router32(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_4_4),
    .valid_i                        (valid_i_4_4),
    .ready_o                        (ready_o_4_4),
    .data_o                         (data_o_4_4),
    .valid_o                        (valid_o_4_4),
    .ready_i                        (ready_i_4_4)
);


always@(*) begin
    data_i_4_4[3] = data_o_4_3[4];
    valid_i_4_4[3] = valid_o_4_3[4];
    ready_i_4_4[3] = ready_o_4_3[4];
    data_i_4_4[4] = data_o_4_5[3];
    valid_i_4_4[4] = valid_o_4_5[3];
    ready_i_4_4[4] = ready_o_4_5[3];
    data_i_4_4[1] = data_o_3_4[2];
    valid_i_4_4[1] = valid_o_3_4[2];
    ready_i_4_4[1] = ready_o_3_4[2];
    data_i_4_4[2] = data_o_5_4[1];
    valid_i_4_4[2] = valid_o_5_4[1];
    ready_i_4_4[2] = ready_o_5_4[1];
    data_i_4_4[0] = data_i[4][4];
    valid_i_4_4[0] = valid_i[4][4];
    ready_i_4_4[0] = ready_i[4][4];
end


/*Router 4,5*/    
merge_router #(
    .input_mask                     (input_mask_4_5),
    .output_sel                     (output_sel_4_5)
)router39(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_4_5),
    .valid_i                        (valid_i_4_5),
    .ready_o                        (ready_o_4_5),
    .data_o                         (data_o_4_5),
    .valid_o                        (valid_o_4_5),
    .ready_i                        (ready_i_4_5)
);


always@(*) begin
    data_i_4_5[3] = data_o_4_4[4];
    valid_i_4_5[3] = valid_o_4_4[4];
    ready_i_4_5[3] = ready_o_4_4[4];
    data_i_4_5[4] = data_o_4_6[3];
    valid_i_4_5[4] = valid_o_4_6[3];
    ready_i_4_5[4] = ready_o_4_6[3];
    data_i_4_5[1] = data_o_3_5[2];
    valid_i_4_5[1] = valid_o_3_5[2];
    ready_i_4_5[1] = ready_o_3_5[2];
    data_i_4_5[2] = data_o_5_5[1];
    valid_i_4_5[2] = valid_o_5_5[1];
    ready_i_4_5[2] = ready_o_5_5[1];
    data_i_4_5[0] = data_i[4][5];
    valid_i_4_5[0] = valid_i[4][5];
    ready_i_4_5[0] = ready_i[4][5];
end


/*Router 4,6*/    
merge_router #(
    .input_mask                     (input_mask_4_6),
    .output_sel                     (output_sel_4_6)
)router46(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_4_6),
    .valid_i                        (valid_i_4_6),
    .ready_o                        (ready_o_4_6),
    .data_o                         (data_o_4_6),
    .valid_o                        (valid_o_4_6),
    .ready_i                        (ready_i_4_6)
);


always@(*) begin
    data_i_4_6[3] = data_o_4_5[4];
    valid_i_4_6[3] = valid_o_4_5[4];
    ready_i_4_6[3] = ready_o_4_5[4];
    data_i_4_6[4] = data_o_4_7[3];
    valid_i_4_6[4] = valid_o_4_7[3];
    ready_i_4_6[4] = ready_o_4_7[3];
    data_i_4_6[1] = data_o_3_6[2];
    valid_i_4_6[1] = valid_o_3_6[2];
    ready_i_4_6[1] = ready_o_3_6[2];
    data_i_4_6[2] = data_o_5_6[1];
    valid_i_4_6[2] = valid_o_5_6[1];
    ready_i_4_6[2] = ready_o_5_6[1];
    data_i_4_6[0] = data_i[4][6];
    valid_i_4_6[0] = valid_i[4][6];
    ready_i_4_6[0] = ready_i[4][6];
end


/*Router 4,7*/    
merge_router #(
    .input_mask                     (input_mask_4_7),
    .output_sel                     (output_sel_4_7)
)router53(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_4_7),
    .valid_i                        (valid_i_4_7),
    .ready_o                        (ready_o_4_7),
    .data_o                         (data_o_4_7),
    .valid_o                        (valid_o_4_7),
    .ready_i                        (ready_i_4_7)
);


always@(*) begin
    data_i_4_7[3] = data_o_4_6[4];
    valid_i_4_7[3] = valid_o_4_6[4];
    ready_i_4_7[3] = ready_o_4_6[4];
    data_i_4_7[1] = data_o_3_7[2];
    valid_i_4_7[1] = valid_o_3_7[2];
    ready_i_4_7[1] = ready_o_3_7[2];
    data_i_4_7[2] = data_o_5_7[1];
    valid_i_4_7[2] = valid_o_5_7[1];
    ready_i_4_7[2] = ready_o_5_7[1];
    data_i_4_7[0] = data_i[4][7];
    valid_i_4_7[0] = valid_i[4][7];
    ready_i_4_7[0] = ready_i[4][7];
end


/*Router 5,0*/    
merge_router #(
    .input_mask                     (input_mask_5_0),
    .output_sel                     (output_sel_5_0)
)router5(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_5_0),
    .valid_i                        (valid_i_5_0),
    .ready_o                        (ready_o_5_0),
    .data_o                         (data_o_5_0),
    .valid_o                        (valid_o_5_0),
    .ready_i                        (ready_i_5_0)
);


always@(*) begin
    data_i_5_0[4] = data_o_5_1[3];
    valid_i_5_0[4] = valid_o_5_1[3];
    ready_i_5_0[4] = ready_o_5_1[3];
    data_i_5_0[1] = data_o_4_0[2];
    valid_i_5_0[1] = valid_o_4_0[2];
    ready_i_5_0[1] = ready_o_4_0[2];
    data_i_5_0[2] = data_o_6_0[1];
    valid_i_5_0[2] = valid_o_6_0[1];
    ready_i_5_0[2] = ready_o_6_0[1];
    data_i_5_0[0] = data_i[5][0];
    valid_i_5_0[0] = valid_i[5][0];
    ready_i_5_0[0] = ready_i[5][0];
end


/*Router 5,1*/    
merge_router #(
    .input_mask                     (input_mask_5_1),
    .output_sel                     (output_sel_5_1)
)router12(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_5_1),
    .valid_i                        (valid_i_5_1),
    .ready_o                        (ready_o_5_1),
    .data_o                         (data_o_5_1),
    .valid_o                        (valid_o_5_1),
    .ready_i                        (ready_i_5_1)
);


always@(*) begin
    data_i_5_1[3] = data_o_5_0[4];
    valid_i_5_1[3] = valid_o_5_0[4];
    ready_i_5_1[3] = ready_o_5_0[4];
    data_i_5_1[4] = data_o_5_2[3];
    valid_i_5_1[4] = valid_o_5_2[3];
    ready_i_5_1[4] = ready_o_5_2[3];
    data_i_5_1[1] = data_o_4_1[2];
    valid_i_5_1[1] = valid_o_4_1[2];
    ready_i_5_1[1] = ready_o_4_1[2];
    data_i_5_1[2] = data_o_6_1[1];
    valid_i_5_1[2] = valid_o_6_1[1];
    ready_i_5_1[2] = ready_o_6_1[1];
    data_i_5_1[0] = data_i[5][1];
    valid_i_5_1[0] = valid_i[5][1];
    ready_i_5_1[0] = ready_i[5][1];
end


/*Router 5,2*/    
merge_router #(
    .input_mask                     (input_mask_5_2),
    .output_sel                     (output_sel_5_2)
)router19(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_5_2),
    .valid_i                        (valid_i_5_2),
    .ready_o                        (ready_o_5_2),
    .data_o                         (data_o_5_2),
    .valid_o                        (valid_o_5_2),
    .ready_i                        (ready_i_5_2)
);


always@(*) begin
    data_i_5_2[3] = data_o_5_1[4];
    valid_i_5_2[3] = valid_o_5_1[4];
    ready_i_5_2[3] = ready_o_5_1[4];
    data_i_5_2[4] = data_o_5_3[3];
    valid_i_5_2[4] = valid_o_5_3[3];
    ready_i_5_2[4] = ready_o_5_3[3];
    data_i_5_2[1] = data_o_4_2[2];
    valid_i_5_2[1] = valid_o_4_2[2];
    ready_i_5_2[1] = ready_o_4_2[2];
    data_i_5_2[2] = data_o_6_2[1];
    valid_i_5_2[2] = valid_o_6_2[1];
    ready_i_5_2[2] = ready_o_6_2[1];
    data_i_5_2[0] = data_i[5][2];
    valid_i_5_2[0] = valid_i[5][2];
    ready_i_5_2[0] = ready_i[5][2];
end


/*Router 5,3*/    
merge_router #(
    .input_mask                     (input_mask_5_3),
    .output_sel                     (output_sel_5_3)
)router26(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_5_3),
    .valid_i                        (valid_i_5_3),
    .ready_o                        (ready_o_5_3),
    .data_o                         (data_o_5_3),
    .valid_o                        (valid_o_5_3),
    .ready_i                        (ready_i_5_3)
);


always@(*) begin
    data_i_5_3[3] = data_o_5_2[4];
    valid_i_5_3[3] = valid_o_5_2[4];
    ready_i_5_3[3] = ready_o_5_2[4];
    data_i_5_3[4] = data_o_5_4[3];
    valid_i_5_3[4] = valid_o_5_4[3];
    ready_i_5_3[4] = ready_o_5_4[3];
    data_i_5_3[1] = data_o_4_3[2];
    valid_i_5_3[1] = valid_o_4_3[2];
    ready_i_5_3[1] = ready_o_4_3[2];
    data_i_5_3[2] = data_o_6_3[1];
    valid_i_5_3[2] = valid_o_6_3[1];
    ready_i_5_3[2] = ready_o_6_3[1];
    data_i_5_3[0] = data_i[5][3];
    valid_i_5_3[0] = valid_i[5][3];
    ready_i_5_3[0] = ready_i[5][3];
end


/*Router 5,4*/    
merge_router #(
    .input_mask                     (input_mask_5_4),
    .output_sel                     (output_sel_5_4)
)router33(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_5_4),
    .valid_i                        (valid_i_5_4),
    .ready_o                        (ready_o_5_4),
    .data_o                         (data_o_5_4),
    .valid_o                        (valid_o_5_4),
    .ready_i                        (ready_i_5_4)
);


always@(*) begin
    data_i_5_4[3] = data_o_5_3[4];
    valid_i_5_4[3] = valid_o_5_3[4];
    ready_i_5_4[3] = ready_o_5_3[4];
    data_i_5_4[4] = data_o_5_5[3];
    valid_i_5_4[4] = valid_o_5_5[3];
    ready_i_5_4[4] = ready_o_5_5[3];
    data_i_5_4[1] = data_o_4_4[2];
    valid_i_5_4[1] = valid_o_4_4[2];
    ready_i_5_4[1] = ready_o_4_4[2];
    data_i_5_4[2] = data_o_6_4[1];
    valid_i_5_4[2] = valid_o_6_4[1];
    ready_i_5_4[2] = ready_o_6_4[1];
    data_i_5_4[0] = data_i[5][4];
    valid_i_5_4[0] = valid_i[5][4];
    ready_i_5_4[0] = ready_i[5][4];
end


/*Router 5,5*/    
merge_router #(
    .input_mask                     (input_mask_5_5),
    .output_sel                     (output_sel_5_5)
)router40(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_5_5),
    .valid_i                        (valid_i_5_5),
    .ready_o                        (ready_o_5_5),
    .data_o                         (data_o_5_5),
    .valid_o                        (valid_o_5_5),
    .ready_i                        (ready_i_5_5)
);


always@(*) begin
    data_i_5_5[3] = data_o_5_4[4];
    valid_i_5_5[3] = valid_o_5_4[4];
    ready_i_5_5[3] = ready_o_5_4[4];
    data_i_5_5[4] = data_o_5_6[3];
    valid_i_5_5[4] = valid_o_5_6[3];
    ready_i_5_5[4] = ready_o_5_6[3];
    data_i_5_5[1] = data_o_4_5[2];
    valid_i_5_5[1] = valid_o_4_5[2];
    ready_i_5_5[1] = ready_o_4_5[2];
    data_i_5_5[2] = data_o_6_5[1];
    valid_i_5_5[2] = valid_o_6_5[1];
    ready_i_5_5[2] = ready_o_6_5[1];
    data_i_5_5[0] = data_i[5][5];
    valid_i_5_5[0] = valid_i[5][5];
    ready_i_5_5[0] = ready_i[5][5];
end


/*Router 5,6*/    
merge_router #(
    .input_mask                     (input_mask_5_6),
    .output_sel                     (output_sel_5_6)
)router47(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_5_6),
    .valid_i                        (valid_i_5_6),
    .ready_o                        (ready_o_5_6),
    .data_o                         (data_o_5_6),
    .valid_o                        (valid_o_5_6),
    .ready_i                        (ready_i_5_6)
);


always@(*) begin
    data_i_5_6[3] = data_o_5_5[4];
    valid_i_5_6[3] = valid_o_5_5[4];
    ready_i_5_6[3] = ready_o_5_5[4];
    data_i_5_6[4] = data_o_5_7[3];
    valid_i_5_6[4] = valid_o_5_7[3];
    ready_i_5_6[4] = ready_o_5_7[3];
    data_i_5_6[1] = data_o_4_6[2];
    valid_i_5_6[1] = valid_o_4_6[2];
    ready_i_5_6[1] = ready_o_4_6[2];
    data_i_5_6[2] = data_o_6_6[1];
    valid_i_5_6[2] = valid_o_6_6[1];
    ready_i_5_6[2] = ready_o_6_6[1];
    data_i_5_6[0] = data_i[5][6];
    valid_i_5_6[0] = valid_i[5][6];
    ready_i_5_6[0] = ready_i[5][6];
end


/*Router 5,7*/    
merge_router #(
    .input_mask                     (input_mask_5_7),
    .output_sel                     (output_sel_5_7)
)router54(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_5_7),
    .valid_i                        (valid_i_5_7),
    .ready_o                        (ready_o_5_7),
    .data_o                         (data_o_5_7),
    .valid_o                        (valid_o_5_7),
    .ready_i                        (ready_i_5_7)
);


always@(*) begin
    data_i_5_7[3] = data_o_5_6[4];
    valid_i_5_7[3] = valid_o_5_6[4];
    ready_i_5_7[3] = ready_o_5_6[4];
    data_i_5_7[1] = data_o_4_7[2];
    valid_i_5_7[1] = valid_o_4_7[2];
    ready_i_5_7[1] = ready_o_4_7[2];
    data_i_5_7[2] = data_o_6_7[1];
    valid_i_5_7[2] = valid_o_6_7[1];
    ready_i_5_7[2] = ready_o_6_7[1];
    data_i_5_7[0] = data_i[5][7];
    valid_i_5_7[0] = valid_i[5][7];
    ready_i_5_7[0] = ready_i[5][7];
end


/*Router 6,0*/    
merge_router #(
    .input_mask                     (input_mask_6_0),
    .output_sel                     (output_sel_6_0)
)router6(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_6_0),
    .valid_i                        (valid_i_6_0),
    .ready_o                        (ready_o_6_0),
    .data_o                         (data_o_6_0),
    .valid_o                        (valid_o_6_0),
    .ready_i                        (ready_i_6_0)
);


always@(*) begin
    data_i_6_0[4] = data_o_6_1[3];
    valid_i_6_0[4] = valid_o_6_1[3];
    ready_i_6_0[4] = ready_o_6_1[3];
    data_i_6_0[1] = data_o_5_0[2];
    valid_i_6_0[1] = valid_o_5_0[2];
    ready_i_6_0[1] = ready_o_5_0[2];
    data_i_6_0[0] = data_i[6][0];
    valid_i_6_0[0] = valid_i[6][0];
    ready_i_6_0[0] = ready_i[6][0];
end


/*Router 6,1*/    
merge_router #(
    .input_mask                     (input_mask_6_1),
    .output_sel                     (output_sel_6_1)
)router13(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_6_1),
    .valid_i                        (valid_i_6_1),
    .ready_o                        (ready_o_6_1),
    .data_o                         (data_o_6_1),
    .valid_o                        (valid_o_6_1),
    .ready_i                        (ready_i_6_1)
);


always@(*) begin
    data_i_6_1[3] = data_o_6_0[4];
    valid_i_6_1[3] = valid_o_6_0[4];
    ready_i_6_1[3] = ready_o_6_0[4];
    data_i_6_1[4] = data_o_6_2[3];
    valid_i_6_1[4] = valid_o_6_2[3];
    ready_i_6_1[4] = ready_o_6_2[3];
    data_i_6_1[1] = data_o_5_1[2];
    valid_i_6_1[1] = valid_o_5_1[2];
    ready_i_6_1[1] = ready_o_5_1[2];
    data_i_6_1[0] = data_i[6][1];
    valid_i_6_1[0] = valid_i[6][1];
    ready_i_6_1[0] = ready_i[6][1];
end


/*Router 6,2*/    
merge_router #(
    .input_mask                     (input_mask_6_2),
    .output_sel                     (output_sel_6_2)
)router20(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_6_2),
    .valid_i                        (valid_i_6_2),
    .ready_o                        (ready_o_6_2),
    .data_o                         (data_o_6_2),
    .valid_o                        (valid_o_6_2),
    .ready_i                        (ready_i_6_2)
);


always@(*) begin
    data_i_6_2[3] = data_o_6_1[4];
    valid_i_6_2[3] = valid_o_6_1[4];
    ready_i_6_2[3] = ready_o_6_1[4];
    data_i_6_2[4] = data_o_6_3[3];
    valid_i_6_2[4] = valid_o_6_3[3];
    ready_i_6_2[4] = ready_o_6_3[3];
    data_i_6_2[1] = data_o_5_2[2];
    valid_i_6_2[1] = valid_o_5_2[2];
    ready_i_6_2[1] = ready_o_5_2[2];
    data_i_6_2[0] = data_i[6][2];
    valid_i_6_2[0] = valid_i[6][2];
    ready_i_6_2[0] = ready_i[6][2];
end


/*Router 6,3*/    
merge_router #(
    .input_mask                     (input_mask_6_3),
    .output_sel                     (output_sel_6_3)
)router27(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_6_3),
    .valid_i                        (valid_i_6_3),
    .ready_o                        (ready_o_6_3),
    .data_o                         (data_o_6_3),
    .valid_o                        (valid_o_6_3),
    .ready_i                        (ready_i_6_3)
);


always@(*) begin
    data_i_6_3[3] = data_o_6_2[4];
    valid_i_6_3[3] = valid_o_6_2[4];
    ready_i_6_3[3] = ready_o_6_2[4];
    data_i_6_3[4] = data_o_6_4[3];
    valid_i_6_3[4] = valid_o_6_4[3];
    ready_i_6_3[4] = ready_o_6_4[3];
    data_i_6_3[1] = data_o_5_3[2];
    valid_i_6_3[1] = valid_o_5_3[2];
    ready_i_6_3[1] = ready_o_5_3[2];
    data_i_6_3[0] = data_i[6][3];
    valid_i_6_3[0] = valid_i[6][3];
    ready_i_6_3[0] = ready_i[6][3];
end


/*Router 6,4*/    
merge_router #(
    .input_mask                     (input_mask_6_4),
    .output_sel                     (output_sel_6_4)
)router34(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_6_4),
    .valid_i                        (valid_i_6_4),
    .ready_o                        (ready_o_6_4),
    .data_o                         (data_o_6_4),
    .valid_o                        (valid_o_6_4),
    .ready_i                        (ready_i_6_4)
);


always@(*) begin
    data_i_6_4[3] = data_o_6_3[4];
    valid_i_6_4[3] = valid_o_6_3[4];
    ready_i_6_4[3] = ready_o_6_3[4];
    data_i_6_4[4] = data_o_6_5[3];
    valid_i_6_4[4] = valid_o_6_5[3];
    ready_i_6_4[4] = ready_o_6_5[3];
    data_i_6_4[1] = data_o_5_4[2];
    valid_i_6_4[1] = valid_o_5_4[2];
    ready_i_6_4[1] = ready_o_5_4[2];
    data_i_6_4[0] = data_i[6][4];
    valid_i_6_4[0] = valid_i[6][4];
    ready_i_6_4[0] = ready_i[6][4];
end


/*Router 6,5*/    
merge_router #(
    .input_mask                     (input_mask_6_5),
    .output_sel                     (output_sel_6_5)
)router41(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_6_5),
    .valid_i                        (valid_i_6_5),
    .ready_o                        (ready_o_6_5),
    .data_o                         (data_o_6_5),
    .valid_o                        (valid_o_6_5),
    .ready_i                        (ready_i_6_5)
);


always@(*) begin
    data_i_6_5[3] = data_o_6_4[4];
    valid_i_6_5[3] = valid_o_6_4[4];
    ready_i_6_5[3] = ready_o_6_4[4];
    data_i_6_5[4] = data_o_6_6[3];
    valid_i_6_5[4] = valid_o_6_6[3];
    ready_i_6_5[4] = ready_o_6_6[3];
    data_i_6_5[1] = data_o_5_5[2];
    valid_i_6_5[1] = valid_o_5_5[2];
    ready_i_6_5[1] = ready_o_5_5[2];
    data_i_6_5[0] = data_i[6][5];
    valid_i_6_5[0] = valid_i[6][5];
    ready_i_6_5[0] = ready_i[6][5];
end


/*Router 6,6*/    
merge_router #(
    .input_mask                     (input_mask_6_6),
    .output_sel                     (output_sel_6_6)
)router48(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_6_6),
    .valid_i                        (valid_i_6_6),
    .ready_o                        (ready_o_6_6),
    .data_o                         (data_o_6_6),
    .valid_o                        (valid_o_6_6),
    .ready_i                        (ready_i_6_6)
);


always@(*) begin
    data_i_6_6[3] = data_o_6_5[4];
    valid_i_6_6[3] = valid_o_6_5[4];
    ready_i_6_6[3] = ready_o_6_5[4];
    data_i_6_6[4] = data_o_6_7[3];
    valid_i_6_6[4] = valid_o_6_7[3];
    ready_i_6_6[4] = ready_o_6_7[3];
    data_i_6_6[1] = data_o_5_6[2];
    valid_i_6_6[1] = valid_o_5_6[2];
    ready_i_6_6[1] = ready_o_5_6[2];
    data_i_6_6[0] = data_i[6][6];
    valid_i_6_6[0] = valid_i[6][6];
    ready_i_6_6[0] = ready_i[6][6];
end


/*Router 6,7*/    
merge_router #(
    .input_mask                     (input_mask_6_7),
    .output_sel                     (output_sel_6_7)
)router55(
    .clk                            (clk),
    .rstn                           (rstn),
    .data_i                         (data_i_6_7),
    .valid_i                        (valid_i_6_7),
    .ready_o                        (ready_o_6_7),
    .data_o                         (data_o_6_7),
    .valid_o                        (valid_o_6_7),
    .ready_i                        (ready_i_6_7)
);


always@(*) begin
    data_i_6_7[3] = data_o_6_6[4];
    valid_i_6_7[3] = valid_o_6_6[4];
    ready_i_6_7[3] = ready_o_6_6[4];
    data_i_6_7[1] = data_o_5_7[2];
    valid_i_6_7[1] = valid_o_5_7[2];
    ready_i_6_7[1] = ready_o_5_7[2];
    data_i_6_7[0] = data_i[6][7];
    valid_i_6_7[0] = valid_i[6][7];
    ready_i_6_7[0] = ready_i[6][7];
end


endmodule
