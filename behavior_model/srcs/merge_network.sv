//Merge Network
//Width: 3
//Height:3
`include "params.svh"
`include "merge_network_config.svh"

module merge_network(
    input       wire                            clk,
    input       wire                            rstn,
    
    //router local ports
    input       wire        [`DW-1:0]           data_i[`NOC_WIDTH][`NOC_HEIGHT],
    input       wire                            valid_i[`NOC_WIDTH][`NOC_HEIGHT],
    output      wire                            ready_o[`NOC_WIDTH][`NOC_HEIGHT],

    output      wire        [`DW-1:0]           data_o[`NOC_WIDTH][`NOC_HEIGHT],
    output      wire                            valid_o[`NOC_WIDTH][`NOC_HEIGHT],
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

/*Router 0,0*/    
merge_router #(
    .input_mask                     (input_mask[0][0]),
    .output_sel                     (output_sel[0][0])
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
    data_i_0_0[2] = data_o_1_0[1];
    valid_i_0_0[2] = valid_o_1_0[1];
    ready_i_0_0[2] = ready_o_1_0[1];
    data_i_0_0[0] = data_o_[0][0];
    valid_i_0_0[0] = valid_o_[0][0];
    ready_i_0_0[0] = ready_o_[0][0];
end


/*Router 0,1*/    
merge_router #(
    .input_mask                     (input_mask[0][1]),
    .output_sel                     (output_sel[0][1])
)router3(
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
    data_i_0_1[3] = data_o_0_2[4];
    valid_i_0_1[3] = valid_o_0_2[4];
    ready_i_0_1[3] = ready_o_0_2[4];
    data_i_0_1[4] = data_o_0_0[3];
    valid_i_0_1[4] = valid_o_0_0[3];
    ready_i_0_1[4] = ready_o_0_0[3];
    data_i_0_1[2] = data_o_1_1[1];
    valid_i_0_1[2] = valid_o_1_1[1];
    ready_i_0_1[2] = ready_o_1_1[1];
    data_i_0_1[0] = data_o_[0][1];
    valid_i_0_1[0] = valid_o_[0][1];
    ready_i_0_1[0] = ready_o_[0][1];
end


/*Router 0,2*/    
merge_router #(
    .input_mask                     (input_mask[0][2]),
    .output_sel                     (output_sel[0][2])
)router6(
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
    data_i_0_2[3] = data_o_0_3[4];
    valid_i_0_2[3] = valid_o_0_3[4];
    ready_i_0_2[3] = ready_o_0_3[4];
    data_i_0_2[4] = data_o_0_1[3];
    valid_i_0_2[4] = valid_o_0_1[3];
    ready_i_0_2[4] = ready_o_0_1[3];
    data_i_0_2[2] = data_o_1_2[1];
    valid_i_0_2[2] = valid_o_1_2[1];
    ready_i_0_2[2] = ready_o_1_2[1];
    data_i_0_2[0] = data_o_[0][2];
    valid_i_0_2[0] = valid_o_[0][2];
    ready_i_0_2[0] = ready_o_[0][2];
end


/*Router 1,0*/    
merge_router #(
    .input_mask                     (input_mask[1][0]),
    .output_sel                     (output_sel[1][0])
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
    data_i_1_0[1] = data_o_0_0[2];
    valid_i_1_0[1] = valid_o_0_0[2];
    ready_i_1_0[1] = ready_o_0_0[2];
    data_i_1_0[2] = data_o_2_0[1];
    valid_i_1_0[2] = valid_o_2_0[1];
    ready_i_1_0[2] = ready_o_2_0[1];
    data_i_1_0[0] = data_o_[1][0];
    valid_i_1_0[0] = valid_o_[1][0];
    ready_i_1_0[0] = ready_o_[1][0];
end


/*Router 1,1*/    
merge_router #(
    .input_mask                     (input_mask[1][1]),
    .output_sel                     (output_sel[1][1])
)router4(
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
    data_i_1_1[3] = data_o_1_2[4];
    valid_i_1_1[3] = valid_o_1_2[4];
    ready_i_1_1[3] = ready_o_1_2[4];
    data_i_1_1[4] = data_o_1_0[3];
    valid_i_1_1[4] = valid_o_1_0[3];
    ready_i_1_1[4] = ready_o_1_0[3];
    data_i_1_1[1] = data_o_0_1[2];
    valid_i_1_1[1] = valid_o_0_1[2];
    ready_i_1_1[1] = ready_o_0_1[2];
    data_i_1_1[2] = data_o_2_1[1];
    valid_i_1_1[2] = valid_o_2_1[1];
    ready_i_1_1[2] = ready_o_2_1[1];
    data_i_1_1[0] = data_o_[1][1];
    valid_i_1_1[0] = valid_o_[1][1];
    ready_i_1_1[0] = ready_o_[1][1];
end


/*Router 1,2*/    
merge_router #(
    .input_mask                     (input_mask[1][2]),
    .output_sel                     (output_sel[1][2])
)router7(
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
    data_i_1_2[3] = data_o_1_3[4];
    valid_i_1_2[3] = valid_o_1_3[4];
    ready_i_1_2[3] = ready_o_1_3[4];
    data_i_1_2[4] = data_o_1_1[3];
    valid_i_1_2[4] = valid_o_1_1[3];
    ready_i_1_2[4] = ready_o_1_1[3];
    data_i_1_2[1] = data_o_0_2[2];
    valid_i_1_2[1] = valid_o_0_2[2];
    ready_i_1_2[1] = ready_o_0_2[2];
    data_i_1_2[2] = data_o_2_2[1];
    valid_i_1_2[2] = valid_o_2_2[1];
    ready_i_1_2[2] = ready_o_2_2[1];
    data_i_1_2[0] = data_o_[1][2];
    valid_i_1_2[0] = valid_o_[1][2];
    ready_i_1_2[0] = ready_o_[1][2];
end


/*Router 2,0*/    
merge_router #(
    .input_mask                     (input_mask[2][0]),
    .output_sel                     (output_sel[2][0])
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
    data_i_2_0[1] = data_o_1_0[2];
    valid_i_2_0[1] = valid_o_1_0[2];
    ready_i_2_0[1] = ready_o_1_0[2];
    data_i_2_0[0] = data_o_[2][0];
    valid_i_2_0[0] = valid_o_[2][0];
    ready_i_2_0[0] = ready_o_[2][0];
end


/*Router 2,1*/    
merge_router #(
    .input_mask                     (input_mask[2][1]),
    .output_sel                     (output_sel[2][1])
)router5(
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
    data_i_2_1[3] = data_o_2_2[4];
    valid_i_2_1[3] = valid_o_2_2[4];
    ready_i_2_1[3] = ready_o_2_2[4];
    data_i_2_1[4] = data_o_2_0[3];
    valid_i_2_1[4] = valid_o_2_0[3];
    ready_i_2_1[4] = ready_o_2_0[3];
    data_i_2_1[1] = data_o_1_1[2];
    valid_i_2_1[1] = valid_o_1_1[2];
    ready_i_2_1[1] = ready_o_1_1[2];
    data_i_2_1[0] = data_o_[2][1];
    valid_i_2_1[0] = valid_o_[2][1];
    ready_i_2_1[0] = ready_o_[2][1];
end


/*Router 2,2*/    
merge_router #(
    .input_mask                     (input_mask[2][2]),
    .output_sel                     (output_sel[2][2])
)router8(
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
    data_i_2_2[3] = data_o_2_3[4];
    valid_i_2_2[3] = valid_o_2_3[4];
    ready_i_2_2[3] = ready_o_2_3[4];
    data_i_2_2[4] = data_o_2_1[3];
    valid_i_2_2[4] = valid_o_2_1[3];
    ready_i_2_2[4] = ready_o_2_1[3];
    data_i_2_2[1] = data_o_1_2[2];
    valid_i_2_2[1] = valid_o_1_2[2];
    ready_i_2_2[1] = ready_o_1_2[2];
    data_i_2_2[0] = data_o_[2][2];
    valid_i_2_2[0] = valid_o_[2][2];
    ready_i_2_2[0] = ready_o_[2][2];
end


endmodule
