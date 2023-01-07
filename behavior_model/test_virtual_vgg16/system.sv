`include "params.svh"
`include "system_config.svh"

module system (
    input       wire                            clk,
    input       wire                            rstn,

    input       wire        [`DW-1:0]           data_i_stab,
    input       wire                            valid_i_stab,
    output      wire                            ready_o_stab,

    output      wire        [`DW-1:0]           data_o_flee0,
    output      wire                            valid_o_flee0,
    input       wire                            ready_i_flee0,

    output      wire        [`DW-1:0]           data_o_flee1,
    output      wire                            valid_o_flee1,
    input       wire                            ready_i_flee1  
);

wire [`DW-1:0] cast_data_o[`NOC_WIDTH][`NOC_HEIGHT];
wire cast_valid_o[`NOC_WIDTH][`NOC_HEIGHT],cast_ready_o[`NOC_WIDTH][`NOC_HEIGHT];

wire [`DW-1:0] pe_cast_data_o[`NOC_WIDTH][`NOC_HEIGHT];
wire pe_cast_valid_o[`NOC_WIDTH][`NOC_HEIGHT],pe_cast_ready_o[`NOC_WIDTH][`NOC_HEIGHT];

wire credit_upd[`NOC_WIDTH][`NOC_HEIGHT];

cast_network cast_nw(
    .clk                                               (clk),
    .rstn                                              (rstn),
    .data_i                                            (pe_cast_data_o),
    .valid_i                                           (pe_cast_valid_o),
    .ready_o                                           (cast_ready_o),
    .data_o                                            (cast_data_o),
    .valid_o                                           (cast_valid_o),
    .ready_i                                           (pe_cast_ready_o),
    .data_i_stab                                       (data_i_stab),
    .valid_i_stab                                      (valid_i_stab),
    .ready_o_stab                                      (ready_o_stab),
    .data_o_flee0                                      (data_o_flee0),
    .valid_o_flee0                                     (valid_o_flee0),
    .ready_i_flee0                                     (ready_i_flee0),
    .data_o_flee1                                      (data_o_flee1),
    .valid_o_flee1                                     (valid_o_flee1),
    .ready_i_flee1                                     (ready_i_flee1),
    .credit_upd                                        (credit_upd)
);

wire [`DW-1:0] merge_data_o[`NOC_WIDTH][`NOC_HEIGHT];
wire merge_valid_o[`NOC_WIDTH][`NOC_HEIGHT],merge_ready_o[`NOC_WIDTH][`NOC_HEIGHT];

wire [`DW-1:0] pe_merge_data_o[`NOC_WIDTH][`NOC_HEIGHT];
wire pe_merge_valid_o[`NOC_WIDTH][`NOC_HEIGHT],pe_merge_ready_o[`NOC_WIDTH][`NOC_HEIGHT];

merge_network merge_nw(
    .clk                                            (clk),
    .rstn                                           (rstn),
    .data_i                                         (pe_merge_data_o),
    .valid_i                                        (pe_merge_valid_o),
    .ready_o                                        (merge_ready_o),
    .data_o                                         (merge_data_o),
    .valid_o                                        (merge_valid_o),
    .ready_i                                        (pe_merge_ready_o)
);

virtual_pe #(
    .isCaster                    (isCaster_0_0),
    .stream_id                   (stream_id_0_0)
)pe_0_0(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[0][0]),
    .data_i_cast                 (cast_data_o[0][0]),
    .ready_o_cast                (pe_cast_ready_o[0][0]),
    .valid_o_cast                (pe_cast_valid_o[0][0]),
    .data_o_cast                 (pe_cast_data_o[0][0]),
    .ready_i_cast                (cast_ready_o[0][0]),
    .valid_i_merge               (merge_valid_o[0][0]),
    .data_i_merge                (merge_data_o[0][0]),
    .ready_o_merge               (pe_merge_ready_o[0][0]),
    .valid_o_merge               (pe_merge_valid_o[0][0]),
    .data_o_merge                (pe_merge_data_o[0][0]),
    .ready_i_merge               (merge_ready_o[0][0]),
    .credit_upd                  (credit_upd[0][0])
);


virtual_pe #(
    .isCaster                    (isCaster_0_1),
    .stream_id                   (stream_id_0_1)
)pe_0_1(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[0][1]),
    .data_i_cast                 (cast_data_o[0][1]),
    .ready_o_cast                (pe_cast_ready_o[0][1]),
    .valid_o_cast                (pe_cast_valid_o[0][1]),
    .data_o_cast                 (pe_cast_data_o[0][1]),
    .ready_i_cast                (cast_ready_o[0][1]),
    .valid_i_merge               (merge_valid_o[0][1]),
    .data_i_merge                (merge_data_o[0][1]),
    .ready_o_merge               (pe_merge_ready_o[0][1]),
    .valid_o_merge               (pe_merge_valid_o[0][1]),
    .data_o_merge                (pe_merge_data_o[0][1]),
    .ready_i_merge               (merge_ready_o[0][1]),
    .credit_upd                  (credit_upd[0][1])
);


virtual_pe #(
    .isCaster                    (isCaster_0_2),
    .stream_id                   (stream_id_0_2)
)pe_0_2(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[0][2]),
    .data_i_cast                 (cast_data_o[0][2]),
    .ready_o_cast                (pe_cast_ready_o[0][2]),
    .valid_o_cast                (pe_cast_valid_o[0][2]),
    .data_o_cast                 (pe_cast_data_o[0][2]),
    .ready_i_cast                (cast_ready_o[0][2]),
    .valid_i_merge               (merge_valid_o[0][2]),
    .data_i_merge                (merge_data_o[0][2]),
    .ready_o_merge               (pe_merge_ready_o[0][2]),
    .valid_o_merge               (pe_merge_valid_o[0][2]),
    .data_o_merge                (pe_merge_data_o[0][2]),
    .ready_i_merge               (merge_ready_o[0][2]),
    .credit_upd                  (credit_upd[0][2])
);


virtual_pe #(
    .isCaster                    (isCaster_0_3),
    .stream_id                   (stream_id_0_3)
)pe_0_3(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[0][3]),
    .data_i_cast                 (cast_data_o[0][3]),
    .ready_o_cast                (pe_cast_ready_o[0][3]),
    .valid_o_cast                (pe_cast_valid_o[0][3]),
    .data_o_cast                 (pe_cast_data_o[0][3]),
    .ready_i_cast                (cast_ready_o[0][3]),
    .valid_i_merge               (merge_valid_o[0][3]),
    .data_i_merge                (merge_data_o[0][3]),
    .ready_o_merge               (pe_merge_ready_o[0][3]),
    .valid_o_merge               (pe_merge_valid_o[0][3]),
    .data_o_merge                (pe_merge_data_o[0][3]),
    .ready_i_merge               (merge_ready_o[0][3]),
    .credit_upd                  (credit_upd[0][3])
);


virtual_pe #(
    .isCaster                    (isCaster_0_4),
    .stream_id                   (stream_id_0_4)
)pe_0_4(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[0][4]),
    .data_i_cast                 (cast_data_o[0][4]),
    .ready_o_cast                (pe_cast_ready_o[0][4]),
    .valid_o_cast                (pe_cast_valid_o[0][4]),
    .data_o_cast                 (pe_cast_data_o[0][4]),
    .ready_i_cast                (cast_ready_o[0][4]),
    .valid_i_merge               (merge_valid_o[0][4]),
    .data_i_merge                (merge_data_o[0][4]),
    .ready_o_merge               (pe_merge_ready_o[0][4]),
    .valid_o_merge               (pe_merge_valid_o[0][4]),
    .data_o_merge                (pe_merge_data_o[0][4]),
    .ready_i_merge               (merge_ready_o[0][4]),
    .credit_upd                  (credit_upd[0][4])
);


virtual_pe #(
    .isCaster                    (isCaster_0_5),
    .stream_id                   (stream_id_0_5)
)pe_0_5(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[0][5]),
    .data_i_cast                 (cast_data_o[0][5]),
    .ready_o_cast                (pe_cast_ready_o[0][5]),
    .valid_o_cast                (pe_cast_valid_o[0][5]),
    .data_o_cast                 (pe_cast_data_o[0][5]),
    .ready_i_cast                (cast_ready_o[0][5]),
    .valid_i_merge               (merge_valid_o[0][5]),
    .data_i_merge                (merge_data_o[0][5]),
    .ready_o_merge               (pe_merge_ready_o[0][5]),
    .valid_o_merge               (pe_merge_valid_o[0][5]),
    .data_o_merge                (pe_merge_data_o[0][5]),
    .ready_i_merge               (merge_ready_o[0][5]),
    .credit_upd                  (credit_upd[0][5])
);


virtual_pe #(
    .isCaster                    (isCaster_0_6),
    .stream_id                   (stream_id_0_6)
)pe_0_6(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[0][6]),
    .data_i_cast                 (cast_data_o[0][6]),
    .ready_o_cast                (pe_cast_ready_o[0][6]),
    .valid_o_cast                (pe_cast_valid_o[0][6]),
    .data_o_cast                 (pe_cast_data_o[0][6]),
    .ready_i_cast                (cast_ready_o[0][6]),
    .valid_i_merge               (merge_valid_o[0][6]),
    .data_i_merge                (merge_data_o[0][6]),
    .ready_o_merge               (pe_merge_ready_o[0][6]),
    .valid_o_merge               (pe_merge_valid_o[0][6]),
    .data_o_merge                (pe_merge_data_o[0][6]),
    .ready_i_merge               (merge_ready_o[0][6]),
    .credit_upd                  (credit_upd[0][6])
);


virtual_pe #(
    .isCaster                    (isCaster_0_7),
    .stream_id                   (stream_id_0_7)
)pe_0_7(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[0][7]),
    .data_i_cast                 (cast_data_o[0][7]),
    .ready_o_cast                (pe_cast_ready_o[0][7]),
    .valid_o_cast                (pe_cast_valid_o[0][7]),
    .data_o_cast                 (pe_cast_data_o[0][7]),
    .ready_i_cast                (cast_ready_o[0][7]),
    .valid_i_merge               (merge_valid_o[0][7]),
    .data_i_merge                (merge_data_o[0][7]),
    .ready_o_merge               (pe_merge_ready_o[0][7]),
    .valid_o_merge               (pe_merge_valid_o[0][7]),
    .data_o_merge                (pe_merge_data_o[0][7]),
    .ready_i_merge               (merge_ready_o[0][7]),
    .credit_upd                  (credit_upd[0][7])
);


virtual_pe #(
    .isCaster                    (isCaster_1_0),
    .stream_id                   (stream_id_1_0)
)pe_1_0(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[1][0]),
    .data_i_cast                 (cast_data_o[1][0]),
    .ready_o_cast                (pe_cast_ready_o[1][0]),
    .valid_o_cast                (pe_cast_valid_o[1][0]),
    .data_o_cast                 (pe_cast_data_o[1][0]),
    .ready_i_cast                (cast_ready_o[1][0]),
    .valid_i_merge               (merge_valid_o[1][0]),
    .data_i_merge                (merge_data_o[1][0]),
    .ready_o_merge               (pe_merge_ready_o[1][0]),
    .valid_o_merge               (pe_merge_valid_o[1][0]),
    .data_o_merge                (pe_merge_data_o[1][0]),
    .ready_i_merge               (merge_ready_o[1][0]),
    .credit_upd                  (credit_upd[1][0])
);


virtual_pe #(
    .isCaster                    (isCaster_1_1),
    .stream_id                   (stream_id_1_1)
)pe_1_1(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[1][1]),
    .data_i_cast                 (cast_data_o[1][1]),
    .ready_o_cast                (pe_cast_ready_o[1][1]),
    .valid_o_cast                (pe_cast_valid_o[1][1]),
    .data_o_cast                 (pe_cast_data_o[1][1]),
    .ready_i_cast                (cast_ready_o[1][1]),
    .valid_i_merge               (merge_valid_o[1][1]),
    .data_i_merge                (merge_data_o[1][1]),
    .ready_o_merge               (pe_merge_ready_o[1][1]),
    .valid_o_merge               (pe_merge_valid_o[1][1]),
    .data_o_merge                (pe_merge_data_o[1][1]),
    .ready_i_merge               (merge_ready_o[1][1]),
    .credit_upd                  (credit_upd[1][1])
);


virtual_pe #(
    .isCaster                    (isCaster_1_2),
    .stream_id                   (stream_id_1_2)
)pe_1_2(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[1][2]),
    .data_i_cast                 (cast_data_o[1][2]),
    .ready_o_cast                (pe_cast_ready_o[1][2]),
    .valid_o_cast                (pe_cast_valid_o[1][2]),
    .data_o_cast                 (pe_cast_data_o[1][2]),
    .ready_i_cast                (cast_ready_o[1][2]),
    .valid_i_merge               (merge_valid_o[1][2]),
    .data_i_merge                (merge_data_o[1][2]),
    .ready_o_merge               (pe_merge_ready_o[1][2]),
    .valid_o_merge               (pe_merge_valid_o[1][2]),
    .data_o_merge                (pe_merge_data_o[1][2]),
    .ready_i_merge               (merge_ready_o[1][2]),
    .credit_upd                  (credit_upd[1][2])
);


virtual_pe #(
    .isCaster                    (isCaster_1_3),
    .stream_id                   (stream_id_1_3)
)pe_1_3(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[1][3]),
    .data_i_cast                 (cast_data_o[1][3]),
    .ready_o_cast                (pe_cast_ready_o[1][3]),
    .valid_o_cast                (pe_cast_valid_o[1][3]),
    .data_o_cast                 (pe_cast_data_o[1][3]),
    .ready_i_cast                (cast_ready_o[1][3]),
    .valid_i_merge               (merge_valid_o[1][3]),
    .data_i_merge                (merge_data_o[1][3]),
    .ready_o_merge               (pe_merge_ready_o[1][3]),
    .valid_o_merge               (pe_merge_valid_o[1][3]),
    .data_o_merge                (pe_merge_data_o[1][3]),
    .ready_i_merge               (merge_ready_o[1][3]),
    .credit_upd                  (credit_upd[1][3])
);


virtual_pe #(
    .isCaster                    (isCaster_1_4),
    .stream_id                   (stream_id_1_4)
)pe_1_4(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[1][4]),
    .data_i_cast                 (cast_data_o[1][4]),
    .ready_o_cast                (pe_cast_ready_o[1][4]),
    .valid_o_cast                (pe_cast_valid_o[1][4]),
    .data_o_cast                 (pe_cast_data_o[1][4]),
    .ready_i_cast                (cast_ready_o[1][4]),
    .valid_i_merge               (merge_valid_o[1][4]),
    .data_i_merge                (merge_data_o[1][4]),
    .ready_o_merge               (pe_merge_ready_o[1][4]),
    .valid_o_merge               (pe_merge_valid_o[1][4]),
    .data_o_merge                (pe_merge_data_o[1][4]),
    .ready_i_merge               (merge_ready_o[1][4]),
    .credit_upd                  (credit_upd[1][4])
);


virtual_pe #(
    .isCaster                    (isCaster_1_5),
    .stream_id                   (stream_id_1_5)
)pe_1_5(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[1][5]),
    .data_i_cast                 (cast_data_o[1][5]),
    .ready_o_cast                (pe_cast_ready_o[1][5]),
    .valid_o_cast                (pe_cast_valid_o[1][5]),
    .data_o_cast                 (pe_cast_data_o[1][5]),
    .ready_i_cast                (cast_ready_o[1][5]),
    .valid_i_merge               (merge_valid_o[1][5]),
    .data_i_merge                (merge_data_o[1][5]),
    .ready_o_merge               (pe_merge_ready_o[1][5]),
    .valid_o_merge               (pe_merge_valid_o[1][5]),
    .data_o_merge                (pe_merge_data_o[1][5]),
    .ready_i_merge               (merge_ready_o[1][5]),
    .credit_upd                  (credit_upd[1][5])
);


virtual_pe #(
    .isCaster                    (isCaster_1_6),
    .stream_id                   (stream_id_1_6)
)pe_1_6(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[1][6]),
    .data_i_cast                 (cast_data_o[1][6]),
    .ready_o_cast                (pe_cast_ready_o[1][6]),
    .valid_o_cast                (pe_cast_valid_o[1][6]),
    .data_o_cast                 (pe_cast_data_o[1][6]),
    .ready_i_cast                (cast_ready_o[1][6]),
    .valid_i_merge               (merge_valid_o[1][6]),
    .data_i_merge                (merge_data_o[1][6]),
    .ready_o_merge               (pe_merge_ready_o[1][6]),
    .valid_o_merge               (pe_merge_valid_o[1][6]),
    .data_o_merge                (pe_merge_data_o[1][6]),
    .ready_i_merge               (merge_ready_o[1][6]),
    .credit_upd                  (credit_upd[1][6])
);


virtual_pe #(
    .isCaster                    (isCaster_1_7),
    .stream_id                   (stream_id_1_7)
)pe_1_7(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[1][7]),
    .data_i_cast                 (cast_data_o[1][7]),
    .ready_o_cast                (pe_cast_ready_o[1][7]),
    .valid_o_cast                (pe_cast_valid_o[1][7]),
    .data_o_cast                 (pe_cast_data_o[1][7]),
    .ready_i_cast                (cast_ready_o[1][7]),
    .valid_i_merge               (merge_valid_o[1][7]),
    .data_i_merge                (merge_data_o[1][7]),
    .ready_o_merge               (pe_merge_ready_o[1][7]),
    .valid_o_merge               (pe_merge_valid_o[1][7]),
    .data_o_merge                (pe_merge_data_o[1][7]),
    .ready_i_merge               (merge_ready_o[1][7]),
    .credit_upd                  (credit_upd[1][7])
);


virtual_pe #(
    .isCaster                    (isCaster_2_0),
    .stream_id                   (stream_id_2_0)
)pe_2_0(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[2][0]),
    .data_i_cast                 (cast_data_o[2][0]),
    .ready_o_cast                (pe_cast_ready_o[2][0]),
    .valid_o_cast                (pe_cast_valid_o[2][0]),
    .data_o_cast                 (pe_cast_data_o[2][0]),
    .ready_i_cast                (cast_ready_o[2][0]),
    .valid_i_merge               (merge_valid_o[2][0]),
    .data_i_merge                (merge_data_o[2][0]),
    .ready_o_merge               (pe_merge_ready_o[2][0]),
    .valid_o_merge               (pe_merge_valid_o[2][0]),
    .data_o_merge                (pe_merge_data_o[2][0]),
    .ready_i_merge               (merge_ready_o[2][0]),
    .credit_upd                  (credit_upd[2][0])
);


virtual_pe #(
    .isCaster                    (isCaster_2_1),
    .stream_id                   (stream_id_2_1)
)pe_2_1(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[2][1]),
    .data_i_cast                 (cast_data_o[2][1]),
    .ready_o_cast                (pe_cast_ready_o[2][1]),
    .valid_o_cast                (pe_cast_valid_o[2][1]),
    .data_o_cast                 (pe_cast_data_o[2][1]),
    .ready_i_cast                (cast_ready_o[2][1]),
    .valid_i_merge               (merge_valid_o[2][1]),
    .data_i_merge                (merge_data_o[2][1]),
    .ready_o_merge               (pe_merge_ready_o[2][1]),
    .valid_o_merge               (pe_merge_valid_o[2][1]),
    .data_o_merge                (pe_merge_data_o[2][1]),
    .ready_i_merge               (merge_ready_o[2][1]),
    .credit_upd                  (credit_upd[2][1])
);


virtual_pe #(
    .isCaster                    (isCaster_2_2),
    .stream_id                   (stream_id_2_2)
)pe_2_2(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[2][2]),
    .data_i_cast                 (cast_data_o[2][2]),
    .ready_o_cast                (pe_cast_ready_o[2][2]),
    .valid_o_cast                (pe_cast_valid_o[2][2]),
    .data_o_cast                 (pe_cast_data_o[2][2]),
    .ready_i_cast                (cast_ready_o[2][2]),
    .valid_i_merge               (merge_valid_o[2][2]),
    .data_i_merge                (merge_data_o[2][2]),
    .ready_o_merge               (pe_merge_ready_o[2][2]),
    .valid_o_merge               (pe_merge_valid_o[2][2]),
    .data_o_merge                (pe_merge_data_o[2][2]),
    .ready_i_merge               (merge_ready_o[2][2]),
    .credit_upd                  (credit_upd[2][2])
);


virtual_pe #(
    .isCaster                    (isCaster_2_3),
    .stream_id                   (stream_id_2_3)
)pe_2_3(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[2][3]),
    .data_i_cast                 (cast_data_o[2][3]),
    .ready_o_cast                (pe_cast_ready_o[2][3]),
    .valid_o_cast                (pe_cast_valid_o[2][3]),
    .data_o_cast                 (pe_cast_data_o[2][3]),
    .ready_i_cast                (cast_ready_o[2][3]),
    .valid_i_merge               (merge_valid_o[2][3]),
    .data_i_merge                (merge_data_o[2][3]),
    .ready_o_merge               (pe_merge_ready_o[2][3]),
    .valid_o_merge               (pe_merge_valid_o[2][3]),
    .data_o_merge                (pe_merge_data_o[2][3]),
    .ready_i_merge               (merge_ready_o[2][3]),
    .credit_upd                  (credit_upd[2][3])
);


virtual_pe #(
    .isCaster                    (isCaster_2_4),
    .stream_id                   (stream_id_2_4)
)pe_2_4(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[2][4]),
    .data_i_cast                 (cast_data_o[2][4]),
    .ready_o_cast                (pe_cast_ready_o[2][4]),
    .valid_o_cast                (pe_cast_valid_o[2][4]),
    .data_o_cast                 (pe_cast_data_o[2][4]),
    .ready_i_cast                (cast_ready_o[2][4]),
    .valid_i_merge               (merge_valid_o[2][4]),
    .data_i_merge                (merge_data_o[2][4]),
    .ready_o_merge               (pe_merge_ready_o[2][4]),
    .valid_o_merge               (pe_merge_valid_o[2][4]),
    .data_o_merge                (pe_merge_data_o[2][4]),
    .ready_i_merge               (merge_ready_o[2][4]),
    .credit_upd                  (credit_upd[2][4])
);


virtual_pe #(
    .isCaster                    (isCaster_2_5),
    .stream_id                   (stream_id_2_5)
)pe_2_5(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[2][5]),
    .data_i_cast                 (cast_data_o[2][5]),
    .ready_o_cast                (pe_cast_ready_o[2][5]),
    .valid_o_cast                (pe_cast_valid_o[2][5]),
    .data_o_cast                 (pe_cast_data_o[2][5]),
    .ready_i_cast                (cast_ready_o[2][5]),
    .valid_i_merge               (merge_valid_o[2][5]),
    .data_i_merge                (merge_data_o[2][5]),
    .ready_o_merge               (pe_merge_ready_o[2][5]),
    .valid_o_merge               (pe_merge_valid_o[2][5]),
    .data_o_merge                (pe_merge_data_o[2][5]),
    .ready_i_merge               (merge_ready_o[2][5]),
    .credit_upd                  (credit_upd[2][5])
);


virtual_pe #(
    .isCaster                    (isCaster_2_6),
    .stream_id                   (stream_id_2_6)
)pe_2_6(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[2][6]),
    .data_i_cast                 (cast_data_o[2][6]),
    .ready_o_cast                (pe_cast_ready_o[2][6]),
    .valid_o_cast                (pe_cast_valid_o[2][6]),
    .data_o_cast                 (pe_cast_data_o[2][6]),
    .ready_i_cast                (cast_ready_o[2][6]),
    .valid_i_merge               (merge_valid_o[2][6]),
    .data_i_merge                (merge_data_o[2][6]),
    .ready_o_merge               (pe_merge_ready_o[2][6]),
    .valid_o_merge               (pe_merge_valid_o[2][6]),
    .data_o_merge                (pe_merge_data_o[2][6]),
    .ready_i_merge               (merge_ready_o[2][6]),
    .credit_upd                  (credit_upd[2][6])
);


virtual_pe #(
    .isCaster                    (isCaster_2_7),
    .stream_id                   (stream_id_2_7)
)pe_2_7(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[2][7]),
    .data_i_cast                 (cast_data_o[2][7]),
    .ready_o_cast                (pe_cast_ready_o[2][7]),
    .valid_o_cast                (pe_cast_valid_o[2][7]),
    .data_o_cast                 (pe_cast_data_o[2][7]),
    .ready_i_cast                (cast_ready_o[2][7]),
    .valid_i_merge               (merge_valid_o[2][7]),
    .data_i_merge                (merge_data_o[2][7]),
    .ready_o_merge               (pe_merge_ready_o[2][7]),
    .valid_o_merge               (pe_merge_valid_o[2][7]),
    .data_o_merge                (pe_merge_data_o[2][7]),
    .ready_i_merge               (merge_ready_o[2][7]),
    .credit_upd                  (credit_upd[2][7])
);


virtual_pe #(
    .isCaster                    (isCaster_3_0),
    .stream_id                   (stream_id_3_0)
)pe_3_0(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[3][0]),
    .data_i_cast                 (cast_data_o[3][0]),
    .ready_o_cast                (pe_cast_ready_o[3][0]),
    .valid_o_cast                (pe_cast_valid_o[3][0]),
    .data_o_cast                 (pe_cast_data_o[3][0]),
    .ready_i_cast                (cast_ready_o[3][0]),
    .valid_i_merge               (merge_valid_o[3][0]),
    .data_i_merge                (merge_data_o[3][0]),
    .ready_o_merge               (pe_merge_ready_o[3][0]),
    .valid_o_merge               (pe_merge_valid_o[3][0]),
    .data_o_merge                (pe_merge_data_o[3][0]),
    .ready_i_merge               (merge_ready_o[3][0]),
    .credit_upd                  (credit_upd[3][0])
);


virtual_pe #(
    .isCaster                    (isCaster_3_1),
    .stream_id                   (stream_id_3_1)
)pe_3_1(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[3][1]),
    .data_i_cast                 (cast_data_o[3][1]),
    .ready_o_cast                (pe_cast_ready_o[3][1]),
    .valid_o_cast                (pe_cast_valid_o[3][1]),
    .data_o_cast                 (pe_cast_data_o[3][1]),
    .ready_i_cast                (cast_ready_o[3][1]),
    .valid_i_merge               (merge_valid_o[3][1]),
    .data_i_merge                (merge_data_o[3][1]),
    .ready_o_merge               (pe_merge_ready_o[3][1]),
    .valid_o_merge               (pe_merge_valid_o[3][1]),
    .data_o_merge                (pe_merge_data_o[3][1]),
    .ready_i_merge               (merge_ready_o[3][1]),
    .credit_upd                  (credit_upd[3][1])
);


virtual_pe #(
    .isCaster                    (isCaster_3_2),
    .stream_id                   (stream_id_3_2)
)pe_3_2(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[3][2]),
    .data_i_cast                 (cast_data_o[3][2]),
    .ready_o_cast                (pe_cast_ready_o[3][2]),
    .valid_o_cast                (pe_cast_valid_o[3][2]),
    .data_o_cast                 (pe_cast_data_o[3][2]),
    .ready_i_cast                (cast_ready_o[3][2]),
    .valid_i_merge               (merge_valid_o[3][2]),
    .data_i_merge                (merge_data_o[3][2]),
    .ready_o_merge               (pe_merge_ready_o[3][2]),
    .valid_o_merge               (pe_merge_valid_o[3][2]),
    .data_o_merge                (pe_merge_data_o[3][2]),
    .ready_i_merge               (merge_ready_o[3][2]),
    .credit_upd                  (credit_upd[3][2])
);


virtual_pe #(
    .isCaster                    (isCaster_3_3),
    .stream_id                   (stream_id_3_3)
)pe_3_3(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[3][3]),
    .data_i_cast                 (cast_data_o[3][3]),
    .ready_o_cast                (pe_cast_ready_o[3][3]),
    .valid_o_cast                (pe_cast_valid_o[3][3]),
    .data_o_cast                 (pe_cast_data_o[3][3]),
    .ready_i_cast                (cast_ready_o[3][3]),
    .valid_i_merge               (merge_valid_o[3][3]),
    .data_i_merge                (merge_data_o[3][3]),
    .ready_o_merge               (pe_merge_ready_o[3][3]),
    .valid_o_merge               (pe_merge_valid_o[3][3]),
    .data_o_merge                (pe_merge_data_o[3][3]),
    .ready_i_merge               (merge_ready_o[3][3]),
    .credit_upd                  (credit_upd[3][3])
);


virtual_pe #(
    .isCaster                    (isCaster_3_4),
    .stream_id                   (stream_id_3_4)
)pe_3_4(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[3][4]),
    .data_i_cast                 (cast_data_o[3][4]),
    .ready_o_cast                (pe_cast_ready_o[3][4]),
    .valid_o_cast                (pe_cast_valid_o[3][4]),
    .data_o_cast                 (pe_cast_data_o[3][4]),
    .ready_i_cast                (cast_ready_o[3][4]),
    .valid_i_merge               (merge_valid_o[3][4]),
    .data_i_merge                (merge_data_o[3][4]),
    .ready_o_merge               (pe_merge_ready_o[3][4]),
    .valid_o_merge               (pe_merge_valid_o[3][4]),
    .data_o_merge                (pe_merge_data_o[3][4]),
    .ready_i_merge               (merge_ready_o[3][4]),
    .credit_upd                  (credit_upd[3][4])
);


virtual_pe #(
    .isCaster                    (isCaster_3_5),
    .stream_id                   (stream_id_3_5)
)pe_3_5(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[3][5]),
    .data_i_cast                 (cast_data_o[3][5]),
    .ready_o_cast                (pe_cast_ready_o[3][5]),
    .valid_o_cast                (pe_cast_valid_o[3][5]),
    .data_o_cast                 (pe_cast_data_o[3][5]),
    .ready_i_cast                (cast_ready_o[3][5]),
    .valid_i_merge               (merge_valid_o[3][5]),
    .data_i_merge                (merge_data_o[3][5]),
    .ready_o_merge               (pe_merge_ready_o[3][5]),
    .valid_o_merge               (pe_merge_valid_o[3][5]),
    .data_o_merge                (pe_merge_data_o[3][5]),
    .ready_i_merge               (merge_ready_o[3][5]),
    .credit_upd                  (credit_upd[3][5])
);


virtual_pe #(
    .isCaster                    (isCaster_3_6),
    .stream_id                   (stream_id_3_6)
)pe_3_6(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[3][6]),
    .data_i_cast                 (cast_data_o[3][6]),
    .ready_o_cast                (pe_cast_ready_o[3][6]),
    .valid_o_cast                (pe_cast_valid_o[3][6]),
    .data_o_cast                 (pe_cast_data_o[3][6]),
    .ready_i_cast                (cast_ready_o[3][6]),
    .valid_i_merge               (merge_valid_o[3][6]),
    .data_i_merge                (merge_data_o[3][6]),
    .ready_o_merge               (pe_merge_ready_o[3][6]),
    .valid_o_merge               (pe_merge_valid_o[3][6]),
    .data_o_merge                (pe_merge_data_o[3][6]),
    .ready_i_merge               (merge_ready_o[3][6]),
    .credit_upd                  (credit_upd[3][6])
);


virtual_pe #(
    .isCaster                    (isCaster_3_7),
    .stream_id                   (stream_id_3_7)
)pe_3_7(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[3][7]),
    .data_i_cast                 (cast_data_o[3][7]),
    .ready_o_cast                (pe_cast_ready_o[3][7]),
    .valid_o_cast                (pe_cast_valid_o[3][7]),
    .data_o_cast                 (pe_cast_data_o[3][7]),
    .ready_i_cast                (cast_ready_o[3][7]),
    .valid_i_merge               (merge_valid_o[3][7]),
    .data_i_merge                (merge_data_o[3][7]),
    .ready_o_merge               (pe_merge_ready_o[3][7]),
    .valid_o_merge               (pe_merge_valid_o[3][7]),
    .data_o_merge                (pe_merge_data_o[3][7]),
    .ready_i_merge               (merge_ready_o[3][7]),
    .credit_upd                  (credit_upd[3][7])
);


virtual_pe #(
    .isCaster                    (isCaster_4_0),
    .stream_id                   (stream_id_4_0)
)pe_4_0(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[4][0]),
    .data_i_cast                 (cast_data_o[4][0]),
    .ready_o_cast                (pe_cast_ready_o[4][0]),
    .valid_o_cast                (pe_cast_valid_o[4][0]),
    .data_o_cast                 (pe_cast_data_o[4][0]),
    .ready_i_cast                (cast_ready_o[4][0]),
    .valid_i_merge               (merge_valid_o[4][0]),
    .data_i_merge                (merge_data_o[4][0]),
    .ready_o_merge               (pe_merge_ready_o[4][0]),
    .valid_o_merge               (pe_merge_valid_o[4][0]),
    .data_o_merge                (pe_merge_data_o[4][0]),
    .ready_i_merge               (merge_ready_o[4][0]),
    .credit_upd                  (credit_upd[4][0])
);


virtual_pe #(
    .isCaster                    (isCaster_4_1),
    .stream_id                   (stream_id_4_1)
)pe_4_1(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[4][1]),
    .data_i_cast                 (cast_data_o[4][1]),
    .ready_o_cast                (pe_cast_ready_o[4][1]),
    .valid_o_cast                (pe_cast_valid_o[4][1]),
    .data_o_cast                 (pe_cast_data_o[4][1]),
    .ready_i_cast                (cast_ready_o[4][1]),
    .valid_i_merge               (merge_valid_o[4][1]),
    .data_i_merge                (merge_data_o[4][1]),
    .ready_o_merge               (pe_merge_ready_o[4][1]),
    .valid_o_merge               (pe_merge_valid_o[4][1]),
    .data_o_merge                (pe_merge_data_o[4][1]),
    .ready_i_merge               (merge_ready_o[4][1]),
    .credit_upd                  (credit_upd[4][1])
);


virtual_pe #(
    .isCaster                    (isCaster_4_2),
    .stream_id                   (stream_id_4_2)
)pe_4_2(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[4][2]),
    .data_i_cast                 (cast_data_o[4][2]),
    .ready_o_cast                (pe_cast_ready_o[4][2]),
    .valid_o_cast                (pe_cast_valid_o[4][2]),
    .data_o_cast                 (pe_cast_data_o[4][2]),
    .ready_i_cast                (cast_ready_o[4][2]),
    .valid_i_merge               (merge_valid_o[4][2]),
    .data_i_merge                (merge_data_o[4][2]),
    .ready_o_merge               (pe_merge_ready_o[4][2]),
    .valid_o_merge               (pe_merge_valid_o[4][2]),
    .data_o_merge                (pe_merge_data_o[4][2]),
    .ready_i_merge               (merge_ready_o[4][2]),
    .credit_upd                  (credit_upd[4][2])
);


virtual_pe #(
    .isCaster                    (isCaster_4_3),
    .stream_id                   (stream_id_4_3)
)pe_4_3(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[4][3]),
    .data_i_cast                 (cast_data_o[4][3]),
    .ready_o_cast                (pe_cast_ready_o[4][3]),
    .valid_o_cast                (pe_cast_valid_o[4][3]),
    .data_o_cast                 (pe_cast_data_o[4][3]),
    .ready_i_cast                (cast_ready_o[4][3]),
    .valid_i_merge               (merge_valid_o[4][3]),
    .data_i_merge                (merge_data_o[4][3]),
    .ready_o_merge               (pe_merge_ready_o[4][3]),
    .valid_o_merge               (pe_merge_valid_o[4][3]),
    .data_o_merge                (pe_merge_data_o[4][3]),
    .ready_i_merge               (merge_ready_o[4][3]),
    .credit_upd                  (credit_upd[4][3])
);


virtual_pe #(
    .isCaster                    (isCaster_4_4),
    .stream_id                   (stream_id_4_4)
)pe_4_4(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[4][4]),
    .data_i_cast                 (cast_data_o[4][4]),
    .ready_o_cast                (pe_cast_ready_o[4][4]),
    .valid_o_cast                (pe_cast_valid_o[4][4]),
    .data_o_cast                 (pe_cast_data_o[4][4]),
    .ready_i_cast                (cast_ready_o[4][4]),
    .valid_i_merge               (merge_valid_o[4][4]),
    .data_i_merge                (merge_data_o[4][4]),
    .ready_o_merge               (pe_merge_ready_o[4][4]),
    .valid_o_merge               (pe_merge_valid_o[4][4]),
    .data_o_merge                (pe_merge_data_o[4][4]),
    .ready_i_merge               (merge_ready_o[4][4]),
    .credit_upd                  (credit_upd[4][4])
);


virtual_pe #(
    .isCaster                    (isCaster_4_5),
    .stream_id                   (stream_id_4_5)
)pe_4_5(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[4][5]),
    .data_i_cast                 (cast_data_o[4][5]),
    .ready_o_cast                (pe_cast_ready_o[4][5]),
    .valid_o_cast                (pe_cast_valid_o[4][5]),
    .data_o_cast                 (pe_cast_data_o[4][5]),
    .ready_i_cast                (cast_ready_o[4][5]),
    .valid_i_merge               (merge_valid_o[4][5]),
    .data_i_merge                (merge_data_o[4][5]),
    .ready_o_merge               (pe_merge_ready_o[4][5]),
    .valid_o_merge               (pe_merge_valid_o[4][5]),
    .data_o_merge                (pe_merge_data_o[4][5]),
    .ready_i_merge               (merge_ready_o[4][5]),
    .credit_upd                  (credit_upd[4][5])
);


virtual_pe #(
    .isCaster                    (isCaster_4_6),
    .stream_id                   (stream_id_4_6)
)pe_4_6(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[4][6]),
    .data_i_cast                 (cast_data_o[4][6]),
    .ready_o_cast                (pe_cast_ready_o[4][6]),
    .valid_o_cast                (pe_cast_valid_o[4][6]),
    .data_o_cast                 (pe_cast_data_o[4][6]),
    .ready_i_cast                (cast_ready_o[4][6]),
    .valid_i_merge               (merge_valid_o[4][6]),
    .data_i_merge                (merge_data_o[4][6]),
    .ready_o_merge               (pe_merge_ready_o[4][6]),
    .valid_o_merge               (pe_merge_valid_o[4][6]),
    .data_o_merge                (pe_merge_data_o[4][6]),
    .ready_i_merge               (merge_ready_o[4][6]),
    .credit_upd                  (credit_upd[4][6])
);


virtual_pe #(
    .isCaster                    (isCaster_4_7),
    .stream_id                   (stream_id_4_7)
)pe_4_7(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[4][7]),
    .data_i_cast                 (cast_data_o[4][7]),
    .ready_o_cast                (pe_cast_ready_o[4][7]),
    .valid_o_cast                (pe_cast_valid_o[4][7]),
    .data_o_cast                 (pe_cast_data_o[4][7]),
    .ready_i_cast                (cast_ready_o[4][7]),
    .valid_i_merge               (merge_valid_o[4][7]),
    .data_i_merge                (merge_data_o[4][7]),
    .ready_o_merge               (pe_merge_ready_o[4][7]),
    .valid_o_merge               (pe_merge_valid_o[4][7]),
    .data_o_merge                (pe_merge_data_o[4][7]),
    .ready_i_merge               (merge_ready_o[4][7]),
    .credit_upd                  (credit_upd[4][7])
);


virtual_pe #(
    .isCaster                    (isCaster_5_0),
    .stream_id                   (stream_id_5_0)
)pe_5_0(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[5][0]),
    .data_i_cast                 (cast_data_o[5][0]),
    .ready_o_cast                (pe_cast_ready_o[5][0]),
    .valid_o_cast                (pe_cast_valid_o[5][0]),
    .data_o_cast                 (pe_cast_data_o[5][0]),
    .ready_i_cast                (cast_ready_o[5][0]),
    .valid_i_merge               (merge_valid_o[5][0]),
    .data_i_merge                (merge_data_o[5][0]),
    .ready_o_merge               (pe_merge_ready_o[5][0]),
    .valid_o_merge               (pe_merge_valid_o[5][0]),
    .data_o_merge                (pe_merge_data_o[5][0]),
    .ready_i_merge               (merge_ready_o[5][0]),
    .credit_upd                  (credit_upd[5][0])
);


virtual_pe #(
    .isCaster                    (isCaster_5_1),
    .stream_id                   (stream_id_5_1)
)pe_5_1(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[5][1]),
    .data_i_cast                 (cast_data_o[5][1]),
    .ready_o_cast                (pe_cast_ready_o[5][1]),
    .valid_o_cast                (pe_cast_valid_o[5][1]),
    .data_o_cast                 (pe_cast_data_o[5][1]),
    .ready_i_cast                (cast_ready_o[5][1]),
    .valid_i_merge               (merge_valid_o[5][1]),
    .data_i_merge                (merge_data_o[5][1]),
    .ready_o_merge               (pe_merge_ready_o[5][1]),
    .valid_o_merge               (pe_merge_valid_o[5][1]),
    .data_o_merge                (pe_merge_data_o[5][1]),
    .ready_i_merge               (merge_ready_o[5][1]),
    .credit_upd                  (credit_upd[5][1])
);


virtual_pe #(
    .isCaster                    (isCaster_5_2),
    .stream_id                   (stream_id_5_2)
)pe_5_2(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[5][2]),
    .data_i_cast                 (cast_data_o[5][2]),
    .ready_o_cast                (pe_cast_ready_o[5][2]),
    .valid_o_cast                (pe_cast_valid_o[5][2]),
    .data_o_cast                 (pe_cast_data_o[5][2]),
    .ready_i_cast                (cast_ready_o[5][2]),
    .valid_i_merge               (merge_valid_o[5][2]),
    .data_i_merge                (merge_data_o[5][2]),
    .ready_o_merge               (pe_merge_ready_o[5][2]),
    .valid_o_merge               (pe_merge_valid_o[5][2]),
    .data_o_merge                (pe_merge_data_o[5][2]),
    .ready_i_merge               (merge_ready_o[5][2]),
    .credit_upd                  (credit_upd[5][2])
);


virtual_pe #(
    .isCaster                    (isCaster_5_3),
    .stream_id                   (stream_id_5_3)
)pe_5_3(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[5][3]),
    .data_i_cast                 (cast_data_o[5][3]),
    .ready_o_cast                (pe_cast_ready_o[5][3]),
    .valid_o_cast                (pe_cast_valid_o[5][3]),
    .data_o_cast                 (pe_cast_data_o[5][3]),
    .ready_i_cast                (cast_ready_o[5][3]),
    .valid_i_merge               (merge_valid_o[5][3]),
    .data_i_merge                (merge_data_o[5][3]),
    .ready_o_merge               (pe_merge_ready_o[5][3]),
    .valid_o_merge               (pe_merge_valid_o[5][3]),
    .data_o_merge                (pe_merge_data_o[5][3]),
    .ready_i_merge               (merge_ready_o[5][3]),
    .credit_upd                  (credit_upd[5][3])
);


virtual_pe #(
    .isCaster                    (isCaster_5_4),
    .stream_id                   (stream_id_5_4)
)pe_5_4(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[5][4]),
    .data_i_cast                 (cast_data_o[5][4]),
    .ready_o_cast                (pe_cast_ready_o[5][4]),
    .valid_o_cast                (pe_cast_valid_o[5][4]),
    .data_o_cast                 (pe_cast_data_o[5][4]),
    .ready_i_cast                (cast_ready_o[5][4]),
    .valid_i_merge               (merge_valid_o[5][4]),
    .data_i_merge                (merge_data_o[5][4]),
    .ready_o_merge               (pe_merge_ready_o[5][4]),
    .valid_o_merge               (pe_merge_valid_o[5][4]),
    .data_o_merge                (pe_merge_data_o[5][4]),
    .ready_i_merge               (merge_ready_o[5][4]),
    .credit_upd                  (credit_upd[5][4])
);


virtual_pe #(
    .isCaster                    (isCaster_5_5),
    .stream_id                   (stream_id_5_5)
)pe_5_5(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[5][5]),
    .data_i_cast                 (cast_data_o[5][5]),
    .ready_o_cast                (pe_cast_ready_o[5][5]),
    .valid_o_cast                (pe_cast_valid_o[5][5]),
    .data_o_cast                 (pe_cast_data_o[5][5]),
    .ready_i_cast                (cast_ready_o[5][5]),
    .valid_i_merge               (merge_valid_o[5][5]),
    .data_i_merge                (merge_data_o[5][5]),
    .ready_o_merge               (pe_merge_ready_o[5][5]),
    .valid_o_merge               (pe_merge_valid_o[5][5]),
    .data_o_merge                (pe_merge_data_o[5][5]),
    .ready_i_merge               (merge_ready_o[5][5]),
    .credit_upd                  (credit_upd[5][5])
);


virtual_pe #(
    .isCaster                    (isCaster_5_6),
    .stream_id                   (stream_id_5_6)
)pe_5_6(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[5][6]),
    .data_i_cast                 (cast_data_o[5][6]),
    .ready_o_cast                (pe_cast_ready_o[5][6]),
    .valid_o_cast                (pe_cast_valid_o[5][6]),
    .data_o_cast                 (pe_cast_data_o[5][6]),
    .ready_i_cast                (cast_ready_o[5][6]),
    .valid_i_merge               (merge_valid_o[5][6]),
    .data_i_merge                (merge_data_o[5][6]),
    .ready_o_merge               (pe_merge_ready_o[5][6]),
    .valid_o_merge               (pe_merge_valid_o[5][6]),
    .data_o_merge                (pe_merge_data_o[5][6]),
    .ready_i_merge               (merge_ready_o[5][6]),
    .credit_upd                  (credit_upd[5][6])
);


virtual_pe #(
    .isCaster                    (isCaster_5_7),
    .stream_id                   (stream_id_5_7)
)pe_5_7(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[5][7]),
    .data_i_cast                 (cast_data_o[5][7]),
    .ready_o_cast                (pe_cast_ready_o[5][7]),
    .valid_o_cast                (pe_cast_valid_o[5][7]),
    .data_o_cast                 (pe_cast_data_o[5][7]),
    .ready_i_cast                (cast_ready_o[5][7]),
    .valid_i_merge               (merge_valid_o[5][7]),
    .data_i_merge                (merge_data_o[5][7]),
    .ready_o_merge               (pe_merge_ready_o[5][7]),
    .valid_o_merge               (pe_merge_valid_o[5][7]),
    .data_o_merge                (pe_merge_data_o[5][7]),
    .ready_i_merge               (merge_ready_o[5][7]),
    .credit_upd                  (credit_upd[5][7])
);


virtual_pe #(
    .isCaster                    (isCaster_6_0),
    .stream_id                   (stream_id_6_0)
)pe_6_0(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[6][0]),
    .data_i_cast                 (cast_data_o[6][0]),
    .ready_o_cast                (pe_cast_ready_o[6][0]),
    .valid_o_cast                (pe_cast_valid_o[6][0]),
    .data_o_cast                 (pe_cast_data_o[6][0]),
    .ready_i_cast                (cast_ready_o[6][0]),
    .valid_i_merge               (merge_valid_o[6][0]),
    .data_i_merge                (merge_data_o[6][0]),
    .ready_o_merge               (pe_merge_ready_o[6][0]),
    .valid_o_merge               (pe_merge_valid_o[6][0]),
    .data_o_merge                (pe_merge_data_o[6][0]),
    .ready_i_merge               (merge_ready_o[6][0]),
    .credit_upd                  (credit_upd[6][0])
);


virtual_pe #(
    .isCaster                    (isCaster_6_1),
    .stream_id                   (stream_id_6_1)
)pe_6_1(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[6][1]),
    .data_i_cast                 (cast_data_o[6][1]),
    .ready_o_cast                (pe_cast_ready_o[6][1]),
    .valid_o_cast                (pe_cast_valid_o[6][1]),
    .data_o_cast                 (pe_cast_data_o[6][1]),
    .ready_i_cast                (cast_ready_o[6][1]),
    .valid_i_merge               (merge_valid_o[6][1]),
    .data_i_merge                (merge_data_o[6][1]),
    .ready_o_merge               (pe_merge_ready_o[6][1]),
    .valid_o_merge               (pe_merge_valid_o[6][1]),
    .data_o_merge                (pe_merge_data_o[6][1]),
    .ready_i_merge               (merge_ready_o[6][1]),
    .credit_upd                  (credit_upd[6][1])
);


virtual_pe #(
    .isCaster                    (isCaster_6_2),
    .stream_id                   (stream_id_6_2)
)pe_6_2(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[6][2]),
    .data_i_cast                 (cast_data_o[6][2]),
    .ready_o_cast                (pe_cast_ready_o[6][2]),
    .valid_o_cast                (pe_cast_valid_o[6][2]),
    .data_o_cast                 (pe_cast_data_o[6][2]),
    .ready_i_cast                (cast_ready_o[6][2]),
    .valid_i_merge               (merge_valid_o[6][2]),
    .data_i_merge                (merge_data_o[6][2]),
    .ready_o_merge               (pe_merge_ready_o[6][2]),
    .valid_o_merge               (pe_merge_valid_o[6][2]),
    .data_o_merge                (pe_merge_data_o[6][2]),
    .ready_i_merge               (merge_ready_o[6][2]),
    .credit_upd                  (credit_upd[6][2])
);


virtual_pe #(
    .isCaster                    (isCaster_6_3),
    .stream_id                   (stream_id_6_3)
)pe_6_3(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[6][3]),
    .data_i_cast                 (cast_data_o[6][3]),
    .ready_o_cast                (pe_cast_ready_o[6][3]),
    .valid_o_cast                (pe_cast_valid_o[6][3]),
    .data_o_cast                 (pe_cast_data_o[6][3]),
    .ready_i_cast                (cast_ready_o[6][3]),
    .valid_i_merge               (merge_valid_o[6][3]),
    .data_i_merge                (merge_data_o[6][3]),
    .ready_o_merge               (pe_merge_ready_o[6][3]),
    .valid_o_merge               (pe_merge_valid_o[6][3]),
    .data_o_merge                (pe_merge_data_o[6][3]),
    .ready_i_merge               (merge_ready_o[6][3]),
    .credit_upd                  (credit_upd[6][3])
);


virtual_pe #(
    .isCaster                    (isCaster_6_4),
    .stream_id                   (stream_id_6_4)
)pe_6_4(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[6][4]),
    .data_i_cast                 (cast_data_o[6][4]),
    .ready_o_cast                (pe_cast_ready_o[6][4]),
    .valid_o_cast                (pe_cast_valid_o[6][4]),
    .data_o_cast                 (pe_cast_data_o[6][4]),
    .ready_i_cast                (cast_ready_o[6][4]),
    .valid_i_merge               (merge_valid_o[6][4]),
    .data_i_merge                (merge_data_o[6][4]),
    .ready_o_merge               (pe_merge_ready_o[6][4]),
    .valid_o_merge               (pe_merge_valid_o[6][4]),
    .data_o_merge                (pe_merge_data_o[6][4]),
    .ready_i_merge               (merge_ready_o[6][4]),
    .credit_upd                  (credit_upd[6][4])
);


virtual_pe #(
    .isCaster                    (isCaster_6_5),
    .stream_id                   (stream_id_6_5)
)pe_6_5(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[6][5]),
    .data_i_cast                 (cast_data_o[6][5]),
    .ready_o_cast                (pe_cast_ready_o[6][5]),
    .valid_o_cast                (pe_cast_valid_o[6][5]),
    .data_o_cast                 (pe_cast_data_o[6][5]),
    .ready_i_cast                (cast_ready_o[6][5]),
    .valid_i_merge               (merge_valid_o[6][5]),
    .data_i_merge                (merge_data_o[6][5]),
    .ready_o_merge               (pe_merge_ready_o[6][5]),
    .valid_o_merge               (pe_merge_valid_o[6][5]),
    .data_o_merge                (pe_merge_data_o[6][5]),
    .ready_i_merge               (merge_ready_o[6][5]),
    .credit_upd                  (credit_upd[6][5])
);


virtual_pe #(
    .isCaster                    (isCaster_6_6),
    .stream_id                   (stream_id_6_6)
)pe_6_6(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[6][6]),
    .data_i_cast                 (cast_data_o[6][6]),
    .ready_o_cast                (pe_cast_ready_o[6][6]),
    .valid_o_cast                (pe_cast_valid_o[6][6]),
    .data_o_cast                 (pe_cast_data_o[6][6]),
    .ready_i_cast                (cast_ready_o[6][6]),
    .valid_i_merge               (merge_valid_o[6][6]),
    .data_i_merge                (merge_data_o[6][6]),
    .ready_o_merge               (pe_merge_ready_o[6][6]),
    .valid_o_merge               (pe_merge_valid_o[6][6]),
    .data_o_merge                (pe_merge_data_o[6][6]),
    .ready_i_merge               (merge_ready_o[6][6]),
    .credit_upd                  (credit_upd[6][6])
);


virtual_pe #(
    .isCaster                    (isCaster_6_7),
    .stream_id                   (stream_id_6_7)
)pe_6_7(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o[6][7]),
    .data_i_cast                 (cast_data_o[6][7]),
    .ready_o_cast                (pe_cast_ready_o[6][7]),
    .valid_o_cast                (pe_cast_valid_o[6][7]),
    .data_o_cast                 (pe_cast_data_o[6][7]),
    .ready_i_cast                (cast_ready_o[6][7]),
    .valid_i_merge               (merge_valid_o[6][7]),
    .data_i_merge                (merge_data_o[6][7]),
    .ready_o_merge               (pe_merge_ready_o[6][7]),
    .valid_o_merge               (pe_merge_valid_o[6][7]),
    .data_o_merge                (pe_merge_data_o[6][7]),
    .ready_i_merge               (merge_ready_o[6][7]),
    .credit_upd                  (credit_upd[6][7])
); 

endmodule