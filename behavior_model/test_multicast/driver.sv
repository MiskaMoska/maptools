/*The driver on the multicast source node input port*/
`include "params.svh"

module driver (
    input   wire    clk,
    input   wire    rstn,
    input   wire    ready,
    output  wire    valid,
    output  wire    [`DW-1 : 0]   data
);

reg [31:0] cnt;
int send_cnt = 0;
reg [9:0] addr;
reg valid_reg;
wire valid_wire;
(* ramstyle = "AUTO" *) reg [`DW-1 : 0] packets [0:999];

initial 
begin
    addr = 0;
    cnt = 0;
    $readmemb("/mnt/f/git/NVCIM-COMM/behavior_model/test_multicast/send_pool",packets);
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

assign valid_wire = 1;
// assign valid_wire = ~(
//             (cnt > 153) & (cnt < 200) |
//             (cnt > 400) & (cnt < 440) |
//             (cnt > 510) & (cnt < 540) |
//             (cnt > 700) & (cnt < 719) |
//             (cnt > 800) & (cnt < 840) 
// );

always@(posedge clk or negedge rstn)
begin
    if(~rstn) 
        valid_reg <= 1;
    else if((addr == 999) & valid & ready)
        valid_reg <= 0;
end

assign valid = valid_wire & valid_reg;
assign data = (~rstn) & (addr >= 1000) ? 0 : packets[addr];

endmodule