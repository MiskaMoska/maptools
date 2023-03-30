`include "params.svh"

module gather_input_controller #(
    parameter   x_pos = 0,
    parameter   y_pos = 0,
    parameter   isFC = 0, //is the FC start port or not
    parameter   FCpl = 16 //FC packet length
)(
    input       wire                            clk,
    input       wire                            rstn,   
    input       wire                            fifo_empty, //from input buffer
    input       wire        [`CN-1:0]           candidateOutVC, //from route_calculator
    output      wire        [`CN-1:0]           reqVC, //to vc_allocator, sigle-bit asserted
    input       wire        [`CN-1:0]           selOutVC, //from vc_allocator, single-bit asserted
    input       wire                            VCgranted, //from vc_allocator
    output      wire        [`CN-1:0]           selXBVC, //to crossbar
    input       wire        [1:0]               flit_type,
    input       wire                            flit_fire,
    input       wire        [31:0]              credit_cnt //from credit counter
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

assign reqVC = (flit_type == `HEAD) & (~outVCLock) & (~fifo_empty) & 
                (isFC ? (credit_cnt >= FCpl-2) : 1'b1) ? candidateOutVC : 0;

// output credit log
bit lock = 0;
integer crd_file;
string crd_file_path = {`ROOT_DIR, "/network/log/gather_crd_", $sformatf("x%0d_y%0d.log", x_pos, y_pos)};
initial begin
    if(isFC) begin
        crd_file = $fopen(crd_file_path);
        wait(rstn);
        forever begin
            @(posedge clk)
            if(credit_cnt >= FCpl - 2)
                lock = 0;
            else if(
                (lock == 0) && 
                (flit_type == `HEAD) && 
                (~outVCLock) && 
                (~fifo_empty) && 
                (credit_cnt < FCpl-2)
            ) begin // credit running out
                $fwrite(crd_file, "time %0t\tcredit running out: %0d/%0d\n", $time, credit_cnt, `GATHER_CREDIT_ALLOC);
                lock = 1;
            end
        end
    end
end
endmodule