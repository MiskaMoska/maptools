//Cast Network
//Width: 3
//Height:3
`include "params.svh"
`include "cast_network_config.svh"

module cast_network(
    input       wire                            clk,
    input       wire                            rstn,
    
    //router local ports
    input       wire        [`DW-1:0]           data_i[`NOC_WIDTH][`NOC_HEIGHT],
    input       wire                            valid_i[`NOC_WIDTH][`NOC_HEIGHT],
    output      wire                            ready_o[`NOC_WIDTH][`NOC_HEIGHT],

    output      wire        [`DW-1:0]           data_o[`NOC_WIDTH][`NOC_HEIGHT],
    output      wire                            valid_o[`NOC_WIDTH][`NOC_HEIGHT],
    input       wire                            ready_i[`NOC_WIDTH][`NOC_HEIGHT],

    //credit update signal input
    input       wire                            credit_upd[`NOC_WIDTH][`NOC_HEIGHT]
);

//horizontal signals
wire    [`DW-1:0]   data_0_to_1,	data_1_to_0;
wire                valid_0_to_1,	valid_1_to_0;
wire                ready_0_to_1,	ready_1_to_0;
wire    [`DW-1:0]   data_1_to_2,	data_2_to_1;
wire                valid_1_to_2,	valid_2_to_1;
wire                ready_1_to_2,	ready_2_to_1;
wire    [`DW-1:0]   data_3_to_4,	data_4_to_3;
wire                valid_3_to_4,	valid_4_to_3;
wire                ready_3_to_4,	ready_4_to_3;
wire    [`DW-1:0]   data_4_to_5,	data_5_to_4;
wire                valid_4_to_5,	valid_5_to_4;
wire                ready_4_to_5,	ready_5_to_4;
wire    [`DW-1:0]   data_6_to_7,	data_7_to_6;
wire                valid_6_to_7,	valid_7_to_6;
wire                ready_6_to_7,	ready_7_to_6;
wire    [`DW-1:0]   data_7_to_8,	data_8_to_7;
wire                valid_7_to_8,	valid_8_to_7;
wire                ready_7_to_8,	ready_8_to_7;

//vertical signals
wire    [`DW-1:0]   data_0_to_3_v0,	data_0_to_3_v1;
wire                valid_0_to_3_v0,	valid_0_to_3_v1;
wire                ready_3_to_0_v0,	ready_3_to_0_v1;
wire    [`DW-1:0]   data_3_to_6_v0,	data_3_to_6_v1;
wire                valid_3_to_6_v0,	valid_3_to_6_v1;
wire                ready_6_to_3_v0,	ready_6_to_3_v1;
wire    [`DW-1:0]   data_1_to_4_v0,	data_1_to_4_v1;
wire                valid_1_to_4_v0,	valid_1_to_4_v1;
wire                ready_4_to_1_v0,	ready_4_to_1_v1;
wire    [`DW-1:0]   data_4_to_7_v0,	data_4_to_7_v1;
wire                valid_4_to_7_v0,	valid_4_to_7_v1;
wire                ready_7_to_4_v0,	ready_7_to_4_v1;
wire    [`DW-1:0]   data_2_to_5_v0,	data_2_to_5_v1;
wire                valid_2_to_5_v0,	valid_2_to_5_v1;
wire                ready_5_to_2_v0,	ready_5_to_2_v1;
wire    [`DW-1:0]   data_5_to_8_v0,	data_5_to_8_v1;
wire                valid_5_to_8_v0,	valid_5_to_8_v1;
wire                ready_8_to_5_v0,	ready_8_to_5_v1;

/*Router 0,0*/    
cast_router #(
    .isFC_list               (isFC_list_0_0),
    .FCdn_list               (FCdn_list_0_0),
    .FCpl_list               (FCpl_list_0_0),
    .rt_file_list            (rt_file_list_0_0)
)router0(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (16'b0),
    .west_valid_i          (1'b0),
    .west_ready_o          (),
    .west_data_o           (),
    .west_valid_o          (),
    .west_ready_i          (1'b0),
    .east_data_i           (data_1_to_0),
    .east_valid_i          (valid_1_to_0),
    .east_ready_o          (ready_0_to_1),
    .east_data_o           (data_0_to_1),
    .east_valid_o          (valid_0_to_1),
    .east_ready_i          (ready_1_to_0),
    .vert0_data_i          (16'b0),
    .vert0_valid_i         (1'b0),
    .vert0_ready_o         (),
    .vert0_data_o          (data_0_to_3_v0),
    .vert0_valid_o         (valid_0_to_3_v0),
    .vert0_ready_i         (ready_3_to_0_v0),
    .vert1_data_i          (16'b0),
    .vert1_valid_i         (1'b0),
    .vert1_ready_o         (),
    .vert1_data_o          (data_0_to_3_v1),
    .vert1_valid_o         (valid_0_to_3_v1),
    .vert1_ready_i         (ready_3_to_0_v1),
    .local_data_i          (data_i[0][0]),
    .local_valid_i         (valid_i[0][0]),
    .local_ready_o         (ready_o[0][0]),
    .local_data_o          (data_o[0][0]),
    .local_valid_o         (valid_o[0][0]),
    .local_ready_i         (ready_i[0][0]),
    .credit_upd            (credit_upd)
);

/*Router 0,1*/    
cast_router #(
    .isFC_list               (isFC_list_0_1),
    .FCdn_list               (FCdn_list_0_1),
    .FCpl_list               (FCpl_list_0_1),
    .rt_file_list            (rt_file_list_0_1)
)router3(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (16'b0),
    .west_valid_i          (1'b0),
    .west_ready_o          (),
    .west_data_o           (),
    .west_valid_o          (),
    .west_ready_i          (1'b0),
    .east_data_i           (data_4_to_3),
    .east_valid_i          (valid_4_to_3),
    .east_ready_o          (ready_3_to_4),
    .east_data_o           (data_3_to_4),
    .east_valid_o          (valid_3_to_4),
    .east_ready_i          (ready_4_to_3),
    .vert0_data_i          (data_0_to_3_v0),
    .vert0_valid_i         (valid_0_to_3_v0),
    .vert0_ready_o         (ready_3_to_0_v0),
    .vert0_data_o          (data_3_to_6_v0),
    .vert0_valid_o         (valid_3_to_6_v0),
    .vert0_ready_i         (ready_6_to_3_v0),
    .vert1_data_i          (data_0_to_3_v1),
    .vert1_valid_i         (valid_0_to_3_v1),
    .vert1_ready_o         (ready_3_to_0_v1),
    .vert1_data_o          (data_3_to_6_v1),
    .vert1_valid_o         (valid_3_to_6_v1),
    .vert1_ready_i         (ready_6_to_3_v1),
    .local_data_i          (data_i[0][1]),
    .local_valid_i         (valid_i[0][1]),
    .local_ready_o         (ready_o[0][1]),
    .local_data_o          (data_o[0][1]),
    .local_valid_o         (valid_o[0][1]),
    .local_ready_i         (ready_i[0][1]),
    .credit_upd            (credit_upd)
);

/*Router 0,2*/    
cast_router #(
    .isFC_list               (isFC_list_0_2),
    .FCdn_list               (FCdn_list_0_2),
    .FCpl_list               (FCpl_list_0_2),
    .rt_file_list            (rt_file_list_0_2)
)router6(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (16'b0),
    .west_valid_i          (1'b0),
    .west_ready_o          (),
    .west_data_o           (),
    .west_valid_o          (),
    .west_ready_i          (1'b0),
    .east_data_i           (data_7_to_6),
    .east_valid_i          (valid_7_to_6),
    .east_ready_o          (ready_6_to_7),
    .east_data_o           (data_6_to_7),
    .east_valid_o          (valid_6_to_7),
    .east_ready_i          (ready_7_to_6),
    .vert0_data_i          (data_3_to_6_v0),
    .vert0_valid_i         (valid_3_to_6_v0),
    .vert0_ready_o         (ready_6_to_3_v0),
    .vert0_data_o          (),
    .vert0_valid_o         (),
    .vert0_ready_i         (1'b0),
    .vert1_data_i          (data_3_to_6_v1),
    .vert1_valid_i         (valid_3_to_6_v1),
    .vert1_ready_o         (ready_6_to_3_v1),
    .vert1_data_o          (),
    .vert1_valid_o         (),
    .vert1_ready_i         (1'b0),
    .local_data_i          (data_i[0][2]),
    .local_valid_i         (valid_i[0][2]),
    .local_ready_o         (ready_o[0][2]),
    .local_data_o          (data_o[0][2]),
    .local_valid_o         (valid_o[0][2]),
    .local_ready_i         (ready_i[0][2]),
    .credit_upd            (credit_upd)
);

/*Router 1,0*/    
cast_router #(
    .isFC_list               (isFC_list_1_0),
    .FCdn_list               (FCdn_list_1_0),
    .FCpl_list               (FCpl_list_1_0),
    .rt_file_list            (rt_file_list_1_0)
)router1(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_0_to_1),
    .west_valid_i          (valid_0_to_1),
    .west_ready_o          (ready_1_to_0),
    .west_data_o           (data_1_to_0),
    .west_valid_o          (valid_1_to_0),
    .west_ready_i          (ready_0_to_1),
    .east_data_i           (data_2_to_1),
    .east_valid_i          (valid_2_to_1),
    .east_ready_o          (ready_1_to_2),
    .east_data_o           (data_1_to_2),
    .east_valid_o          (valid_1_to_2),
    .east_ready_i          (ready_2_to_1),
    .vert0_data_i          (16'b0),
    .vert0_valid_i         (1'b0),
    .vert0_ready_o         (),
    .vert0_data_o          (data_1_to_4_v0),
    .vert0_valid_o         (valid_1_to_4_v0),
    .vert0_ready_i         (ready_4_to_1_v0),
    .vert1_data_i          (16'b0),
    .vert1_valid_i         (1'b0),
    .vert1_ready_o         (),
    .vert1_data_o          (data_1_to_4_v1),
    .vert1_valid_o         (valid_1_to_4_v1),
    .vert1_ready_i         (ready_4_to_1_v1),
    .local_data_i          (data_i[1][0]),
    .local_valid_i         (valid_i[1][0]),
    .local_ready_o         (ready_o[1][0]),
    .local_data_o          (data_o[1][0]),
    .local_valid_o         (valid_o[1][0]),
    .local_ready_i         (ready_i[1][0]),
    .credit_upd            (credit_upd)
);

/*Router 1,1*/    
cast_router #(
    .isFC_list               (isFC_list_1_1),
    .FCdn_list               (FCdn_list_1_1),
    .FCpl_list               (FCpl_list_1_1),
    .rt_file_list            (rt_file_list_1_1)
)router4(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_3_to_4),
    .west_valid_i          (valid_3_to_4),
    .west_ready_o          (ready_4_to_3),
    .west_data_o           (data_4_to_3),
    .west_valid_o          (valid_4_to_3),
    .west_ready_i          (ready_3_to_4),
    .east_data_i           (data_5_to_4),
    .east_valid_i          (valid_5_to_4),
    .east_ready_o          (ready_4_to_5),
    .east_data_o           (data_4_to_5),
    .east_valid_o          (valid_4_to_5),
    .east_ready_i          (ready_5_to_4),
    .vert0_data_i          (data_1_to_4_v0),
    .vert0_valid_i         (valid_1_to_4_v0),
    .vert0_ready_o         (ready_4_to_1_v0),
    .vert0_data_o          (data_4_to_7_v0),
    .vert0_valid_o         (valid_4_to_7_v0),
    .vert0_ready_i         (ready_7_to_4_v0),
    .vert1_data_i          (data_1_to_4_v1),
    .vert1_valid_i         (valid_1_to_4_v1),
    .vert1_ready_o         (ready_4_to_1_v1),
    .vert1_data_o          (data_4_to_7_v1),
    .vert1_valid_o         (valid_4_to_7_v1),
    .vert1_ready_i         (ready_7_to_4_v1),
    .local_data_i          (data_i[1][1]),
    .local_valid_i         (valid_i[1][1]),
    .local_ready_o         (ready_o[1][1]),
    .local_data_o          (data_o[1][1]),
    .local_valid_o         (valid_o[1][1]),
    .local_ready_i         (ready_i[1][1]),
    .credit_upd            (credit_upd)
);

/*Router 1,2*/    
cast_router #(
    .isFC_list               (isFC_list_1_2),
    .FCdn_list               (FCdn_list_1_2),
    .FCpl_list               (FCpl_list_1_2),
    .rt_file_list            (rt_file_list_1_2)
)router7(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_6_to_7),
    .west_valid_i          (valid_6_to_7),
    .west_ready_o          (ready_7_to_6),
    .west_data_o           (data_7_to_6),
    .west_valid_o          (valid_7_to_6),
    .west_ready_i          (ready_6_to_7),
    .east_data_i           (data_8_to_7),
    .east_valid_i          (valid_8_to_7),
    .east_ready_o          (ready_7_to_8),
    .east_data_o           (data_7_to_8),
    .east_valid_o          (valid_7_to_8),
    .east_ready_i          (ready_8_to_7),
    .vert0_data_i          (data_4_to_7_v0),
    .vert0_valid_i         (valid_4_to_7_v0),
    .vert0_ready_o         (ready_7_to_4_v0),
    .vert0_data_o          (),
    .vert0_valid_o         (),
    .vert0_ready_i         (1'b0),
    .vert1_data_i          (data_4_to_7_v1),
    .vert1_valid_i         (valid_4_to_7_v1),
    .vert1_ready_o         (ready_7_to_4_v1),
    .vert1_data_o          (),
    .vert1_valid_o         (),
    .vert1_ready_i         (1'b0),
    .local_data_i          (data_i[1][2]),
    .local_valid_i         (valid_i[1][2]),
    .local_ready_o         (ready_o[1][2]),
    .local_data_o          (data_o[1][2]),
    .local_valid_o         (valid_o[1][2]),
    .local_ready_i         (ready_i[1][2]),
    .credit_upd            (credit_upd)
);

/*Router 2,0*/    
cast_router #(
    .isFC_list               (isFC_list_2_0),
    .FCdn_list               (FCdn_list_2_0),
    .FCpl_list               (FCpl_list_2_0),
    .rt_file_list            (rt_file_list_2_0)
)router2(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_1_to_2),
    .west_valid_i          (valid_1_to_2),
    .west_ready_o          (ready_2_to_1),
    .west_data_o           (data_2_to_1),
    .west_valid_o          (valid_2_to_1),
    .west_ready_i          (ready_1_to_2),
    .east_data_i           (16'b0),
    .east_valid_i          (1'b0),
    .east_ready_o          (),
    .east_data_o           (),
    .east_valid_o          (),
    .east_ready_i          (1'b0),
    .vert0_data_i          (16'b0),
    .vert0_valid_i         (1'b0),
    .vert0_ready_o         (),
    .vert0_data_o          (data_2_to_5_v0),
    .vert0_valid_o         (valid_2_to_5_v0),
    .vert0_ready_i         (ready_5_to_2_v0),
    .vert1_data_i          (16'b0),
    .vert1_valid_i         (1'b0),
    .vert1_ready_o         (),
    .vert1_data_o          (data_2_to_5_v1),
    .vert1_valid_o         (valid_2_to_5_v1),
    .vert1_ready_i         (ready_5_to_2_v1),
    .local_data_i          (data_i[2][0]),
    .local_valid_i         (valid_i[2][0]),
    .local_ready_o         (ready_o[2][0]),
    .local_data_o          (data_o[2][0]),
    .local_valid_o         (valid_o[2][0]),
    .local_ready_i         (ready_i[2][0]),
    .credit_upd            (credit_upd)
);

/*Router 2,1*/    
cast_router #(
    .isFC_list               (isFC_list_2_1),
    .FCdn_list               (FCdn_list_2_1),
    .FCpl_list               (FCpl_list_2_1),
    .rt_file_list            (rt_file_list_2_1)
)router5(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_4_to_5),
    .west_valid_i          (valid_4_to_5),
    .west_ready_o          (ready_5_to_4),
    .west_data_o           (data_5_to_4),
    .west_valid_o          (valid_5_to_4),
    .west_ready_i          (ready_4_to_5),
    .east_data_i           (16'b0),
    .east_valid_i          (1'b0),
    .east_ready_o          (),
    .east_data_o           (),
    .east_valid_o          (),
    .east_ready_i          (1'b0),
    .vert0_data_i          (data_2_to_5_v0),
    .vert0_valid_i         (valid_2_to_5_v0),
    .vert0_ready_o         (ready_5_to_2_v0),
    .vert0_data_o          (data_5_to_8_v0),
    .vert0_valid_o         (valid_5_to_8_v0),
    .vert0_ready_i         (ready_8_to_5_v0),
    .vert1_data_i          (data_2_to_5_v1),
    .vert1_valid_i         (valid_2_to_5_v1),
    .vert1_ready_o         (ready_5_to_2_v1),
    .vert1_data_o          (data_5_to_8_v1),
    .vert1_valid_o         (valid_5_to_8_v1),
    .vert1_ready_i         (ready_8_to_5_v1),
    .local_data_i          (data_i[2][1]),
    .local_valid_i         (valid_i[2][1]),
    .local_ready_o         (ready_o[2][1]),
    .local_data_o          (data_o[2][1]),
    .local_valid_o         (valid_o[2][1]),
    .local_ready_i         (ready_i[2][1]),
    .credit_upd            (credit_upd)
);

/*Router 2,2*/    
cast_router #(
    .isFC_list               (isFC_list_2_2),
    .FCdn_list               (FCdn_list_2_2),
    .FCpl_list               (FCpl_list_2_2),
    .rt_file_list            (rt_file_list_2_2)
)router8(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_7_to_8),
    .west_valid_i          (valid_7_to_8),
    .west_ready_o          (ready_8_to_7),
    .west_data_o           (data_8_to_7),
    .west_valid_o          (valid_8_to_7),
    .west_ready_i          (ready_7_to_8),
    .east_data_i           (16'b0),
    .east_valid_i          (1'b0),
    .east_ready_o          (),
    .east_data_o           (),
    .east_valid_o          (),
    .east_ready_i          (1'b0),
    .vert0_data_i          (data_5_to_8_v0),
    .vert0_valid_i         (valid_5_to_8_v0),
    .vert0_ready_o         (ready_8_to_5_v0),
    .vert0_data_o          (),
    .vert0_valid_o         (),
    .vert0_ready_i         (1'b0),
    .vert1_data_i          (data_5_to_8_v1),
    .vert1_valid_i         (valid_5_to_8_v1),
    .vert1_ready_o         (ready_8_to_5_v1),
    .vert1_data_o          (),
    .vert1_valid_o         (),
    .vert1_ready_i         (1'b0),
    .local_data_i          (data_i[2][2]),
    .local_valid_i         (valid_i[2][2]),
    .local_ready_o         (ready_o[2][2]),
    .local_data_o          (data_o[2][2]),
    .local_valid_o         (valid_o[2][2]),
    .local_ready_i         (ready_i[2][2]),
    .credit_upd            (credit_upd)
);

endmodule
