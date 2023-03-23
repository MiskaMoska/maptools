`include "params.svh"

module cast_input_stage #(
    parameter   isUBM = 0, //whether adopt unicast-based-multicast
    parameter   isFC = 0, //is the FC start port or not
    parameter   [`NOC_WIDTH*`NOC_HEIGHT-1:0] FCdn = {(`NOC_WIDTH*`NOC_HEIGHT){1'b0}}, //FC destination nodes
    parameter   int FCpl = 16, //FC packet length
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
    input       wire                            ready_i,

    input       wire                            credit_upd[`NOC_WIDTH][`NOC_HEIGHT]    
);

wire            fifo_read,fifo_write;
wire            fifo_empty,fifo_full;
wire [`DW-1:0]  fifo_din,fifo_dout;
wire [`CN-1:0]  candidateOutVC;
wire [15:0]     credit_cnt;
wire            pop,read_reset;

assign fifo_din = data_i;
assign data_o = fifo_dout;

assign fire = valid_o & ready_i;
assign fifo_read = fire;
assign fifo_write = valid_i & ready_o;

// assign valid_o = ~fifo_empty;
assign valid_o = ~fifo_empty & ready_i;
assign ready_o = ~fifo_full;

nfifo_ubm #(
    .width                   (`DW),
    .depth                   (2**`CAST_ROUTER_BUFFER_DEPTH_LOG),
    .depth_LOG               (`CAST_ROUTER_BUFFER_DEPTH_LOG),
    .FWFT                    (1)
)fifo(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (fifo_read),
    .write_i                 (fifo_write),
    .full_o                  (fifo_full),
    .empty_o                 (fifo_empty),
    .data_i                  (fifo_din),
    .data_o                  (fifo_dout),
    .pop                     (pop),
    .read_reset              (read_reset)
);

cast_route_table #(
    .rt_file                 (rt_file)
)rt(
    .clk                     (clk),
    .rstn                    (rstn),  

    .stream_id               (fifo_dout[`STREAM_ID_H:`STREAM_ID_L]),
    .candidateOutVC          (candidateOutVC)
);

cast_input_controller #(
    .isUBM                   (isUBM),
    .isFC                    (isFC), 
    .FCpl                    (FCpl)
)ctlr(
    .clk                     (clk),
    .rstn                    (rstn),
    .fifo_empty              (fifo_empty),
    .candidateOutVC          (candidateOutVC),
    .reqVC                   (reqVC),
    .selOutVC                (selOutVC),
    .VCgranted               (VCgranted),
    .selXBVC                 (selXBVC),
    .flit_type               (fifo_dout[`DW-1:`DW-2]),
    .flit_fire               (fire),
    .pop                     (pop),
    .read_reset              (read_reset),
    .credit_cnt              (credit_cnt)
);

cast_credit_counter #(
    .isFC                    (isFC), //is the FC start port or not
    .FCdn                    (FCdn), //FC destination nodes
    .FCpl                    (FCpl) //FC packet length
)cc( 
    .clk                     (clk),
    .rstn                    (rstn), 
    .fire                    (fire),
    .flit_type               (fifo_dout[`DW-1:`DW-2]), 
    .credit_upd              (credit_upd),
    .credit_cnt              (credit_cnt),
    .pop                     (pop)
);

endmodule