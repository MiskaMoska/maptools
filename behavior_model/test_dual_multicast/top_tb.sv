`timescale 1ns/1ps
`include "params.svh"

module top_tb;

reg clk;
reg rstn;
wire [`DW-1:0] drv_data_1,drv_data_2;
wire drv_valid_1,drv_valid_2;
reg [`DW-1:0] noc_data_i[`NOC_WIDTH][`NOC_HEIGHT];
reg  noc_valid_i[`NOC_WIDTH][`NOC_HEIGHT];
wire noc_ready_o[`NOC_WIDTH][`NOC_HEIGHT],noc_valid_o[`NOC_WIDTH][`NOC_HEIGHT];
wire [`DW-1:0] noc_data_o[`NOC_WIDTH][`NOC_HEIGHT];
reg noc_ready_i[`NOC_WIDTH][`NOC_HEIGHT];
reg noc_credit_upd[`NOC_WIDTH][`NOC_HEIGHT];

wire mon_ready_0;
wire mon_ready_1;
wire mon_ready_2;
wire mon_ready_3;
wire mon_ready_4;
wire mon_ready_5;
wire mon_ready_6;
wire mon_ready_7;
wire mon_ready_8;

wire mon_credit_0;
wire mon_credit_1;
wire mon_credit_2;
wire mon_credit_3;
wire mon_credit_4;
wire mon_credit_5;
wire mon_credit_6;
wire mon_credit_7;
wire mon_credit_8;

initial begin
    $fsdbDumpfile("wave.fsdb");
    $fsdbDumpvars(0,cast_network);
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
            noc_credit_upd[i][j] = 1'b0;
        end
    end
end

cast_network noc(
    .clk(clk),
    .rstn(rstn),
    
    //router local ports
    .data_i(noc_data_i),
    .valid_i(noc_valid_i),
    .ready_o(noc_ready_o),

    .data_o(noc_data_o),
    .valid_o(noc_valid_o),
    .ready_i(noc_ready_i),

    //credit update signal input
    .credit_upd(noc_credit_upd)
);

driver #(
    .id("1")
)drv1(
    .clk(clk),
    .rstn(rstn),
    .ready(noc_ready_o[1][0]),
    .valid(drv_valid_1),
    .data(drv_data_1)
);

driver #(
    .id("2")
)drv2(
    .clk(clk),
    .rstn(rstn),
    .ready(noc_ready_o[2][0]),
    .valid(drv_valid_2),
    .data(drv_data_2)
);

monitor #(
    .id("0")
)mon0(
    .clk(clk),
    .rstn(rstn),
    .valid(noc_valid_o[0][0]),
    .ready(mon_ready_0),
    .data(noc_data_o[0][0]),
    .credit_upd(mon_credit_0)
);

monitor #(
    .id("1")
)mon1(
    .clk(clk),
    .rstn(rstn),
    .valid(noc_valid_o[1][0]),
    .ready(mon_ready_1),
    .data(noc_data_o[1][0]),
    .credit_upd(mon_credit_1)
);

monitor #(
    .id("2")
)mon2(
    .clk(clk),
    .rstn(rstn),
    .valid(noc_valid_o[2][0]),
    .ready(mon_ready_2),
    .data(noc_data_o[2][0]),
    .credit_upd(mon_credit_2)
);

monitor #(
    .id("3")
)mon3(
    .clk(clk),
    .rstn(rstn),
    .valid(noc_valid_o[0][1]),
    .ready(mon_ready_3),
    .data(noc_data_o[0][1]),
    .credit_upd(mon_credit_3)
);

monitor #(
    .id("4")
)mon4(
    .clk(clk),
    .rstn(rstn),
    .valid(noc_valid_o[1][1]),
    .ready(mon_ready_4),
    .data(noc_data_o[1][1]),
    .credit_upd(mon_credit_4)
);

monitor #(
    .id("5")
)mon5(
    .clk(clk),
    .rstn(rstn),
    .valid(noc_valid_o[2][1]),
    .ready(mon_ready_5),
    .data(noc_data_o[2][1]),
    .credit_upd(mon_credit_5)
);

monitor #(
    .id("6")
)mon6(
    .clk(clk),
    .rstn(rstn),
    .valid(noc_valid_o[0][2]),
    .ready(mon_ready_6),
    .data(noc_data_o[0][2]),
    .credit_upd(mon_credit_6)
);

monitor #(
    .id("7")
)mon7(
    .clk(clk),
    .rstn(rstn),
    .valid(noc_valid_o[1][2]),
    .ready(mon_ready_7),
    .data(noc_data_o[1][2]),
    .credit_upd(mon_credit_7)
);

monitor #(
    .id("8")
)mon8(
    .clk(clk),
    .rstn(rstn),
    .valid(noc_valid_o[2][2]),
    .ready(mon_ready_8),
    .data(noc_data_o[2][2]),
    .credit_upd(mon_credit_8)
);

always@(drv_data_1 or drv_data_2) begin
    noc_data_i[1][0] = drv_data_1;
    noc_data_i[2][0] = drv_data_2;
end

always@(drv_valid_1 or drv_valid_2) begin
    noc_valid_i[1][0] = drv_valid_1;
    noc_valid_i[2][0] = drv_valid_2;
end

always@(mon_ready_0 or mon_ready_1 or mon_ready_2 or mon_ready_3 or mon_ready_4 or mon_ready_5 or mon_ready_6 or mon_ready_7 or mon_ready_8) begin
    noc_ready_i[0][0] = mon_ready_0;
    noc_ready_i[1][0] = mon_ready_1;
    noc_ready_i[2][0] = mon_ready_2;
    noc_ready_i[0][1] = mon_ready_3;
    noc_ready_i[1][1] = mon_ready_4;
    noc_ready_i[2][1] = mon_ready_5;
    noc_ready_i[0][2] = mon_ready_6;
    noc_ready_i[1][2] = mon_ready_7;
    noc_ready_i[2][2] = mon_ready_8;
end

always@(mon_credit_0 or mon_credit_1 or mon_credit_2 or mon_credit_3 or mon_credit_4 or mon_credit_5 or mon_credit_6 or mon_credit_7 or mon_credit_8) begin
    noc_credit_upd[0][0] = mon_credit_0;
    noc_credit_upd[1][0] = mon_credit_1;
    noc_credit_upd[2][0] = mon_credit_2;
    noc_credit_upd[0][1] = mon_credit_3;
    noc_credit_upd[1][1] = mon_credit_4;
    noc_credit_upd[2][1] = mon_credit_5;
    noc_credit_upd[0][2] = mon_credit_6;
    noc_credit_upd[1][2] = mon_credit_7;
    noc_credit_upd[2][2] = mon_credit_8;
end

endmodule