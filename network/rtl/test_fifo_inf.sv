module test_fifo_inf;

reg clk;
reg rstn;
wire empty;
reg [7:0] data_i;
wire [7:0] data_o;
wire read;
reg write;
assign read = ~empty;

clocking cb @(posedge clk);
    default output #0;
    output write, data_i;
endclocking

initial begin
    $display("starting simulation");
    $fsdbDumpfile("fifo.fsdb");
    $fsdbDumpvars(0,test_fifo_inf);
    $fsdbDumpMDA(); //show array values
    clk = 0;
    write = 0;
    rstn = 1;
    data_i = 0;
    # 33 rstn = 0;
    # 70 rstn = 1;
    repeat(10) begin
        @(cb)
        cb.write <= 1;
        cb.data_i <= data_i + 1;
    end
    # 3
    cb.write <= 1'b0;
    # 1000
    $display("ending simulation");
    $finish;
end

always #5 clk = ~clk;

nfifo_inf #(
    .width                   (8)
)nfifo_inf(
    .clk_i                   (clk),
    .rst_i                   (~rstn),
    .read_i                  (read),
    .write_i                 (write),
    .empty_o                 (empty),
    .data_i                  (data_i),
    .data_o                  (data_o)
);

endmodule