`include "params.svh"

module cast_input_controller #(
    parameter   isUBM = 0, //whether adopt unicast-based-multicast
    parameter   isFC = 0, //is the FC start port or not
    parameter   FCpl = 16 //FC packet length
)(
    input       wire                            clk,
    input       wire                            rstn,   
    input       wire                            fifo_empty, //from input buffer
    input       wire        [`CN-1:0]           candidateOutVC, //from route_calculator
    output      wire        [`CN-1:0]           reqVC, //to vc_allocator, multi-bit possibly asserted
    input       wire        [`CN-1:0]           selOutVC, //from vc_allocator, multi-bit possibly asserted
    input       wire                            VCgranted, //from vc_allocator
    output      wire        [`CN-1:0]           selXBVC, //to crossbar
    input       wire        [1:0]               flit_type,
    input       wire                            flit_fire,
    output      reg                             pop, // to FIFO
    input       wire        [15:0]              credit_cnt //from credit counter
);

reg in_flight; // whether a unicast-based-multicast is being processed
reg [`CN-1:0] candidateOutVC_reg;
wire [`CN-1:0] arb_req,arb_grt;

always@(posedge clk or negedge rstn) begin
    if(~rstn) in_flight <= 1'b0;
    else begin
        if(~in_flight & (isUBM == 1) & ~isOneHot(candidateOutVC) & (flit_type == `HEAD) & flit_fire) 
            in_flight <= 1'b1;
        else if(in_flight & pop & (flit_type == `TAIL) & flit_fire) 
            in_flight <= 1'b0;
    end
end

assign arb_req = (isUBM == 1) & (flit_type == `HEAD) ? (in_flight ? candidateOutVC_reg : candidateOutVC) : 0;

always@(posedge clk or negedge rstn) begin
    if(~rstn) candidateOutVC <= 0;
    else begin
        if((isUBM == 1) & (flit_type == `HEAD) & flit_fire)
            candidateOutVC_reg <= candidateOutVC & (~arb_grt);
    end
end

always@(posedge clk or negedge rstn) begin
    if(~rstn) pop <= 1'b0;
    else begin
        if(~pop & isOneHot(candidateOutVC_reg) & (flit_type == `TAIL) & flit_fire)
            pop <= 1'b1;
        else if(pop & (flit_type == `TAIL) & flit_fire)
            pop <= 1'b0;
    end
end

mtx_arbiter #(
    .LEN                   (`CN)
)arbiterVC0(
    .clk                   (clk),
    .rstn                  (rstn),
    .request               (arb_req),
    .grant                 (arb_grt),
    .update                (1'b0)
);

reg [`CN-1:0]   outVC;
reg             outVCLock;

always@(posedge clk or negedge rstn) begin
    if(~rstn) begin
        outVCLock <= 1'b0;
        outVC <= 0;
    end else if(flit_fire & (flit_type == `TAIL)) begin
        outVCLock <= 1'b0;
        outVC <= 0;
    end else if(VCgranted) begin
        outVCLock <= 1'b1;
        outVC <= selOutVC;
    end
end

assign selXBVC = outVCLock ? outVC : 
                    VCgranted ? selOutVC : 5'b0;

assign reqVC = (flit_type == `HEAD) & (~outVCLock) & (~fifo_empty) & (isFC ? (credit_cnt > FCpl) : 1'b1) ? ((isUBM == 1) ? arb_grt : candidateOutVC) : 0;
endmodule