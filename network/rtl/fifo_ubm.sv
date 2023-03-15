/*
    RTL synchronous FIFO for Unitcast-Based-Multicast  
    Data width configurable
    FIFO depth configurable
    Can be configured as FWFT mode or standard mode
*/
module fifo_ubm #(
    parameter   width =                 32,
    parameter   depth =                 16,
    parameter   depth_LOG =             4,
    parameter   FWFT =                  1 //1:First Word Fall Through,0:Standard
)(
    input   wire                        clk_i,
    input   wire                        rst_i,

    input   wire                        read_i, 
    input   wire                        write_i,
    output  wire                        full_o, 
    output  wire                        empty_o,

    input   wire    [width-1 : 0]       data_i,
    output  wire    [width-1 : 0]       data_o,

    // when pop is high, a read operation pops out a data and increments rp, and rt_rp is set as rp
    // when pop is low, a read operation does not pop out data and does not affect rp, but only increments the rt_rp
    input   wire                        pop,

    // when read_reset is high, rt_rp is reset to rp at the next clock edge
    input   wire                        read_reset
);

reg [width-1 : 0] data_o_std;
reg [width-1 : 0] mem [depth-1 : 0];
reg [depth_LOG : 0] wp, rt_rp, rp;

always@(posedge clk_i or posedge rst_i) 
begin
    if(rst_i) 
    begin
        wp <= 0;
    end 
    else if(~full_o & write_i) 
    begin 
        wp <= (wp==2*depth-1) ? 'b0 : wp+1;
    end
end

always@(posedge clk_i) 
begin
    if(~full_o & write_i)
    begin
        mem[wp[depth_LOG-1:0]] <= data_i;
    end
end

always@(posedge clk_i or posedge rst_i) 
begin
    if(rst_i) 
    begin
        rt_rp <= 0;
    end 
    else if(read_reset) rt_rp <= rp;
    else if(~empty_o & read_i) 
    begin 
        if(pop) rt_rp <= (rp==2*depth-1) ? 'b0 : rp+1;
        else rt_rp <= (rt_rp==2*depth-1) ? 'b0 : rt_rp+1;
    end
end

always@(posedge clk_i or posedge rst_i) 
begin
    if(rst_i) 
    begin
        rp <= 0;
    end 
    else if(~empty_o & read_i & pop) 
    begin 
        rp <= (rp==2*depth-1) ? 'b0 : rp+1;
    end
end

always@(posedge clk_i or posedge rst_i)
begin
    if(rst_i) data_o_std <= 0;
    else
    begin
        if(~empty_o & read_i)
            data_o_std <= mem[rt_rp[depth_LOG-1:0]];
    end
end

assign full_o = (wp[depth_LOG-1:0]==rp[depth_LOG-1:0]) ? wp[depth_LOG] != rp[depth_LOG] : 1'b0;
assign empty_o = (wp[depth_LOG-1:0]==rt_rp[depth_LOG-1:0]) ? wp[depth_LOG] == rt_rp[depth_LOG] : 1'b0;

generate if(FWFT == 0) begin: FWFT_MODE
    assign data_o = data_o_std;
end else begin: STANDARD_MOD
    assign data_o = mem[rt_rp[depth_LOG-1:0]];
end endgenerate

endmodule