/*
    Merge router with input buffer
*/

`include "params.svh"

module merge_router #(
    parameter  [0:4]  input_mask = 0, //[0]-local [1]-west [2]-east [3]-north [4]-south, 1 means assert
    parameter  [0:4]  output_sel = 0  //[0]-local [1]-west [2]-east [3]-north [4]-south, one-hot code
)(
    input       wire                            clk,
    input       wire                            rstn,

    input       wire        [`DW-1:0]           data_i[5],
    input       wire                            valid_i[5],
    output      wire                            ready_o[5],

    output      reg         [`DW-1:0]           data_o[5],
    output      reg                             valid_o[5],
    input       wire                            ready_i[5]
);

wire valid, ready;

/** fifos **/
wire [`DW-1:0] data_i_fifo[5];
wire valid_i_fifo[5];
reg ready_o_fifo[5];
wire fifo_read[5],fifo_empty[5],fifo_full[5];

assign fifo_read[0] = ~fifo_empty[0] & ready_o_fifo[0];
assign fifo_read[1] = ~fifo_empty[1] & ready_o_fifo[1];
assign fifo_read[2] = ~fifo_empty[2] & ready_o_fifo[2];
assign fifo_read[3] = ~fifo_empty[3] & ready_o_fifo[3];
assign fifo_read[4] = ~fifo_empty[4] & ready_o_fifo[4];

assign ready_o[0] = ~fifo_full[0];
assign ready_o[1] = ~fifo_full[1];
assign ready_o[2] = ~fifo_full[2];
assign ready_o[3] = ~fifo_full[3];
assign ready_o[4] = ~fifo_full[4];

assign valid_i_fifo[0] = ~fifo_empty[0];
assign valid_i_fifo[1] = ~fifo_empty[1];
assign valid_i_fifo[2] = ~fifo_empty[2];
assign valid_i_fifo[3] = ~fifo_empty[3];
assign valid_i_fifo[4] = ~fifo_empty[4];

localparam fifo_depth_log = `MERGE_ROUTER_BUFFER_DEPTH_LOG;
localparam fifo_depth = 2**`MERGE_ROUTER_BUFFER_DEPTH_LOG;

fifo #(
    .width                   (`DW),
    .depth                   (fifo_depth),
    .depth_LOG               (fifo_depth_log),
    .FWFT                    (1)
)fifo0(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (fifo_read[0]),
    .write_i                 (valid_i[0] & ready_o[0]),
    .full_o                  (fifo_full[0]),
    .empty_o                 (fifo_empty[0]),
    .data_i                  (data_i[0]),
    .data_o                  (data_i_fifo[0])
);

fifo #(
    .width                   (`DW),
    .depth                   (fifo_depth),
    .depth_LOG               (fifo_depth_log),
    .FWFT                    (1)
)fifo1(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (fifo_read[1]),
    .write_i                 (valid_i[1] & ready_o[1]),
    .full_o                  (fifo_full[1]),
    .empty_o                 (fifo_empty[1]),
    .data_i                  (data_i[1]),
    .data_o                  (data_i_fifo[1])
);

fifo #(
    .width                   (`DW),
    .depth                   (fifo_depth),
    .depth_LOG               (fifo_depth_log),
    .FWFT                    (1)
)fifo2(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (fifo_read[2]),
    .write_i                 (valid_i[2] & ready_o[2]),
    .full_o                  (fifo_full[2]),
    .empty_o                 (fifo_empty[2]),
    .data_i                  (data_i[2]),
    .data_o                  (data_i_fifo[2])
);

fifo #(
    .width                   (`DW),
    .depth                   (fifo_depth),
    .depth_LOG               (fifo_depth_log),
    .FWFT                    (1)
)fifo3(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (fifo_read[3]),
    .write_i                 (valid_i[3] & ready_o[3]),
    .full_o                  (fifo_full[3]),
    .empty_o                 (fifo_empty[3]),
    .data_i                  (data_i[3]),
    .data_o                  (data_i_fifo[3])
);

fifo #(
    .width                   (`DW),
    .depth                   (fifo_depth),
    .depth_LOG               (fifo_depth_log),
    .FWFT                    (1)
)fifo4(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (fifo_read[4]),
    .write_i                 (valid_i[4] & ready_o[4]),
    .full_o                  (fifo_full[4]),
    .empty_o                 (fifo_empty[4]),
    .data_i                  (data_i[4]),
    .data_o                  (data_i_fifo[4])
);

/** float_point adder begin**/
shortreal data_i_sr[5];
shortreal sum;

always@(*) begin
    for(int i=0; i<5; i++) begin
        if(input_mask[i]) data_i_sr[i] = $bitstoshortreal(data_i_fifo[i][`DW-3:0]);
        else data_i_sr[i] = 0;
    end

    sum = 0;
    for(int i=0; i<5; i++) begin
        if(input_mask[i]) sum = sum + data_i_sr[i];
    end    

    for(int i=0; i<5; i++) begin
        if(output_sel[i]) begin 
            data_o[i] = {`BODY, $shortrealtobits(sum)};
            valid_o[i] = valid;
        end else begin
            data_o[i] = {`BODY,{(`DW-3){1'b0}}};
            valid_o[i] = 1'b0;
        end
    end
end

always@(*) begin
    for(int i=0; i<5; i++) begin
        if(input_mask[i])
            ready_o_fifo[i] = valid & ready;
        else
            ready_o_fifo[i] = 1'b0;
    end
end

assign valid = (~input_mask[0] | valid_i_fifo[0]) & (~input_mask[1] | valid_i_fifo[1]) & (~input_mask[2] | valid_i_fifo[2]) & (~input_mask[3] | valid_i_fifo[3]) & (~input_mask[4] | valid_i_fifo[4]);
assign ready = output_sel[0] & ready_i[0] | output_sel[1] & ready_i[1] | output_sel[2] & ready_i[2] | output_sel[3] & ready_i[3] | output_sel[4] & ready_i[4];

/** float_point adder end**/

endmodule

