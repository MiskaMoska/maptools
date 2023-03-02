`include "params.svh"

module pe_ni #(
    parameter isCaster = 0, //indicate whether the current node is a caster
    parameter [9:0] stream_id = 0 //the stream id generated from the current node, fixed at 10-bit
)(
    input       wire                            clk,
    input       wire                            rstn, 

    //cast network end
    input       wire                            valid_i_cast_nw,
    input       wire        [`DW-1:0]           data_i_cast_nw,
    output      wire                            ready_o_cast_nw,

    output      wire                            valid_o_cast_nw,
    output      wire        [`DW-1:0]           data_o_cast_nw,
    input       wire                            ready_i_cast_nw,

    //merge network end
    input       wire                            valid_i_merge_nw,
    input       wire        [`DW-1:0]           data_i_merge_nw,
    output      wire                            ready_o_merge_nw,

    output      wire                            valid_o_merge_nw,
    output      wire        [`DW-1:0]           data_o_merge_nw,
    input       wire                            ready_i_merge_nw,

    //cast pe end
    input       wire                            valid_i_cast_pe,
    input       wire        [`DW-1:0]           data_i_cast_pe,
    output      wire                            ready_o_cast_pe,

    output      wire                            valid_o_cast_pe,
    output      wire        [`DW-1:0]           data_o_cast_pe,
    input       wire                            ready_i_cast_pe,

    //merge pe end
    input       wire                            valid_i_merge_pe,
    input       wire        [`DW-1:0]           data_i_merge_pe,
    output      wire                            ready_o_merge_pe,

    output      wire                            valid_o_merge_pe,
    output      wire        [`DW-1:0]           data_o_merge_pe,
    input       wire                            ready_i_merge_pe,

    //credit update signal
    output      wire                            credit_upd
);

assign valid_o_merge_pe = valid_i_merge_nw;
assign data_o_merge_pe = data_i_merge_nw;
assign ready_o_merge_pe = ready_i_merge_nw;
assign valid_o_merge_nw = valid_i_merge_pe;
assign data_o_merge_nw = data_i_merge_pe;
assign ready_o_merge_nw = ready_i_merge_pe;

wire valid_o_nw;
wire [`DW-1:0] data_o_nw;
wire fifo_empty, fifo_full, fifo_read;
wire [`DW-1:0] fifo_dout;
wire [7:0] ofifo_cnt;
wire ofifo_full;
wire [`DW-1:0] ofifo_dout;

assign data_o_cast_nw = ofifo_dout;
assign fifo_read = ~fifo_empty & ready_o_nw;
assign credit_upd = fifo_read;

// cast network end receive buffer
SyncFIFO_RTL #(
    .width                   (`DW),
    .depth                   (`BUFFER_ALLOC),
    .depth_LOG               (`BUFFER_ALLOC_LOG),
    .FWFT                    (1)
)cast_receive_fifo(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (fifo_read),
    .write_i                 (valid_i_cast_nw & ready_o_cast_nw),
    .full_o                  (fifo_full),
    .empty_o                 (fifo_empty),
    .data_i                  (data_i_cast_nw),
    .data_o                  (fifo_dout)
);

// cast network end send buffer
SyncFIFO_RTL_CNT #(
    .width                   (`DW),
    .depth                   (128),
    .depth_LOG               (7),
    .FWFT                    (1)
)cast_send_fifo(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (valid_o_cast_nw & ready_i_cast_nw),
    .write_i                 (valid_o_nw & (~ofifo_full)),
    .full_o                  (ofifo_full),
    .empty_o                 (),
    .data_i                  (data_o_nw),
    .data_o                  (ofifo_dout),
    .cnt                     (ofifo_cnt)
);

cast_converter #(
    .isCaster                 (isCaster),
    .stream_id                (stream_id)
)converter(
    .clk                      (clk),
    .rstn                     (rstn),
    .valid_i_pe               (valid_i_cast_pe),
    .data_i_pe                (data_i_cast_pe),
    .ready_o_pe               (ready_o_cast_pe),
    .valid_o_pe               (valid_o_cast_pe),
    .data_o_pe                (data_o_cast_pe),
    .ready_i_pe               (ready_i_cast_pe),
    .valid_i_nw               (~fifo_empty),
    .data_i_nw                (fifo_dout),
    .ready_o_nw               (ready_o_nw),
    .valid_o_nw               (valid_o_nw),
    .data_o_nw                (data_o_nw),
    .ready_i_nw               (~ofifo_full)
);

assign ready_o_cast_nw = ~fifo_full;

reg state;
always@(posedge clk or negedge rstn) begin
    if(~rstn) state <= 1'b0;
    else begin
        if(~state & (data_o_cast_nw[`DW-1:`DW-2] == `HEAD) & (ofifo_cnt >= `PKT_LEN))
            state <= 1'b1;
        else if(state & (data_o_cast_nw[`DW-1:`DW-2] == `TAIL) & valid_o_cast_nw & ready_i_cast_nw)
            state <= 1'b0;
    end
end

assign valid_o_cast_nw = state;
endmodule