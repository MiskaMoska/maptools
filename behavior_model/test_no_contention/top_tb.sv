`timescale 1ns/1ps
`include "params.svh"

module top_tb;

reg clk;
reg rstn;
reg [31:0] addr;

integer file0,file1;
(* ramstyle = "AUTO" *) reg [`DW-1 : 0] packets [0:10000];
wire [`DW-1:0] data_i_stab;
wire valid_i_stab, ready_o_stab;
assign valid_i_stab = rstn & (addr < 10000);

wire [`DW-1:0] data_o_flee0, data_o_flee1;
wire valid_o_flee0, valid_o_flee1;
wire ready_i_flee0, ready_i_flee1;

reg [31:0] push;
always@(posedge clk or negedge rstn) begin
    if(~rstn) push <= 0;
    else begin
        if(push == 15) push <= 0;
        else push <= push + 1;
    end
end

assign ready_i_flee0 = rstn & (push > 14);
assign ready_i_flee1 = rstn;

always@(posedge clk) begin
    $display("rom_addr@driver: %f",addr);
end

real t;

initial begin
    $fsdbDumpfile("wave.fsdb");
    $fsdbDumpvars(0,dut);
    $fsdbDumpMDA(); //show array values 
    file0 = $fopen("/mnt/c/git/NVCIM-COMM/behavior_model/test_no_contention/receive_pool_flee0");
    file1 = $fopen("/mnt/c/git/NVCIM-COMM/behavior_model/test_no_contention/receive_pool_flee1");
    clk = 0;
    rstn = 1;
    # 33 rstn = 0;
    # 71 rstn = 1;
    // #10000 $stop;
    wait(addr == 10000);
    t = $realtime;
    # 500000
    $fclose(file0);
    $fclose(file1);
    $display("elapsed sending time: %f",t);
    $stop;
end

always #5 clk = ~clk;

initial begin
    addr = 0;
    $readmemb("/mnt/c/git/NVCIM-COMM/behavior_model/test_virtual_vgg16/send_pool",packets);
    // $display("cnt@driver: %f",cnt);
end

always@(posedge clk or negedge rstn)
begin
    if(~rstn) addr <= 0;
    else if(valid_i_stab & ready_o_stab) addr <= addr + 1;
end

assign data_i_stab = packets[addr];

system dut(
    .clk                         (clk),
    .rstn                        (rstn),
    .data_i_stab                 (data_i_stab),
    .valid_i_stab                (valid_i_stab),
    .ready_o_stab                (ready_o_stab),
    .data_o_flee0                (data_o_flee0),
    .valid_o_flee0               (valid_o_flee0),
    .ready_i_flee0               (ready_i_flee0),
    .data_o_flee1                (data_o_flee1),
    .valid_o_flee1               (valid_o_flee1),
    .ready_i_flee1               (ready_i_flee1)
);

always@(posedge clk) begin
    if(valid_o_flee0 & ready_i_flee0)  $fwrite(file0, "%b\n", data_o_flee0);
    if(valid_o_flee1 & ready_i_flee1)  $fwrite(file1, "%b\n", data_o_flee1);
end

endmodule