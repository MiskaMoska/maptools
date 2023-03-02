`timescale 1ns/1ps
`include "params.svh"

module top_tb;

reg clk;
reg rstn;
reg [31:0] addr;

integer file0,file1,state_file;

(* ramstyle = "AUTO" *) reg [`DW-1 : 0] packets [0:9999];
wire [`DW-1:0] data_i_stab;
wire ready_o_stab;
reg valid_i_stab;

wire [`DW-1:0] data_o_flee0, data_o_flee1;
wire valid_o_flee0, valid_o_flee1;
wire ready_i_flee0, ready_i_flee1;

// //back pressure
// reg [31:0] push0,push1;
// always@(posedge clk or negedge rstn) begin
//     if(~rstn) push0 <= 0;
//     else begin
//         if(push0 == 15) push0 <= 0;
//         else push0 <= push0 + 1;
//     end
// end

// always@(posedge clk or negedge rstn) begin
//     if(~rstn) push1 <= 0;
//     else begin
//         if(push1 == 19) push1 <= 0;
//         else push1 <= push1 + 1;
//     end
// end

assign ready_i_flee0 = rstn;
assign ready_i_flee1 = rstn;

initial begin
    clk = 0;
    rstn = 1;
    # 33 rstn = 0;
    # 71 rstn = 1;
    valid_i_stab = 1;
    wait((addr == 9999) & valid_i_stab & ready_o_stab);
    valid_i_stab <= 1'b0;
    # 100000
    $fwrite(state_file,"%s","normal");
    $fclose(file0);
    $fclose(file1);
    $fclose(state_file);
    $finish;
end

initial begin
    $fsdbDumpfile("wave.fsdb");
    $fsdbDumpvars(0,top_tb);
    $fsdbDumpMDA(); //show array values 
    file0 = $fopen("/mnt/c/git/NVCIM-COMM/network/receive_pool_flee0.txt");
    file1 = $fopen("/mnt/c/git/NVCIM-COMM/network/receive_pool_flee1.txt");
    state_file = $fopen("/mnt/c/git/NVCIM-COMM/network/run_state");
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
            else if(win == 9999 && addr == start_addr) begin // deadlock occurs
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
    $readmemb("/mnt/c/git/NVCIM-COMM/network/send_pool.txt",packets);
end

always@(posedge clk or negedge rstn)
begin
    if(~rstn) addr <= 0;
    else if(valid_i_stab & ready_o_stab) begin
        if(addr == 9999) addr <= 0;
        else addr <= addr + 1;
    end 
end

always@(posedge clk) begin
    $display("addr@driver: %d",addr);
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