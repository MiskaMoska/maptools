//packing and unpacking
`include "params.svh"

module cast_converter #(
    parameter isCaster = 0, //indicate whether the current node is the source of cast communication
    parameter [9:0] stream_id = 0 //the stream-id of the stream generated from the current node, fixed at 10-bit
)(
    input       wire                            clk,
    input       wire                            rstn, 

    //input port from PE
    input       wire                            valid_i_pe,
    input       wire        [`DW-1:0]           data_i_pe,
    output      wire                            ready_o_pe,

    //output port to PE
    output      wire                            valid_o_pe,
    output      wire        [`DW-1:0]           data_o_pe,
    input       wire                            ready_i_pe,

    //input port from network
    input       wire                            valid_i_nw,
    input       wire        [`DW-1:0]           data_i_nw,
    output      wire                            ready_o_nw,

    //output port to network
    output      wire                            valid_o_nw,
    output      wire        [`DW-1:0]           data_o_nw,
    input       wire                            ready_i_nw
);

/**packing**/
localparam IDLE = 2'b00;
localparam HEAD = 2'b01;
localparam BODY = 2'b11;
localparam TAIL = 2'b10;

reg [1:0] pack_state;
wire [1:0] nxt_pack_state;
reg [`PKT_LEN_LOG-1:0] pack_cnt;

always@(posedge clk or negedge rstn) begin
    if(~rstn) pack_state <= IDLE;
    else pack_state <= nxt_pack_state;
end

assign nxt_pack_state = (pack_state == IDLE) & (isCaster == 1) ? HEAD : ( //to enable packing, the node must be a caster
                        (pack_state == HEAD) & valid_o_nw & ready_i_nw ? BODY : (
                        (pack_state == BODY) & (pack_cnt == `PKT_LEN - 3) & valid_o_nw & ready_i_nw ? TAIL : (
                        (pack_state == TAIL) & valid_o_nw & ready_i_nw ? HEAD : pack_state )));

always@(posedge clk or negedge rstn) begin
    if(~rstn) pack_cnt <= 0;
    else begin
        if(pack_state == BODY) begin
            if(valid_i_pe & ready_o_pe) pack_cnt <= pack_cnt + 1'b1;
        end
        else pack_cnt <= 0;
    end
end

assign valid_o_nw = (pack_state == HEAD) ? 1'b1 : (
                    (pack_state == BODY) ? valid_i_pe : (
                    (pack_state == TAIL) ? 1'b1 : 1'b0 ));

assign data_o_nw =  (pack_state == HEAD) ? {`HEAD,{(`DW-12){1'b0}},stream_id} : (
                    (pack_state == BODY) ? {`BODY,data_i_pe[`DW-3:0]} : (
                    (pack_state == TAIL) ? {`TAIL,{(`DW-2){1'b1}}} : 0 ));

assign ready_o_pe = (pack_state == BODY) ? ready_i_nw : 1'b0;


/**unpacking**/
//only need to filter out the head and tail from the network
wire [1:0] flit_type = data_i_nw[`DW-1:`DW-2];
assign valid_o_pe = ((flit_type == `HEAD) | (flit_type == `TAIL)) ? 1'b0 : valid_i_nw;
assign data_o_pe = data_i_nw;
assign ready_o_nw = ((flit_type == `HEAD) | (flit_type == `TAIL)) ? 1'b1 : ready_i_pe;
endmodule