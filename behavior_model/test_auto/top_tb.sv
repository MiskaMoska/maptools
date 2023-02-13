`timescale 1ns/1ps
`include "params.svh"

module top_tb;

reg clk;
reg rstn;
reg [31:0] addr;

integer file0,file1,state_file;

(* ramstyle = "AUTO" *) reg [`DW-1 : 0] packets [0:10000];
wire [`DW-1:0] data_i_stab;
wire valid_i_stab, ready_o_stab;
assign valid_i_stab = rstn & (addr < 10000);

wire [`DW-1:0] data_o_flee0, data_o_flee1;
wire valid_o_flee0, valid_o_flee1;
wire ready_i_flee0, ready_i_flee1;

reg [31:0] push0,push1;
always@(posedge clk or negedge rstn) begin
    if(~rstn) push0 <= 0;
    else begin
        if(push0 == 15) push0 <= 0;
        else push0 <= push0 + 1;
    end
end

always@(posedge clk or negedge rstn) begin
    if(~rstn) push1 <= 0;
    else begin
        if(push1 == 19) push1 <= 0;
        else push1 <= push1 + 1;
    end
end

assign ready_i_flee0 = rstn & (push0 > 9);
assign ready_i_flee1 = rstn & (push1 > 11);

always@(posedge clk) begin
    $display("rom_addr@driver: %f",addr);
end

real t;

initial begin
    $fsdbDumpfile("wave.fsdb");
    $fsdbDumpvars(0,dut);
    $fsdbDumpMDA(); //show array values 
    file0 = $fopen("/mnt/c/git/NVCIM-COMM/behavior_model/test_auto/receive_pool_flee0");
    file1 = $fopen("/mnt/c/git/NVCIM-COMM/behavior_model/test_auto/receive_pool_flee1");
    state_file = $fopen("/mnt/c/git/NVCIM-COMM/behavior_model/test_auto/run_state");
    clk = 0;
    rstn = 1;
    # 33 rstn = 0;
    # 71 rstn = 1;
    // #10000 $stop;
    wait(addr == 10000);
    t = $realtime;
    # 500000
    $fwrite(state_file,"%s","normal");
    $fclose(file0);
    $fclose(file1);
    $fclose(state_file);
    $display("elapsed sending time: %f",t);
    $finish;
end

// deadlock detection
initial begin
    int win;
    int start_addr;
    forever begin
        @(posedge clk)
        if(~rstn) win <= 0;
        else begin
            if(win == 9999) win <= 0;
            else win <= win + 1;
            if(win == 0) start_addr <= addr;
            else if(win == 9999 && addr != 10000 && addr == start_addr) begin // deadlock occurs
                $fwrite(state_file,"%s","deadlock");
                $fclose(file0);
                $fclose(file1);
                $fclose(state_file);
                $display("ERROR: deadlock detected!!!!!");
                $finish;
            end
        end
    end
end

always #5 clk = ~clk;

initial begin
    addr = 0;
    $readmemb("/mnt/c/git/NVCIM-COMM/behavior_model/test_auto/send_pool",packets);
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