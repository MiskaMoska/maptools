`include "params.svh"

module network_interface #(
    parameter                                   cast_out = 0,
    parameter                                   gather_out = 0,
    parameter               [9:0]               cast_sid = 0,
    parameter               [9:0]               gather_sid = 0
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

    //gather network end
    input       wire                            valid_i_gather_nw,
    input       wire        [`DW-1:0]           data_i_gather_nw,
    output      wire                            ready_o_gather_nw,

    output      wire                            valid_o_gather_nw,
    output      wire        [`DW-1:0]           data_o_gather_nw,
    input       wire                            ready_i_gather_nw,

    //cast pe end
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

    //gather pe end
    output      wire                            valid_o_gather_pe,
    output      wire        [`DW-1:0]           data_o_gather_pe,
    input       wire                            ready_i_gather_pe,

    //combined pe end
    input       wire                            valid_i_cast_gather_pe,
    input       wire        [`DW-1:0]           data_i_cast_gather_pe,
    output      wire                            ready_o_cast_gather_pe,

    //credit update signal
    output      wire                            credit_upd
);

`ifdef TEST
localparam fifo_depth_log = 30;
`else
localparam fifo_depth_log = 2
`endif


wire valid_i_cast_pe, ready_o_cast_pe, valid_i_gather_pe, ready_o_gather_pe;
wire [`DW-1:0] data_i_cast_pe, data_i_gather_pe;

/*****************************************************
                Merge interface
*****************************************************/

assign valid_o_merge_pe = valid_i_merge_nw;
assign data_o_merge_pe = data_i_merge_nw;
assign ready_o_merge_pe = ready_i_merge_nw;
assign valid_o_merge_nw = valid_i_merge_pe;
assign data_o_merge_nw = data_i_merge_pe;
assign ready_o_merge_nw = ready_i_merge_pe;


/*****************************************************
                Cast interface
*****************************************************/

wire cast_valid_o_nw, cast_ready_o_nw;
wire [`DW-1:0] cast_data_o_nw;
wire cast_rbuf_empty, cast_rbuf_full, cast_rbuf_read;
wire [`DW-1:0] cast_rbuf_dout;
wire [7:0] cast_sbuf_cnt;
wire cast_sbuf_full;
wire [`DW-1:0] cast_sbuf_dout;

assign data_o_cast_nw = cast_sbuf_dout;
assign cast_rbuf_read = ~cast_rbuf_empty & cast_ready_o_nw;
assign credit_upd = cast_rbuf_read;
assign ready_o_cast_nw = 1'b1;

// // cast network end receive buffer
// nfifo_inf #(
//     .width                   (`DW)
// )cast_receive_fifo(
//     .clk_i                   (clk),
//     .rst_i                   (~rstn),
//     .read_i                  (cast_rbuf_read),
//     .write_i                 (valid_i_cast_nw),
//     .empty_o                 (cast_rbuf_empty),
//     .data_i                  (data_i_cast_nw),
//     .data_o                  (cast_rbuf_dout)
// );

// cast network end receive buffer
nfifo #(
    .width                   (`DW),
    .depth                   (2**fifo_depth_log),
    .depth_LOG               (fifo_depth_log),
    .FWFT                    (1)
)cast_receive_fifo(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (cast_rbuf_read),
    .write_i                 (valid_i_cast_nw),
    .empty_o                 (cast_rbuf_empty),
    .full_o                  (),
    .data_i                  (data_i_cast_nw),
    .data_o                  (cast_rbuf_dout)
);

// cast network end send buffer
nfifo_cnt #(
    .width                   (`DW),
    .depth                   (`SEND_BUFFER_DEPTH),
    .depth_LOG               (7),
    .FWFT                    (1)
)cast_send_fifo(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (valid_o_cast_nw & ready_i_cast_nw),
    .write_i                 (cast_valid_o_nw & (~cast_sbuf_full)),
    .full_o                  (cast_sbuf_full),
    .empty_o                 (),
    .data_i                  (cast_data_o_nw),
    .data_o                  (cast_sbuf_dout),
    .cnt                     (cast_sbuf_cnt)
);

converter #(
    .out                     (cast_out),
    .sid                     (cast_sid)
)cast_converter(
    .clk                     (clk),
    .rstn                    (rstn),
    .valid_i_pe              (valid_i_cast_pe),
    .data_i_pe               (data_i_cast_pe),
    .ready_o_pe              (ready_o_cast_pe),
    .valid_o_pe              (valid_o_cast_pe),
    .data_o_pe               (data_o_cast_pe),
    .ready_i_pe              (ready_i_cast_pe),
    .valid_i_nw              (~cast_rbuf_empty),
    .data_i_nw               (cast_rbuf_dout),
    .ready_o_nw              (cast_ready_o_nw),
    .valid_o_nw              (cast_valid_o_nw),
    .data_o_nw               (cast_data_o_nw),
    .ready_i_nw              (~cast_sbuf_full)
);

reg cast_state;
always@(posedge clk or negedge rstn) begin
    if(~rstn) cast_state <= 1'b0;
    else begin
        if(~cast_state & (data_o_cast_nw[`DW-1:`DW-2] == `HEAD) & (cast_sbuf_cnt >= `PKT_LEN))
            cast_state <= 1'b1;
        else if(cast_state & (data_o_cast_nw[`DW-1:`DW-2] == `TAIL) & valid_o_cast_nw & ready_i_cast_nw)
            cast_state <= 1'b0;
    end
end 

assign valid_o_cast_nw = cast_state;

/*****************************************************
                Gather interface
*****************************************************/

wire gather_valid_o_nw, gather_ready_o_nw;
wire [`DW-1:0] gather_data_o_nw;
wire gather_rbuf_empty, gather_rbuf_full, gather_rbuf_read;
wire [`DW-1:0] gather_rbuf_dout;
wire [7:0] gather_sbuf_cnt;
wire gather_sbuf_full;
wire [`DW-1:0] gather_sbuf_dout;

assign data_o_gather_nw = gather_sbuf_dout;
assign gather_rbuf_read = ~gather_rbuf_empty & gather_ready_o_nw;
assign ready_o_gather_nw = 1'b1;

// // gather network end receive buffer
// nfifo_inf #(
//     .width                   (`DW)
// )gather_receive_fifo(
//     .clk_i                   (clk),
//     .rst_i                   (~rstn),
//     .read_i                  (gather_rbuf_read),
//     .write_i                 (valid_i_gather_nw),
//     .empty_o                 (gather_rbuf_empty),
//     .data_i                  (data_i_gather_nw),
//     .data_o                  (gather_rbuf_dout)
// );

// gather network end receive buffer
nfifo #(
    .width                   (`DW),
    .depth                   (2**fifo_depth_log),
    .depth_LOG               (fifo_depth_log),
    .FWFT                    (1)
)gather_receive_fifo(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (gather_rbuf_read),
    .write_i                 (valid_i_gather_nw),
    .empty_o                 (gather_rbuf_empty),
    .full_o                  (),
    .data_i                  (data_i_gather_nw),
    .data_o                  (gather_rbuf_dout)
);

// gather network end send buffer
nfifo_cnt #(
    .width                   (`DW),
    .depth                   (`SEND_BUFFER_DEPTH),
    .depth_LOG               (7),
    .FWFT                    (1)
)gather_send_fifo(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (valid_o_gather_nw & ready_i_gather_nw),
    .write_i                 (gather_valid_o_nw & (~gather_sbuf_full)),
    .full_o                  (gather_sbuf_full),
    .empty_o                 (),
    .data_i                  (gather_data_o_nw),
    .data_o                  (gather_sbuf_dout),
    .cnt                     (gather_sbuf_cnt)
);

converter #(
    .out                     (gather_out),
    .sid                     (gather_sid)
)gather_converter(
    .clk                     (clk),
    .rstn                    (rstn),
    .valid_i_pe              (valid_i_gather_pe),
    .data_i_pe               (data_i_gather_pe),
    .ready_o_pe              (ready_o_gather_pe),
    .valid_o_pe              (valid_o_gather_pe),
    .data_o_pe               (data_o_gather_pe),
    .ready_i_pe              (ready_i_gather_pe),
    .valid_i_nw              (~gather_rbuf_empty),
    .data_i_nw               (gather_rbuf_dout),
    .ready_o_nw              (gather_ready_o_nw),
    .valid_o_nw              (gather_valid_o_nw),
    .data_o_nw               (gather_data_o_nw),
    .ready_i_nw              (~gather_sbuf_full)
);

reg gather_state;
always@(posedge clk or negedge rstn) begin
    if(~rstn) gather_state <= 1'b0;
    else begin
        if(~gather_state & (data_o_gather_nw[`DW-1:`DW-2] == `HEAD) & (gather_sbuf_cnt >= `PKT_LEN))
            gather_state <= 1'b1;
        else if(gather_state & (data_o_gather_nw[`DW-1:`DW-2] == `TAIL) & valid_o_gather_nw & ready_i_gather_nw)
            gather_state <= 1'b0;
    end
end

assign valid_o_gather_nw = gather_state;

// asynchronous sending for cast and gather
wire fifo_read, fifo_write;
wire [`DW-1:0] fifo_dout;
reg resend;
reg [`PKT_LEN_LOG : 0] slice_cnt;

always@(posedge clk or negedge rstn) begin
    if(~rstn) begin
        slice_cnt <= 0;
        resend <= 1'b0;
    end
    else begin
        if((cast_out == 1) & (gather_out == 1)) begin
            if((~resend) & valid_i_cast_pe & ready_o_cast_pe) begin
                if(slice_cnt == `PKT_LEN-3) begin
                    slice_cnt <= 0;
                    resend <= 1'b1;
                end
                else slice_cnt <= slice_cnt + 1;
            end
            else if(resend & valid_i_gather_pe & ready_o_gather_pe) begin
                if(slice_cnt == `PKT_LEN-3) begin
                    slice_cnt <= 0;
                    resend <= 1'b0;
                end
                else slice_cnt <= slice_cnt + 1;
            end
        end
    end
end

assign ready_o_cast_gather_pe = ((cast_out == 1) & (gather_out == 1)) ? (~resend) & ready_o_cast_pe : (
                                (cast_out == 1)                       ? ready_o_cast_pe             : ready_o_gather_pe);

assign valid_i_cast_pe = ((cast_out == 1) & (gather_out == 1)) ? (~resend) & valid_i_cast_gather_pe : ( // read out data_sum
                            (cast_out == 1)                    ? valid_i_cast_gather_pe : 1'b0);

assign valid_i_gather_pe = ((cast_out == 1) & (gather_out == 1)) ? resend : ( // read out fifo
                            (cast_out == 1)                      ? 1'b0 : valid_i_cast_gather_pe);

assign data_i_cast_pe = data_i_cast_gather_pe;
assign data_i_gather_pe = ((cast_out == 1) & (gather_out == 1)) ? fifo_dout : data_i_cast_gather_pe;

nfifo #(
    .width                   (`DW),
    .depth                   (`PKT_LEN-2),
    .depth_LOG               (`PKT_LEN_LOG + 1),
    .FWFT                    (1)
)slice_fifo(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (fifo_read),
    .write_i                 (fifo_write),
    .empty_o                 (),
    .full_o                  (),
    .data_i                  (data_i_cast_gather_pe),
    .data_o                  (fifo_dout)
);

assign fifo_write = ((cast_out == 1) & (gather_out == 1)) & (~resend) & valid_i_cast_pe & ready_o_cast_pe;
assign fifo_read = ((cast_out == 1) & (gather_out == 1)) & resend & valid_i_gather_pe & ready_o_gather_pe;
endmodule