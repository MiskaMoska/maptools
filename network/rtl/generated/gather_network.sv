
//Gather Network
//Width: 5
//Height:6
`include "params.svh"
`include "gather_config.svh"

module gather_network(
input       wire                            clk,
input       wire                            rstn,

//router local ports
input       wire        [`DW-1:0]           data_i[`NOC_WIDTH][`NOC_HEIGHT],
input       wire                            valid_i[`NOC_WIDTH][`NOC_HEIGHT],
output      wire                            ready_o[`NOC_WIDTH][`NOC_HEIGHT],

output      wire        [`DW-1:0]           data_o[`NOC_WIDTH][`NOC_HEIGHT],
output      wire                            valid_o[`NOC_WIDTH][`NOC_HEIGHT],
input       wire                            ready_i[`NOC_WIDTH][`NOC_HEIGHT]);

//horizontal signals
wire    [`DW-1:0]   data_0_to_1,	data_1_to_0;
wire                valid_0_to_1,	valid_1_to_0;
wire                ready_0_to_1,	ready_1_to_0;
wire    [`DW-1:0]   data_1_to_2,	data_2_to_1;
wire                valid_1_to_2,	valid_2_to_1;
wire                ready_1_to_2,	ready_2_to_1;
wire    [`DW-1:0]   data_2_to_3,	data_3_to_2;
wire                valid_2_to_3,	valid_3_to_2;
wire                ready_2_to_3,	ready_3_to_2;
wire    [`DW-1:0]   data_3_to_4,	data_4_to_3;
wire                valid_3_to_4,	valid_4_to_3;
wire                ready_3_to_4,	ready_4_to_3;
wire    [`DW-1:0]   data_5_to_6,	data_6_to_5;
wire                valid_5_to_6,	valid_6_to_5;
wire                ready_5_to_6,	ready_6_to_5;
wire    [`DW-1:0]   data_6_to_7,	data_7_to_6;
wire                valid_6_to_7,	valid_7_to_6;
wire                ready_6_to_7,	ready_7_to_6;
wire    [`DW-1:0]   data_7_to_8,	data_8_to_7;
wire                valid_7_to_8,	valid_8_to_7;
wire                ready_7_to_8,	ready_8_to_7;
wire    [`DW-1:0]   data_8_to_9,	data_9_to_8;
wire                valid_8_to_9,	valid_9_to_8;
wire                ready_8_to_9,	ready_9_to_8;
wire    [`DW-1:0]   data_10_to_11,	data_11_to_10;
wire                valid_10_to_11,	valid_11_to_10;
wire                ready_10_to_11,	ready_11_to_10;
wire    [`DW-1:0]   data_11_to_12,	data_12_to_11;
wire                valid_11_to_12,	valid_12_to_11;
wire                ready_11_to_12,	ready_12_to_11;
wire    [`DW-1:0]   data_12_to_13,	data_13_to_12;
wire                valid_12_to_13,	valid_13_to_12;
wire                ready_12_to_13,	ready_13_to_12;
wire    [`DW-1:0]   data_13_to_14,	data_14_to_13;
wire                valid_13_to_14,	valid_14_to_13;
wire                ready_13_to_14,	ready_14_to_13;
wire    [`DW-1:0]   data_15_to_16,	data_16_to_15;
wire                valid_15_to_16,	valid_16_to_15;
wire                ready_15_to_16,	ready_16_to_15;
wire    [`DW-1:0]   data_16_to_17,	data_17_to_16;
wire                valid_16_to_17,	valid_17_to_16;
wire                ready_16_to_17,	ready_17_to_16;
wire    [`DW-1:0]   data_17_to_18,	data_18_to_17;
wire                valid_17_to_18,	valid_18_to_17;
wire                ready_17_to_18,	ready_18_to_17;
wire    [`DW-1:0]   data_18_to_19,	data_19_to_18;
wire                valid_18_to_19,	valid_19_to_18;
wire                ready_18_to_19,	ready_19_to_18;
wire    [`DW-1:0]   data_20_to_21,	data_21_to_20;
wire                valid_20_to_21,	valid_21_to_20;
wire                ready_20_to_21,	ready_21_to_20;
wire    [`DW-1:0]   data_21_to_22,	data_22_to_21;
wire                valid_21_to_22,	valid_22_to_21;
wire                ready_21_to_22,	ready_22_to_21;
wire    [`DW-1:0]   data_22_to_23,	data_23_to_22;
wire                valid_22_to_23,	valid_23_to_22;
wire                ready_22_to_23,	ready_23_to_22;
wire    [`DW-1:0]   data_23_to_24,	data_24_to_23;
wire                valid_23_to_24,	valid_24_to_23;
wire                ready_23_to_24,	ready_24_to_23;
wire    [`DW-1:0]   data_25_to_26,	data_26_to_25;
wire                valid_25_to_26,	valid_26_to_25;
wire                ready_25_to_26,	ready_26_to_25;
wire    [`DW-1:0]   data_26_to_27,	data_27_to_26;
wire                valid_26_to_27,	valid_27_to_26;
wire                ready_26_to_27,	ready_27_to_26;
wire    [`DW-1:0]   data_27_to_28,	data_28_to_27;
wire                valid_27_to_28,	valid_28_to_27;
wire                ready_27_to_28,	ready_28_to_27;
wire    [`DW-1:0]   data_28_to_29,	data_29_to_28;
wire                valid_28_to_29,	valid_29_to_28;
wire                ready_28_to_29,	ready_29_to_28;

//vertical signals
wire    [`DW-1:0]   data_0_to_5;	data_5_to_0;
wire                valid_0_to_5;	valid_5_to_0;
wire                ready_5_to_0;	ready_0_to_5;
wire    [`DW-1:0]   data_5_to_10;	data_10_to_5;
wire                valid_5_to_10;	valid_10_to_5;
wire                ready_10_to_5;	ready_5_to_10;
wire    [`DW-1:0]   data_10_to_15;	data_15_to_10;
wire                valid_10_to_15;	valid_15_to_10;
wire                ready_15_to_10;	ready_10_to_15;
wire    [`DW-1:0]   data_15_to_20;	data_20_to_15;
wire                valid_15_to_20;	valid_20_to_15;
wire                ready_20_to_15;	ready_15_to_20;
wire    [`DW-1:0]   data_20_to_25;	data_25_to_20;
wire                valid_20_to_25;	valid_25_to_20;
wire                ready_25_to_20;	ready_20_to_25;
wire    [`DW-1:0]   data_1_to_6;	data_6_to_1;
wire                valid_1_to_6;	valid_6_to_1;
wire                ready_6_to_1;	ready_1_to_6;
wire    [`DW-1:0]   data_6_to_11;	data_11_to_6;
wire                valid_6_to_11;	valid_11_to_6;
wire                ready_11_to_6;	ready_6_to_11;
wire    [`DW-1:0]   data_11_to_16;	data_16_to_11;
wire                valid_11_to_16;	valid_16_to_11;
wire                ready_16_to_11;	ready_11_to_16;
wire    [`DW-1:0]   data_16_to_21;	data_21_to_16;
wire                valid_16_to_21;	valid_21_to_16;
wire                ready_21_to_16;	ready_16_to_21;
wire    [`DW-1:0]   data_21_to_26;	data_26_to_21;
wire                valid_21_to_26;	valid_26_to_21;
wire                ready_26_to_21;	ready_21_to_26;
wire    [`DW-1:0]   data_2_to_7;	data_7_to_2;
wire                valid_2_to_7;	valid_7_to_2;
wire                ready_7_to_2;	ready_2_to_7;
wire    [`DW-1:0]   data_7_to_12;	data_12_to_7;
wire                valid_7_to_12;	valid_12_to_7;
wire                ready_12_to_7;	ready_7_to_12;
wire    [`DW-1:0]   data_12_to_17;	data_17_to_12;
wire                valid_12_to_17;	valid_17_to_12;
wire                ready_17_to_12;	ready_12_to_17;
wire    [`DW-1:0]   data_17_to_22;	data_22_to_17;
wire                valid_17_to_22;	valid_22_to_17;
wire                ready_22_to_17;	ready_17_to_22;
wire    [`DW-1:0]   data_22_to_27;	data_27_to_22;
wire                valid_22_to_27;	valid_27_to_22;
wire                ready_27_to_22;	ready_22_to_27;
wire    [`DW-1:0]   data_3_to_8;	data_8_to_3;
wire                valid_3_to_8;	valid_8_to_3;
wire                ready_8_to_3;	ready_3_to_8;
wire    [`DW-1:0]   data_8_to_13;	data_13_to_8;
wire                valid_8_to_13;	valid_13_to_8;
wire                ready_13_to_8;	ready_8_to_13;
wire    [`DW-1:0]   data_13_to_18;	data_18_to_13;
wire                valid_13_to_18;	valid_18_to_13;
wire                ready_18_to_13;	ready_13_to_18;
wire    [`DW-1:0]   data_18_to_23;	data_23_to_18;
wire                valid_18_to_23;	valid_23_to_18;
wire                ready_23_to_18;	ready_18_to_23;
wire    [`DW-1:0]   data_23_to_28;	data_28_to_23;
wire                valid_23_to_28;	valid_28_to_23;
wire                ready_28_to_23;	ready_23_to_28;
wire    [`DW-1:0]   data_4_to_9;	data_9_to_4;
wire                valid_4_to_9;	valid_9_to_4;
wire                ready_9_to_4;	ready_4_to_9;
wire    [`DW-1:0]   data_9_to_14;	data_14_to_9;
wire                valid_9_to_14;	valid_14_to_9;
wire                ready_14_to_9;	ready_9_to_14;
wire    [`DW-1:0]   data_14_to_19;	data_19_to_14;
wire                valid_14_to_19;	valid_19_to_14;
wire                ready_19_to_14;	ready_14_to_19;
wire    [`DW-1:0]   data_19_to_24;	data_24_to_19;
wire                valid_19_to_24;	valid_24_to_19;
wire                ready_24_to_19;	ready_19_to_24;
wire    [`DW-1:0]   data_24_to_29;	data_29_to_24;
wire                valid_24_to_29;	valid_29_to_24;
wire                ready_29_to_24;	ready_24_to_29;

/*Router 0,0*/    
gather_router #(
    .rt_file_list          (rt_file_list_0_0)
)router_0_0(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (34'b0),
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
    .north_data_i          (34'b0),
    .north_valid_i         (1'b0),
    .north_ready_o         (),
    .north_data_o          (),
    .north_valid_o         (),
    .north_ready_i         (1'b0),
    .south_data_i          (data_5_to_0_v0),
    .south_valid_i         (valid_5_to_0_v0),
    .south_ready_o         (ready_0_to_5_v0),
    .south_data_o          (data_0_to_5_v1),
    .south_valid_o         (valid_0_to_5_v1),
    .south_ready_i         (ready_5_to_0_v1),
    .local_data_i          (data_i[0][0]),
    .local_valid_i         (valid_i[0][0]),
    .local_ready_o         (ready_o[0][0]),
    .local_data_o          (data_o[0][0]),
    .local_valid_o         (valid_o[0][0]),
    .local_ready_i         (ready_i[0][0])
);

/*Router 0,1*/    
gather_router #(
    .rt_file_list          (rt_file_list_0_1)
)router_0_1(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (34'b0),
    .west_valid_i          (1'b0),
    .west_ready_o          (),
    .west_data_o           (),
    .west_valid_o          (),
    .west_ready_i          (1'b0),
    .east_data_i           (data_6_to_5),
    .east_valid_i          (valid_6_to_5),
    .east_ready_o          (ready_5_to_6),
    .east_data_o           (data_5_to_6),
    .east_valid_o          (valid_5_to_6),
    .east_ready_i          (ready_6_to_5),
    .north_data_i          (data_0_to_5),
    .north_valid_i         (valid_0_to_5),
    .north_ready_o         (ready_5_to_0),
    .north_data_o          (data_5_to_0),
    .north_valid_o         (valid_5_to_0),
    .north_ready_i         (ready_0_to_5),
    .south_data_i          (data_10_to_5_v0),
    .south_valid_i         (valid_10_to_5_v0),
    .south_ready_o         (ready_5_to_10_v0),
    .south_data_o          (data_5_to_10_v1),
    .south_valid_o         (valid_5_to_10_v1),
    .south_ready_i         (ready_10_to_5_v1),
    .local_data_i          (data_i[0][1]),
    .local_valid_i         (valid_i[0][1]),
    .local_ready_o         (ready_o[0][1]),
    .local_data_o          (data_o[0][1]),
    .local_valid_o         (valid_o[0][1]),
    .local_ready_i         (ready_i[0][1])
);

/*Router 0,2*/    
gather_router #(
    .rt_file_list          (rt_file_list_0_2)
)router_0_2(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (34'b0),
    .west_valid_i          (1'b0),
    .west_ready_o          (),
    .west_data_o           (),
    .west_valid_o          (),
    .west_ready_i          (1'b0),
    .east_data_i           (data_11_to_10),
    .east_valid_i          (valid_11_to_10),
    .east_ready_o          (ready_10_to_11),
    .east_data_o           (data_10_to_11),
    .east_valid_o          (valid_10_to_11),
    .east_ready_i          (ready_11_to_10),
    .north_data_i          (data_5_to_10),
    .north_valid_i         (valid_5_to_10),
    .north_ready_o         (ready_10_to_5),
    .north_data_o          (data_10_to_5),
    .north_valid_o         (valid_10_to_5),
    .north_ready_i         (ready_5_to_10),
    .south_data_i          (data_15_to_10_v0),
    .south_valid_i         (valid_15_to_10_v0),
    .south_ready_o         (ready_10_to_15_v0),
    .south_data_o          (data_10_to_15_v1),
    .south_valid_o         (valid_10_to_15_v1),
    .south_ready_i         (ready_15_to_10_v1),
    .local_data_i          (data_i[0][2]),
    .local_valid_i         (valid_i[0][2]),
    .local_ready_o         (ready_o[0][2]),
    .local_data_o          (data_o[0][2]),
    .local_valid_o         (valid_o[0][2]),
    .local_ready_i         (ready_i[0][2])
);

/*Router 0,3*/    
gather_router #(
    .rt_file_list          (rt_file_list_0_3)
)router_0_3(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (34'b0),
    .west_valid_i          (1'b0),
    .west_ready_o          (),
    .west_data_o           (),
    .west_valid_o          (),
    .west_ready_i          (1'b0),
    .east_data_i           (data_16_to_15),
    .east_valid_i          (valid_16_to_15),
    .east_ready_o          (ready_15_to_16),
    .east_data_o           (data_15_to_16),
    .east_valid_o          (valid_15_to_16),
    .east_ready_i          (ready_16_to_15),
    .north_data_i          (data_10_to_15),
    .north_valid_i         (valid_10_to_15),
    .north_ready_o         (ready_15_to_10),
    .north_data_o          (data_15_to_10),
    .north_valid_o         (valid_15_to_10),
    .north_ready_i         (ready_10_to_15),
    .south_data_i          (data_20_to_15_v0),
    .south_valid_i         (valid_20_to_15_v0),
    .south_ready_o         (ready_15_to_20_v0),
    .south_data_o          (data_15_to_20_v1),
    .south_valid_o         (valid_15_to_20_v1),
    .south_ready_i         (ready_20_to_15_v1),
    .local_data_i          (data_i[0][3]),
    .local_valid_i         (valid_i[0][3]),
    .local_ready_o         (ready_o[0][3]),
    .local_data_o          (data_o[0][3]),
    .local_valid_o         (valid_o[0][3]),
    .local_ready_i         (ready_i[0][3])
);

/*Router 0,4*/    
gather_router #(
    .rt_file_list          (rt_file_list_0_4)
)router_0_4(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (34'b0),
    .west_valid_i          (1'b0),
    .west_ready_o          (),
    .west_data_o           (),
    .west_valid_o          (),
    .west_ready_i          (1'b0),
    .east_data_i           (data_21_to_20),
    .east_valid_i          (valid_21_to_20),
    .east_ready_o          (ready_20_to_21),
    .east_data_o           (data_20_to_21),
    .east_valid_o          (valid_20_to_21),
    .east_ready_i          (ready_21_to_20),
    .north_data_i          (data_15_to_20),
    .north_valid_i         (valid_15_to_20),
    .north_ready_o         (ready_20_to_15),
    .north_data_o          (data_20_to_15),
    .north_valid_o         (valid_20_to_15),
    .north_ready_i         (ready_15_to_20),
    .south_data_i          (data_25_to_20_v0),
    .south_valid_i         (valid_25_to_20_v0),
    .south_ready_o         (ready_20_to_25_v0),
    .south_data_o          (data_20_to_25_v1),
    .south_valid_o         (valid_20_to_25_v1),
    .south_ready_i         (ready_25_to_20_v1),
    .local_data_i          (data_i[0][4]),
    .local_valid_i         (valid_i[0][4]),
    .local_ready_o         (ready_o[0][4]),
    .local_data_o          (data_o[0][4]),
    .local_valid_o         (valid_o[0][4]),
    .local_ready_i         (ready_i[0][4])
);

/*Router 0,5*/    
gather_router #(
    .rt_file_list          (rt_file_list_0_5)
)router_0_5(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (34'b0),
    .west_valid_i          (1'b0),
    .west_ready_o          (),
    .west_data_o           (),
    .west_valid_o          (),
    .west_ready_i          (1'b0),
    .east_data_i           (data_26_to_25),
    .east_valid_i          (valid_26_to_25),
    .east_ready_o          (ready_25_to_26),
    .east_data_o           (data_25_to_26),
    .east_valid_o          (valid_25_to_26),
    .east_ready_i          (ready_26_to_25),
    .north_data_i          (data_20_to_25),
    .north_valid_i         (valid_20_to_25),
    .north_ready_o         (ready_25_to_20),
    .north_data_o          (data_25_to_20),
    .north_valid_o         (valid_25_to_20),
    .north_ready_i         (ready_20_to_25),
    .south_data_i          (34'b0),
    .south_valid_i         (1'b0),
    .south_ready_o         (),
    .south_data_o          (),
    .south_valid_o         (),
    .south_ready_i         (1'b0),
    .local_data_i          (data_i[0][5]),
    .local_valid_i         (valid_i[0][5]),
    .local_ready_o         (ready_o[0][5]),
    .local_data_o          (data_o[0][5]),
    .local_valid_o         (valid_o[0][5]),
    .local_ready_i         (ready_i[0][5])
);

/*Router 1,0*/    
gather_router #(
    .rt_file_list          (rt_file_list_1_0)
)router_1_0(
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
    .north_data_i          (34'b0),
    .north_valid_i         (1'b0),
    .north_ready_o         (),
    .north_data_o          (),
    .north_valid_o         (),
    .north_ready_i         (1'b0),
    .south_data_i          (data_6_to_1_v0),
    .south_valid_i         (valid_6_to_1_v0),
    .south_ready_o         (ready_1_to_6_v0),
    .south_data_o          (data_1_to_6_v1),
    .south_valid_o         (valid_1_to_6_v1),
    .south_ready_i         (ready_6_to_1_v1),
    .local_data_i          (data_i[1][0]),
    .local_valid_i         (valid_i[1][0]),
    .local_ready_o         (ready_o[1][0]),
    .local_data_o          (data_o[1][0]),
    .local_valid_o         (valid_o[1][0]),
    .local_ready_i         (ready_i[1][0])
);

/*Router 1,1*/    
gather_router #(
    .rt_file_list          (rt_file_list_1_1)
)router_1_1(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_5_to_6),
    .west_valid_i          (valid_5_to_6),
    .west_ready_o          (ready_6_to_5),
    .west_data_o           (data_6_to_5),
    .west_valid_o          (valid_6_to_5),
    .west_ready_i          (ready_5_to_6),
    .east_data_i           (data_7_to_6),
    .east_valid_i          (valid_7_to_6),
    .east_ready_o          (ready_6_to_7),
    .east_data_o           (data_6_to_7),
    .east_valid_o          (valid_6_to_7),
    .east_ready_i          (ready_7_to_6),
    .north_data_i          (data_1_to_6),
    .north_valid_i         (valid_1_to_6),
    .north_ready_o         (ready_6_to_1),
    .north_data_o          (data_6_to_1),
    .north_valid_o         (valid_6_to_1),
    .north_ready_i         (ready_1_to_6),
    .south_data_i          (data_11_to_6_v0),
    .south_valid_i         (valid_11_to_6_v0),
    .south_ready_o         (ready_6_to_11_v0),
    .south_data_o          (data_6_to_11_v1),
    .south_valid_o         (valid_6_to_11_v1),
    .south_ready_i         (ready_11_to_6_v1),
    .local_data_i          (data_i[1][1]),
    .local_valid_i         (valid_i[1][1]),
    .local_ready_o         (ready_o[1][1]),
    .local_data_o          (data_o[1][1]),
    .local_valid_o         (valid_o[1][1]),
    .local_ready_i         (ready_i[1][1])
);

/*Router 1,2*/    
gather_router #(
    .rt_file_list          (rt_file_list_1_2)
)router_1_2(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_10_to_11),
    .west_valid_i          (valid_10_to_11),
    .west_ready_o          (ready_11_to_10),
    .west_data_o           (data_11_to_10),
    .west_valid_o          (valid_11_to_10),
    .west_ready_i          (ready_10_to_11),
    .east_data_i           (data_12_to_11),
    .east_valid_i          (valid_12_to_11),
    .east_ready_o          (ready_11_to_12),
    .east_data_o           (data_11_to_12),
    .east_valid_o          (valid_11_to_12),
    .east_ready_i          (ready_12_to_11),
    .north_data_i          (data_6_to_11),
    .north_valid_i         (valid_6_to_11),
    .north_ready_o         (ready_11_to_6),
    .north_data_o          (data_11_to_6),
    .north_valid_o         (valid_11_to_6),
    .north_ready_i         (ready_6_to_11),
    .south_data_i          (data_16_to_11_v0),
    .south_valid_i         (valid_16_to_11_v0),
    .south_ready_o         (ready_11_to_16_v0),
    .south_data_o          (data_11_to_16_v1),
    .south_valid_o         (valid_11_to_16_v1),
    .south_ready_i         (ready_16_to_11_v1),
    .local_data_i          (data_i[1][2]),
    .local_valid_i         (valid_i[1][2]),
    .local_ready_o         (ready_o[1][2]),
    .local_data_o          (data_o[1][2]),
    .local_valid_o         (valid_o[1][2]),
    .local_ready_i         (ready_i[1][2])
);

/*Router 1,3*/    
gather_router #(
    .rt_file_list          (rt_file_list_1_3)
)router_1_3(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_15_to_16),
    .west_valid_i          (valid_15_to_16),
    .west_ready_o          (ready_16_to_15),
    .west_data_o           (data_16_to_15),
    .west_valid_o          (valid_16_to_15),
    .west_ready_i          (ready_15_to_16),
    .east_data_i           (data_17_to_16),
    .east_valid_i          (valid_17_to_16),
    .east_ready_o          (ready_16_to_17),
    .east_data_o           (data_16_to_17),
    .east_valid_o          (valid_16_to_17),
    .east_ready_i          (ready_17_to_16),
    .north_data_i          (data_11_to_16),
    .north_valid_i         (valid_11_to_16),
    .north_ready_o         (ready_16_to_11),
    .north_data_o          (data_16_to_11),
    .north_valid_o         (valid_16_to_11),
    .north_ready_i         (ready_11_to_16),
    .south_data_i          (data_21_to_16_v0),
    .south_valid_i         (valid_21_to_16_v0),
    .south_ready_o         (ready_16_to_21_v0),
    .south_data_o          (data_16_to_21_v1),
    .south_valid_o         (valid_16_to_21_v1),
    .south_ready_i         (ready_21_to_16_v1),
    .local_data_i          (data_i[1][3]),
    .local_valid_i         (valid_i[1][3]),
    .local_ready_o         (ready_o[1][3]),
    .local_data_o          (data_o[1][3]),
    .local_valid_o         (valid_o[1][3]),
    .local_ready_i         (ready_i[1][3])
);

/*Router 1,4*/    
gather_router #(
    .rt_file_list          (rt_file_list_1_4)
)router_1_4(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_20_to_21),
    .west_valid_i          (valid_20_to_21),
    .west_ready_o          (ready_21_to_20),
    .west_data_o           (data_21_to_20),
    .west_valid_o          (valid_21_to_20),
    .west_ready_i          (ready_20_to_21),
    .east_data_i           (data_22_to_21),
    .east_valid_i          (valid_22_to_21),
    .east_ready_o          (ready_21_to_22),
    .east_data_o           (data_21_to_22),
    .east_valid_o          (valid_21_to_22),
    .east_ready_i          (ready_22_to_21),
    .north_data_i          (data_16_to_21),
    .north_valid_i         (valid_16_to_21),
    .north_ready_o         (ready_21_to_16),
    .north_data_o          (data_21_to_16),
    .north_valid_o         (valid_21_to_16),
    .north_ready_i         (ready_16_to_21),
    .south_data_i          (data_26_to_21_v0),
    .south_valid_i         (valid_26_to_21_v0),
    .south_ready_o         (ready_21_to_26_v0),
    .south_data_o          (data_21_to_26_v1),
    .south_valid_o         (valid_21_to_26_v1),
    .south_ready_i         (ready_26_to_21_v1),
    .local_data_i          (data_i[1][4]),
    .local_valid_i         (valid_i[1][4]),
    .local_ready_o         (ready_o[1][4]),
    .local_data_o          (data_o[1][4]),
    .local_valid_o         (valid_o[1][4]),
    .local_ready_i         (ready_i[1][4])
);

/*Router 1,5*/    
gather_router #(
    .rt_file_list          (rt_file_list_1_5)
)router_1_5(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_25_to_26),
    .west_valid_i          (valid_25_to_26),
    .west_ready_o          (ready_26_to_25),
    .west_data_o           (data_26_to_25),
    .west_valid_o          (valid_26_to_25),
    .west_ready_i          (ready_25_to_26),
    .east_data_i           (data_27_to_26),
    .east_valid_i          (valid_27_to_26),
    .east_ready_o          (ready_26_to_27),
    .east_data_o           (data_26_to_27),
    .east_valid_o          (valid_26_to_27),
    .east_ready_i          (ready_27_to_26),
    .north_data_i          (data_21_to_26),
    .north_valid_i         (valid_21_to_26),
    .north_ready_o         (ready_26_to_21),
    .north_data_o          (data_26_to_21),
    .north_valid_o         (valid_26_to_21),
    .north_ready_i         (ready_21_to_26),
    .south_data_i          (34'b0),
    .south_valid_i         (1'b0),
    .south_ready_o         (),
    .south_data_o          (),
    .south_valid_o         (),
    .south_ready_i         (1'b0),
    .local_data_i          (data_i[1][5]),
    .local_valid_i         (valid_i[1][5]),
    .local_ready_o         (ready_o[1][5]),
    .local_data_o          (data_o[1][5]),
    .local_valid_o         (valid_o[1][5]),
    .local_ready_i         (ready_i[1][5])
);

/*Router 2,0*/    
gather_router #(
    .rt_file_list          (rt_file_list_2_0)
)router_2_0(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_1_to_2),
    .west_valid_i          (valid_1_to_2),
    .west_ready_o          (ready_2_to_1),
    .west_data_o           (data_2_to_1),
    .west_valid_o          (valid_2_to_1),
    .west_ready_i          (ready_1_to_2),
    .east_data_i           (data_3_to_2),
    .east_valid_i          (valid_3_to_2),
    .east_ready_o          (ready_2_to_3),
    .east_data_o           (data_2_to_3),
    .east_valid_o          (valid_2_to_3),
    .east_ready_i          (ready_3_to_2),
    .north_data_i          (34'b0),
    .north_valid_i         (1'b0),
    .north_ready_o         (),
    .north_data_o          (),
    .north_valid_o         (),
    .north_ready_i         (1'b0),
    .south_data_i          (data_7_to_2_v0),
    .south_valid_i         (valid_7_to_2_v0),
    .south_ready_o         (ready_2_to_7_v0),
    .south_data_o          (data_2_to_7_v1),
    .south_valid_o         (valid_2_to_7_v1),
    .south_ready_i         (ready_7_to_2_v1),
    .local_data_i          (data_i[2][0]),
    .local_valid_i         (valid_i[2][0]),
    .local_ready_o         (ready_o[2][0]),
    .local_data_o          (data_o[2][0]),
    .local_valid_o         (valid_o[2][0]),
    .local_ready_i         (ready_i[2][0])
);

/*Router 2,1*/    
gather_router #(
    .rt_file_list          (rt_file_list_2_1)
)router_2_1(
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
    .north_data_i          (data_2_to_7),
    .north_valid_i         (valid_2_to_7),
    .north_ready_o         (ready_7_to_2),
    .north_data_o          (data_7_to_2),
    .north_valid_o         (valid_7_to_2),
    .north_ready_i         (ready_2_to_7),
    .south_data_i          (data_12_to_7_v0),
    .south_valid_i         (valid_12_to_7_v0),
    .south_ready_o         (ready_7_to_12_v0),
    .south_data_o          (data_7_to_12_v1),
    .south_valid_o         (valid_7_to_12_v1),
    .south_ready_i         (ready_12_to_7_v1),
    .local_data_i          (data_i[2][1]),
    .local_valid_i         (valid_i[2][1]),
    .local_ready_o         (ready_o[2][1]),
    .local_data_o          (data_o[2][1]),
    .local_valid_o         (valid_o[2][1]),
    .local_ready_i         (ready_i[2][1])
);

/*Router 2,2*/    
gather_router #(
    .rt_file_list          (rt_file_list_2_2)
)router_2_2(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_11_to_12),
    .west_valid_i          (valid_11_to_12),
    .west_ready_o          (ready_12_to_11),
    .west_data_o           (data_12_to_11),
    .west_valid_o          (valid_12_to_11),
    .west_ready_i          (ready_11_to_12),
    .east_data_i           (data_13_to_12),
    .east_valid_i          (valid_13_to_12),
    .east_ready_o          (ready_12_to_13),
    .east_data_o           (data_12_to_13),
    .east_valid_o          (valid_12_to_13),
    .east_ready_i          (ready_13_to_12),
    .north_data_i          (data_7_to_12),
    .north_valid_i         (valid_7_to_12),
    .north_ready_o         (ready_12_to_7),
    .north_data_o          (data_12_to_7),
    .north_valid_o         (valid_12_to_7),
    .north_ready_i         (ready_7_to_12),
    .south_data_i          (data_17_to_12_v0),
    .south_valid_i         (valid_17_to_12_v0),
    .south_ready_o         (ready_12_to_17_v0),
    .south_data_o          (data_12_to_17_v1),
    .south_valid_o         (valid_12_to_17_v1),
    .south_ready_i         (ready_17_to_12_v1),
    .local_data_i          (data_i[2][2]),
    .local_valid_i         (valid_i[2][2]),
    .local_ready_o         (ready_o[2][2]),
    .local_data_o          (data_o[2][2]),
    .local_valid_o         (valid_o[2][2]),
    .local_ready_i         (ready_i[2][2])
);

/*Router 2,3*/    
gather_router #(
    .rt_file_list          (rt_file_list_2_3)
)router_2_3(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_16_to_17),
    .west_valid_i          (valid_16_to_17),
    .west_ready_o          (ready_17_to_16),
    .west_data_o           (data_17_to_16),
    .west_valid_o          (valid_17_to_16),
    .west_ready_i          (ready_16_to_17),
    .east_data_i           (data_18_to_17),
    .east_valid_i          (valid_18_to_17),
    .east_ready_o          (ready_17_to_18),
    .east_data_o           (data_17_to_18),
    .east_valid_o          (valid_17_to_18),
    .east_ready_i          (ready_18_to_17),
    .north_data_i          (data_12_to_17),
    .north_valid_i         (valid_12_to_17),
    .north_ready_o         (ready_17_to_12),
    .north_data_o          (data_17_to_12),
    .north_valid_o         (valid_17_to_12),
    .north_ready_i         (ready_12_to_17),
    .south_data_i          (data_22_to_17_v0),
    .south_valid_i         (valid_22_to_17_v0),
    .south_ready_o         (ready_17_to_22_v0),
    .south_data_o          (data_17_to_22_v1),
    .south_valid_o         (valid_17_to_22_v1),
    .south_ready_i         (ready_22_to_17_v1),
    .local_data_i          (data_i[2][3]),
    .local_valid_i         (valid_i[2][3]),
    .local_ready_o         (ready_o[2][3]),
    .local_data_o          (data_o[2][3]),
    .local_valid_o         (valid_o[2][3]),
    .local_ready_i         (ready_i[2][3])
);

/*Router 2,4*/    
gather_router #(
    .rt_file_list          (rt_file_list_2_4)
)router_2_4(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_21_to_22),
    .west_valid_i          (valid_21_to_22),
    .west_ready_o          (ready_22_to_21),
    .west_data_o           (data_22_to_21),
    .west_valid_o          (valid_22_to_21),
    .west_ready_i          (ready_21_to_22),
    .east_data_i           (data_23_to_22),
    .east_valid_i          (valid_23_to_22),
    .east_ready_o          (ready_22_to_23),
    .east_data_o           (data_22_to_23),
    .east_valid_o          (valid_22_to_23),
    .east_ready_i          (ready_23_to_22),
    .north_data_i          (data_17_to_22),
    .north_valid_i         (valid_17_to_22),
    .north_ready_o         (ready_22_to_17),
    .north_data_o          (data_22_to_17),
    .north_valid_o         (valid_22_to_17),
    .north_ready_i         (ready_17_to_22),
    .south_data_i          (data_27_to_22_v0),
    .south_valid_i         (valid_27_to_22_v0),
    .south_ready_o         (ready_22_to_27_v0),
    .south_data_o          (data_22_to_27_v1),
    .south_valid_o         (valid_22_to_27_v1),
    .south_ready_i         (ready_27_to_22_v1),
    .local_data_i          (data_i[2][4]),
    .local_valid_i         (valid_i[2][4]),
    .local_ready_o         (ready_o[2][4]),
    .local_data_o          (data_o[2][4]),
    .local_valid_o         (valid_o[2][4]),
    .local_ready_i         (ready_i[2][4])
);

/*Router 2,5*/    
gather_router #(
    .rt_file_list          (rt_file_list_2_5)
)router_2_5(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_26_to_27),
    .west_valid_i          (valid_26_to_27),
    .west_ready_o          (ready_27_to_26),
    .west_data_o           (data_27_to_26),
    .west_valid_o          (valid_27_to_26),
    .west_ready_i          (ready_26_to_27),
    .east_data_i           (data_28_to_27),
    .east_valid_i          (valid_28_to_27),
    .east_ready_o          (ready_27_to_28),
    .east_data_o           (data_27_to_28),
    .east_valid_o          (valid_27_to_28),
    .east_ready_i          (ready_28_to_27),
    .north_data_i          (data_22_to_27),
    .north_valid_i         (valid_22_to_27),
    .north_ready_o         (ready_27_to_22),
    .north_data_o          (data_27_to_22),
    .north_valid_o         (valid_27_to_22),
    .north_ready_i         (ready_22_to_27),
    .south_data_i          (34'b0),
    .south_valid_i         (1'b0),
    .south_ready_o         (),
    .south_data_o          (),
    .south_valid_o         (),
    .south_ready_i         (1'b0),
    .local_data_i          (data_i[2][5]),
    .local_valid_i         (valid_i[2][5]),
    .local_ready_o         (ready_o[2][5]),
    .local_data_o          (data_o[2][5]),
    .local_valid_o         (valid_o[2][5]),
    .local_ready_i         (ready_i[2][5])
);

/*Router 3,0*/    
gather_router #(
    .rt_file_list          (rt_file_list_3_0)
)router_3_0(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_2_to_3),
    .west_valid_i          (valid_2_to_3),
    .west_ready_o          (ready_3_to_2),
    .west_data_o           (data_3_to_2),
    .west_valid_o          (valid_3_to_2),
    .west_ready_i          (ready_2_to_3),
    .east_data_i           (data_4_to_3),
    .east_valid_i          (valid_4_to_3),
    .east_ready_o          (ready_3_to_4),
    .east_data_o           (data_3_to_4),
    .east_valid_o          (valid_3_to_4),
    .east_ready_i          (ready_4_to_3),
    .north_data_i          (34'b0),
    .north_valid_i         (1'b0),
    .north_ready_o         (),
    .north_data_o          (),
    .north_valid_o         (),
    .north_ready_i         (1'b0),
    .south_data_i          (data_8_to_3_v0),
    .south_valid_i         (valid_8_to_3_v0),
    .south_ready_o         (ready_3_to_8_v0),
    .south_data_o          (data_3_to_8_v1),
    .south_valid_o         (valid_3_to_8_v1),
    .south_ready_i         (ready_8_to_3_v1),
    .local_data_i          (data_i[3][0]),
    .local_valid_i         (valid_i[3][0]),
    .local_ready_o         (ready_o[3][0]),
    .local_data_o          (data_o[3][0]),
    .local_valid_o         (valid_o[3][0]),
    .local_ready_i         (ready_i[3][0])
);

/*Router 3,1*/    
gather_router #(
    .rt_file_list          (rt_file_list_3_1)
)router_3_1(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_7_to_8),
    .west_valid_i          (valid_7_to_8),
    .west_ready_o          (ready_8_to_7),
    .west_data_o           (data_8_to_7),
    .west_valid_o          (valid_8_to_7),
    .west_ready_i          (ready_7_to_8),
    .east_data_i           (data_9_to_8),
    .east_valid_i          (valid_9_to_8),
    .east_ready_o          (ready_8_to_9),
    .east_data_o           (data_8_to_9),
    .east_valid_o          (valid_8_to_9),
    .east_ready_i          (ready_9_to_8),
    .north_data_i          (data_3_to_8),
    .north_valid_i         (valid_3_to_8),
    .north_ready_o         (ready_8_to_3),
    .north_data_o          (data_8_to_3),
    .north_valid_o         (valid_8_to_3),
    .north_ready_i         (ready_3_to_8),
    .south_data_i          (data_13_to_8_v0),
    .south_valid_i         (valid_13_to_8_v0),
    .south_ready_o         (ready_8_to_13_v0),
    .south_data_o          (data_8_to_13_v1),
    .south_valid_o         (valid_8_to_13_v1),
    .south_ready_i         (ready_13_to_8_v1),
    .local_data_i          (data_i[3][1]),
    .local_valid_i         (valid_i[3][1]),
    .local_ready_o         (ready_o[3][1]),
    .local_data_o          (data_o[3][1]),
    .local_valid_o         (valid_o[3][1]),
    .local_ready_i         (ready_i[3][1])
);

/*Router 3,2*/    
gather_router #(
    .rt_file_list          (rt_file_list_3_2)
)router_3_2(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_12_to_13),
    .west_valid_i          (valid_12_to_13),
    .west_ready_o          (ready_13_to_12),
    .west_data_o           (data_13_to_12),
    .west_valid_o          (valid_13_to_12),
    .west_ready_i          (ready_12_to_13),
    .east_data_i           (data_14_to_13),
    .east_valid_i          (valid_14_to_13),
    .east_ready_o          (ready_13_to_14),
    .east_data_o           (data_13_to_14),
    .east_valid_o          (valid_13_to_14),
    .east_ready_i          (ready_14_to_13),
    .north_data_i          (data_8_to_13),
    .north_valid_i         (valid_8_to_13),
    .north_ready_o         (ready_13_to_8),
    .north_data_o          (data_13_to_8),
    .north_valid_o         (valid_13_to_8),
    .north_ready_i         (ready_8_to_13),
    .south_data_i          (data_18_to_13_v0),
    .south_valid_i         (valid_18_to_13_v0),
    .south_ready_o         (ready_13_to_18_v0),
    .south_data_o          (data_13_to_18_v1),
    .south_valid_o         (valid_13_to_18_v1),
    .south_ready_i         (ready_18_to_13_v1),
    .local_data_i          (data_i[3][2]),
    .local_valid_i         (valid_i[3][2]),
    .local_ready_o         (ready_o[3][2]),
    .local_data_o          (data_o[3][2]),
    .local_valid_o         (valid_o[3][2]),
    .local_ready_i         (ready_i[3][2])
);

/*Router 3,3*/    
gather_router #(
    .rt_file_list          (rt_file_list_3_3)
)router_3_3(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_17_to_18),
    .west_valid_i          (valid_17_to_18),
    .west_ready_o          (ready_18_to_17),
    .west_data_o           (data_18_to_17),
    .west_valid_o          (valid_18_to_17),
    .west_ready_i          (ready_17_to_18),
    .east_data_i           (data_19_to_18),
    .east_valid_i          (valid_19_to_18),
    .east_ready_o          (ready_18_to_19),
    .east_data_o           (data_18_to_19),
    .east_valid_o          (valid_18_to_19),
    .east_ready_i          (ready_19_to_18),
    .north_data_i          (data_13_to_18),
    .north_valid_i         (valid_13_to_18),
    .north_ready_o         (ready_18_to_13),
    .north_data_o          (data_18_to_13),
    .north_valid_o         (valid_18_to_13),
    .north_ready_i         (ready_13_to_18),
    .south_data_i          (data_23_to_18_v0),
    .south_valid_i         (valid_23_to_18_v0),
    .south_ready_o         (ready_18_to_23_v0),
    .south_data_o          (data_18_to_23_v1),
    .south_valid_o         (valid_18_to_23_v1),
    .south_ready_i         (ready_23_to_18_v1),
    .local_data_i          (data_i[3][3]),
    .local_valid_i         (valid_i[3][3]),
    .local_ready_o         (ready_o[3][3]),
    .local_data_o          (data_o[3][3]),
    .local_valid_o         (valid_o[3][3]),
    .local_ready_i         (ready_i[3][3])
);

/*Router 3,4*/    
gather_router #(
    .rt_file_list          (rt_file_list_3_4)
)router_3_4(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_22_to_23),
    .west_valid_i          (valid_22_to_23),
    .west_ready_o          (ready_23_to_22),
    .west_data_o           (data_23_to_22),
    .west_valid_o          (valid_23_to_22),
    .west_ready_i          (ready_22_to_23),
    .east_data_i           (data_24_to_23),
    .east_valid_i          (valid_24_to_23),
    .east_ready_o          (ready_23_to_24),
    .east_data_o           (data_23_to_24),
    .east_valid_o          (valid_23_to_24),
    .east_ready_i          (ready_24_to_23),
    .north_data_i          (data_18_to_23),
    .north_valid_i         (valid_18_to_23),
    .north_ready_o         (ready_23_to_18),
    .north_data_o          (data_23_to_18),
    .north_valid_o         (valid_23_to_18),
    .north_ready_i         (ready_18_to_23),
    .south_data_i          (data_28_to_23_v0),
    .south_valid_i         (valid_28_to_23_v0),
    .south_ready_o         (ready_23_to_28_v0),
    .south_data_o          (data_23_to_28_v1),
    .south_valid_o         (valid_23_to_28_v1),
    .south_ready_i         (ready_28_to_23_v1),
    .local_data_i          (data_i[3][4]),
    .local_valid_i         (valid_i[3][4]),
    .local_ready_o         (ready_o[3][4]),
    .local_data_o          (data_o[3][4]),
    .local_valid_o         (valid_o[3][4]),
    .local_ready_i         (ready_i[3][4])
);

/*Router 3,5*/    
gather_router #(
    .rt_file_list          (rt_file_list_3_5)
)router_3_5(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_27_to_28),
    .west_valid_i          (valid_27_to_28),
    .west_ready_o          (ready_28_to_27),
    .west_data_o           (data_28_to_27),
    .west_valid_o          (valid_28_to_27),
    .west_ready_i          (ready_27_to_28),
    .east_data_i           (data_29_to_28),
    .east_valid_i          (valid_29_to_28),
    .east_ready_o          (ready_28_to_29),
    .east_data_o           (data_28_to_29),
    .east_valid_o          (valid_28_to_29),
    .east_ready_i          (ready_29_to_28),
    .north_data_i          (data_23_to_28),
    .north_valid_i         (valid_23_to_28),
    .north_ready_o         (ready_28_to_23),
    .north_data_o          (data_28_to_23),
    .north_valid_o         (valid_28_to_23),
    .north_ready_i         (ready_23_to_28),
    .south_data_i          (34'b0),
    .south_valid_i         (1'b0),
    .south_ready_o         (),
    .south_data_o          (),
    .south_valid_o         (),
    .south_ready_i         (1'b0),
    .local_data_i          (data_i[3][5]),
    .local_valid_i         (valid_i[3][5]),
    .local_ready_o         (ready_o[3][5]),
    .local_data_o          (data_o[3][5]),
    .local_valid_o         (valid_o[3][5]),
    .local_ready_i         (ready_i[3][5])
);

/*Router 4,0*/    
gather_router #(
    .rt_file_list          (rt_file_list_4_0)
)router_4_0(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_3_to_4),
    .west_valid_i          (valid_3_to_4),
    .west_ready_o          (ready_4_to_3),
    .west_data_o           (data_4_to_3),
    .west_valid_o          (valid_4_to_3),
    .west_ready_i          (ready_3_to_4),
    .east_data_i           (34'b0),
    .east_valid_i          (1'b0),
    .east_ready_o          (),
    .east_data_o           (),
    .east_valid_o          (),
    .east_ready_i          (1'b0),
    .north_data_i          (34'b0),
    .north_valid_i         (1'b0),
    .north_ready_o         (),
    .north_data_o          (),
    .north_valid_o         (),
    .north_ready_i         (1'b0),
    .south_data_i          (data_9_to_4_v0),
    .south_valid_i         (valid_9_to_4_v0),
    .south_ready_o         (ready_4_to_9_v0),
    .south_data_o          (data_4_to_9_v1),
    .south_valid_o         (valid_4_to_9_v1),
    .south_ready_i         (ready_9_to_4_v1),
    .local_data_i          (data_i[4][0]),
    .local_valid_i         (valid_i[4][0]),
    .local_ready_o         (ready_o[4][0]),
    .local_data_o          (data_o[4][0]),
    .local_valid_o         (valid_o[4][0]),
    .local_ready_i         (ready_i[4][0])
);

/*Router 4,1*/    
gather_router #(
    .rt_file_list          (rt_file_list_4_1)
)router_4_1(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_8_to_9),
    .west_valid_i          (valid_8_to_9),
    .west_ready_o          (ready_9_to_8),
    .west_data_o           (data_9_to_8),
    .west_valid_o          (valid_9_to_8),
    .west_ready_i          (ready_8_to_9),
    .east_data_i           (34'b0),
    .east_valid_i          (1'b0),
    .east_ready_o          (),
    .east_data_o           (),
    .east_valid_o          (),
    .east_ready_i          (1'b0),
    .north_data_i          (data_4_to_9),
    .north_valid_i         (valid_4_to_9),
    .north_ready_o         (ready_9_to_4),
    .north_data_o          (data_9_to_4),
    .north_valid_o         (valid_9_to_4),
    .north_ready_i         (ready_4_to_9),
    .south_data_i          (data_14_to_9_v0),
    .south_valid_i         (valid_14_to_9_v0),
    .south_ready_o         (ready_9_to_14_v0),
    .south_data_o          (data_9_to_14_v1),
    .south_valid_o         (valid_9_to_14_v1),
    .south_ready_i         (ready_14_to_9_v1),
    .local_data_i          (data_i[4][1]),
    .local_valid_i         (valid_i[4][1]),
    .local_ready_o         (ready_o[4][1]),
    .local_data_o          (data_o[4][1]),
    .local_valid_o         (valid_o[4][1]),
    .local_ready_i         (ready_i[4][1])
);

/*Router 4,2*/    
gather_router #(
    .rt_file_list          (rt_file_list_4_2)
)router_4_2(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_13_to_14),
    .west_valid_i          (valid_13_to_14),
    .west_ready_o          (ready_14_to_13),
    .west_data_o           (data_14_to_13),
    .west_valid_o          (valid_14_to_13),
    .west_ready_i          (ready_13_to_14),
    .east_data_i           (34'b0),
    .east_valid_i          (1'b0),
    .east_ready_o          (),
    .east_data_o           (),
    .east_valid_o          (),
    .east_ready_i          (1'b0),
    .north_data_i          (data_9_to_14),
    .north_valid_i         (valid_9_to_14),
    .north_ready_o         (ready_14_to_9),
    .north_data_o          (data_14_to_9),
    .north_valid_o         (valid_14_to_9),
    .north_ready_i         (ready_9_to_14),
    .south_data_i          (data_19_to_14_v0),
    .south_valid_i         (valid_19_to_14_v0),
    .south_ready_o         (ready_14_to_19_v0),
    .south_data_o          (data_14_to_19_v1),
    .south_valid_o         (valid_14_to_19_v1),
    .south_ready_i         (ready_19_to_14_v1),
    .local_data_i          (data_i[4][2]),
    .local_valid_i         (valid_i[4][2]),
    .local_ready_o         (ready_o[4][2]),
    .local_data_o          (data_o[4][2]),
    .local_valid_o         (valid_o[4][2]),
    .local_ready_i         (ready_i[4][2])
);

/*Router 4,3*/    
gather_router #(
    .rt_file_list          (rt_file_list_4_3)
)router_4_3(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_18_to_19),
    .west_valid_i          (valid_18_to_19),
    .west_ready_o          (ready_19_to_18),
    .west_data_o           (data_19_to_18),
    .west_valid_o          (valid_19_to_18),
    .west_ready_i          (ready_18_to_19),
    .east_data_i           (34'b0),
    .east_valid_i          (1'b0),
    .east_ready_o          (),
    .east_data_o           (),
    .east_valid_o          (),
    .east_ready_i          (1'b0),
    .north_data_i          (data_14_to_19),
    .north_valid_i         (valid_14_to_19),
    .north_ready_o         (ready_19_to_14),
    .north_data_o          (data_19_to_14),
    .north_valid_o         (valid_19_to_14),
    .north_ready_i         (ready_14_to_19),
    .south_data_i          (data_24_to_19_v0),
    .south_valid_i         (valid_24_to_19_v0),
    .south_ready_o         (ready_19_to_24_v0),
    .south_data_o          (data_19_to_24_v1),
    .south_valid_o         (valid_19_to_24_v1),
    .south_ready_i         (ready_24_to_19_v1),
    .local_data_i          (data_i[4][3]),
    .local_valid_i         (valid_i[4][3]),
    .local_ready_o         (ready_o[4][3]),
    .local_data_o          (data_o[4][3]),
    .local_valid_o         (valid_o[4][3]),
    .local_ready_i         (ready_i[4][3])
);

/*Router 4,4*/    
gather_router #(
    .rt_file_list          (rt_file_list_4_4)
)router_4_4(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_23_to_24),
    .west_valid_i          (valid_23_to_24),
    .west_ready_o          (ready_24_to_23),
    .west_data_o           (data_24_to_23),
    .west_valid_o          (valid_24_to_23),
    .west_ready_i          (ready_23_to_24),
    .east_data_i           (34'b0),
    .east_valid_i          (1'b0),
    .east_ready_o          (),
    .east_data_o           (),
    .east_valid_o          (),
    .east_ready_i          (1'b0),
    .north_data_i          (data_19_to_24),
    .north_valid_i         (valid_19_to_24),
    .north_ready_o         (ready_24_to_19),
    .north_data_o          (data_24_to_19),
    .north_valid_o         (valid_24_to_19),
    .north_ready_i         (ready_19_to_24),
    .south_data_i          (data_29_to_24_v0),
    .south_valid_i         (valid_29_to_24_v0),
    .south_ready_o         (ready_24_to_29_v0),
    .south_data_o          (data_24_to_29_v1),
    .south_valid_o         (valid_24_to_29_v1),
    .south_ready_i         (ready_29_to_24_v1),
    .local_data_i          (data_i[4][4]),
    .local_valid_i         (valid_i[4][4]),
    .local_ready_o         (ready_o[4][4]),
    .local_data_o          (data_o[4][4]),
    .local_valid_o         (valid_o[4][4]),
    .local_ready_i         (ready_i[4][4])
);

/*Router 4,5*/    
gather_router #(
    .rt_file_list          (rt_file_list_4_5)
)router_4_5(
    .clk                   (clk),
    .rstn                  (rstn),
    .west_data_i           (data_28_to_29),
    .west_valid_i          (valid_28_to_29),
    .west_ready_o          (ready_29_to_28),
    .west_data_o           (data_29_to_28),
    .west_valid_o          (valid_29_to_28),
    .west_ready_i          (ready_28_to_29),
    .east_data_i           (34'b0),
    .east_valid_i          (1'b0),
    .east_ready_o          (),
    .east_data_o           (),
    .east_valid_o          (),
    .east_ready_i          (1'b0),
    .north_data_i          (data_24_to_29),
    .north_valid_i         (valid_24_to_29),
    .north_ready_o         (ready_29_to_24),
    .north_data_o          (data_29_to_24),
    .north_valid_o         (valid_29_to_24),
    .north_ready_i         (ready_24_to_29),
    .south_data_i          (34'b0),
    .south_valid_i         (1'b0),
    .south_ready_o         (),
    .south_data_o          (),
    .south_valid_o         (),
    .south_ready_i         (1'b0),
    .local_data_i          (data_i[4][5]),
    .local_valid_i         (valid_i[4][5]),
    .local_ready_o         (ready_o[4][5]),
    .local_data_o          (data_o[4][5]),
    .local_valid_o         (valid_o[4][5]),
    .local_ready_i         (ready_i[4][5])
);

endmodule
