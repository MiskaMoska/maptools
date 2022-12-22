`include "params.svh"

module monitor #(
    parameter string id = "0" //destination node id
)(
    input   wire    clk,
    input   wire    rstn,
    input   wire    valid,
    output  wire    ready,
    input   wire    [`DW-1:0]   data,
    output  wire    credit_upd 
);

wire [`DW-1:0] fifo_dout;
wire fifo_full,fifo_empty;
wire fifo_read;

reg [31:0] cnt,eject_cnt;
integer file_id;

reg [4:0] push; //control the fifo_read signal
always@(posedge clk) begin
    if(push == 15) push <= 0;
    else push <= push + 1;
end

initial
begin
    push = 0;
    cnt = 0;
    eject_cnt = 0;
    file_id = $fopen({"/mnt/f/git/NVCIM-COMM/behavior_model/test_multicast/receive_pool_",id});
    wait(eject_cnt == 990);
    #25000
    $fclose(file_id);
    $stop;
end

always@(posedge clk)
begin
    cnt <= cnt + 1;
    if(fifo_read)
        $fwrite(file_id, "%b\n", fifo_dout);
end

assign fifo_read = ~fifo_empty & (push > 13); //push back

SyncFIFO_RTL #(
    .width                   (`DW),
    .depth                   (`BUFFER_ALLOC),
    .depth_LOG               (`BUFFER_ALLOC_LOG),
    .FWFT                    (1)
)fifo(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (fifo_read),
    .write_i                 (valid & ~fifo_full),
    .full_o                  (fifo_full),
    .empty_o                 (fifo_empty),
    .data_i                  (data),
    .data_o                  (fifo_dout)
);

always@(posedge clk) begin
    if(rstn & fifo_read)
        eject_cnt <= eject_cnt + 1;
end

assign ready = ~fifo_full;
assign credit_upd = fifo_read;

endmodule
