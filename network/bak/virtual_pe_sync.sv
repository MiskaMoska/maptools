// for synchronous cast gather sending
`include "params.svh"
`include "network_config.svh"

module virtual_pe #(
    parameter                                   cast_out = 0,
    parameter                                   merge_in = 0,
    parameter                                   merge_out = 0,
    parameter                                   gather_in = 0,
    parameter                                   gather_out = 0,
    parameter                                   x = 0,
    parameter                                   y = 0
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
    input       wire                            merge_ready_i,

    // gather port 
    input       wire        [`DW-1:0]           gather_data_i,
    input       wire                            gather_valid_i,
    output      wire                            gather_ready_o,

    output      wire        [`DW-1:0]           gather_data_o,
    output      wire                            gather_valid_o,
    input       wire                            gather_ready_i
);

// All xbars have cast_in
wire valid_all; // cast_in, [merge_in], [gather_in] all valid (only for merge_out == 0)
wire ready_all; // [cast_out], [gather_out] all valid (only for merge_out == 0)
wire [`DW-1 : 0] data_sum;

int rcnt = 0;
always@(posedge clk) begin
    if(cast_valid_i & cast_ready_o) rcnt <= rcnt + 1;
    if(rcnt == 0 & cast_valid_i & cast_ready_o)
        $display("node (%d, %d) starting computing ...", x, y);
end

int scnt = 0;
always@(posedge clk) begin
    if(merge_out == 1) begin
        if(merge_valid_o & merge_ready_i) begin
            scnt <= scnt + 1;
            if(scnt == 9999) 
                $display("node (%d, %d) finished computing ...", x, y);
        end
    end else begin
        if(valid_all & ready_all) begin
            scnt <= scnt + 1;
            if(scnt == 9999) 
                $display("node (%d, %d) finished computing ...", x, y);
        end
    end
end

assign valid_all = cast_valid_i & 
                    (merge_in == 1 ? merge_valid_i : 1'b1) &
                    (gather_in == 1 ? gather_valid_i : 1'b1);

assign ready_all = (cast_out == 1 ? cast_ready_i : 1'b1) & (gather_out == 1 ? gather_ready_i : 1'b1); // cast_out and gather_out at least one enabled
assign data_sum = cast_data_i; // no need to all, only simulate dependency
assign cast_valid_o = (merge_out == 0) & valid_all;
assign gather_valid_o = (merge_out == 0) & (gather_out == 1) & valid_all;
assign cast_ready_o = (merge_out == 0) ? valid_all & ready_all : merge_ready_i;
assign merge_ready_o = (merge_out == 0) ? (merge_in == 1) & valid_all & ready_all : 1'b0;
assign gather_ready_o = (merge_out == 0) ? (gather_in == 1) & valid_all & ready_all : 1'b0;
assign merge_valid_o = (merge_out == 1) & cast_valid_i;
assign merge_data_o = data_sum;
assign cast_data_o = data_sum;
assign gather_data_o = data_sum;
endmodule