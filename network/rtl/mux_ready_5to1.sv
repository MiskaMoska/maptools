`include "params.svh"

module mux_ready_5to1 #(
    parameter   multi_ready = 0
)(
    input       wire            [4:0]           mux_sel,
    input       wire            [4:0]           ready_in,
    output      reg                             ready_out   
);

always_comb begin
    if(multi_ready == 1)
        ready_out = (mux_sel == 0) ? 1'b0 : 
                    (~mux_sel[0] | ready_in[0]) & 
                    (~mux_sel[1] | ready_in[1]) & 
                    (~mux_sel[2] | ready_in[2]) & 
                    (~mux_sel[3] | ready_in[3]) & 
                    (~mux_sel[4] | ready_in[4]);
    else
        case(mux_sel)
            5'b00001:  ready_out = ready_in[0];
            5'b00010:  ready_out = ready_in[1];
            5'b00100:  ready_out = ready_in[2];
            5'b01000:  ready_out = ready_in[3];
            5'b10000:  ready_out = ready_in[4];
            default:   ready_out = 1'b0;
        endcase
end

endmodule