/*
    RTL synchronous FIFO with infinity volume
*/
module nfifo_inf #(
    parameter   width =                 32
)(
    input   wire                        clk_i,
    input   wire                        rst_i,

    input   wire                        read_i, 
    input   wire                        write_i,
    output  reg                         empty_o,

    input   wire    [width-1 : 0]       data_i,
    output  reg     [width-1 : 0]       data_o
);

reg [width-1 : 0] _buf_[$];

always_ff @(posedge clk_i or negedge rst_i) begin
    if(rst_i)
        _buf_ = {};
    else begin
        if(write_i)
            _buf_.push_back(data_i);
        if(read_i & (~empty_o))
            data_o <= _buf_.pop_front();
    end
end

always_comb begin
    empty_o = rst_i ? 1'b1 : (_buf_.size() == 0);
end

endmodule