//Not a behavior PE model, but a "virtual" PE model
//This PE model only simulates the data dependencies between different network interfaces, but does not simulate the computational behavior of the PE
//This PE model can only be used to verify where there exist deadlocks in the whole network
`include "params.svh"
`include "network_config.svh"

module virtual_pe #(
    parameter isCaster = 0 //indicate whether the current node is a caster
)(
    input       wire                            clk,
    input       wire                            rstn, 

    // cast port
    input       wire        [`DW-1:0]           cast_data_i,
    input       wire                            cast_valid_i,
    output      wire                            cast_ready_o,

    output      wire        [`DW-1:0]           cast_data_o,
    output      wire                            cast_valid_o,
    input       wire                            cast_ready_i,

    // merge port
    input       wire        [`DW-1:0]           merge_data_i,
    input       wire                            merge_valid_i,
    output      wire                            merge_ready_o,

    output      wire        [`DW-1:0]           merge_data_o,
    output      wire                            merge_valid_o,
    input       wire                            merge_ready_i
);

wire valid, ready;
wire [`DW-3:0] sum;

assign valid = cast_valid_i & merge_valid_i;
assign cast_valid_o = isCaster ? valid : 1'b0;
assign cast_data_o = {`BODY,sum}; //only add up the no-flit-type field of the data
assign sum = cast_data_i[`DW-3:0] + merge_data_i[`DW-3:0];
assign ready = valid & cast_ready_i;

assign cast_ready_o = isCaster ? ready : merge_ready_i;

assign merge_ready_o = isCaster ? ready : 1'b0;

assign merge_valid_o = isCaster ? 1'b0 : cast_valid_i;
assign merge_data_o = cast_data_i;

endmodule