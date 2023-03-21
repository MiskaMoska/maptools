/*
    RTL synchronous FIFO with infinity volume
*/
module fifo_inf #(
    parameter   width =                 32
)(
    input   wire                        clk_i,
    input   wire                        rst_i,

    input   wire                        read_i, 
    input   wire                        write_i,
    output  reg                         empty_o,

    input   wire    [width-1 : 0]       data_i,
    output  wire    [width-1 : 0]       data_o
);

reg [width-1 : 0] buf[$];

always_ff @(posedge clk_i or negedge rst_i) begin
    if(rst_i)
        buf = {};
    else begin
        if(write_i)
            buf.push_back(data_i);
        if(read_i & (~empty_o))
            data_o <= buf.pop_front();
    end
end

always_comb begin
    empty_o = rst_i ? 1'b1 : (buf.size() == 0);
end

endmodule