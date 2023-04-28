`include "params.svh"

module mux_data_valid_5to1(
    input       wire            [4:0]           mux_sel,
    input       wire            [`DW-1:0]       data_in_vc0,
    input       wire            [`DW-1:0]       data_in_vc1,
    input       wire            [`DW-1:0]       data_in_vc2,
    input       wire            [`DW-1:0]       data_in_vc3,
    input       wire            [`DW-1:0]       data_in_vc4,
    input       wire            [4:0]           valid_in,
    output      reg             [`DW-1:0]       data_out,
    output      reg                             valid_out   
);

always@(*) begin
    case(mux_sel)
        5'b00001:    data_out = data_in_vc0;
        5'b00010:    data_out = data_in_vc1;
        5'b00100:    data_out = data_in_vc2;
        5'b01000:    data_out = data_in_vc3;
        5'b10000:    data_out = data_in_vc4;
        default:     data_out = 0;
    endcase
end

always@(*) begin
    case(mux_sel)
        5'b00001:    valid_out = valid_in[0];
        5'b00010:    valid_out = valid_in[1];
        5'b00100:    valid_out = valid_in[2];
        5'b01000:    valid_out = valid_in[3];
        5'b10000:    valid_out = valid_in[4];
        default:      valid_out = 0;
    endcase
end

endmodule