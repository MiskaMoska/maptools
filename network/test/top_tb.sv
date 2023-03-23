
`timescale 1ns/1ps
`include "params.svh"

module top_tb;

reg clk;
reg rstn;
reg [31:0] addr;

integer state_file;
integer file0; wire [`DW-1:0] data_o_flee0; wire valid_o_flee0, ready_i_flee0;
assign ready_i_flee0 = rstn;
integer file1; wire [`DW-1:0] data_o_flee1; wire valid_o_flee1, ready_i_flee1;
assign ready_i_flee1 = rstn;
integer file2; wire [`DW-1:0] data_o_flee2; wire valid_o_flee2, ready_i_flee2;
assign ready_i_flee2 = rstn;
integer file3; wire [`DW-1:0] data_o_flee3; wire valid_o_flee3, ready_i_flee3;
assign ready_i_flee3 = rstn;
integer file4; wire [`DW-1:0] data_o_flee4; wire valid_o_flee4, ready_i_flee4;
assign ready_i_flee4 = rstn;
integer file5; wire [`DW-1:0] data_o_flee5; wire valid_o_flee5, ready_i_flee5;
assign ready_i_flee5 = rstn;
integer file6; wire [`DW-1:0] data_o_flee6; wire valid_o_flee6, ready_i_flee6;
assign ready_i_flee6 = rstn;
integer file7; wire [`DW-1:0] data_o_flee7; wire valid_o_flee7, ready_i_flee7;
assign ready_i_flee7 = rstn;

(* ramstyle = "AUTO" *) reg [`DW-1 : 0] packets [0:9999];
wire [`DW-1:0] data_i_stab;
wire ready_o_stab;
reg valid_i_stab;

initial begin
    clk = 0;
    rstn = 1;
    # 33 rstn = 0;
    # 71 rstn = 1;
    valid_i_stab = 1;
    while(1) begin
        @(posedge clk);
        if((addr == 9999) & valid_i_stab & ready_o_stab) begin
            valid_i_stab <= 1'b0;
            // break;
        end
    end
    # 1000000
    $fwrite(state_file,"%s","normal");

    $fclose(file0);
    $fclose(file1);
    $fclose(file2);
    $fclose(file3);
    $fclose(file4);
    $fclose(file5);
    $fclose(file6);
    $fclose(file7);
    $fclose(state_file);
    $finish;
end

initial begin
    $fsdbDumpfile("wave.fsdb");
    $fsdbDumpvars(0,top_tb);
    $fsdbDumpMDA(); //show array values
file0 = $fopen("/mnt/c/git/nvcim-comm/network/test/receive_pool_flee0.txt");
file1 = $fopen("/mnt/c/git/nvcim-comm/network/test/receive_pool_flee1.txt");
file2 = $fopen("/mnt/c/git/nvcim-comm/network/test/receive_pool_flee2.txt");
file3 = $fopen("/mnt/c/git/nvcim-comm/network/test/receive_pool_flee3.txt");
file4 = $fopen("/mnt/c/git/nvcim-comm/network/test/receive_pool_flee4.txt");
file5 = $fopen("/mnt/c/git/nvcim-comm/network/test/receive_pool_flee5.txt");
file6 = $fopen("/mnt/c/git/nvcim-comm/network/test/receive_pool_flee6.txt");
file7 = $fopen("/mnt/c/git/nvcim-comm/network/test/receive_pool_flee7.txt");

    state_file = $fopen("/mnt/c/git/nvcim-comm/network/test/run_state");
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
            else if(addr != 9999 & addr != 0 & win == 9999 && addr == start_addr) begin // deadlock occurs
                $fwrite(state_file,"%s","deadlock");

                $fclose(file0);
                $fclose(file1);
                $fclose(file2);
                $fclose(file3);
                $fclose(file4);
                $fclose(file5);
                $fclose(file6);
                $fclose(file7);
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
    $readmemb("/mnt/c/git/nvcim-comm/network/test/send_pool.txt",packets);
end

always@(posedge clk or negedge rstn)
begin
    if(~rstn) addr <= 0;
    else if(valid_i_stab & ready_o_stab) begin
        if(addr == 9999) addr <= 0;
        else addr <= addr + 1;
    end 
end

//always@(posedge clk) begin
//    $display("addr@driver: %d",addr);
//end

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
    .ready_i_flee1               (ready_i_flee1),
    .data_o_flee2                (data_o_flee2),
    .valid_o_flee2               (valid_o_flee2),
    .ready_i_flee2               (ready_i_flee2),
    .data_o_flee3                (data_o_flee3),
    .valid_o_flee3               (valid_o_flee3),
    .ready_i_flee3               (ready_i_flee3),
    .data_o_flee4                (data_o_flee4),
    .valid_o_flee4               (valid_o_flee4),
    .ready_i_flee4               (ready_i_flee4),
    .data_o_flee5                (data_o_flee5),
    .valid_o_flee5               (valid_o_flee5),
    .ready_i_flee5               (ready_i_flee5),
    .data_o_flee6                (data_o_flee6),
    .valid_o_flee6               (valid_o_flee6),
    .ready_i_flee6               (ready_i_flee6),
    .data_o_flee7                (data_o_flee7),
    .valid_o_flee7               (valid_o_flee7),
    .ready_i_flee7               (ready_i_flee7)
);

always@(posedge clk) begin
    if(valid_o_flee0 & ready_i_flee0)  
        $fwrite(file0, "%b\n", data_o_flee0);
    if(valid_o_flee1 & ready_i_flee1)  
        $fwrite(file1, "%b\n", data_o_flee1);
    if(valid_o_flee2 & ready_i_flee2)  
        $fwrite(file2, "%b\n", data_o_flee2);
    if(valid_o_flee3 & ready_i_flee3)  
        $fwrite(file3, "%b\n", data_o_flee3);
    if(valid_o_flee4 & ready_i_flee4)  
        $fwrite(file4, "%b\n", data_o_flee4);
    if(valid_o_flee5 & ready_i_flee5)  
        $fwrite(file5, "%b\n", data_o_flee5);
    if(valid_o_flee6 & ready_i_flee6)  
        $fwrite(file6, "%b\n", data_o_flee6);
    if(valid_o_flee7 & ready_i_flee7)  
        $fwrite(file7, "%b\n", data_o_flee7);
end

endmodule

