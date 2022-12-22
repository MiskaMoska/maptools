`include "params.svh"

module cast_credit_counter #(
    parameter   isFC = 0, //is the FC start port or not
    parameter   [`NOC_WIDTH*`NOC_HEIGHT-1:0] FCdn = {(`NOC_WIDTH*`NOC_HEIGHT){1'b0}}, //FC destination nodes
    parameter   int FCpl = 16 //FC packet length
)( 
    input       wire                            clk,
    input       wire                            rstn, 

    input       wire                            fire, //input port fire
    input       wire        [1:0]               flit_type, //input port flit type

    input       wire                            credit_upd[`NOC_WIDTH][`NOC_HEIGHT],
    output      wire        [15:0]              credit_cnt 
);

wire [4:0] pl;
assign pl = FCpl;

wire [`NOC_WIDTH*`NOC_HEIGHT-1:0] dn;
assign dn = FCdn;

reg [15:0] cnt;
assign credit_cnt = cnt;
bit flag;

int credit_inc[0:`NOC_WIDTH*`NOC_HEIGHT-1];
initial begin
    for(int i=0; i<`NOC_WIDTH*`NOC_HEIGHT; i++) begin
        credit_inc[i] = 0;
    end
    forever begin
        @(posedge clk);
        if(rstn && isFC) begin

            for(int x=0; x<`NOC_WIDTH; x++) begin
                for(int y=0; y<`NOC_HEIGHT; y++) begin
                    if(credit_upd[x][y]) begin
                        if(FCdn[y*`NOC_WIDTH+x]) begin
                            credit_inc[y*`NOC_WIDTH+x] = credit_inc[y*`NOC_WIDTH+x] + 1;
                        end
                    end
                end
            end

            flag = 0;
            for(int i=0; i<`NOC_WIDTH*`NOC_HEIGHT; i++) begin
                if(FCdn[i]) begin
                    if(credit_inc[i]==0) begin
                        flag = 1;
                        break;
                    end
                end
            end

            if(flag==0) begin
                cnt = cnt + 1;
                for(int i=0; i<`NOC_WIDTH*`NOC_HEIGHT; i++) begin
                    if(FCdn[i]) begin
                        credit_inc[i] = credit_inc[i] - 1;
                    end
                end
            end
        end
    end
end

always@(posedge clk or negedge rstn) begin
    if(~rstn) cnt <= `BUFFER_ALLOC;
    else if(~isFC) cnt = 65535; //indicate this is not a FC start node
    else begin
        if((flit_type == `HEAD) & fire)
            cnt = cnt - FCpl;
    end
end

endmodule
