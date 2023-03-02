
`include "params.svh"
`include "network_config.svh"

module network(
        input       wire                        clk,
        input       wire                        rstn,

        //stab port
        input       wire        [`DW-1:0]       data_i_stab,
        input       wire                        valid_i_stab,
        output      wire                        ready_o_stab,

        //flee0 port
        output      wire        [`DW-1:0]       data_o_flee0,
        output      wire                        valid_o_flee0,
        input       wire                        ready_i_flee0,

        //flee1 port
        output      wire        [`DW-1:0]       data_o_flee1,
        output      wire                        valid_o_flee1,
        input       wire                        ready_i_flee1,

        //cast local ports
        input       wire        [`DW-1:0]       cast_data_i[`NOC_WIDTH][`NOC_HEIGHT],
        input       wire                        cast_valid_i[`NOC_WIDTH][`NOC_HEIGHT],
        output      wire                        cast_ready_o[`NOC_WIDTH][`NOC_HEIGHT],

        output      wire        [`DW-1:0]       cast_data_o[`NOC_WIDTH][`NOC_HEIGHT],
        output      wire                        cast_valid_o[`NOC_WIDTH][`NOC_HEIGHT],
        input       wire                        cast_ready_i[`NOC_WIDTH][`NOC_HEIGHT],

        //merge local ports
        input       wire        [`DW-1:0]       merge_data_i[`NOC_WIDTH][`NOC_HEIGHT],
        input       wire                        merge_valid_i[`NOC_WIDTH][`NOC_HEIGHT],
        output      wire                        merge_ready_o[`NOC_WIDTH][`NOC_HEIGHT],

        output      wire        [`DW-1:0]       merge_data_o[`NOC_WIDTH][`NOC_HEIGHT],
        output      wire                        merge_valid_o[`NOC_WIDTH][`NOC_HEIGHT],
        input       wire                        merge_ready_i[`NOC_WIDTH][`NOC_HEIGHT],
);

wire [`DW-1:0] data_stab, data_flee0, data_flee1;
wire valid_stab, ready_stab, valid_flee0, valid_flee1, ready_flee0, ready_flee1;

wire [`DW-1:0] data_i_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], data_o_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], data_i_merge_nw[`NOC_WIDTH][`NOC_HEIGHT], data_o_merge_nw[`NOC_WIDTH][`NOC_HEIGHT];
wire valid_i_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], valid_o_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], valid_i_merge_nw[`NOC_WIDTH][`NOC_HEIGHT], valid_o_merge_nw[`NOC_WIDTH][`NOC_HEIGHT];
wire ready_i_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], ready_o_cast_nw[`NOC_WIDTH][`NOC_HEIGHT], ready_i_merge_nw[`NOC_WIDTH][`NOC_HEIGHT], ready_o_merge_nw[`NOC_WIDTH][`NOC_HEIGHT];

wire credit_upd[`NOC_WIDTH][`NOC_HEIGHT];

// from stab port to network, must enable packeting
cast_converter #(
    .isCaster                 (1),
    .stream_id                (1023)
)converter_stab(
    .clk                      (clk),
    .rstn                     (rstn),
    .valid_i_pe               (valid_i_stab),
    .data_i_pe                (data_i_stab),
    .ready_o_pe               (ready_o_stab),
    .valid_o_pe               (),
    .data_o_pe                (),
    .ready_i_pe               (1'b0),
    .valid_i_nw               (1'b0),
    .data_i_nw                ({(`DW){1'b0}}),
    .ready_o_nw               (),
    .valid_o_nw               (valid_stab),
    .data_o_nw                (data_stab),
    .ready_i_nw               (ready_stab)
);

// from flee0 port to outside
cast_converter #(
    .isCaster                 (0),
    .stream_id                (1022)
)converter_stab(
    .clk                      (clk),
    .rstn                     (rstn),
    .valid_i_pe               (1'b0),
    .data_i_pe                ({(`DW){1'b0}}),
    .ready_o_pe               (),
    .valid_o_pe               (valid_flee0),
    .data_o_pe                (data_flee0),
    .ready_i_pe               (ready_flee0),
    .valid_i_nw               (valid_o_flee0),
    .data_i_nw                (data_o_flee0),
    .ready_o_nw               (ready_i_flee0),
    .valid_o_nw               (),
    .data_o_nw                (),
    .ready_i_nw               (1'b0)
);

// from flee1 port to outside
cast_converter #(
    .isCaster                 (0),
    .stream_id                (1022)
)converter_stab(
    .clk                      (clk),
    .rstn                     (rstn),
    .valid_i_pe               (1'b0),
    .data_i_pe                ({(`DW){1'b0}}),
    .ready_o_pe               (),
    .valid_o_pe               (valid_flee1),
    .data_o_pe                (data_flee1),
    .ready_i_pe               (ready_flee1),
    .valid_i_nw               (valid_o_flee1),
    .data_i_nw                (data_o_flee1),
    .ready_o_nw               (ready_i_flee1),
    .valid_o_nw               (),
    .data_o_nw                (),
    .ready_i_nw               (1'b0)
);

cast_network cast_nw(
    .clk                                               (clk),
    .rstn                                              (rstn),
    .data_i                                            (cast_data_i_nw),
    .valid_i                                           (cast_valid_i_nw),
    .ready_o                                           (cast_ready_o_nw),
    .data_o                                            (cast_data_o_nw),
    .valid_o                                           (cast_valid_o_nw),
    .ready_i                                           (cast_ready_i_nw),
    .data_i_stab                                       (data_stab),
    .valid_i_stab                                      (valid_stab),
    .ready_o_stab                                      (ready_stab),
    .data_o_flee0                                      (data_flee0),
    .valid_o_flee0                                     (valid_flee0),
    .ready_i_flee0                                     (ready_flee0),
    .data_o_flee1                                      (data_flee1),
    .valid_o_flee1                                     (valid_flee1),
    .ready_i_flee1                                     (ready_flee1),
    .credit_upd                                        (credit_upd)
);

merge_network merge_nw(
    .clk                                            (clk),
    .rstn                                           (rstn),
    .data_i                                         (merge_data_i_nw),
    .valid_i                                        (merge_valid_i_nw),
    .ready_o                                        (merge_ready_o_nw),
    .data_o                                         (merge_data_o_nw),
    .valid_o                                        (merge_valid_o_nw),
    .ready_i                                        (merge_ready_i_nw)
);

network_interface #(
    .isCaster                       (isCaster_0_0),
    .stream_id                      (stream_id_0_0)
)ni_0_0(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[0][0]),
    .data_i_cast_nw                 (data_o_cast_nw[0][0]),
    .ready_o_cast_nw                (ready_i_cast_nw[0][0]),
    .valid_o_cast_nw                (valid_i_cast_nw[0][0]),
    .data_o_cast_nw                 (data_i_cast_nw[0][0]),
    .ready_i_cast_nw                (ready_o_cast_nw[0][0]),
    .valid_i_merge_nw               (valid_o_merge_nw[0][0]),
    .data_i_merge_nw                (data_o_merge_nw[0][0]),
    .ready_o_merge_nw               (ready_i_merge_nw[0][0]),
    .valid_o_merge_nw               (valid_i_merge_nw[0][0]),
    .data_o_merge_nw                (data_i_merge_nw[0][0]),
    .ready_i_merge_nw               (ready_o_merge_nw[0][0]),
    .valid_i_cast_pe                (cast_valid_i[0][0]),
    .data_i_cast_pe                 (cast_data_i[0][0]),
    .ready_o_cast_pe                (cast_ready_o[0][0]),
    .valid_o_cast_pe                (cast_valid_o[0][0]),
    .data_o_cast_pe                 (cast_data_o[0][0]),
    .ready_i_cast_pe                (cast_ready_i[0][0]),
    .valid_i_merge_pe               (merge_valid_i[0][0]),
    .data_i_merge_pe                (merge_data_i[0][0]),
    .ready_o_merge_pe               (merge_ready_o[0][0]),
    .valid_o_merge_pe               (merge_valid_o[0][0]),
    .data_o_merge_pe                (merge_data_o[0][0]),
    .ready_i_merge_pe               (merge_ready_i[0][0]),
    .credit_upd                     (credit_upd[0][0])
);


network_interface #(
    .isCaster                       (isCaster_0_1),
    .stream_id                      (stream_id_0_1)
)ni_0_1(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[0][1]),
    .data_i_cast_nw                 (data_o_cast_nw[0][1]),
    .ready_o_cast_nw                (ready_i_cast_nw[0][1]),
    .valid_o_cast_nw                (valid_i_cast_nw[0][1]),
    .data_o_cast_nw                 (data_i_cast_nw[0][1]),
    .ready_i_cast_nw                (ready_o_cast_nw[0][1]),
    .valid_i_merge_nw               (valid_o_merge_nw[0][1]),
    .data_i_merge_nw                (data_o_merge_nw[0][1]),
    .ready_o_merge_nw               (ready_i_merge_nw[0][1]),
    .valid_o_merge_nw               (valid_i_merge_nw[0][1]),
    .data_o_merge_nw                (data_i_merge_nw[0][1]),
    .ready_i_merge_nw               (ready_o_merge_nw[0][1]),
    .valid_i_cast_pe                (cast_valid_i[0][1]),
    .data_i_cast_pe                 (cast_data_i[0][1]),
    .ready_o_cast_pe                (cast_ready_o[0][1]),
    .valid_o_cast_pe                (cast_valid_o[0][1]),
    .data_o_cast_pe                 (cast_data_o[0][1]),
    .ready_i_cast_pe                (cast_ready_i[0][1]),
    .valid_i_merge_pe               (merge_valid_i[0][1]),
    .data_i_merge_pe                (merge_data_i[0][1]),
    .ready_o_merge_pe               (merge_ready_o[0][1]),
    .valid_o_merge_pe               (merge_valid_o[0][1]),
    .data_o_merge_pe                (merge_data_o[0][1]),
    .ready_i_merge_pe               (merge_ready_i[0][1]),
    .credit_upd                     (credit_upd[0][1])
);


network_interface #(
    .isCaster                       (isCaster_0_2),
    .stream_id                      (stream_id_0_2)
)ni_0_2(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[0][2]),
    .data_i_cast_nw                 (data_o_cast_nw[0][2]),
    .ready_o_cast_nw                (ready_i_cast_nw[0][2]),
    .valid_o_cast_nw                (valid_i_cast_nw[0][2]),
    .data_o_cast_nw                 (data_i_cast_nw[0][2]),
    .ready_i_cast_nw                (ready_o_cast_nw[0][2]),
    .valid_i_merge_nw               (valid_o_merge_nw[0][2]),
    .data_i_merge_nw                (data_o_merge_nw[0][2]),
    .ready_o_merge_nw               (ready_i_merge_nw[0][2]),
    .valid_o_merge_nw               (valid_i_merge_nw[0][2]),
    .data_o_merge_nw                (data_i_merge_nw[0][2]),
    .ready_i_merge_nw               (ready_o_merge_nw[0][2]),
    .valid_i_cast_pe                (cast_valid_i[0][2]),
    .data_i_cast_pe                 (cast_data_i[0][2]),
    .ready_o_cast_pe                (cast_ready_o[0][2]),
    .valid_o_cast_pe                (cast_valid_o[0][2]),
    .data_o_cast_pe                 (cast_data_o[0][2]),
    .ready_i_cast_pe                (cast_ready_i[0][2]),
    .valid_i_merge_pe               (merge_valid_i[0][2]),
    .data_i_merge_pe                (merge_data_i[0][2]),
    .ready_o_merge_pe               (merge_ready_o[0][2]),
    .valid_o_merge_pe               (merge_valid_o[0][2]),
    .data_o_merge_pe                (merge_data_o[0][2]),
    .ready_i_merge_pe               (merge_ready_i[0][2]),
    .credit_upd                     (credit_upd[0][2])
);


network_interface #(
    .isCaster                       (isCaster_0_3),
    .stream_id                      (stream_id_0_3)
)ni_0_3(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[0][3]),
    .data_i_cast_nw                 (data_o_cast_nw[0][3]),
    .ready_o_cast_nw                (ready_i_cast_nw[0][3]),
    .valid_o_cast_nw                (valid_i_cast_nw[0][3]),
    .data_o_cast_nw                 (data_i_cast_nw[0][3]),
    .ready_i_cast_nw                (ready_o_cast_nw[0][3]),
    .valid_i_merge_nw               (valid_o_merge_nw[0][3]),
    .data_i_merge_nw                (data_o_merge_nw[0][3]),
    .ready_o_merge_nw               (ready_i_merge_nw[0][3]),
    .valid_o_merge_nw               (valid_i_merge_nw[0][3]),
    .data_o_merge_nw                (data_i_merge_nw[0][3]),
    .ready_i_merge_nw               (ready_o_merge_nw[0][3]),
    .valid_i_cast_pe                (cast_valid_i[0][3]),
    .data_i_cast_pe                 (cast_data_i[0][3]),
    .ready_o_cast_pe                (cast_ready_o[0][3]),
    .valid_o_cast_pe                (cast_valid_o[0][3]),
    .data_o_cast_pe                 (cast_data_o[0][3]),
    .ready_i_cast_pe                (cast_ready_i[0][3]),
    .valid_i_merge_pe               (merge_valid_i[0][3]),
    .data_i_merge_pe                (merge_data_i[0][3]),
    .ready_o_merge_pe               (merge_ready_o[0][3]),
    .valid_o_merge_pe               (merge_valid_o[0][3]),
    .data_o_merge_pe                (merge_data_o[0][3]),
    .ready_i_merge_pe               (merge_ready_i[0][3]),
    .credit_upd                     (credit_upd[0][3])
);


network_interface #(
    .isCaster                       (isCaster_0_4),
    .stream_id                      (stream_id_0_4)
)ni_0_4(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[0][4]),
    .data_i_cast_nw                 (data_o_cast_nw[0][4]),
    .ready_o_cast_nw                (ready_i_cast_nw[0][4]),
    .valid_o_cast_nw                (valid_i_cast_nw[0][4]),
    .data_o_cast_nw                 (data_i_cast_nw[0][4]),
    .ready_i_cast_nw                (ready_o_cast_nw[0][4]),
    .valid_i_merge_nw               (valid_o_merge_nw[0][4]),
    .data_i_merge_nw                (data_o_merge_nw[0][4]),
    .ready_o_merge_nw               (ready_i_merge_nw[0][4]),
    .valid_o_merge_nw               (valid_i_merge_nw[0][4]),
    .data_o_merge_nw                (data_i_merge_nw[0][4]),
    .ready_i_merge_nw               (ready_o_merge_nw[0][4]),
    .valid_i_cast_pe                (cast_valid_i[0][4]),
    .data_i_cast_pe                 (cast_data_i[0][4]),
    .ready_o_cast_pe                (cast_ready_o[0][4]),
    .valid_o_cast_pe                (cast_valid_o[0][4]),
    .data_o_cast_pe                 (cast_data_o[0][4]),
    .ready_i_cast_pe                (cast_ready_i[0][4]),
    .valid_i_merge_pe               (merge_valid_i[0][4]),
    .data_i_merge_pe                (merge_data_i[0][4]),
    .ready_o_merge_pe               (merge_ready_o[0][4]),
    .valid_o_merge_pe               (merge_valid_o[0][4]),
    .data_o_merge_pe                (merge_data_o[0][4]),
    .ready_i_merge_pe               (merge_ready_i[0][4]),
    .credit_upd                     (credit_upd[0][4])
);


network_interface #(
    .isCaster                       (isCaster_0_5),
    .stream_id                      (stream_id_0_5)
)ni_0_5(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[0][5]),
    .data_i_cast_nw                 (data_o_cast_nw[0][5]),
    .ready_o_cast_nw                (ready_i_cast_nw[0][5]),
    .valid_o_cast_nw                (valid_i_cast_nw[0][5]),
    .data_o_cast_nw                 (data_i_cast_nw[0][5]),
    .ready_i_cast_nw                (ready_o_cast_nw[0][5]),
    .valid_i_merge_nw               (valid_o_merge_nw[0][5]),
    .data_i_merge_nw                (data_o_merge_nw[0][5]),
    .ready_o_merge_nw               (ready_i_merge_nw[0][5]),
    .valid_o_merge_nw               (valid_i_merge_nw[0][5]),
    .data_o_merge_nw                (data_i_merge_nw[0][5]),
    .ready_i_merge_nw               (ready_o_merge_nw[0][5]),
    .valid_i_cast_pe                (cast_valid_i[0][5]),
    .data_i_cast_pe                 (cast_data_i[0][5]),
    .ready_o_cast_pe                (cast_ready_o[0][5]),
    .valid_o_cast_pe                (cast_valid_o[0][5]),
    .data_o_cast_pe                 (cast_data_o[0][5]),
    .ready_i_cast_pe                (cast_ready_i[0][5]),
    .valid_i_merge_pe               (merge_valid_i[0][5]),
    .data_i_merge_pe                (merge_data_i[0][5]),
    .ready_o_merge_pe               (merge_ready_o[0][5]),
    .valid_o_merge_pe               (merge_valid_o[0][5]),
    .data_o_merge_pe                (merge_data_o[0][5]),
    .ready_i_merge_pe               (merge_ready_i[0][5]),
    .credit_upd                     (credit_upd[0][5])
);


network_interface #(
    .isCaster                       (isCaster_0_6),
    .stream_id                      (stream_id_0_6)
)ni_0_6(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[0][6]),
    .data_i_cast_nw                 (data_o_cast_nw[0][6]),
    .ready_o_cast_nw                (ready_i_cast_nw[0][6]),
    .valid_o_cast_nw                (valid_i_cast_nw[0][6]),
    .data_o_cast_nw                 (data_i_cast_nw[0][6]),
    .ready_i_cast_nw                (ready_o_cast_nw[0][6]),
    .valid_i_merge_nw               (valid_o_merge_nw[0][6]),
    .data_i_merge_nw                (data_o_merge_nw[0][6]),
    .ready_o_merge_nw               (ready_i_merge_nw[0][6]),
    .valid_o_merge_nw               (valid_i_merge_nw[0][6]),
    .data_o_merge_nw                (data_i_merge_nw[0][6]),
    .ready_i_merge_nw               (ready_o_merge_nw[0][6]),
    .valid_i_cast_pe                (cast_valid_i[0][6]),
    .data_i_cast_pe                 (cast_data_i[0][6]),
    .ready_o_cast_pe                (cast_ready_o[0][6]),
    .valid_o_cast_pe                (cast_valid_o[0][6]),
    .data_o_cast_pe                 (cast_data_o[0][6]),
    .ready_i_cast_pe                (cast_ready_i[0][6]),
    .valid_i_merge_pe               (merge_valid_i[0][6]),
    .data_i_merge_pe                (merge_data_i[0][6]),
    .ready_o_merge_pe               (merge_ready_o[0][6]),
    .valid_o_merge_pe               (merge_valid_o[0][6]),
    .data_o_merge_pe                (merge_data_o[0][6]),
    .ready_i_merge_pe               (merge_ready_i[0][6]),
    .credit_upd                     (credit_upd[0][6])
);


network_interface #(
    .isCaster                       (isCaster_0_7),
    .stream_id                      (stream_id_0_7)
)ni_0_7(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[0][7]),
    .data_i_cast_nw                 (data_o_cast_nw[0][7]),
    .ready_o_cast_nw                (ready_i_cast_nw[0][7]),
    .valid_o_cast_nw                (valid_i_cast_nw[0][7]),
    .data_o_cast_nw                 (data_i_cast_nw[0][7]),
    .ready_i_cast_nw                (ready_o_cast_nw[0][7]),
    .valid_i_merge_nw               (valid_o_merge_nw[0][7]),
    .data_i_merge_nw                (data_o_merge_nw[0][7]),
    .ready_o_merge_nw               (ready_i_merge_nw[0][7]),
    .valid_o_merge_nw               (valid_i_merge_nw[0][7]),
    .data_o_merge_nw                (data_i_merge_nw[0][7]),
    .ready_i_merge_nw               (ready_o_merge_nw[0][7]),
    .valid_i_cast_pe                (cast_valid_i[0][7]),
    .data_i_cast_pe                 (cast_data_i[0][7]),
    .ready_o_cast_pe                (cast_ready_o[0][7]),
    .valid_o_cast_pe                (cast_valid_o[0][7]),
    .data_o_cast_pe                 (cast_data_o[0][7]),
    .ready_i_cast_pe                (cast_ready_i[0][7]),
    .valid_i_merge_pe               (merge_valid_i[0][7]),
    .data_i_merge_pe                (merge_data_i[0][7]),
    .ready_o_merge_pe               (merge_ready_o[0][7]),
    .valid_o_merge_pe               (merge_valid_o[0][7]),
    .data_o_merge_pe                (merge_data_o[0][7]),
    .ready_i_merge_pe               (merge_ready_i[0][7]),
    .credit_upd                     (credit_upd[0][7])
);


network_interface #(
    .isCaster                       (isCaster_0_8),
    .stream_id                      (stream_id_0_8)
)ni_0_8(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[0][8]),
    .data_i_cast_nw                 (data_o_cast_nw[0][8]),
    .ready_o_cast_nw                (ready_i_cast_nw[0][8]),
    .valid_o_cast_nw                (valid_i_cast_nw[0][8]),
    .data_o_cast_nw                 (data_i_cast_nw[0][8]),
    .ready_i_cast_nw                (ready_o_cast_nw[0][8]),
    .valid_i_merge_nw               (valid_o_merge_nw[0][8]),
    .data_i_merge_nw                (data_o_merge_nw[0][8]),
    .ready_o_merge_nw               (ready_i_merge_nw[0][8]),
    .valid_o_merge_nw               (valid_i_merge_nw[0][8]),
    .data_o_merge_nw                (data_i_merge_nw[0][8]),
    .ready_i_merge_nw               (ready_o_merge_nw[0][8]),
    .valid_i_cast_pe                (cast_valid_i[0][8]),
    .data_i_cast_pe                 (cast_data_i[0][8]),
    .ready_o_cast_pe                (cast_ready_o[0][8]),
    .valid_o_cast_pe                (cast_valid_o[0][8]),
    .data_o_cast_pe                 (cast_data_o[0][8]),
    .ready_i_cast_pe                (cast_ready_i[0][8]),
    .valid_i_merge_pe               (merge_valid_i[0][8]),
    .data_i_merge_pe                (merge_data_i[0][8]),
    .ready_o_merge_pe               (merge_ready_o[0][8]),
    .valid_o_merge_pe               (merge_valid_o[0][8]),
    .data_o_merge_pe                (merge_data_o[0][8]),
    .ready_i_merge_pe               (merge_ready_i[0][8]),
    .credit_upd                     (credit_upd[0][8])
);


network_interface #(
    .isCaster                       (isCaster_0_9),
    .stream_id                      (stream_id_0_9)
)ni_0_9(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[0][9]),
    .data_i_cast_nw                 (data_o_cast_nw[0][9]),
    .ready_o_cast_nw                (ready_i_cast_nw[0][9]),
    .valid_o_cast_nw                (valid_i_cast_nw[0][9]),
    .data_o_cast_nw                 (data_i_cast_nw[0][9]),
    .ready_i_cast_nw                (ready_o_cast_nw[0][9]),
    .valid_i_merge_nw               (valid_o_merge_nw[0][9]),
    .data_i_merge_nw                (data_o_merge_nw[0][9]),
    .ready_o_merge_nw               (ready_i_merge_nw[0][9]),
    .valid_o_merge_nw               (valid_i_merge_nw[0][9]),
    .data_o_merge_nw                (data_i_merge_nw[0][9]),
    .ready_i_merge_nw               (ready_o_merge_nw[0][9]),
    .valid_i_cast_pe                (cast_valid_i[0][9]),
    .data_i_cast_pe                 (cast_data_i[0][9]),
    .ready_o_cast_pe                (cast_ready_o[0][9]),
    .valid_o_cast_pe                (cast_valid_o[0][9]),
    .data_o_cast_pe                 (cast_data_o[0][9]),
    .ready_i_cast_pe                (cast_ready_i[0][9]),
    .valid_i_merge_pe               (merge_valid_i[0][9]),
    .data_i_merge_pe                (merge_data_i[0][9]),
    .ready_o_merge_pe               (merge_ready_o[0][9]),
    .valid_o_merge_pe               (merge_valid_o[0][9]),
    .data_o_merge_pe                (merge_data_o[0][9]),
    .ready_i_merge_pe               (merge_ready_i[0][9]),
    .credit_upd                     (credit_upd[0][9])
);


network_interface #(
    .isCaster                       (isCaster_0_10),
    .stream_id                      (stream_id_0_10)
)ni_0_10(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[0][10]),
    .data_i_cast_nw                 (data_o_cast_nw[0][10]),
    .ready_o_cast_nw                (ready_i_cast_nw[0][10]),
    .valid_o_cast_nw                (valid_i_cast_nw[0][10]),
    .data_o_cast_nw                 (data_i_cast_nw[0][10]),
    .ready_i_cast_nw                (ready_o_cast_nw[0][10]),
    .valid_i_merge_nw               (valid_o_merge_nw[0][10]),
    .data_i_merge_nw                (data_o_merge_nw[0][10]),
    .ready_o_merge_nw               (ready_i_merge_nw[0][10]),
    .valid_o_merge_nw               (valid_i_merge_nw[0][10]),
    .data_o_merge_nw                (data_i_merge_nw[0][10]),
    .ready_i_merge_nw               (ready_o_merge_nw[0][10]),
    .valid_i_cast_pe                (cast_valid_i[0][10]),
    .data_i_cast_pe                 (cast_data_i[0][10]),
    .ready_o_cast_pe                (cast_ready_o[0][10]),
    .valid_o_cast_pe                (cast_valid_o[0][10]),
    .data_o_cast_pe                 (cast_data_o[0][10]),
    .ready_i_cast_pe                (cast_ready_i[0][10]),
    .valid_i_merge_pe               (merge_valid_i[0][10]),
    .data_i_merge_pe                (merge_data_i[0][10]),
    .ready_o_merge_pe               (merge_ready_o[0][10]),
    .valid_o_merge_pe               (merge_valid_o[0][10]),
    .data_o_merge_pe                (merge_data_o[0][10]),
    .ready_i_merge_pe               (merge_ready_i[0][10]),
    .credit_upd                     (credit_upd[0][10])
);


network_interface #(
    .isCaster                       (isCaster_1_0),
    .stream_id                      (stream_id_1_0)
)ni_1_0(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[1][0]),
    .data_i_cast_nw                 (data_o_cast_nw[1][0]),
    .ready_o_cast_nw                (ready_i_cast_nw[1][0]),
    .valid_o_cast_nw                (valid_i_cast_nw[1][0]),
    .data_o_cast_nw                 (data_i_cast_nw[1][0]),
    .ready_i_cast_nw                (ready_o_cast_nw[1][0]),
    .valid_i_merge_nw               (valid_o_merge_nw[1][0]),
    .data_i_merge_nw                (data_o_merge_nw[1][0]),
    .ready_o_merge_nw               (ready_i_merge_nw[1][0]),
    .valid_o_merge_nw               (valid_i_merge_nw[1][0]),
    .data_o_merge_nw                (data_i_merge_nw[1][0]),
    .ready_i_merge_nw               (ready_o_merge_nw[1][0]),
    .valid_i_cast_pe                (cast_valid_i[1][0]),
    .data_i_cast_pe                 (cast_data_i[1][0]),
    .ready_o_cast_pe                (cast_ready_o[1][0]),
    .valid_o_cast_pe                (cast_valid_o[1][0]),
    .data_o_cast_pe                 (cast_data_o[1][0]),
    .ready_i_cast_pe                (cast_ready_i[1][0]),
    .valid_i_merge_pe               (merge_valid_i[1][0]),
    .data_i_merge_pe                (merge_data_i[1][0]),
    .ready_o_merge_pe               (merge_ready_o[1][0]),
    .valid_o_merge_pe               (merge_valid_o[1][0]),
    .data_o_merge_pe                (merge_data_o[1][0]),
    .ready_i_merge_pe               (merge_ready_i[1][0]),
    .credit_upd                     (credit_upd[1][0])
);


network_interface #(
    .isCaster                       (isCaster_1_1),
    .stream_id                      (stream_id_1_1)
)ni_1_1(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[1][1]),
    .data_i_cast_nw                 (data_o_cast_nw[1][1]),
    .ready_o_cast_nw                (ready_i_cast_nw[1][1]),
    .valid_o_cast_nw                (valid_i_cast_nw[1][1]),
    .data_o_cast_nw                 (data_i_cast_nw[1][1]),
    .ready_i_cast_nw                (ready_o_cast_nw[1][1]),
    .valid_i_merge_nw               (valid_o_merge_nw[1][1]),
    .data_i_merge_nw                (data_o_merge_nw[1][1]),
    .ready_o_merge_nw               (ready_i_merge_nw[1][1]),
    .valid_o_merge_nw               (valid_i_merge_nw[1][1]),
    .data_o_merge_nw                (data_i_merge_nw[1][1]),
    .ready_i_merge_nw               (ready_o_merge_nw[1][1]),
    .valid_i_cast_pe                (cast_valid_i[1][1]),
    .data_i_cast_pe                 (cast_data_i[1][1]),
    .ready_o_cast_pe                (cast_ready_o[1][1]),
    .valid_o_cast_pe                (cast_valid_o[1][1]),
    .data_o_cast_pe                 (cast_data_o[1][1]),
    .ready_i_cast_pe                (cast_ready_i[1][1]),
    .valid_i_merge_pe               (merge_valid_i[1][1]),
    .data_i_merge_pe                (merge_data_i[1][1]),
    .ready_o_merge_pe               (merge_ready_o[1][1]),
    .valid_o_merge_pe               (merge_valid_o[1][1]),
    .data_o_merge_pe                (merge_data_o[1][1]),
    .ready_i_merge_pe               (merge_ready_i[1][1]),
    .credit_upd                     (credit_upd[1][1])
);


network_interface #(
    .isCaster                       (isCaster_1_2),
    .stream_id                      (stream_id_1_2)
)ni_1_2(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[1][2]),
    .data_i_cast_nw                 (data_o_cast_nw[1][2]),
    .ready_o_cast_nw                (ready_i_cast_nw[1][2]),
    .valid_o_cast_nw                (valid_i_cast_nw[1][2]),
    .data_o_cast_nw                 (data_i_cast_nw[1][2]),
    .ready_i_cast_nw                (ready_o_cast_nw[1][2]),
    .valid_i_merge_nw               (valid_o_merge_nw[1][2]),
    .data_i_merge_nw                (data_o_merge_nw[1][2]),
    .ready_o_merge_nw               (ready_i_merge_nw[1][2]),
    .valid_o_merge_nw               (valid_i_merge_nw[1][2]),
    .data_o_merge_nw                (data_i_merge_nw[1][2]),
    .ready_i_merge_nw               (ready_o_merge_nw[1][2]),
    .valid_i_cast_pe                (cast_valid_i[1][2]),
    .data_i_cast_pe                 (cast_data_i[1][2]),
    .ready_o_cast_pe                (cast_ready_o[1][2]),
    .valid_o_cast_pe                (cast_valid_o[1][2]),
    .data_o_cast_pe                 (cast_data_o[1][2]),
    .ready_i_cast_pe                (cast_ready_i[1][2]),
    .valid_i_merge_pe               (merge_valid_i[1][2]),
    .data_i_merge_pe                (merge_data_i[1][2]),
    .ready_o_merge_pe               (merge_ready_o[1][2]),
    .valid_o_merge_pe               (merge_valid_o[1][2]),
    .data_o_merge_pe                (merge_data_o[1][2]),
    .ready_i_merge_pe               (merge_ready_i[1][2]),
    .credit_upd                     (credit_upd[1][2])
);


network_interface #(
    .isCaster                       (isCaster_1_3),
    .stream_id                      (stream_id_1_3)
)ni_1_3(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[1][3]),
    .data_i_cast_nw                 (data_o_cast_nw[1][3]),
    .ready_o_cast_nw                (ready_i_cast_nw[1][3]),
    .valid_o_cast_nw                (valid_i_cast_nw[1][3]),
    .data_o_cast_nw                 (data_i_cast_nw[1][3]),
    .ready_i_cast_nw                (ready_o_cast_nw[1][3]),
    .valid_i_merge_nw               (valid_o_merge_nw[1][3]),
    .data_i_merge_nw                (data_o_merge_nw[1][3]),
    .ready_o_merge_nw               (ready_i_merge_nw[1][3]),
    .valid_o_merge_nw               (valid_i_merge_nw[1][3]),
    .data_o_merge_nw                (data_i_merge_nw[1][3]),
    .ready_i_merge_nw               (ready_o_merge_nw[1][3]),
    .valid_i_cast_pe                (cast_valid_i[1][3]),
    .data_i_cast_pe                 (cast_data_i[1][3]),
    .ready_o_cast_pe                (cast_ready_o[1][3]),
    .valid_o_cast_pe                (cast_valid_o[1][3]),
    .data_o_cast_pe                 (cast_data_o[1][3]),
    .ready_i_cast_pe                (cast_ready_i[1][3]),
    .valid_i_merge_pe               (merge_valid_i[1][3]),
    .data_i_merge_pe                (merge_data_i[1][3]),
    .ready_o_merge_pe               (merge_ready_o[1][3]),
    .valid_o_merge_pe               (merge_valid_o[1][3]),
    .data_o_merge_pe                (merge_data_o[1][3]),
    .ready_i_merge_pe               (merge_ready_i[1][3]),
    .credit_upd                     (credit_upd[1][3])
);


network_interface #(
    .isCaster                       (isCaster_1_4),
    .stream_id                      (stream_id_1_4)
)ni_1_4(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[1][4]),
    .data_i_cast_nw                 (data_o_cast_nw[1][4]),
    .ready_o_cast_nw                (ready_i_cast_nw[1][4]),
    .valid_o_cast_nw                (valid_i_cast_nw[1][4]),
    .data_o_cast_nw                 (data_i_cast_nw[1][4]),
    .ready_i_cast_nw                (ready_o_cast_nw[1][4]),
    .valid_i_merge_nw               (valid_o_merge_nw[1][4]),
    .data_i_merge_nw                (data_o_merge_nw[1][4]),
    .ready_o_merge_nw               (ready_i_merge_nw[1][4]),
    .valid_o_merge_nw               (valid_i_merge_nw[1][4]),
    .data_o_merge_nw                (data_i_merge_nw[1][4]),
    .ready_i_merge_nw               (ready_o_merge_nw[1][4]),
    .valid_i_cast_pe                (cast_valid_i[1][4]),
    .data_i_cast_pe                 (cast_data_i[1][4]),
    .ready_o_cast_pe                (cast_ready_o[1][4]),
    .valid_o_cast_pe                (cast_valid_o[1][4]),
    .data_o_cast_pe                 (cast_data_o[1][4]),
    .ready_i_cast_pe                (cast_ready_i[1][4]),
    .valid_i_merge_pe               (merge_valid_i[1][4]),
    .data_i_merge_pe                (merge_data_i[1][4]),
    .ready_o_merge_pe               (merge_ready_o[1][4]),
    .valid_o_merge_pe               (merge_valid_o[1][4]),
    .data_o_merge_pe                (merge_data_o[1][4]),
    .ready_i_merge_pe               (merge_ready_i[1][4]),
    .credit_upd                     (credit_upd[1][4])
);


network_interface #(
    .isCaster                       (isCaster_1_5),
    .stream_id                      (stream_id_1_5)
)ni_1_5(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[1][5]),
    .data_i_cast_nw                 (data_o_cast_nw[1][5]),
    .ready_o_cast_nw                (ready_i_cast_nw[1][5]),
    .valid_o_cast_nw                (valid_i_cast_nw[1][5]),
    .data_o_cast_nw                 (data_i_cast_nw[1][5]),
    .ready_i_cast_nw                (ready_o_cast_nw[1][5]),
    .valid_i_merge_nw               (valid_o_merge_nw[1][5]),
    .data_i_merge_nw                (data_o_merge_nw[1][5]),
    .ready_o_merge_nw               (ready_i_merge_nw[1][5]),
    .valid_o_merge_nw               (valid_i_merge_nw[1][5]),
    .data_o_merge_nw                (data_i_merge_nw[1][5]),
    .ready_i_merge_nw               (ready_o_merge_nw[1][5]),
    .valid_i_cast_pe                (cast_valid_i[1][5]),
    .data_i_cast_pe                 (cast_data_i[1][5]),
    .ready_o_cast_pe                (cast_ready_o[1][5]),
    .valid_o_cast_pe                (cast_valid_o[1][5]),
    .data_o_cast_pe                 (cast_data_o[1][5]),
    .ready_i_cast_pe                (cast_ready_i[1][5]),
    .valid_i_merge_pe               (merge_valid_i[1][5]),
    .data_i_merge_pe                (merge_data_i[1][5]),
    .ready_o_merge_pe               (merge_ready_o[1][5]),
    .valid_o_merge_pe               (merge_valid_o[1][5]),
    .data_o_merge_pe                (merge_data_o[1][5]),
    .ready_i_merge_pe               (merge_ready_i[1][5]),
    .credit_upd                     (credit_upd[1][5])
);


network_interface #(
    .isCaster                       (isCaster_1_6),
    .stream_id                      (stream_id_1_6)
)ni_1_6(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[1][6]),
    .data_i_cast_nw                 (data_o_cast_nw[1][6]),
    .ready_o_cast_nw                (ready_i_cast_nw[1][6]),
    .valid_o_cast_nw                (valid_i_cast_nw[1][6]),
    .data_o_cast_nw                 (data_i_cast_nw[1][6]),
    .ready_i_cast_nw                (ready_o_cast_nw[1][6]),
    .valid_i_merge_nw               (valid_o_merge_nw[1][6]),
    .data_i_merge_nw                (data_o_merge_nw[1][6]),
    .ready_o_merge_nw               (ready_i_merge_nw[1][6]),
    .valid_o_merge_nw               (valid_i_merge_nw[1][6]),
    .data_o_merge_nw                (data_i_merge_nw[1][6]),
    .ready_i_merge_nw               (ready_o_merge_nw[1][6]),
    .valid_i_cast_pe                (cast_valid_i[1][6]),
    .data_i_cast_pe                 (cast_data_i[1][6]),
    .ready_o_cast_pe                (cast_ready_o[1][6]),
    .valid_o_cast_pe                (cast_valid_o[1][6]),
    .data_o_cast_pe                 (cast_data_o[1][6]),
    .ready_i_cast_pe                (cast_ready_i[1][6]),
    .valid_i_merge_pe               (merge_valid_i[1][6]),
    .data_i_merge_pe                (merge_data_i[1][6]),
    .ready_o_merge_pe               (merge_ready_o[1][6]),
    .valid_o_merge_pe               (merge_valid_o[1][6]),
    .data_o_merge_pe                (merge_data_o[1][6]),
    .ready_i_merge_pe               (merge_ready_i[1][6]),
    .credit_upd                     (credit_upd[1][6])
);


network_interface #(
    .isCaster                       (isCaster_1_7),
    .stream_id                      (stream_id_1_7)
)ni_1_7(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[1][7]),
    .data_i_cast_nw                 (data_o_cast_nw[1][7]),
    .ready_o_cast_nw                (ready_i_cast_nw[1][7]),
    .valid_o_cast_nw                (valid_i_cast_nw[1][7]),
    .data_o_cast_nw                 (data_i_cast_nw[1][7]),
    .ready_i_cast_nw                (ready_o_cast_nw[1][7]),
    .valid_i_merge_nw               (valid_o_merge_nw[1][7]),
    .data_i_merge_nw                (data_o_merge_nw[1][7]),
    .ready_o_merge_nw               (ready_i_merge_nw[1][7]),
    .valid_o_merge_nw               (valid_i_merge_nw[1][7]),
    .data_o_merge_nw                (data_i_merge_nw[1][7]),
    .ready_i_merge_nw               (ready_o_merge_nw[1][7]),
    .valid_i_cast_pe                (cast_valid_i[1][7]),
    .data_i_cast_pe                 (cast_data_i[1][7]),
    .ready_o_cast_pe                (cast_ready_o[1][7]),
    .valid_o_cast_pe                (cast_valid_o[1][7]),
    .data_o_cast_pe                 (cast_data_o[1][7]),
    .ready_i_cast_pe                (cast_ready_i[1][7]),
    .valid_i_merge_pe               (merge_valid_i[1][7]),
    .data_i_merge_pe                (merge_data_i[1][7]),
    .ready_o_merge_pe               (merge_ready_o[1][7]),
    .valid_o_merge_pe               (merge_valid_o[1][7]),
    .data_o_merge_pe                (merge_data_o[1][7]),
    .ready_i_merge_pe               (merge_ready_i[1][7]),
    .credit_upd                     (credit_upd[1][7])
);


network_interface #(
    .isCaster                       (isCaster_1_8),
    .stream_id                      (stream_id_1_8)
)ni_1_8(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[1][8]),
    .data_i_cast_nw                 (data_o_cast_nw[1][8]),
    .ready_o_cast_nw                (ready_i_cast_nw[1][8]),
    .valid_o_cast_nw                (valid_i_cast_nw[1][8]),
    .data_o_cast_nw                 (data_i_cast_nw[1][8]),
    .ready_i_cast_nw                (ready_o_cast_nw[1][8]),
    .valid_i_merge_nw               (valid_o_merge_nw[1][8]),
    .data_i_merge_nw                (data_o_merge_nw[1][8]),
    .ready_o_merge_nw               (ready_i_merge_nw[1][8]),
    .valid_o_merge_nw               (valid_i_merge_nw[1][8]),
    .data_o_merge_nw                (data_i_merge_nw[1][8]),
    .ready_i_merge_nw               (ready_o_merge_nw[1][8]),
    .valid_i_cast_pe                (cast_valid_i[1][8]),
    .data_i_cast_pe                 (cast_data_i[1][8]),
    .ready_o_cast_pe                (cast_ready_o[1][8]),
    .valid_o_cast_pe                (cast_valid_o[1][8]),
    .data_o_cast_pe                 (cast_data_o[1][8]),
    .ready_i_cast_pe                (cast_ready_i[1][8]),
    .valid_i_merge_pe               (merge_valid_i[1][8]),
    .data_i_merge_pe                (merge_data_i[1][8]),
    .ready_o_merge_pe               (merge_ready_o[1][8]),
    .valid_o_merge_pe               (merge_valid_o[1][8]),
    .data_o_merge_pe                (merge_data_o[1][8]),
    .ready_i_merge_pe               (merge_ready_i[1][8]),
    .credit_upd                     (credit_upd[1][8])
);


network_interface #(
    .isCaster                       (isCaster_1_9),
    .stream_id                      (stream_id_1_9)
)ni_1_9(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[1][9]),
    .data_i_cast_nw                 (data_o_cast_nw[1][9]),
    .ready_o_cast_nw                (ready_i_cast_nw[1][9]),
    .valid_o_cast_nw                (valid_i_cast_nw[1][9]),
    .data_o_cast_nw                 (data_i_cast_nw[1][9]),
    .ready_i_cast_nw                (ready_o_cast_nw[1][9]),
    .valid_i_merge_nw               (valid_o_merge_nw[1][9]),
    .data_i_merge_nw                (data_o_merge_nw[1][9]),
    .ready_o_merge_nw               (ready_i_merge_nw[1][9]),
    .valid_o_merge_nw               (valid_i_merge_nw[1][9]),
    .data_o_merge_nw                (data_i_merge_nw[1][9]),
    .ready_i_merge_nw               (ready_o_merge_nw[1][9]),
    .valid_i_cast_pe                (cast_valid_i[1][9]),
    .data_i_cast_pe                 (cast_data_i[1][9]),
    .ready_o_cast_pe                (cast_ready_o[1][9]),
    .valid_o_cast_pe                (cast_valid_o[1][9]),
    .data_o_cast_pe                 (cast_data_o[1][9]),
    .ready_i_cast_pe                (cast_ready_i[1][9]),
    .valid_i_merge_pe               (merge_valid_i[1][9]),
    .data_i_merge_pe                (merge_data_i[1][9]),
    .ready_o_merge_pe               (merge_ready_o[1][9]),
    .valid_o_merge_pe               (merge_valid_o[1][9]),
    .data_o_merge_pe                (merge_data_o[1][9]),
    .ready_i_merge_pe               (merge_ready_i[1][9]),
    .credit_upd                     (credit_upd[1][9])
);


network_interface #(
    .isCaster                       (isCaster_1_10),
    .stream_id                      (stream_id_1_10)
)ni_1_10(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[1][10]),
    .data_i_cast_nw                 (data_o_cast_nw[1][10]),
    .ready_o_cast_nw                (ready_i_cast_nw[1][10]),
    .valid_o_cast_nw                (valid_i_cast_nw[1][10]),
    .data_o_cast_nw                 (data_i_cast_nw[1][10]),
    .ready_i_cast_nw                (ready_o_cast_nw[1][10]),
    .valid_i_merge_nw               (valid_o_merge_nw[1][10]),
    .data_i_merge_nw                (data_o_merge_nw[1][10]),
    .ready_o_merge_nw               (ready_i_merge_nw[1][10]),
    .valid_o_merge_nw               (valid_i_merge_nw[1][10]),
    .data_o_merge_nw                (data_i_merge_nw[1][10]),
    .ready_i_merge_nw               (ready_o_merge_nw[1][10]),
    .valid_i_cast_pe                (cast_valid_i[1][10]),
    .data_i_cast_pe                 (cast_data_i[1][10]),
    .ready_o_cast_pe                (cast_ready_o[1][10]),
    .valid_o_cast_pe                (cast_valid_o[1][10]),
    .data_o_cast_pe                 (cast_data_o[1][10]),
    .ready_i_cast_pe                (cast_ready_i[1][10]),
    .valid_i_merge_pe               (merge_valid_i[1][10]),
    .data_i_merge_pe                (merge_data_i[1][10]),
    .ready_o_merge_pe               (merge_ready_o[1][10]),
    .valid_o_merge_pe               (merge_valid_o[1][10]),
    .data_o_merge_pe                (merge_data_o[1][10]),
    .ready_i_merge_pe               (merge_ready_i[1][10]),
    .credit_upd                     (credit_upd[1][10])
);


network_interface #(
    .isCaster                       (isCaster_2_0),
    .stream_id                      (stream_id_2_0)
)ni_2_0(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[2][0]),
    .data_i_cast_nw                 (data_o_cast_nw[2][0]),
    .ready_o_cast_nw                (ready_i_cast_nw[2][0]),
    .valid_o_cast_nw                (valid_i_cast_nw[2][0]),
    .data_o_cast_nw                 (data_i_cast_nw[2][0]),
    .ready_i_cast_nw                (ready_o_cast_nw[2][0]),
    .valid_i_merge_nw               (valid_o_merge_nw[2][0]),
    .data_i_merge_nw                (data_o_merge_nw[2][0]),
    .ready_o_merge_nw               (ready_i_merge_nw[2][0]),
    .valid_o_merge_nw               (valid_i_merge_nw[2][0]),
    .data_o_merge_nw                (data_i_merge_nw[2][0]),
    .ready_i_merge_nw               (ready_o_merge_nw[2][0]),
    .valid_i_cast_pe                (cast_valid_i[2][0]),
    .data_i_cast_pe                 (cast_data_i[2][0]),
    .ready_o_cast_pe                (cast_ready_o[2][0]),
    .valid_o_cast_pe                (cast_valid_o[2][0]),
    .data_o_cast_pe                 (cast_data_o[2][0]),
    .ready_i_cast_pe                (cast_ready_i[2][0]),
    .valid_i_merge_pe               (merge_valid_i[2][0]),
    .data_i_merge_pe                (merge_data_i[2][0]),
    .ready_o_merge_pe               (merge_ready_o[2][0]),
    .valid_o_merge_pe               (merge_valid_o[2][0]),
    .data_o_merge_pe                (merge_data_o[2][0]),
    .ready_i_merge_pe               (merge_ready_i[2][0]),
    .credit_upd                     (credit_upd[2][0])
);


network_interface #(
    .isCaster                       (isCaster_2_1),
    .stream_id                      (stream_id_2_1)
)ni_2_1(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[2][1]),
    .data_i_cast_nw                 (data_o_cast_nw[2][1]),
    .ready_o_cast_nw                (ready_i_cast_nw[2][1]),
    .valid_o_cast_nw                (valid_i_cast_nw[2][1]),
    .data_o_cast_nw                 (data_i_cast_nw[2][1]),
    .ready_i_cast_nw                (ready_o_cast_nw[2][1]),
    .valid_i_merge_nw               (valid_o_merge_nw[2][1]),
    .data_i_merge_nw                (data_o_merge_nw[2][1]),
    .ready_o_merge_nw               (ready_i_merge_nw[2][1]),
    .valid_o_merge_nw               (valid_i_merge_nw[2][1]),
    .data_o_merge_nw                (data_i_merge_nw[2][1]),
    .ready_i_merge_nw               (ready_o_merge_nw[2][1]),
    .valid_i_cast_pe                (cast_valid_i[2][1]),
    .data_i_cast_pe                 (cast_data_i[2][1]),
    .ready_o_cast_pe                (cast_ready_o[2][1]),
    .valid_o_cast_pe                (cast_valid_o[2][1]),
    .data_o_cast_pe                 (cast_data_o[2][1]),
    .ready_i_cast_pe                (cast_ready_i[2][1]),
    .valid_i_merge_pe               (merge_valid_i[2][1]),
    .data_i_merge_pe                (merge_data_i[2][1]),
    .ready_o_merge_pe               (merge_ready_o[2][1]),
    .valid_o_merge_pe               (merge_valid_o[2][1]),
    .data_o_merge_pe                (merge_data_o[2][1]),
    .ready_i_merge_pe               (merge_ready_i[2][1]),
    .credit_upd                     (credit_upd[2][1])
);


network_interface #(
    .isCaster                       (isCaster_2_2),
    .stream_id                      (stream_id_2_2)
)ni_2_2(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[2][2]),
    .data_i_cast_nw                 (data_o_cast_nw[2][2]),
    .ready_o_cast_nw                (ready_i_cast_nw[2][2]),
    .valid_o_cast_nw                (valid_i_cast_nw[2][2]),
    .data_o_cast_nw                 (data_i_cast_nw[2][2]),
    .ready_i_cast_nw                (ready_o_cast_nw[2][2]),
    .valid_i_merge_nw               (valid_o_merge_nw[2][2]),
    .data_i_merge_nw                (data_o_merge_nw[2][2]),
    .ready_o_merge_nw               (ready_i_merge_nw[2][2]),
    .valid_o_merge_nw               (valid_i_merge_nw[2][2]),
    .data_o_merge_nw                (data_i_merge_nw[2][2]),
    .ready_i_merge_nw               (ready_o_merge_nw[2][2]),
    .valid_i_cast_pe                (cast_valid_i[2][2]),
    .data_i_cast_pe                 (cast_data_i[2][2]),
    .ready_o_cast_pe                (cast_ready_o[2][2]),
    .valid_o_cast_pe                (cast_valid_o[2][2]),
    .data_o_cast_pe                 (cast_data_o[2][2]),
    .ready_i_cast_pe                (cast_ready_i[2][2]),
    .valid_i_merge_pe               (merge_valid_i[2][2]),
    .data_i_merge_pe                (merge_data_i[2][2]),
    .ready_o_merge_pe               (merge_ready_o[2][2]),
    .valid_o_merge_pe               (merge_valid_o[2][2]),
    .data_o_merge_pe                (merge_data_o[2][2]),
    .ready_i_merge_pe               (merge_ready_i[2][2]),
    .credit_upd                     (credit_upd[2][2])
);


network_interface #(
    .isCaster                       (isCaster_2_3),
    .stream_id                      (stream_id_2_3)
)ni_2_3(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[2][3]),
    .data_i_cast_nw                 (data_o_cast_nw[2][3]),
    .ready_o_cast_nw                (ready_i_cast_nw[2][3]),
    .valid_o_cast_nw                (valid_i_cast_nw[2][3]),
    .data_o_cast_nw                 (data_i_cast_nw[2][3]),
    .ready_i_cast_nw                (ready_o_cast_nw[2][3]),
    .valid_i_merge_nw               (valid_o_merge_nw[2][3]),
    .data_i_merge_nw                (data_o_merge_nw[2][3]),
    .ready_o_merge_nw               (ready_i_merge_nw[2][3]),
    .valid_o_merge_nw               (valid_i_merge_nw[2][3]),
    .data_o_merge_nw                (data_i_merge_nw[2][3]),
    .ready_i_merge_nw               (ready_o_merge_nw[2][3]),
    .valid_i_cast_pe                (cast_valid_i[2][3]),
    .data_i_cast_pe                 (cast_data_i[2][3]),
    .ready_o_cast_pe                (cast_ready_o[2][3]),
    .valid_o_cast_pe                (cast_valid_o[2][3]),
    .data_o_cast_pe                 (cast_data_o[2][3]),
    .ready_i_cast_pe                (cast_ready_i[2][3]),
    .valid_i_merge_pe               (merge_valid_i[2][3]),
    .data_i_merge_pe                (merge_data_i[2][3]),
    .ready_o_merge_pe               (merge_ready_o[2][3]),
    .valid_o_merge_pe               (merge_valid_o[2][3]),
    .data_o_merge_pe                (merge_data_o[2][3]),
    .ready_i_merge_pe               (merge_ready_i[2][3]),
    .credit_upd                     (credit_upd[2][3])
);


network_interface #(
    .isCaster                       (isCaster_2_4),
    .stream_id                      (stream_id_2_4)
)ni_2_4(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[2][4]),
    .data_i_cast_nw                 (data_o_cast_nw[2][4]),
    .ready_o_cast_nw                (ready_i_cast_nw[2][4]),
    .valid_o_cast_nw                (valid_i_cast_nw[2][4]),
    .data_o_cast_nw                 (data_i_cast_nw[2][4]),
    .ready_i_cast_nw                (ready_o_cast_nw[2][4]),
    .valid_i_merge_nw               (valid_o_merge_nw[2][4]),
    .data_i_merge_nw                (data_o_merge_nw[2][4]),
    .ready_o_merge_nw               (ready_i_merge_nw[2][4]),
    .valid_o_merge_nw               (valid_i_merge_nw[2][4]),
    .data_o_merge_nw                (data_i_merge_nw[2][4]),
    .ready_i_merge_nw               (ready_o_merge_nw[2][4]),
    .valid_i_cast_pe                (cast_valid_i[2][4]),
    .data_i_cast_pe                 (cast_data_i[2][4]),
    .ready_o_cast_pe                (cast_ready_o[2][4]),
    .valid_o_cast_pe                (cast_valid_o[2][4]),
    .data_o_cast_pe                 (cast_data_o[2][4]),
    .ready_i_cast_pe                (cast_ready_i[2][4]),
    .valid_i_merge_pe               (merge_valid_i[2][4]),
    .data_i_merge_pe                (merge_data_i[2][4]),
    .ready_o_merge_pe               (merge_ready_o[2][4]),
    .valid_o_merge_pe               (merge_valid_o[2][4]),
    .data_o_merge_pe                (merge_data_o[2][4]),
    .ready_i_merge_pe               (merge_ready_i[2][4]),
    .credit_upd                     (credit_upd[2][4])
);


network_interface #(
    .isCaster                       (isCaster_2_5),
    .stream_id                      (stream_id_2_5)
)ni_2_5(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[2][5]),
    .data_i_cast_nw                 (data_o_cast_nw[2][5]),
    .ready_o_cast_nw                (ready_i_cast_nw[2][5]),
    .valid_o_cast_nw                (valid_i_cast_nw[2][5]),
    .data_o_cast_nw                 (data_i_cast_nw[2][5]),
    .ready_i_cast_nw                (ready_o_cast_nw[2][5]),
    .valid_i_merge_nw               (valid_o_merge_nw[2][5]),
    .data_i_merge_nw                (data_o_merge_nw[2][5]),
    .ready_o_merge_nw               (ready_i_merge_nw[2][5]),
    .valid_o_merge_nw               (valid_i_merge_nw[2][5]),
    .data_o_merge_nw                (data_i_merge_nw[2][5]),
    .ready_i_merge_nw               (ready_o_merge_nw[2][5]),
    .valid_i_cast_pe                (cast_valid_i[2][5]),
    .data_i_cast_pe                 (cast_data_i[2][5]),
    .ready_o_cast_pe                (cast_ready_o[2][5]),
    .valid_o_cast_pe                (cast_valid_o[2][5]),
    .data_o_cast_pe                 (cast_data_o[2][5]),
    .ready_i_cast_pe                (cast_ready_i[2][5]),
    .valid_i_merge_pe               (merge_valid_i[2][5]),
    .data_i_merge_pe                (merge_data_i[2][5]),
    .ready_o_merge_pe               (merge_ready_o[2][5]),
    .valid_o_merge_pe               (merge_valid_o[2][5]),
    .data_o_merge_pe                (merge_data_o[2][5]),
    .ready_i_merge_pe               (merge_ready_i[2][5]),
    .credit_upd                     (credit_upd[2][5])
);


network_interface #(
    .isCaster                       (isCaster_2_6),
    .stream_id                      (stream_id_2_6)
)ni_2_6(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[2][6]),
    .data_i_cast_nw                 (data_o_cast_nw[2][6]),
    .ready_o_cast_nw                (ready_i_cast_nw[2][6]),
    .valid_o_cast_nw                (valid_i_cast_nw[2][6]),
    .data_o_cast_nw                 (data_i_cast_nw[2][6]),
    .ready_i_cast_nw                (ready_o_cast_nw[2][6]),
    .valid_i_merge_nw               (valid_o_merge_nw[2][6]),
    .data_i_merge_nw                (data_o_merge_nw[2][6]),
    .ready_o_merge_nw               (ready_i_merge_nw[2][6]),
    .valid_o_merge_nw               (valid_i_merge_nw[2][6]),
    .data_o_merge_nw                (data_i_merge_nw[2][6]),
    .ready_i_merge_nw               (ready_o_merge_nw[2][6]),
    .valid_i_cast_pe                (cast_valid_i[2][6]),
    .data_i_cast_pe                 (cast_data_i[2][6]),
    .ready_o_cast_pe                (cast_ready_o[2][6]),
    .valid_o_cast_pe                (cast_valid_o[2][6]),
    .data_o_cast_pe                 (cast_data_o[2][6]),
    .ready_i_cast_pe                (cast_ready_i[2][6]),
    .valid_i_merge_pe               (merge_valid_i[2][6]),
    .data_i_merge_pe                (merge_data_i[2][6]),
    .ready_o_merge_pe               (merge_ready_o[2][6]),
    .valid_o_merge_pe               (merge_valid_o[2][6]),
    .data_o_merge_pe                (merge_data_o[2][6]),
    .ready_i_merge_pe               (merge_ready_i[2][6]),
    .credit_upd                     (credit_upd[2][6])
);


network_interface #(
    .isCaster                       (isCaster_2_7),
    .stream_id                      (stream_id_2_7)
)ni_2_7(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[2][7]),
    .data_i_cast_nw                 (data_o_cast_nw[2][7]),
    .ready_o_cast_nw                (ready_i_cast_nw[2][7]),
    .valid_o_cast_nw                (valid_i_cast_nw[2][7]),
    .data_o_cast_nw                 (data_i_cast_nw[2][7]),
    .ready_i_cast_nw                (ready_o_cast_nw[2][7]),
    .valid_i_merge_nw               (valid_o_merge_nw[2][7]),
    .data_i_merge_nw                (data_o_merge_nw[2][7]),
    .ready_o_merge_nw               (ready_i_merge_nw[2][7]),
    .valid_o_merge_nw               (valid_i_merge_nw[2][7]),
    .data_o_merge_nw                (data_i_merge_nw[2][7]),
    .ready_i_merge_nw               (ready_o_merge_nw[2][7]),
    .valid_i_cast_pe                (cast_valid_i[2][7]),
    .data_i_cast_pe                 (cast_data_i[2][7]),
    .ready_o_cast_pe                (cast_ready_o[2][7]),
    .valid_o_cast_pe                (cast_valid_o[2][7]),
    .data_o_cast_pe                 (cast_data_o[2][7]),
    .ready_i_cast_pe                (cast_ready_i[2][7]),
    .valid_i_merge_pe               (merge_valid_i[2][7]),
    .data_i_merge_pe                (merge_data_i[2][7]),
    .ready_o_merge_pe               (merge_ready_o[2][7]),
    .valid_o_merge_pe               (merge_valid_o[2][7]),
    .data_o_merge_pe                (merge_data_o[2][7]),
    .ready_i_merge_pe               (merge_ready_i[2][7]),
    .credit_upd                     (credit_upd[2][7])
);


network_interface #(
    .isCaster                       (isCaster_2_8),
    .stream_id                      (stream_id_2_8)
)ni_2_8(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[2][8]),
    .data_i_cast_nw                 (data_o_cast_nw[2][8]),
    .ready_o_cast_nw                (ready_i_cast_nw[2][8]),
    .valid_o_cast_nw                (valid_i_cast_nw[2][8]),
    .data_o_cast_nw                 (data_i_cast_nw[2][8]),
    .ready_i_cast_nw                (ready_o_cast_nw[2][8]),
    .valid_i_merge_nw               (valid_o_merge_nw[2][8]),
    .data_i_merge_nw                (data_o_merge_nw[2][8]),
    .ready_o_merge_nw               (ready_i_merge_nw[2][8]),
    .valid_o_merge_nw               (valid_i_merge_nw[2][8]),
    .data_o_merge_nw                (data_i_merge_nw[2][8]),
    .ready_i_merge_nw               (ready_o_merge_nw[2][8]),
    .valid_i_cast_pe                (cast_valid_i[2][8]),
    .data_i_cast_pe                 (cast_data_i[2][8]),
    .ready_o_cast_pe                (cast_ready_o[2][8]),
    .valid_o_cast_pe                (cast_valid_o[2][8]),
    .data_o_cast_pe                 (cast_data_o[2][8]),
    .ready_i_cast_pe                (cast_ready_i[2][8]),
    .valid_i_merge_pe               (merge_valid_i[2][8]),
    .data_i_merge_pe                (merge_data_i[2][8]),
    .ready_o_merge_pe               (merge_ready_o[2][8]),
    .valid_o_merge_pe               (merge_valid_o[2][8]),
    .data_o_merge_pe                (merge_data_o[2][8]),
    .ready_i_merge_pe               (merge_ready_i[2][8]),
    .credit_upd                     (credit_upd[2][8])
);


network_interface #(
    .isCaster                       (isCaster_2_9),
    .stream_id                      (stream_id_2_9)
)ni_2_9(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[2][9]),
    .data_i_cast_nw                 (data_o_cast_nw[2][9]),
    .ready_o_cast_nw                (ready_i_cast_nw[2][9]),
    .valid_o_cast_nw                (valid_i_cast_nw[2][9]),
    .data_o_cast_nw                 (data_i_cast_nw[2][9]),
    .ready_i_cast_nw                (ready_o_cast_nw[2][9]),
    .valid_i_merge_nw               (valid_o_merge_nw[2][9]),
    .data_i_merge_nw                (data_o_merge_nw[2][9]),
    .ready_o_merge_nw               (ready_i_merge_nw[2][9]),
    .valid_o_merge_nw               (valid_i_merge_nw[2][9]),
    .data_o_merge_nw                (data_i_merge_nw[2][9]),
    .ready_i_merge_nw               (ready_o_merge_nw[2][9]),
    .valid_i_cast_pe                (cast_valid_i[2][9]),
    .data_i_cast_pe                 (cast_data_i[2][9]),
    .ready_o_cast_pe                (cast_ready_o[2][9]),
    .valid_o_cast_pe                (cast_valid_o[2][9]),
    .data_o_cast_pe                 (cast_data_o[2][9]),
    .ready_i_cast_pe                (cast_ready_i[2][9]),
    .valid_i_merge_pe               (merge_valid_i[2][9]),
    .data_i_merge_pe                (merge_data_i[2][9]),
    .ready_o_merge_pe               (merge_ready_o[2][9]),
    .valid_o_merge_pe               (merge_valid_o[2][9]),
    .data_o_merge_pe                (merge_data_o[2][9]),
    .ready_i_merge_pe               (merge_ready_i[2][9]),
    .credit_upd                     (credit_upd[2][9])
);


network_interface #(
    .isCaster                       (isCaster_2_10),
    .stream_id                      (stream_id_2_10)
)ni_2_10(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[2][10]),
    .data_i_cast_nw                 (data_o_cast_nw[2][10]),
    .ready_o_cast_nw                (ready_i_cast_nw[2][10]),
    .valid_o_cast_nw                (valid_i_cast_nw[2][10]),
    .data_o_cast_nw                 (data_i_cast_nw[2][10]),
    .ready_i_cast_nw                (ready_o_cast_nw[2][10]),
    .valid_i_merge_nw               (valid_o_merge_nw[2][10]),
    .data_i_merge_nw                (data_o_merge_nw[2][10]),
    .ready_o_merge_nw               (ready_i_merge_nw[2][10]),
    .valid_o_merge_nw               (valid_i_merge_nw[2][10]),
    .data_o_merge_nw                (data_i_merge_nw[2][10]),
    .ready_i_merge_nw               (ready_o_merge_nw[2][10]),
    .valid_i_cast_pe                (cast_valid_i[2][10]),
    .data_i_cast_pe                 (cast_data_i[2][10]),
    .ready_o_cast_pe                (cast_ready_o[2][10]),
    .valid_o_cast_pe                (cast_valid_o[2][10]),
    .data_o_cast_pe                 (cast_data_o[2][10]),
    .ready_i_cast_pe                (cast_ready_i[2][10]),
    .valid_i_merge_pe               (merge_valid_i[2][10]),
    .data_i_merge_pe                (merge_data_i[2][10]),
    .ready_o_merge_pe               (merge_ready_o[2][10]),
    .valid_o_merge_pe               (merge_valid_o[2][10]),
    .data_o_merge_pe                (merge_data_o[2][10]),
    .ready_i_merge_pe               (merge_ready_i[2][10]),
    .credit_upd                     (credit_upd[2][10])
);


network_interface #(
    .isCaster                       (isCaster_3_0),
    .stream_id                      (stream_id_3_0)
)ni_3_0(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[3][0]),
    .data_i_cast_nw                 (data_o_cast_nw[3][0]),
    .ready_o_cast_nw                (ready_i_cast_nw[3][0]),
    .valid_o_cast_nw                (valid_i_cast_nw[3][0]),
    .data_o_cast_nw                 (data_i_cast_nw[3][0]),
    .ready_i_cast_nw                (ready_o_cast_nw[3][0]),
    .valid_i_merge_nw               (valid_o_merge_nw[3][0]),
    .data_i_merge_nw                (data_o_merge_nw[3][0]),
    .ready_o_merge_nw               (ready_i_merge_nw[3][0]),
    .valid_o_merge_nw               (valid_i_merge_nw[3][0]),
    .data_o_merge_nw                (data_i_merge_nw[3][0]),
    .ready_i_merge_nw               (ready_o_merge_nw[3][0]),
    .valid_i_cast_pe                (cast_valid_i[3][0]),
    .data_i_cast_pe                 (cast_data_i[3][0]),
    .ready_o_cast_pe                (cast_ready_o[3][0]),
    .valid_o_cast_pe                (cast_valid_o[3][0]),
    .data_o_cast_pe                 (cast_data_o[3][0]),
    .ready_i_cast_pe                (cast_ready_i[3][0]),
    .valid_i_merge_pe               (merge_valid_i[3][0]),
    .data_i_merge_pe                (merge_data_i[3][0]),
    .ready_o_merge_pe               (merge_ready_o[3][0]),
    .valid_o_merge_pe               (merge_valid_o[3][0]),
    .data_o_merge_pe                (merge_data_o[3][0]),
    .ready_i_merge_pe               (merge_ready_i[3][0]),
    .credit_upd                     (credit_upd[3][0])
);


network_interface #(
    .isCaster                       (isCaster_3_1),
    .stream_id                      (stream_id_3_1)
)ni_3_1(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[3][1]),
    .data_i_cast_nw                 (data_o_cast_nw[3][1]),
    .ready_o_cast_nw                (ready_i_cast_nw[3][1]),
    .valid_o_cast_nw                (valid_i_cast_nw[3][1]),
    .data_o_cast_nw                 (data_i_cast_nw[3][1]),
    .ready_i_cast_nw                (ready_o_cast_nw[3][1]),
    .valid_i_merge_nw               (valid_o_merge_nw[3][1]),
    .data_i_merge_nw                (data_o_merge_nw[3][1]),
    .ready_o_merge_nw               (ready_i_merge_nw[3][1]),
    .valid_o_merge_nw               (valid_i_merge_nw[3][1]),
    .data_o_merge_nw                (data_i_merge_nw[3][1]),
    .ready_i_merge_nw               (ready_o_merge_nw[3][1]),
    .valid_i_cast_pe                (cast_valid_i[3][1]),
    .data_i_cast_pe                 (cast_data_i[3][1]),
    .ready_o_cast_pe                (cast_ready_o[3][1]),
    .valid_o_cast_pe                (cast_valid_o[3][1]),
    .data_o_cast_pe                 (cast_data_o[3][1]),
    .ready_i_cast_pe                (cast_ready_i[3][1]),
    .valid_i_merge_pe               (merge_valid_i[3][1]),
    .data_i_merge_pe                (merge_data_i[3][1]),
    .ready_o_merge_pe               (merge_ready_o[3][1]),
    .valid_o_merge_pe               (merge_valid_o[3][1]),
    .data_o_merge_pe                (merge_data_o[3][1]),
    .ready_i_merge_pe               (merge_ready_i[3][1]),
    .credit_upd                     (credit_upd[3][1])
);


network_interface #(
    .isCaster                       (isCaster_3_2),
    .stream_id                      (stream_id_3_2)
)ni_3_2(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[3][2]),
    .data_i_cast_nw                 (data_o_cast_nw[3][2]),
    .ready_o_cast_nw                (ready_i_cast_nw[3][2]),
    .valid_o_cast_nw                (valid_i_cast_nw[3][2]),
    .data_o_cast_nw                 (data_i_cast_nw[3][2]),
    .ready_i_cast_nw                (ready_o_cast_nw[3][2]),
    .valid_i_merge_nw               (valid_o_merge_nw[3][2]),
    .data_i_merge_nw                (data_o_merge_nw[3][2]),
    .ready_o_merge_nw               (ready_i_merge_nw[3][2]),
    .valid_o_merge_nw               (valid_i_merge_nw[3][2]),
    .data_o_merge_nw                (data_i_merge_nw[3][2]),
    .ready_i_merge_nw               (ready_o_merge_nw[3][2]),
    .valid_i_cast_pe                (cast_valid_i[3][2]),
    .data_i_cast_pe                 (cast_data_i[3][2]),
    .ready_o_cast_pe                (cast_ready_o[3][2]),
    .valid_o_cast_pe                (cast_valid_o[3][2]),
    .data_o_cast_pe                 (cast_data_o[3][2]),
    .ready_i_cast_pe                (cast_ready_i[3][2]),
    .valid_i_merge_pe               (merge_valid_i[3][2]),
    .data_i_merge_pe                (merge_data_i[3][2]),
    .ready_o_merge_pe               (merge_ready_o[3][2]),
    .valid_o_merge_pe               (merge_valid_o[3][2]),
    .data_o_merge_pe                (merge_data_o[3][2]),
    .ready_i_merge_pe               (merge_ready_i[3][2]),
    .credit_upd                     (credit_upd[3][2])
);


network_interface #(
    .isCaster                       (isCaster_3_3),
    .stream_id                      (stream_id_3_3)
)ni_3_3(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[3][3]),
    .data_i_cast_nw                 (data_o_cast_nw[3][3]),
    .ready_o_cast_nw                (ready_i_cast_nw[3][3]),
    .valid_o_cast_nw                (valid_i_cast_nw[3][3]),
    .data_o_cast_nw                 (data_i_cast_nw[3][3]),
    .ready_i_cast_nw                (ready_o_cast_nw[3][3]),
    .valid_i_merge_nw               (valid_o_merge_nw[3][3]),
    .data_i_merge_nw                (data_o_merge_nw[3][3]),
    .ready_o_merge_nw               (ready_i_merge_nw[3][3]),
    .valid_o_merge_nw               (valid_i_merge_nw[3][3]),
    .data_o_merge_nw                (data_i_merge_nw[3][3]),
    .ready_i_merge_nw               (ready_o_merge_nw[3][3]),
    .valid_i_cast_pe                (cast_valid_i[3][3]),
    .data_i_cast_pe                 (cast_data_i[3][3]),
    .ready_o_cast_pe                (cast_ready_o[3][3]),
    .valid_o_cast_pe                (cast_valid_o[3][3]),
    .data_o_cast_pe                 (cast_data_o[3][3]),
    .ready_i_cast_pe                (cast_ready_i[3][3]),
    .valid_i_merge_pe               (merge_valid_i[3][3]),
    .data_i_merge_pe                (merge_data_i[3][3]),
    .ready_o_merge_pe               (merge_ready_o[3][3]),
    .valid_o_merge_pe               (merge_valid_o[3][3]),
    .data_o_merge_pe                (merge_data_o[3][3]),
    .ready_i_merge_pe               (merge_ready_i[3][3]),
    .credit_upd                     (credit_upd[3][3])
);


network_interface #(
    .isCaster                       (isCaster_3_4),
    .stream_id                      (stream_id_3_4)
)ni_3_4(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[3][4]),
    .data_i_cast_nw                 (data_o_cast_nw[3][4]),
    .ready_o_cast_nw                (ready_i_cast_nw[3][4]),
    .valid_o_cast_nw                (valid_i_cast_nw[3][4]),
    .data_o_cast_nw                 (data_i_cast_nw[3][4]),
    .ready_i_cast_nw                (ready_o_cast_nw[3][4]),
    .valid_i_merge_nw               (valid_o_merge_nw[3][4]),
    .data_i_merge_nw                (data_o_merge_nw[3][4]),
    .ready_o_merge_nw               (ready_i_merge_nw[3][4]),
    .valid_o_merge_nw               (valid_i_merge_nw[3][4]),
    .data_o_merge_nw                (data_i_merge_nw[3][4]),
    .ready_i_merge_nw               (ready_o_merge_nw[3][4]),
    .valid_i_cast_pe                (cast_valid_i[3][4]),
    .data_i_cast_pe                 (cast_data_i[3][4]),
    .ready_o_cast_pe                (cast_ready_o[3][4]),
    .valid_o_cast_pe                (cast_valid_o[3][4]),
    .data_o_cast_pe                 (cast_data_o[3][4]),
    .ready_i_cast_pe                (cast_ready_i[3][4]),
    .valid_i_merge_pe               (merge_valid_i[3][4]),
    .data_i_merge_pe                (merge_data_i[3][4]),
    .ready_o_merge_pe               (merge_ready_o[3][4]),
    .valid_o_merge_pe               (merge_valid_o[3][4]),
    .data_o_merge_pe                (merge_data_o[3][4]),
    .ready_i_merge_pe               (merge_ready_i[3][4]),
    .credit_upd                     (credit_upd[3][4])
);


network_interface #(
    .isCaster                       (isCaster_3_5),
    .stream_id                      (stream_id_3_5)
)ni_3_5(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[3][5]),
    .data_i_cast_nw                 (data_o_cast_nw[3][5]),
    .ready_o_cast_nw                (ready_i_cast_nw[3][5]),
    .valid_o_cast_nw                (valid_i_cast_nw[3][5]),
    .data_o_cast_nw                 (data_i_cast_nw[3][5]),
    .ready_i_cast_nw                (ready_o_cast_nw[3][5]),
    .valid_i_merge_nw               (valid_o_merge_nw[3][5]),
    .data_i_merge_nw                (data_o_merge_nw[3][5]),
    .ready_o_merge_nw               (ready_i_merge_nw[3][5]),
    .valid_o_merge_nw               (valid_i_merge_nw[3][5]),
    .data_o_merge_nw                (data_i_merge_nw[3][5]),
    .ready_i_merge_nw               (ready_o_merge_nw[3][5]),
    .valid_i_cast_pe                (cast_valid_i[3][5]),
    .data_i_cast_pe                 (cast_data_i[3][5]),
    .ready_o_cast_pe                (cast_ready_o[3][5]),
    .valid_o_cast_pe                (cast_valid_o[3][5]),
    .data_o_cast_pe                 (cast_data_o[3][5]),
    .ready_i_cast_pe                (cast_ready_i[3][5]),
    .valid_i_merge_pe               (merge_valid_i[3][5]),
    .data_i_merge_pe                (merge_data_i[3][5]),
    .ready_o_merge_pe               (merge_ready_o[3][5]),
    .valid_o_merge_pe               (merge_valid_o[3][5]),
    .data_o_merge_pe                (merge_data_o[3][5]),
    .ready_i_merge_pe               (merge_ready_i[3][5]),
    .credit_upd                     (credit_upd[3][5])
);


network_interface #(
    .isCaster                       (isCaster_3_6),
    .stream_id                      (stream_id_3_6)
)ni_3_6(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[3][6]),
    .data_i_cast_nw                 (data_o_cast_nw[3][6]),
    .ready_o_cast_nw                (ready_i_cast_nw[3][6]),
    .valid_o_cast_nw                (valid_i_cast_nw[3][6]),
    .data_o_cast_nw                 (data_i_cast_nw[3][6]),
    .ready_i_cast_nw                (ready_o_cast_nw[3][6]),
    .valid_i_merge_nw               (valid_o_merge_nw[3][6]),
    .data_i_merge_nw                (data_o_merge_nw[3][6]),
    .ready_o_merge_nw               (ready_i_merge_nw[3][6]),
    .valid_o_merge_nw               (valid_i_merge_nw[3][6]),
    .data_o_merge_nw                (data_i_merge_nw[3][6]),
    .ready_i_merge_nw               (ready_o_merge_nw[3][6]),
    .valid_i_cast_pe                (cast_valid_i[3][6]),
    .data_i_cast_pe                 (cast_data_i[3][6]),
    .ready_o_cast_pe                (cast_ready_o[3][6]),
    .valid_o_cast_pe                (cast_valid_o[3][6]),
    .data_o_cast_pe                 (cast_data_o[3][6]),
    .ready_i_cast_pe                (cast_ready_i[3][6]),
    .valid_i_merge_pe               (merge_valid_i[3][6]),
    .data_i_merge_pe                (merge_data_i[3][6]),
    .ready_o_merge_pe               (merge_ready_o[3][6]),
    .valid_o_merge_pe               (merge_valid_o[3][6]),
    .data_o_merge_pe                (merge_data_o[3][6]),
    .ready_i_merge_pe               (merge_ready_i[3][6]),
    .credit_upd                     (credit_upd[3][6])
);


network_interface #(
    .isCaster                       (isCaster_3_7),
    .stream_id                      (stream_id_3_7)
)ni_3_7(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[3][7]),
    .data_i_cast_nw                 (data_o_cast_nw[3][7]),
    .ready_o_cast_nw                (ready_i_cast_nw[3][7]),
    .valid_o_cast_nw                (valid_i_cast_nw[3][7]),
    .data_o_cast_nw                 (data_i_cast_nw[3][7]),
    .ready_i_cast_nw                (ready_o_cast_nw[3][7]),
    .valid_i_merge_nw               (valid_o_merge_nw[3][7]),
    .data_i_merge_nw                (data_o_merge_nw[3][7]),
    .ready_o_merge_nw               (ready_i_merge_nw[3][7]),
    .valid_o_merge_nw               (valid_i_merge_nw[3][7]),
    .data_o_merge_nw                (data_i_merge_nw[3][7]),
    .ready_i_merge_nw               (ready_o_merge_nw[3][7]),
    .valid_i_cast_pe                (cast_valid_i[3][7]),
    .data_i_cast_pe                 (cast_data_i[3][7]),
    .ready_o_cast_pe                (cast_ready_o[3][7]),
    .valid_o_cast_pe                (cast_valid_o[3][7]),
    .data_o_cast_pe                 (cast_data_o[3][7]),
    .ready_i_cast_pe                (cast_ready_i[3][7]),
    .valid_i_merge_pe               (merge_valid_i[3][7]),
    .data_i_merge_pe                (merge_data_i[3][7]),
    .ready_o_merge_pe               (merge_ready_o[3][7]),
    .valid_o_merge_pe               (merge_valid_o[3][7]),
    .data_o_merge_pe                (merge_data_o[3][7]),
    .ready_i_merge_pe               (merge_ready_i[3][7]),
    .credit_upd                     (credit_upd[3][7])
);


network_interface #(
    .isCaster                       (isCaster_3_8),
    .stream_id                      (stream_id_3_8)
)ni_3_8(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[3][8]),
    .data_i_cast_nw                 (data_o_cast_nw[3][8]),
    .ready_o_cast_nw                (ready_i_cast_nw[3][8]),
    .valid_o_cast_nw                (valid_i_cast_nw[3][8]),
    .data_o_cast_nw                 (data_i_cast_nw[3][8]),
    .ready_i_cast_nw                (ready_o_cast_nw[3][8]),
    .valid_i_merge_nw               (valid_o_merge_nw[3][8]),
    .data_i_merge_nw                (data_o_merge_nw[3][8]),
    .ready_o_merge_nw               (ready_i_merge_nw[3][8]),
    .valid_o_merge_nw               (valid_i_merge_nw[3][8]),
    .data_o_merge_nw                (data_i_merge_nw[3][8]),
    .ready_i_merge_nw               (ready_o_merge_nw[3][8]),
    .valid_i_cast_pe                (cast_valid_i[3][8]),
    .data_i_cast_pe                 (cast_data_i[3][8]),
    .ready_o_cast_pe                (cast_ready_o[3][8]),
    .valid_o_cast_pe                (cast_valid_o[3][8]),
    .data_o_cast_pe                 (cast_data_o[3][8]),
    .ready_i_cast_pe                (cast_ready_i[3][8]),
    .valid_i_merge_pe               (merge_valid_i[3][8]),
    .data_i_merge_pe                (merge_data_i[3][8]),
    .ready_o_merge_pe               (merge_ready_o[3][8]),
    .valid_o_merge_pe               (merge_valid_o[3][8]),
    .data_o_merge_pe                (merge_data_o[3][8]),
    .ready_i_merge_pe               (merge_ready_i[3][8]),
    .credit_upd                     (credit_upd[3][8])
);


network_interface #(
    .isCaster                       (isCaster_3_9),
    .stream_id                      (stream_id_3_9)
)ni_3_9(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[3][9]),
    .data_i_cast_nw                 (data_o_cast_nw[3][9]),
    .ready_o_cast_nw                (ready_i_cast_nw[3][9]),
    .valid_o_cast_nw                (valid_i_cast_nw[3][9]),
    .data_o_cast_nw                 (data_i_cast_nw[3][9]),
    .ready_i_cast_nw                (ready_o_cast_nw[3][9]),
    .valid_i_merge_nw               (valid_o_merge_nw[3][9]),
    .data_i_merge_nw                (data_o_merge_nw[3][9]),
    .ready_o_merge_nw               (ready_i_merge_nw[3][9]),
    .valid_o_merge_nw               (valid_i_merge_nw[3][9]),
    .data_o_merge_nw                (data_i_merge_nw[3][9]),
    .ready_i_merge_nw               (ready_o_merge_nw[3][9]),
    .valid_i_cast_pe                (cast_valid_i[3][9]),
    .data_i_cast_pe                 (cast_data_i[3][9]),
    .ready_o_cast_pe                (cast_ready_o[3][9]),
    .valid_o_cast_pe                (cast_valid_o[3][9]),
    .data_o_cast_pe                 (cast_data_o[3][9]),
    .ready_i_cast_pe                (cast_ready_i[3][9]),
    .valid_i_merge_pe               (merge_valid_i[3][9]),
    .data_i_merge_pe                (merge_data_i[3][9]),
    .ready_o_merge_pe               (merge_ready_o[3][9]),
    .valid_o_merge_pe               (merge_valid_o[3][9]),
    .data_o_merge_pe                (merge_data_o[3][9]),
    .ready_i_merge_pe               (merge_ready_i[3][9]),
    .credit_upd                     (credit_upd[3][9])
);


network_interface #(
    .isCaster                       (isCaster_3_10),
    .stream_id                      (stream_id_3_10)
)ni_3_10(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[3][10]),
    .data_i_cast_nw                 (data_o_cast_nw[3][10]),
    .ready_o_cast_nw                (ready_i_cast_nw[3][10]),
    .valid_o_cast_nw                (valid_i_cast_nw[3][10]),
    .data_o_cast_nw                 (data_i_cast_nw[3][10]),
    .ready_i_cast_nw                (ready_o_cast_nw[3][10]),
    .valid_i_merge_nw               (valid_o_merge_nw[3][10]),
    .data_i_merge_nw                (data_o_merge_nw[3][10]),
    .ready_o_merge_nw               (ready_i_merge_nw[3][10]),
    .valid_o_merge_nw               (valid_i_merge_nw[3][10]),
    .data_o_merge_nw                (data_i_merge_nw[3][10]),
    .ready_i_merge_nw               (ready_o_merge_nw[3][10]),
    .valid_i_cast_pe                (cast_valid_i[3][10]),
    .data_i_cast_pe                 (cast_data_i[3][10]),
    .ready_o_cast_pe                (cast_ready_o[3][10]),
    .valid_o_cast_pe                (cast_valid_o[3][10]),
    .data_o_cast_pe                 (cast_data_o[3][10]),
    .ready_i_cast_pe                (cast_ready_i[3][10]),
    .valid_i_merge_pe               (merge_valid_i[3][10]),
    .data_i_merge_pe                (merge_data_i[3][10]),
    .ready_o_merge_pe               (merge_ready_o[3][10]),
    .valid_o_merge_pe               (merge_valid_o[3][10]),
    .data_o_merge_pe                (merge_data_o[3][10]),
    .ready_i_merge_pe               (merge_ready_i[3][10]),
    .credit_upd                     (credit_upd[3][10])
);


network_interface #(
    .isCaster                       (isCaster_4_0),
    .stream_id                      (stream_id_4_0)
)ni_4_0(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[4][0]),
    .data_i_cast_nw                 (data_o_cast_nw[4][0]),
    .ready_o_cast_nw                (ready_i_cast_nw[4][0]),
    .valid_o_cast_nw                (valid_i_cast_nw[4][0]),
    .data_o_cast_nw                 (data_i_cast_nw[4][0]),
    .ready_i_cast_nw                (ready_o_cast_nw[4][0]),
    .valid_i_merge_nw               (valid_o_merge_nw[4][0]),
    .data_i_merge_nw                (data_o_merge_nw[4][0]),
    .ready_o_merge_nw               (ready_i_merge_nw[4][0]),
    .valid_o_merge_nw               (valid_i_merge_nw[4][0]),
    .data_o_merge_nw                (data_i_merge_nw[4][0]),
    .ready_i_merge_nw               (ready_o_merge_nw[4][0]),
    .valid_i_cast_pe                (cast_valid_i[4][0]),
    .data_i_cast_pe                 (cast_data_i[4][0]),
    .ready_o_cast_pe                (cast_ready_o[4][0]),
    .valid_o_cast_pe                (cast_valid_o[4][0]),
    .data_o_cast_pe                 (cast_data_o[4][0]),
    .ready_i_cast_pe                (cast_ready_i[4][0]),
    .valid_i_merge_pe               (merge_valid_i[4][0]),
    .data_i_merge_pe                (merge_data_i[4][0]),
    .ready_o_merge_pe               (merge_ready_o[4][0]),
    .valid_o_merge_pe               (merge_valid_o[4][0]),
    .data_o_merge_pe                (merge_data_o[4][0]),
    .ready_i_merge_pe               (merge_ready_i[4][0]),
    .credit_upd                     (credit_upd[4][0])
);


network_interface #(
    .isCaster                       (isCaster_4_1),
    .stream_id                      (stream_id_4_1)
)ni_4_1(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[4][1]),
    .data_i_cast_nw                 (data_o_cast_nw[4][1]),
    .ready_o_cast_nw                (ready_i_cast_nw[4][1]),
    .valid_o_cast_nw                (valid_i_cast_nw[4][1]),
    .data_o_cast_nw                 (data_i_cast_nw[4][1]),
    .ready_i_cast_nw                (ready_o_cast_nw[4][1]),
    .valid_i_merge_nw               (valid_o_merge_nw[4][1]),
    .data_i_merge_nw                (data_o_merge_nw[4][1]),
    .ready_o_merge_nw               (ready_i_merge_nw[4][1]),
    .valid_o_merge_nw               (valid_i_merge_nw[4][1]),
    .data_o_merge_nw                (data_i_merge_nw[4][1]),
    .ready_i_merge_nw               (ready_o_merge_nw[4][1]),
    .valid_i_cast_pe                (cast_valid_i[4][1]),
    .data_i_cast_pe                 (cast_data_i[4][1]),
    .ready_o_cast_pe                (cast_ready_o[4][1]),
    .valid_o_cast_pe                (cast_valid_o[4][1]),
    .data_o_cast_pe                 (cast_data_o[4][1]),
    .ready_i_cast_pe                (cast_ready_i[4][1]),
    .valid_i_merge_pe               (merge_valid_i[4][1]),
    .data_i_merge_pe                (merge_data_i[4][1]),
    .ready_o_merge_pe               (merge_ready_o[4][1]),
    .valid_o_merge_pe               (merge_valid_o[4][1]),
    .data_o_merge_pe                (merge_data_o[4][1]),
    .ready_i_merge_pe               (merge_ready_i[4][1]),
    .credit_upd                     (credit_upd[4][1])
);


network_interface #(
    .isCaster                       (isCaster_4_2),
    .stream_id                      (stream_id_4_2)
)ni_4_2(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[4][2]),
    .data_i_cast_nw                 (data_o_cast_nw[4][2]),
    .ready_o_cast_nw                (ready_i_cast_nw[4][2]),
    .valid_o_cast_nw                (valid_i_cast_nw[4][2]),
    .data_o_cast_nw                 (data_i_cast_nw[4][2]),
    .ready_i_cast_nw                (ready_o_cast_nw[4][2]),
    .valid_i_merge_nw               (valid_o_merge_nw[4][2]),
    .data_i_merge_nw                (data_o_merge_nw[4][2]),
    .ready_o_merge_nw               (ready_i_merge_nw[4][2]),
    .valid_o_merge_nw               (valid_i_merge_nw[4][2]),
    .data_o_merge_nw                (data_i_merge_nw[4][2]),
    .ready_i_merge_nw               (ready_o_merge_nw[4][2]),
    .valid_i_cast_pe                (cast_valid_i[4][2]),
    .data_i_cast_pe                 (cast_data_i[4][2]),
    .ready_o_cast_pe                (cast_ready_o[4][2]),
    .valid_o_cast_pe                (cast_valid_o[4][2]),
    .data_o_cast_pe                 (cast_data_o[4][2]),
    .ready_i_cast_pe                (cast_ready_i[4][2]),
    .valid_i_merge_pe               (merge_valid_i[4][2]),
    .data_i_merge_pe                (merge_data_i[4][2]),
    .ready_o_merge_pe               (merge_ready_o[4][2]),
    .valid_o_merge_pe               (merge_valid_o[4][2]),
    .data_o_merge_pe                (merge_data_o[4][2]),
    .ready_i_merge_pe               (merge_ready_i[4][2]),
    .credit_upd                     (credit_upd[4][2])
);


network_interface #(
    .isCaster                       (isCaster_4_3),
    .stream_id                      (stream_id_4_3)
)ni_4_3(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[4][3]),
    .data_i_cast_nw                 (data_o_cast_nw[4][3]),
    .ready_o_cast_nw                (ready_i_cast_nw[4][3]),
    .valid_o_cast_nw                (valid_i_cast_nw[4][3]),
    .data_o_cast_nw                 (data_i_cast_nw[4][3]),
    .ready_i_cast_nw                (ready_o_cast_nw[4][3]),
    .valid_i_merge_nw               (valid_o_merge_nw[4][3]),
    .data_i_merge_nw                (data_o_merge_nw[4][3]),
    .ready_o_merge_nw               (ready_i_merge_nw[4][3]),
    .valid_o_merge_nw               (valid_i_merge_nw[4][3]),
    .data_o_merge_nw                (data_i_merge_nw[4][3]),
    .ready_i_merge_nw               (ready_o_merge_nw[4][3]),
    .valid_i_cast_pe                (cast_valid_i[4][3]),
    .data_i_cast_pe                 (cast_data_i[4][3]),
    .ready_o_cast_pe                (cast_ready_o[4][3]),
    .valid_o_cast_pe                (cast_valid_o[4][3]),
    .data_o_cast_pe                 (cast_data_o[4][3]),
    .ready_i_cast_pe                (cast_ready_i[4][3]),
    .valid_i_merge_pe               (merge_valid_i[4][3]),
    .data_i_merge_pe                (merge_data_i[4][3]),
    .ready_o_merge_pe               (merge_ready_o[4][3]),
    .valid_o_merge_pe               (merge_valid_o[4][3]),
    .data_o_merge_pe                (merge_data_o[4][3]),
    .ready_i_merge_pe               (merge_ready_i[4][3]),
    .credit_upd                     (credit_upd[4][3])
);


network_interface #(
    .isCaster                       (isCaster_4_4),
    .stream_id                      (stream_id_4_4)
)ni_4_4(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[4][4]),
    .data_i_cast_nw                 (data_o_cast_nw[4][4]),
    .ready_o_cast_nw                (ready_i_cast_nw[4][4]),
    .valid_o_cast_nw                (valid_i_cast_nw[4][4]),
    .data_o_cast_nw                 (data_i_cast_nw[4][4]),
    .ready_i_cast_nw                (ready_o_cast_nw[4][4]),
    .valid_i_merge_nw               (valid_o_merge_nw[4][4]),
    .data_i_merge_nw                (data_o_merge_nw[4][4]),
    .ready_o_merge_nw               (ready_i_merge_nw[4][4]),
    .valid_o_merge_nw               (valid_i_merge_nw[4][4]),
    .data_o_merge_nw                (data_i_merge_nw[4][4]),
    .ready_i_merge_nw               (ready_o_merge_nw[4][4]),
    .valid_i_cast_pe                (cast_valid_i[4][4]),
    .data_i_cast_pe                 (cast_data_i[4][4]),
    .ready_o_cast_pe                (cast_ready_o[4][4]),
    .valid_o_cast_pe                (cast_valid_o[4][4]),
    .data_o_cast_pe                 (cast_data_o[4][4]),
    .ready_i_cast_pe                (cast_ready_i[4][4]),
    .valid_i_merge_pe               (merge_valid_i[4][4]),
    .data_i_merge_pe                (merge_data_i[4][4]),
    .ready_o_merge_pe               (merge_ready_o[4][4]),
    .valid_o_merge_pe               (merge_valid_o[4][4]),
    .data_o_merge_pe                (merge_data_o[4][4]),
    .ready_i_merge_pe               (merge_ready_i[4][4]),
    .credit_upd                     (credit_upd[4][4])
);


network_interface #(
    .isCaster                       (isCaster_4_5),
    .stream_id                      (stream_id_4_5)
)ni_4_5(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[4][5]),
    .data_i_cast_nw                 (data_o_cast_nw[4][5]),
    .ready_o_cast_nw                (ready_i_cast_nw[4][5]),
    .valid_o_cast_nw                (valid_i_cast_nw[4][5]),
    .data_o_cast_nw                 (data_i_cast_nw[4][5]),
    .ready_i_cast_nw                (ready_o_cast_nw[4][5]),
    .valid_i_merge_nw               (valid_o_merge_nw[4][5]),
    .data_i_merge_nw                (data_o_merge_nw[4][5]),
    .ready_o_merge_nw               (ready_i_merge_nw[4][5]),
    .valid_o_merge_nw               (valid_i_merge_nw[4][5]),
    .data_o_merge_nw                (data_i_merge_nw[4][5]),
    .ready_i_merge_nw               (ready_o_merge_nw[4][5]),
    .valid_i_cast_pe                (cast_valid_i[4][5]),
    .data_i_cast_pe                 (cast_data_i[4][5]),
    .ready_o_cast_pe                (cast_ready_o[4][5]),
    .valid_o_cast_pe                (cast_valid_o[4][5]),
    .data_o_cast_pe                 (cast_data_o[4][5]),
    .ready_i_cast_pe                (cast_ready_i[4][5]),
    .valid_i_merge_pe               (merge_valid_i[4][5]),
    .data_i_merge_pe                (merge_data_i[4][5]),
    .ready_o_merge_pe               (merge_ready_o[4][5]),
    .valid_o_merge_pe               (merge_valid_o[4][5]),
    .data_o_merge_pe                (merge_data_o[4][5]),
    .ready_i_merge_pe               (merge_ready_i[4][5]),
    .credit_upd                     (credit_upd[4][5])
);


network_interface #(
    .isCaster                       (isCaster_4_6),
    .stream_id                      (stream_id_4_6)
)ni_4_6(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[4][6]),
    .data_i_cast_nw                 (data_o_cast_nw[4][6]),
    .ready_o_cast_nw                (ready_i_cast_nw[4][6]),
    .valid_o_cast_nw                (valid_i_cast_nw[4][6]),
    .data_o_cast_nw                 (data_i_cast_nw[4][6]),
    .ready_i_cast_nw                (ready_o_cast_nw[4][6]),
    .valid_i_merge_nw               (valid_o_merge_nw[4][6]),
    .data_i_merge_nw                (data_o_merge_nw[4][6]),
    .ready_o_merge_nw               (ready_i_merge_nw[4][6]),
    .valid_o_merge_nw               (valid_i_merge_nw[4][6]),
    .data_o_merge_nw                (data_i_merge_nw[4][6]),
    .ready_i_merge_nw               (ready_o_merge_nw[4][6]),
    .valid_i_cast_pe                (cast_valid_i[4][6]),
    .data_i_cast_pe                 (cast_data_i[4][6]),
    .ready_o_cast_pe                (cast_ready_o[4][6]),
    .valid_o_cast_pe                (cast_valid_o[4][6]),
    .data_o_cast_pe                 (cast_data_o[4][6]),
    .ready_i_cast_pe                (cast_ready_i[4][6]),
    .valid_i_merge_pe               (merge_valid_i[4][6]),
    .data_i_merge_pe                (merge_data_i[4][6]),
    .ready_o_merge_pe               (merge_ready_o[4][6]),
    .valid_o_merge_pe               (merge_valid_o[4][6]),
    .data_o_merge_pe                (merge_data_o[4][6]),
    .ready_i_merge_pe               (merge_ready_i[4][6]),
    .credit_upd                     (credit_upd[4][6])
);


network_interface #(
    .isCaster                       (isCaster_4_7),
    .stream_id                      (stream_id_4_7)
)ni_4_7(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[4][7]),
    .data_i_cast_nw                 (data_o_cast_nw[4][7]),
    .ready_o_cast_nw                (ready_i_cast_nw[4][7]),
    .valid_o_cast_nw                (valid_i_cast_nw[4][7]),
    .data_o_cast_nw                 (data_i_cast_nw[4][7]),
    .ready_i_cast_nw                (ready_o_cast_nw[4][7]),
    .valid_i_merge_nw               (valid_o_merge_nw[4][7]),
    .data_i_merge_nw                (data_o_merge_nw[4][7]),
    .ready_o_merge_nw               (ready_i_merge_nw[4][7]),
    .valid_o_merge_nw               (valid_i_merge_nw[4][7]),
    .data_o_merge_nw                (data_i_merge_nw[4][7]),
    .ready_i_merge_nw               (ready_o_merge_nw[4][7]),
    .valid_i_cast_pe                (cast_valid_i[4][7]),
    .data_i_cast_pe                 (cast_data_i[4][7]),
    .ready_o_cast_pe                (cast_ready_o[4][7]),
    .valid_o_cast_pe                (cast_valid_o[4][7]),
    .data_o_cast_pe                 (cast_data_o[4][7]),
    .ready_i_cast_pe                (cast_ready_i[4][7]),
    .valid_i_merge_pe               (merge_valid_i[4][7]),
    .data_i_merge_pe                (merge_data_i[4][7]),
    .ready_o_merge_pe               (merge_ready_o[4][7]),
    .valid_o_merge_pe               (merge_valid_o[4][7]),
    .data_o_merge_pe                (merge_data_o[4][7]),
    .ready_i_merge_pe               (merge_ready_i[4][7]),
    .credit_upd                     (credit_upd[4][7])
);


network_interface #(
    .isCaster                       (isCaster_4_8),
    .stream_id                      (stream_id_4_8)
)ni_4_8(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[4][8]),
    .data_i_cast_nw                 (data_o_cast_nw[4][8]),
    .ready_o_cast_nw                (ready_i_cast_nw[4][8]),
    .valid_o_cast_nw                (valid_i_cast_nw[4][8]),
    .data_o_cast_nw                 (data_i_cast_nw[4][8]),
    .ready_i_cast_nw                (ready_o_cast_nw[4][8]),
    .valid_i_merge_nw               (valid_o_merge_nw[4][8]),
    .data_i_merge_nw                (data_o_merge_nw[4][8]),
    .ready_o_merge_nw               (ready_i_merge_nw[4][8]),
    .valid_o_merge_nw               (valid_i_merge_nw[4][8]),
    .data_o_merge_nw                (data_i_merge_nw[4][8]),
    .ready_i_merge_nw               (ready_o_merge_nw[4][8]),
    .valid_i_cast_pe                (cast_valid_i[4][8]),
    .data_i_cast_pe                 (cast_data_i[4][8]),
    .ready_o_cast_pe                (cast_ready_o[4][8]),
    .valid_o_cast_pe                (cast_valid_o[4][8]),
    .data_o_cast_pe                 (cast_data_o[4][8]),
    .ready_i_cast_pe                (cast_ready_i[4][8]),
    .valid_i_merge_pe               (merge_valid_i[4][8]),
    .data_i_merge_pe                (merge_data_i[4][8]),
    .ready_o_merge_pe               (merge_ready_o[4][8]),
    .valid_o_merge_pe               (merge_valid_o[4][8]),
    .data_o_merge_pe                (merge_data_o[4][8]),
    .ready_i_merge_pe               (merge_ready_i[4][8]),
    .credit_upd                     (credit_upd[4][8])
);


network_interface #(
    .isCaster                       (isCaster_4_9),
    .stream_id                      (stream_id_4_9)
)ni_4_9(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[4][9]),
    .data_i_cast_nw                 (data_o_cast_nw[4][9]),
    .ready_o_cast_nw                (ready_i_cast_nw[4][9]),
    .valid_o_cast_nw                (valid_i_cast_nw[4][9]),
    .data_o_cast_nw                 (data_i_cast_nw[4][9]),
    .ready_i_cast_nw                (ready_o_cast_nw[4][9]),
    .valid_i_merge_nw               (valid_o_merge_nw[4][9]),
    .data_i_merge_nw                (data_o_merge_nw[4][9]),
    .ready_o_merge_nw               (ready_i_merge_nw[4][9]),
    .valid_o_merge_nw               (valid_i_merge_nw[4][9]),
    .data_o_merge_nw                (data_i_merge_nw[4][9]),
    .ready_i_merge_nw               (ready_o_merge_nw[4][9]),
    .valid_i_cast_pe                (cast_valid_i[4][9]),
    .data_i_cast_pe                 (cast_data_i[4][9]),
    .ready_o_cast_pe                (cast_ready_o[4][9]),
    .valid_o_cast_pe                (cast_valid_o[4][9]),
    .data_o_cast_pe                 (cast_data_o[4][9]),
    .ready_i_cast_pe                (cast_ready_i[4][9]),
    .valid_i_merge_pe               (merge_valid_i[4][9]),
    .data_i_merge_pe                (merge_data_i[4][9]),
    .ready_o_merge_pe               (merge_ready_o[4][9]),
    .valid_o_merge_pe               (merge_valid_o[4][9]),
    .data_o_merge_pe                (merge_data_o[4][9]),
    .ready_i_merge_pe               (merge_ready_i[4][9]),
    .credit_upd                     (credit_upd[4][9])
);


network_interface #(
    .isCaster                       (isCaster_4_10),
    .stream_id                      (stream_id_4_10)
)ni_4_10(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[4][10]),
    .data_i_cast_nw                 (data_o_cast_nw[4][10]),
    .ready_o_cast_nw                (ready_i_cast_nw[4][10]),
    .valid_o_cast_nw                (valid_i_cast_nw[4][10]),
    .data_o_cast_nw                 (data_i_cast_nw[4][10]),
    .ready_i_cast_nw                (ready_o_cast_nw[4][10]),
    .valid_i_merge_nw               (valid_o_merge_nw[4][10]),
    .data_i_merge_nw                (data_o_merge_nw[4][10]),
    .ready_o_merge_nw               (ready_i_merge_nw[4][10]),
    .valid_o_merge_nw               (valid_i_merge_nw[4][10]),
    .data_o_merge_nw                (data_i_merge_nw[4][10]),
    .ready_i_merge_nw               (ready_o_merge_nw[4][10]),
    .valid_i_cast_pe                (cast_valid_i[4][10]),
    .data_i_cast_pe                 (cast_data_i[4][10]),
    .ready_o_cast_pe                (cast_ready_o[4][10]),
    .valid_o_cast_pe                (cast_valid_o[4][10]),
    .data_o_cast_pe                 (cast_data_o[4][10]),
    .ready_i_cast_pe                (cast_ready_i[4][10]),
    .valid_i_merge_pe               (merge_valid_i[4][10]),
    .data_i_merge_pe                (merge_data_i[4][10]),
    .ready_o_merge_pe               (merge_ready_o[4][10]),
    .valid_o_merge_pe               (merge_valid_o[4][10]),
    .data_o_merge_pe                (merge_data_o[4][10]),
    .ready_i_merge_pe               (merge_ready_i[4][10]),
    .credit_upd                     (credit_upd[4][10])
);

endmodule
