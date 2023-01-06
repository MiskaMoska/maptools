`timescale 1ns/1ps
`include "params.svh"

module top_tb;

reg clk, rstn;

wire noc_ready_o[`NOC_WIDTH][`NOC_HEIGHT],noc_valid_o[`NOC_WIDTH][`NOC_HEIGHT];
wire [`DW-1:0] noc_data_o[`NOC_WIDTH][`NOC_HEIGHT];

reg noc_ready_i[`NOC_WIDTH][`NOC_HEIGHT],noc_valid_i[`NOC_WIDTH][`NOC_HEIGHT];
reg [`DW-1:0] noc_data_i[`NOC_WIDTH][`NOC_HEIGHT];

wire drv_valid_0;
wire drv_valid_1;
wire drv_valid_2;
wire drv_valid_3;
wire drv_valid_4;
wire drv_valid_5;
wire drv_valid_7;
wire drv_valid_8;

wire [`DW-1:0] drv_data_0;
wire [`DW-1:0] drv_data_1;
wire [`DW-1:0] drv_data_2;
wire [`DW-1:0] drv_data_3;
wire [`DW-1:0] drv_data_4;
wire [`DW-1:0] drv_data_5;
wire [`DW-1:0] drv_data_7;
wire [`DW-1:0] drv_data_8;

wire mon_ready_6;

initial begin
    $fsdbDumpfile("wave.fsdb");
    $fsdbDumpvars(0,merge_network);
    $fsdbDumpMDA(); //show array values 
    clk = 0;
    rstn = 1;
    # 33 rstn = 0;
    # 71 rstn = 1;
    // #10000 $stop;
end

always #5 clk = ~clk;

initial begin
    for(int i=0;i<`NOC_WIDTH;i++) begin
        for(int j=0;j<`NOC_HEIGHT;j++) begin
            noc_data_i[i][j] = {(`DW){1'b0}};
            noc_valid_i[i][j] = 1'b0;
            noc_ready_i[i][j] = 1'b0;
        end
    end
end

merge_network noc(
    .clk(clk),
    .rstn(rstn),
    
    //router local ports
    .data_i(noc_data_i),
    .valid_i(noc_valid_i),
    .ready_o(noc_ready_o),

    .data_o(noc_data_o),
    .valid_o(noc_valid_o),
    .ready_i(noc_ready_i)
);


driver drv0(
    .clk(clk),
    .rstn(rstn),
    .ready(noc_ready_o[0][0]),
    .valid(drv_valid_0),
    .data(drv_data_0)
);

driver drv1(
    .clk(clk),
    .rstn(rstn),
    .ready(noc_ready_o[1][0]),
    .valid(drv_valid_1),
    .data(drv_data_1)
);

driver drv2(
    .clk(clk),
    .rstn(rstn),
    .ready(noc_ready_o[2][0]),
    .valid(drv_valid_2),
    .data(drv_data_2)
);

driver drv3(
    .clk(clk),
    .rstn(rstn),
    .ready(noc_ready_o[0][1]),
    .valid(drv_valid_3),
    .data(drv_data_3)
);

driver drv4(
    .clk(clk),
    .rstn(rstn),
    .ready(noc_ready_o[1][1]),
    .valid(drv_valid_4),
    .data(drv_data_4)
);

driver drv5(
    .clk(clk),
    .rstn(rstn),
    .ready(noc_ready_o[2][1]),
    .valid(drv_valid_5),
    .data(drv_data_5)
);

driver drv7(
    .clk(clk),
    .rstn(rstn),
    .ready(noc_ready_o[1][2]),
    .valid(drv_valid_7),
    .data(drv_data_7)
);

driver drv8(
    .clk(clk),
    .rstn(rstn),
    .ready(noc_ready_o[2][2]),
    .valid(drv_valid_8),
    .data(drv_data_8)
);

monitor mon6(
    .clk(clk),
    .rstn(rstn),
    .valid(noc_valid_o[0][2]),
    .ready(mon_ready_6),
    .data(noc_data_o[0][2])
);

always@(drv_valid_0 or drv_valid_1 or drv_valid_2 or drv_valid_3 or drv_valid_4 or drv_valid_5 or drv_valid_7 or drv_valid_8) begin
    noc_valid_i[0][0] = drv_valid_0;
    noc_valid_i[1][0] = drv_valid_1;
    noc_valid_i[2][0] = drv_valid_2;
    noc_valid_i[0][1] = drv_valid_3;
    noc_valid_i[1][1] = drv_valid_4;
    noc_valid_i[2][1] = drv_valid_5;
    noc_valid_i[1][2] = drv_valid_7;
    noc_valid_i[2][2] = drv_valid_8;
end

always@(mon_ready_6) begin
    noc_ready_i[0][2] = mon_ready_6;
end

always@(drv_data_0 or drv_data_1 or drv_data_2 or drv_data_3 or drv_data_4 or drv_data_5 or drv_data_7 or drv_data_8) begin
    noc_data_i[0][0] = drv_data_0;
    noc_data_i[1][0] = drv_data_1;
    noc_data_i[2][0] = drv_data_2;
    noc_data_i[0][1] = drv_data_3;
    noc_data_i[1][1] = drv_data_4;
    noc_data_i[2][1] = drv_data_5;
    noc_data_i[1][2] = drv_data_7;
    noc_data_i[2][2] = drv_data_8;
end

endmodule