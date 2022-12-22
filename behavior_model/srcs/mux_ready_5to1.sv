`include "params.svh"

module mux_ready_5to1(
    input       wire            [4:0]           mux_sel,
    input       wire            [4:0]           ready_in,
    output      wire                            ready_out   
);

assign ready_out = (mux_sel == 0) ? 1'b0 : (~mux_sel[0] | ready_in[0]) & (~mux_sel[1] | ready_in[1]) & (~mux_sel[2] | ready_in[2]) & (~mux_sel[3] | ready_in[3]) & (~mux_sel[4] | ready_in[4]);

endmodule