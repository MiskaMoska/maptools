`include "params.svh"

module gather_output_stage (
    input       wire                            clk,
    input       wire                            rstn, 

    input       wire        [1:0]               flit_type,
    input       wire                            flit_fire,
    input       wire                            outVCAvailableReset,
    output      reg                             outVCAvailable
);

always@(posedge clk or negedge rstn) begin
    if(~rstn) outVCAvailable <= 1'b1;
    else begin
        if((flit_type == `TAIL) & flit_fire) outVCAvailable <= 1'b1;
        else if(outVCAvailableReset) outVCAvailable <= 1'b0;
    end
end

endmodule