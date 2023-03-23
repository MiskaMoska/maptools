import os

__all__ = ['gen_top_tb']

def gen_top_tb(root_dir, flees, flitnum):
    nf = range(len(flees[0]))
    save_dir = os.path.join(root_dir, 'network', 'test')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_dir = os.path.join(save_dir, 'top_tb.sv')
    state_file = os.path.join(root_dir, 'network', 'test', 'run_state')
    send_pool_file = os.path.join(root_dir, 'network', 'test', 'send_pool.txt')
    receive_pool_files = []
    for i in nf:
        receive_pool_files.append(os.path.join(root_dir, 'network', 'test', f'receive_pool_flee{i}.txt'))
    containt = '''
`timescale 1ns/1ps
`include "params.svh"

module top_tb;

reg clk;
reg rstn;
reg [31:0] addr;

integer state_file;
'''

    for i in nf:
        containt += f"integer file{i}; wire [`DW-1:0] data_o_flee{i}; wire valid_o_flee{i}, ready_i_flee{i};\n"
        containt += f"assign ready_i_flee{i} = rstn;\n"

    containt += f'''
(* ramstyle = "AUTO" *) reg [`DW-1 : 0] packets [0:{flitnum-1}];
wire [`DW-1:0] data_i_stab;
wire ready_o_stab;
reg valid_i_stab;

initial begin
    clk = 0;
    rstn = 1;
    # 33 rstn = 0;
    # 71 rstn = 1;
    valid_i_stab = 1;
    while(1) begin
        @(posedge clk);
        if((addr == {flitnum-1}) & valid_i_stab & ready_o_stab) begin
            valid_i_stab <= 1'b0;
            // break;
        end
    end
    # 1000000
    $fwrite(state_file,"%s","normal");
'''

    for i in nf:
        containt += f'''
    $fclose(file{i});'''
    containt +='''
    $fclose(state_file);
    $finish;
end

initial begin
    // $fsdbDumpfile("wave.fsdb");
    // $fsdbDumpvars(0,top_tb);
    // $fsdbDumpMDA(); //show array values
'''
    for i in nf:
        containt += f'''
    file{i} = $fopen("{receive_pool_files[i]}");'''
    containt += f'''
    state_file = $fopen("{state_file}");
end

// deadlock detection
initial begin
    int win;
    int start_addr;
    forever begin
        @(posedge clk)
        if(~rstn) win <= 0;
        else begin
            if(win == 9999) win <= 0;
            else win <= win + 1;
            if(win == 0) start_addr <= addr;
            else if(addr != {flitnum-1} & addr != 0 & win == 9999 && addr == start_addr) begin // deadlock occurs
                $fwrite(state_file,"%s","deadlock");
'''
    for i in nf:
        containt += f'''
                $fclose(file{i});'''
    containt += f'''
                $fclose(state_file);
                $display("ERROR: deadlock detected!!!!!");
                $finish;
            end
        end
    end
end

always #5 clk = ~clk;

initial begin
    addr = 0;
    $readmemb("{send_pool_file}",packets);
end

always@(posedge clk or negedge rstn)
begin
    if(~rstn) addr <= 0;
    else if(valid_i_stab & ready_o_stab) begin
        if(addr == {flitnum-1}) addr <= 0;
        else addr <= addr + 1;
    end 
end

//always@(posedge clk) begin
//    $display("addr@driver: %d",addr);
//end

assign data_i_stab = packets[addr];

system dut(
    .clk                         (clk),
    .rstn                        (rstn),
    .data_i_stab                 (data_i_stab),
    .valid_i_stab                (valid_i_stab),
    .ready_o_stab                (ready_o_stab),
'''
    for i in nf:
        containt += f'''
    .data_o_flee{i}                (data_o_flee{i}),
    .valid_o_flee{i}               (valid_o_flee{i}),
    .ready_i_flee{i}               (ready_i_flee{i}),'''
    containt = containt.rstrip(',')
    containt += '\n);\n'

    containt += '''
always@(posedge clk) begin'''
    for i in nf:
        containt += f'''
    if(valid_o_flee{i} & ready_i_flee{i})  
        $fwrite(file{i}, "%b\\n", data_o_flee{i});'''

    containt += '''
end

endmodule
'''
    with open(file_dir,"w") as my_file:
        my_file.write("{0}\n".format(containt))
        my_file.flush()
        my_file.close()
    
    print(f"top testbench has been written to: {file_dir}")