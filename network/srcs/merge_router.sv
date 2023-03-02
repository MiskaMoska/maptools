/*
    Merge router without register
*/

`include "params.svh"

module merge_router #(
    parameter  [4:0]  input_mask = 0, //[0]-local [1]-west [2]-east [3]-north [4]-south, 1 means assert
    parameter  [4:0]  output_sel = 0  //[0]-local [1]-west [2]-east [3]-north [4]-south, one-hot code
)(
    input       wire                            clk,
    input       wire                            rstn,

    input       wire        [`DW-1:0]           data_i[5],
    input       wire                            valid_i[5],
    output      reg                             ready_o[5],

    output      reg         [`DW-1:0]           data_o[5],
    output      reg                             valid_o[5],
    input       wire                            ready_i[5]
);

/** float_point adder begin**/
// shortreal data_i_sr[5];
// shortreal sum;

// always@(data_i) begin
//     for(int i=0; i<5; i++) begin
//         if(input_mask[i]) data_i_sr[i] = $bitstoshortreal(data_i[i]);
//         else data_i_sr[i] = 0;
//     end
// end

// always@(data_i_sr) begin
//     sum = 0;
//     for(int i=0; i<5; i++) begin
//         if(input_mask[i]) sum = sum + data_i_sr[i];
//     end
// end

// always@(sum) begin
//     for(int i=0; i<5; i++) begin
//         if(output_sel[i]) data_o[i] = $shortrealtobits(sum);
//         else data_o[i] = 0;
//     end
// end
/** float_point adder end**/

/** fixed_point adder begin**/
wire sum_flit;
reg [`DW-3:0] sum;
assign sum_flit = {`BODY,sum};
always@(data_i) begin
    sum = 0;
    for(int i=0; i<5; i++) begin
        if(input_mask[i]) sum = sum + data_i[i][`DW-3:0];
    end
end

always@(sum_flit) begin
    for(int i=0; i<5; i++) begin
        if(output_sel[i]) data_o[i] = sum_flit;
        else data_o[i] = 0;
    end
end
/** fixed_point adder end**/

wire valid;
assign valid = (~input_mask[0] | valid_i[0]) & (~input_mask[1] | valid_i[1]) & (~input_mask[2] | valid_i[2]) & (~input_mask[3] | valid_i[3]) & (~input_mask[4] | valid_i[4]);

always@(valid) begin
    for(int i=0; i<5; i++) begin
        if(output_sel[i]) valid_o[i] = valid;
        else valid_o[i] = 1'b0;
    end
end

wire ready;
assign ready = output_sel[0] & ready_i[0] | output_sel[1] & ready_i[1] | output_sel[2] & ready_i[2] | output_sel[3] & ready_i[3] | output_sel[4] & ready_i[4];

always@(valid or ready) begin
    for(int i=0; i<5; i++) begin
        if(input_mask[i])
            ready_o[i] = valid & ready;
        else
            ready_o[i] = 1'b0;
    end
end

endmodule