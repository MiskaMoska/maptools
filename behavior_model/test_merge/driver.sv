/*The driver on the merge source node input port*/
`include "params.svh"

module driver(
    input   wire    clk,
    input   wire    rstn,
    input   wire    ready,
    output  wire    valid,
    output  wire    [`DW-1 : 0]   data
);

reg [31:0] cnt;
int send_cnt = 0;
reg [9:0] addr;
reg valid_reg = 1'b1;
(* ramstyle = "AUTO" *) reg [`DW-1 : 0] packets [0:31];

initial 
begin
    addr = 0;
    cnt = 0;
    $readmemb("/mnt/c/git/NVCIM-COMM/behavior_model/test_merge/send_pool",packets);
    // $display("cnt@driver: %f",cnt);
end

always@(posedge clk) begin
    $display("rom_addr@driver: %f",addr);
end

always@(posedge clk or negedge rstn)
begin
    if(~rstn) addr <= 0;
    else if(valid & ready) addr <= addr + 1;
end

always@(posedge clk)
begin
    cnt <= cnt + 1;
end

always@(posedge clk) begin
    if((addr == 1023) & valid & ready) valid_reg <= 1'b0;
end

assign valid = rstn & valid_reg;
assign data = packets[addr[4:0]];

endmodule