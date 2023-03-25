/*
    RTL synchronous FIFO with infinity volume
*/
module nfifo_inf #(
    parameter   width =                 32
)(
    input   logic                       clk_i,
    input   logic                       rst_i,

    input   logic                       read_i, 
    input   logic                       write_i,
    output  reg                         empty_o,

    input   logic    [width-1 : 0]      data_i,
    output  logic    [width-1 : 0]      data_o,

    input   wire                        din,
    output  wire                        dout
);

typedef logic [width-1:0] data_t;
data_t fifo[$];

always @(posedge clk_i or posedge rst_i) begin
    if(rst_i)
        fifo = {};
    else begin
        if(write_i)
            fifo.push_back(data_i);
        if(read_i & (~empty_o))
            fifo.pop_front();
    end
end

always @(posedge clk_i) begin
    empty_o <= fifo.empty();
    data_o <= fifo[0];
end

assign #15 dout = din;

endmodule