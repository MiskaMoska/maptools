`include "params.svh"

module gather_credit_counter #(
    parameter   isFC = 0, //is the FC start port or not
    parameter   [`NOC_WIDTH*`NOC_HEIGHT-1:0] FCdn = {(`NOC_WIDTH*`NOC_HEIGHT){1'b0}}, //FC destination nodes
    parameter   int FCpl = 16 //FC packet length
)( 
    input       wire                            clk,
    input       wire                            rstn, 

    input       wire                            fire, //input port fire
    input       wire        [1:0]               flit_type, //input port flit type

    input       wire        [31:0]              credit_upd[`NOC_WIDTH][`NOC_HEIGHT],
    output      wire        [31:0]              credit_cnt
);

reg [31:0] cnt;
assign credit_cnt = cnt;
bit breakout;

function void update_credit();
    breakout = 0;
    for(int x=0; x<`NOC_WIDTH; x++) begin
        if(breakout) break;
        for(int y=0; y<`NOC_HEIGHT; y++) begin
            if(FCdn[y*`NOC_WIDTH+x]) begin
                if(credit_upd[x][y] > 0) begin
                    if(FCdn[y*`NOC_WIDTH+x]) begin
                        cnt = cnt + credit_upd[x][y];
                    end
                end
                breakout = 1;
                break;
            end
        end
    end
    if((flit_type == `HEAD) & fire)
        cnt = cnt - FCpl + 2;
endfunction

always@(posedge clk or negedge rstn) begin
    if(~rstn) cnt <= `GATHER_CREDIT_ALLOC;
    else if(~isFC) cnt = ~32'b0; //indicate this is not a FC start node
    else begin
        update_credit();
    end
end

endmodule
