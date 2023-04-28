`include "params.svh"

module cast_route_table #(
    parameter string rt_file = ""
)(
    input       wire                            clk,
    input       wire                            rstn,  

    input       wire        [9:0]               stream_id,
    output      reg         [`CN-1:0]           candidateOutVC //multi-bit possibly asserted
);

(* ramstyle = "AUTO" *) reg [10+`CN-1:0] tab [0:`ROUTE_TABLE_DEPTH-1];

initial begin 
    // $display("RT_FILE = %s",rt_file);
    $readmemb(rt_file,tab);  
end

// wire [10+`CN-1:0] temp;
// reg [4:0] addr;

// initial begin
//     addr =0;
// end

// always@(clk) begin
//     if(addr == `ROUTE_TABLE_DEPTH-1) addr <= 0;
//     else addr <= addr + 1;
// end

// assign temp = tab[addr];

always@(*) begin
    candidateOutVC = {(`CN){1'b0}};
    for(int i=0;i<`ROUTE_TABLE_DEPTH;i++) begin
        if(tab[i][9:0] == stream_id) begin
            candidateOutVC = tab[i][10+`CN-1:10];
            break;
        end
    end
end

endmodule