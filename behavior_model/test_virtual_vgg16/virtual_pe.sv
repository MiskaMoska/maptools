//Not a behavior PE model, but a "virtual" PE model
//This PE model only simulates the data dependencies between different network interfaces, but does not simulate the computational behavior of the PE
//This PE model can only be used to verify where there exist deadlocks in the whole network
`include "param.svh"

module virtual_pe #(
    parameter isCaster = 0, //indicate whether the current node is a caster
    parameter [9:0] stream_id = 0 //the stream id generated from the current node, fixed at 10-bit
)(
    input       wire                            clk,
    input       wire                            rstn, 

    //cast network interface
    input       wire                            valid_i_cast,
    input       wire        [`DW-1:0]           data_i_cast,
    output      wire                            ready_o_cast,

    output      wire                            valid_o_cast,
    output      wire        [`DW-1:0]           data_o_cast,
    input       wire                            ready_i_cast,

    //merge network interface
    input       wire                            valid_i_merge,
    input       wire        [`DW-1:0]           data_i_merge,
    output      wire                            ready_o_merge,

    output      wire                            valid_o_merge,
    output      wire        [`DW-1:0]           data_o_merge,
    input       wire                            ready_i_merge
);

wire fifo_empty, fifo_full, fifo_read;
wire [`DW-1:0] fifo_dout;
assign fifo_read = ~fifo_empty & ready_o_nw;

SyncFIFO_RTL #(
    .width                   (`DW),
    .depth                   (`BUFFER_ALLOC),
    .depth_LOG               (`BUFFER_ALLOC_LOG),
    .FWFT                    (1)
)cast_receive_fifo(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (fifo_read),
    .write_i                 (valid_i_cast & ready_o_cast),
    .full_o                  (fifo_full),
    .empty_o                 (fifo_empty),
    .data_i                  (data_i_cast),
    .data_o                  (fifo_dout)
);

wire valid_i_pe, valid_o_pe, ready_o_nw, valid_o_nw, ready_o_pe, ready_i_pe;
wire [`DW-1:0] data_i_pe, data_o_pe, data_o_nw;

cast_converter #(
    .isCaster                 (isCaster),
    .stream_id                (stream_id)
)converter(
    .clk                      (clk),
    .rstn                     (rstn),
    .valid_i_pe               (valid_i_pe),
    .data_i_pe                (data_i_pe),
    .ready_o_pe               (ready_o_pe),
    .valid_o_pe               (valid_o_pe),
    .data_o_pe                (data_o_pe),
    .ready_i_pe               (ready_i_pe),
    .valid_i_nw               (~fifo_empty),
    .data_i_nw                (fifo_dout),
    .ready_o_nw               (ready_o_nw),
    .valid_o_nw               (valid_o_nw),
    .data_o_nw                (data_o_nw),
    .ready_i_nw               (ready_i_cast)
);

wire valid;
assign valid = valid_o_pe & valid_i_merge;
assign valid_i_pe = isCaster ? valid : 1'b0;
assign data_i_pe = data_o_pe + data_i_merge;
assign ready = valid & ready_o_pe;

assign ready_i_pe = isCaster ? ready : ready_i_merge;

assign ready_o_merge = isCaster ? ready : 1'b0;

assign valid_o_merge = isCaster ? 1'b0 : valid_o_pe;
assign data_o_merge = data_o_pe;

assign valid_o_cast = valid_o_nw; 
assign data_o_cast = data_o_nw;
assign ready_o_cast = ~fifo_full;

endmodule