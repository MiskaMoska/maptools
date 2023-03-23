`include "params.svh"

module gather_input_stage #(
    parameter   string rt_file = "/mnt/f/git/NVCIM-COMM/behavior_model/config/cast_rt_0_0_4"
)(
    input       wire                            clk,
    input       wire                            rstn, 

    input       wire                            valid_i,
    input       wire        [`DW-1:0]           data_i,
    output      wire                            ready_o,

    output      wire        [`CN-1:0]           reqVC, //to vc_allocator
    input       wire        [`CN-1:0]           selOutVC, //from vc_allocator
    input       wire                            VCgranted, //from vc_allocator
    output      wire        [`CN-1:0]           selXBVC, //to crossbar

    output      wire                            valid_o,
    output      wire        [`DW-1:0]           data_o,
    input       wire                            ready_i
);

wire            fifo_read,fifo_write;
wire            fifo_empty,fifo_full;
wire [`DW-1:0]  fifo_din,fifo_dout;
wire [`CN-1:0]  candidateOutVC;

assign fifo_din = data_i;
assign data_o = fifo_dout;

assign fire = valid_o & ready_i;
assign fifo_read = fire;
assign fifo_write = valid_i & ready_o;

// assign valid_o = ~fifo_empty;
assign valid_o = ~fifo_empty & ready_i;
assign ready_o = ~fifo_full;

nfifo #(
    .width                   (`DW),
    .depth                   (2**`GATHER_ROUTER_BUFFER_DEPTH_LOG),
    .depth_LOG               (`GATHER_ROUTER_BUFFER_DEPTH_LOG),
    .FWFT                    (1)
)fifo(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (fifo_read),
    .write_i                 (fifo_write),
    .full_o                  (fifo_full),
    .empty_o                 (fifo_empty),
    .data_i                  (fifo_din),
    .data_o                  (fifo_dout)
);

gather_route_table #(
    .rt_file                 (rt_file)
)rt(
    .clk                     (clk),
    .rstn                    (rstn),  

    .stream_id               (fifo_dout[`STREAM_ID_H:`STREAM_ID_L]),
    .candidateOutVC          (candidateOutVC)
);

gather_input_controller ctlr(
    .clk                     (clk),
    .rstn                    (rstn),
    .fifo_empty              (fifo_empty),
    .candidateOutVC          (candidateOutVC),
    .reqVC                   (reqVC),
    .selOutVC                (selOutVC),
    .VCgranted               (VCgranted),
    .selXBVC                 (selXBVC),
    .flit_type               (fifo_dout[`DW-1:`DW-2]),
    .flit_fire               (fire)
);

endmodule