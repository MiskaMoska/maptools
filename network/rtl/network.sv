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

        input       wire        [`DW-1:0]       cast_data_i_0_0,
        input       wire                        cast_valid_i_0_0,
        output      wire                        cast_ready_o_0_0,

        output      wire        [`DW-1:0]       cast_data_o_0_0,
        output      wire                        cast_valid_o_0_0,
        input       wire                        cast_ready_i_0_0,

        input       wire        [`DW-1:0]       cast_data_i_0_1,
        input       wire                        cast_valid_i_0_1,
        output      wire                        cast_ready_o_0_1,

        output      wire        [`DW-1:0]       cast_data_o_0_1,
        output      wire                        cast_valid_o_0_1,
        input       wire                        cast_ready_i_0_1,

        input       wire        [`DW-1:0]       cast_data_i_0_2,
        input       wire                        cast_valid_i_0_2,
        output      wire                        cast_ready_o_0_2,

        output      wire        [`DW-1:0]       cast_data_o_0_2,
        output      wire                        cast_valid_o_0_2,
        input       wire                        cast_ready_i_0_2,

        input       wire        [`DW-1:0]       cast_data_i_0_3,
        input       wire                        cast_valid_i_0_3,
        output      wire                        cast_ready_o_0_3,

        output      wire        [`DW-1:0]       cast_data_o_0_3,
        output      wire                        cast_valid_o_0_3,
        input       wire                        cast_ready_i_0_3,

        input       wire        [`DW-1:0]       cast_data_i_0_4,
        input       wire                        cast_valid_i_0_4,
        output      wire                        cast_ready_o_0_4,

        output      wire        [`DW-1:0]       cast_data_o_0_4,
        output      wire                        cast_valid_o_0_4,
        input       wire                        cast_ready_i_0_4,

        input       wire        [`DW-1:0]       cast_data_i_0_5,
        input       wire                        cast_valid_i_0_5,
        output      wire                        cast_ready_o_0_5,

        output      wire        [`DW-1:0]       cast_data_o_0_5,
        output      wire                        cast_valid_o_0_5,
        input       wire                        cast_ready_i_0_5,

        input       wire        [`DW-1:0]       cast_data_i_0_6,
        input       wire                        cast_valid_i_0_6,
        output      wire                        cast_ready_o_0_6,

        output      wire        [`DW-1:0]       cast_data_o_0_6,
        output      wire                        cast_valid_o_0_6,
        input       wire                        cast_ready_i_0_6,

        input       wire        [`DW-1:0]       cast_data_i_0_7,
        input       wire                        cast_valid_i_0_7,
        output      wire                        cast_ready_o_0_7,

        output      wire        [`DW-1:0]       cast_data_o_0_7,
        output      wire                        cast_valid_o_0_7,
        input       wire                        cast_ready_i_0_7,

        input       wire        [`DW-1:0]       cast_data_i_1_0,
        input       wire                        cast_valid_i_1_0,
        output      wire                        cast_ready_o_1_0,

        output      wire        [`DW-1:0]       cast_data_o_1_0,
        output      wire                        cast_valid_o_1_0,
        input       wire                        cast_ready_i_1_0,

        input       wire        [`DW-1:0]       cast_data_i_1_1,
        input       wire                        cast_valid_i_1_1,
        output      wire                        cast_ready_o_1_1,

        output      wire        [`DW-1:0]       cast_data_o_1_1,
        output      wire                        cast_valid_o_1_1,
        input       wire                        cast_ready_i_1_1,

        input       wire        [`DW-1:0]       cast_data_i_1_2,
        input       wire                        cast_valid_i_1_2,
        output      wire                        cast_ready_o_1_2,

        output      wire        [`DW-1:0]       cast_data_o_1_2,
        output      wire                        cast_valid_o_1_2,
        input       wire                        cast_ready_i_1_2,

        input       wire        [`DW-1:0]       cast_data_i_1_3,
        input       wire                        cast_valid_i_1_3,
        output      wire                        cast_ready_o_1_3,

        output      wire        [`DW-1:0]       cast_data_o_1_3,
        output      wire                        cast_valid_o_1_3,
        input       wire                        cast_ready_i_1_3,

        input       wire        [`DW-1:0]       cast_data_i_1_4,
        input       wire                        cast_valid_i_1_4,
        output      wire                        cast_ready_o_1_4,

        output      wire        [`DW-1:0]       cast_data_o_1_4,
        output      wire                        cast_valid_o_1_4,
        input       wire                        cast_ready_i_1_4,

        input       wire        [`DW-1:0]       cast_data_i_1_5,
        input       wire                        cast_valid_i_1_5,
        output      wire                        cast_ready_o_1_5,

        output      wire        [`DW-1:0]       cast_data_o_1_5,
        output      wire                        cast_valid_o_1_5,
        input       wire                        cast_ready_i_1_5,

        input       wire        [`DW-1:0]       cast_data_i_1_6,
        input       wire                        cast_valid_i_1_6,
        output      wire                        cast_ready_o_1_6,

        output      wire        [`DW-1:0]       cast_data_o_1_6,
        output      wire                        cast_valid_o_1_6,
        input       wire                        cast_ready_i_1_6,

        input       wire        [`DW-1:0]       cast_data_i_1_7,
        input       wire                        cast_valid_i_1_7,
        output      wire                        cast_ready_o_1_7,

        output      wire        [`DW-1:0]       cast_data_o_1_7,
        output      wire                        cast_valid_o_1_7,
        input       wire                        cast_ready_i_1_7,

        input       wire        [`DW-1:0]       cast_data_i_2_0,
        input       wire                        cast_valid_i_2_0,
        output      wire                        cast_ready_o_2_0,

        output      wire        [`DW-1:0]       cast_data_o_2_0,
        output      wire                        cast_valid_o_2_0,
        input       wire                        cast_ready_i_2_0,

        input       wire        [`DW-1:0]       cast_data_i_2_1,
        input       wire                        cast_valid_i_2_1,
        output      wire                        cast_ready_o_2_1,

        output      wire        [`DW-1:0]       cast_data_o_2_1,
        output      wire                        cast_valid_o_2_1,
        input       wire                        cast_ready_i_2_1,

        input       wire        [`DW-1:0]       cast_data_i_2_2,
        input       wire                        cast_valid_i_2_2,
        output      wire                        cast_ready_o_2_2,

        output      wire        [`DW-1:0]       cast_data_o_2_2,
        output      wire                        cast_valid_o_2_2,
        input       wire                        cast_ready_i_2_2,

        input       wire        [`DW-1:0]       cast_data_i_2_3,
        input       wire                        cast_valid_i_2_3,
        output      wire                        cast_ready_o_2_3,

        output      wire        [`DW-1:0]       cast_data_o_2_3,
        output      wire                        cast_valid_o_2_3,
        input       wire                        cast_ready_i_2_3,

        input       wire        [`DW-1:0]       cast_data_i_2_4,
        input       wire                        cast_valid_i_2_4,
        output      wire                        cast_ready_o_2_4,

        output      wire        [`DW-1:0]       cast_data_o_2_4,
        output      wire                        cast_valid_o_2_4,
        input       wire                        cast_ready_i_2_4,

        input       wire        [`DW-1:0]       cast_data_i_2_5,
        input       wire                        cast_valid_i_2_5,
        output      wire                        cast_ready_o_2_5,

        output      wire        [`DW-1:0]       cast_data_o_2_5,
        output      wire                        cast_valid_o_2_5,
        input       wire                        cast_ready_i_2_5,

        input       wire        [`DW-1:0]       cast_data_i_2_6,
        input       wire                        cast_valid_i_2_6,
        output      wire                        cast_ready_o_2_6,

        output      wire        [`DW-1:0]       cast_data_o_2_6,
        output      wire                        cast_valid_o_2_6,
        input       wire                        cast_ready_i_2_6,

        input       wire        [`DW-1:0]       cast_data_i_2_7,
        input       wire                        cast_valid_i_2_7,
        output      wire                        cast_ready_o_2_7,

        output      wire        [`DW-1:0]       cast_data_o_2_7,
        output      wire                        cast_valid_o_2_7,
        input       wire                        cast_ready_i_2_7,

        input       wire        [`DW-1:0]       cast_data_i_3_0,
        input       wire                        cast_valid_i_3_0,
        output      wire                        cast_ready_o_3_0,

        output      wire        [`DW-1:0]       cast_data_o_3_0,
        output      wire                        cast_valid_o_3_0,
        input       wire                        cast_ready_i_3_0,

        input       wire        [`DW-1:0]       cast_data_i_3_1,
        input       wire                        cast_valid_i_3_1,
        output      wire                        cast_ready_o_3_1,

        output      wire        [`DW-1:0]       cast_data_o_3_1,
        output      wire                        cast_valid_o_3_1,
        input       wire                        cast_ready_i_3_1,

        input       wire        [`DW-1:0]       cast_data_i_3_2,
        input       wire                        cast_valid_i_3_2,
        output      wire                        cast_ready_o_3_2,

        output      wire        [`DW-1:0]       cast_data_o_3_2,
        output      wire                        cast_valid_o_3_2,
        input       wire                        cast_ready_i_3_2,

        input       wire        [`DW-1:0]       cast_data_i_3_3,
        input       wire                        cast_valid_i_3_3,
        output      wire                        cast_ready_o_3_3,

        output      wire        [`DW-1:0]       cast_data_o_3_3,
        output      wire                        cast_valid_o_3_3,
        input       wire                        cast_ready_i_3_3,

        input       wire        [`DW-1:0]       cast_data_i_3_4,
        input       wire                        cast_valid_i_3_4,
        output      wire                        cast_ready_o_3_4,

        output      wire        [`DW-1:0]       cast_data_o_3_4,
        output      wire                        cast_valid_o_3_4,
        input       wire                        cast_ready_i_3_4,

        input       wire        [`DW-1:0]       cast_data_i_3_5,
        input       wire                        cast_valid_i_3_5,
        output      wire                        cast_ready_o_3_5,

        output      wire        [`DW-1:0]       cast_data_o_3_5,
        output      wire                        cast_valid_o_3_5,
        input       wire                        cast_ready_i_3_5,

        input       wire        [`DW-1:0]       cast_data_i_3_6,
        input       wire                        cast_valid_i_3_6,
        output      wire                        cast_ready_o_3_6,

        output      wire        [`DW-1:0]       cast_data_o_3_6,
        output      wire                        cast_valid_o_3_6,
        input       wire                        cast_ready_i_3_6,

        input       wire        [`DW-1:0]       cast_data_i_3_7,
        input       wire                        cast_valid_i_3_7,
        output      wire                        cast_ready_o_3_7,

        output      wire        [`DW-1:0]       cast_data_o_3_7,
        output      wire                        cast_valid_o_3_7,
        input       wire                        cast_ready_i_3_7,

        input       wire        [`DW-1:0]       cast_data_i_4_0,
        input       wire                        cast_valid_i_4_0,
        output      wire                        cast_ready_o_4_0,

        output      wire        [`DW-1:0]       cast_data_o_4_0,
        output      wire                        cast_valid_o_4_0,
        input       wire                        cast_ready_i_4_0,

        input       wire        [`DW-1:0]       cast_data_i_4_1,
        input       wire                        cast_valid_i_4_1,
        output      wire                        cast_ready_o_4_1,

        output      wire        [`DW-1:0]       cast_data_o_4_1,
        output      wire                        cast_valid_o_4_1,
        input       wire                        cast_ready_i_4_1,

        input       wire        [`DW-1:0]       cast_data_i_4_2,
        input       wire                        cast_valid_i_4_2,
        output      wire                        cast_ready_o_4_2,

        output      wire        [`DW-1:0]       cast_data_o_4_2,
        output      wire                        cast_valid_o_4_2,
        input       wire                        cast_ready_i_4_2,

        input       wire        [`DW-1:0]       cast_data_i_4_3,
        input       wire                        cast_valid_i_4_3,
        output      wire                        cast_ready_o_4_3,

        output      wire        [`DW-1:0]       cast_data_o_4_3,
        output      wire                        cast_valid_o_4_3,
        input       wire                        cast_ready_i_4_3,

        input       wire        [`DW-1:0]       cast_data_i_4_4,
        input       wire                        cast_valid_i_4_4,
        output      wire                        cast_ready_o_4_4,

        output      wire        [`DW-1:0]       cast_data_o_4_4,
        output      wire                        cast_valid_o_4_4,
        input       wire                        cast_ready_i_4_4,

        input       wire        [`DW-1:0]       cast_data_i_4_5,
        input       wire                        cast_valid_i_4_5,
        output      wire                        cast_ready_o_4_5,

        output      wire        [`DW-1:0]       cast_data_o_4_5,
        output      wire                        cast_valid_o_4_5,
        input       wire                        cast_ready_i_4_5,

        input       wire        [`DW-1:0]       cast_data_i_4_6,
        input       wire                        cast_valid_i_4_6,
        output      wire                        cast_ready_o_4_6,

        output      wire        [`DW-1:0]       cast_data_o_4_6,
        output      wire                        cast_valid_o_4_6,
        input       wire                        cast_ready_i_4_6,

        input       wire        [`DW-1:0]       cast_data_i_4_7,
        input       wire                        cast_valid_i_4_7,
        output      wire                        cast_ready_o_4_7,

        output      wire        [`DW-1:0]       cast_data_o_4_7,
        output      wire                        cast_valid_o_4_7,
        input       wire                        cast_ready_i_4_7,

        input       wire        [`DW-1:0]       cast_data_i_5_0,
        input       wire                        cast_valid_i_5_0,
        output      wire                        cast_ready_o_5_0,

        output      wire        [`DW-1:0]       cast_data_o_5_0,
        output      wire                        cast_valid_o_5_0,
        input       wire                        cast_ready_i_5_0,

        input       wire        [`DW-1:0]       cast_data_i_5_1,
        input       wire                        cast_valid_i_5_1,
        output      wire                        cast_ready_o_5_1,

        output      wire        [`DW-1:0]       cast_data_o_5_1,
        output      wire                        cast_valid_o_5_1,
        input       wire                        cast_ready_i_5_1,

        input       wire        [`DW-1:0]       cast_data_i_5_2,
        input       wire                        cast_valid_i_5_2,
        output      wire                        cast_ready_o_5_2,

        output      wire        [`DW-1:0]       cast_data_o_5_2,
        output      wire                        cast_valid_o_5_2,
        input       wire                        cast_ready_i_5_2,

        input       wire        [`DW-1:0]       cast_data_i_5_3,
        input       wire                        cast_valid_i_5_3,
        output      wire                        cast_ready_o_5_3,

        output      wire        [`DW-1:0]       cast_data_o_5_3,
        output      wire                        cast_valid_o_5_3,
        input       wire                        cast_ready_i_5_3,

        input       wire        [`DW-1:0]       cast_data_i_5_4,
        input       wire                        cast_valid_i_5_4,
        output      wire                        cast_ready_o_5_4,

        output      wire        [`DW-1:0]       cast_data_o_5_4,
        output      wire                        cast_valid_o_5_4,
        input       wire                        cast_ready_i_5_4,

        input       wire        [`DW-1:0]       cast_data_i_5_5,
        input       wire                        cast_valid_i_5_5,
        output      wire                        cast_ready_o_5_5,

        output      wire        [`DW-1:0]       cast_data_o_5_5,
        output      wire                        cast_valid_o_5_5,
        input       wire                        cast_ready_i_5_5,

        input       wire        [`DW-1:0]       cast_data_i_5_6,
        input       wire                        cast_valid_i_5_6,
        output      wire                        cast_ready_o_5_6,

        output      wire        [`DW-1:0]       cast_data_o_5_6,
        output      wire                        cast_valid_o_5_6,
        input       wire                        cast_ready_i_5_6,

        input       wire        [`DW-1:0]       cast_data_i_5_7,
        input       wire                        cast_valid_i_5_7,
        output      wire                        cast_ready_o_5_7,

        output      wire        [`DW-1:0]       cast_data_o_5_7,
        output      wire                        cast_valid_o_5_7,
        input       wire                        cast_ready_i_5_7,

        input       wire        [`DW-1:0]       cast_data_i_6_0,
        input       wire                        cast_valid_i_6_0,
        output      wire                        cast_ready_o_6_0,

        output      wire        [`DW-1:0]       cast_data_o_6_0,
        output      wire                        cast_valid_o_6_0,
        input       wire                        cast_ready_i_6_0,

        input       wire        [`DW-1:0]       cast_data_i_6_1,
        input       wire                        cast_valid_i_6_1,
        output      wire                        cast_ready_o_6_1,

        output      wire        [`DW-1:0]       cast_data_o_6_1,
        output      wire                        cast_valid_o_6_1,
        input       wire                        cast_ready_i_6_1,

        input       wire        [`DW-1:0]       cast_data_i_6_2,
        input       wire                        cast_valid_i_6_2,
        output      wire                        cast_ready_o_6_2,

        output      wire        [`DW-1:0]       cast_data_o_6_2,
        output      wire                        cast_valid_o_6_2,
        input       wire                        cast_ready_i_6_2,

        input       wire        [`DW-1:0]       cast_data_i_6_3,
        input       wire                        cast_valid_i_6_3,
        output      wire                        cast_ready_o_6_3,

        output      wire        [`DW-1:0]       cast_data_o_6_3,
        output      wire                        cast_valid_o_6_3,
        input       wire                        cast_ready_i_6_3,

        input       wire        [`DW-1:0]       cast_data_i_6_4,
        input       wire                        cast_valid_i_6_4,
        output      wire                        cast_ready_o_6_4,

        output      wire        [`DW-1:0]       cast_data_o_6_4,
        output      wire                        cast_valid_o_6_4,
        input       wire                        cast_ready_i_6_4,

        input       wire        [`DW-1:0]       cast_data_i_6_5,
        input       wire                        cast_valid_i_6_5,
        output      wire                        cast_ready_o_6_5,

        output      wire        [`DW-1:0]       cast_data_o_6_5,
        output      wire                        cast_valid_o_6_5,
        input       wire                        cast_ready_i_6_5,

        input       wire        [`DW-1:0]       cast_data_i_6_6,
        input       wire                        cast_valid_i_6_6,
        output      wire                        cast_ready_o_6_6,

        output      wire        [`DW-1:0]       cast_data_o_6_6,
        output      wire                        cast_valid_o_6_6,
        input       wire                        cast_ready_i_6_6,

        input       wire        [`DW-1:0]       cast_data_i_6_7,
        input       wire                        cast_valid_i_6_7,
        output      wire                        cast_ready_o_6_7,

        output      wire        [`DW-1:0]       cast_data_o_6_7,
        output      wire                        cast_valid_o_6_7,
        input       wire                        cast_ready_i_6_7,

        input       wire        [`DW-1:0]       merge_data_i_0_0,
        input       wire                        merge_valid_i_0_0,
        output      wire                        merge_ready_o_0_0,

        output      wire        [`DW-1:0]       merge_data_o_0_0,
        output      wire                        merge_valid_o_0_0,
        input       wire                        merge_ready_i_0_0,
        input       wire        [`DW-1:0]       merge_data_i_0_1,
        input       wire                        merge_valid_i_0_1,
        output      wire                        merge_ready_o_0_1,

        output      wire        [`DW-1:0]       merge_data_o_0_1,
        output      wire                        merge_valid_o_0_1,
        input       wire                        merge_ready_i_0_1,
        input       wire        [`DW-1:0]       merge_data_i_0_2,
        input       wire                        merge_valid_i_0_2,
        output      wire                        merge_ready_o_0_2,

        output      wire        [`DW-1:0]       merge_data_o_0_2,
        output      wire                        merge_valid_o_0_2,
        input       wire                        merge_ready_i_0_2,
        input       wire        [`DW-1:0]       merge_data_i_0_3,
        input       wire                        merge_valid_i_0_3,
        output      wire                        merge_ready_o_0_3,

        output      wire        [`DW-1:0]       merge_data_o_0_3,
        output      wire                        merge_valid_o_0_3,
        input       wire                        merge_ready_i_0_3,
        input       wire        [`DW-1:0]       merge_data_i_0_4,
        input       wire                        merge_valid_i_0_4,
        output      wire                        merge_ready_o_0_4,

        output      wire        [`DW-1:0]       merge_data_o_0_4,
        output      wire                        merge_valid_o_0_4,
        input       wire                        merge_ready_i_0_4,
        input       wire        [`DW-1:0]       merge_data_i_0_5,
        input       wire                        merge_valid_i_0_5,
        output      wire                        merge_ready_o_0_5,

        output      wire        [`DW-1:0]       merge_data_o_0_5,
        output      wire                        merge_valid_o_0_5,
        input       wire                        merge_ready_i_0_5,
        input       wire        [`DW-1:0]       merge_data_i_0_6,
        input       wire                        merge_valid_i_0_6,
        output      wire                        merge_ready_o_0_6,

        output      wire        [`DW-1:0]       merge_data_o_0_6,
        output      wire                        merge_valid_o_0_6,
        input       wire                        merge_ready_i_0_6,
        input       wire        [`DW-1:0]       merge_data_i_0_7,
        input       wire                        merge_valid_i_0_7,
        output      wire                        merge_ready_o_0_7,

        output      wire        [`DW-1:0]       merge_data_o_0_7,
        output      wire                        merge_valid_o_0_7,
        input       wire                        merge_ready_i_0_7,
        input       wire        [`DW-1:0]       merge_data_i_1_0,
        input       wire                        merge_valid_i_1_0,
        output      wire                        merge_ready_o_1_0,

        output      wire        [`DW-1:0]       merge_data_o_1_0,
        output      wire                        merge_valid_o_1_0,
        input       wire                        merge_ready_i_1_0,
        input       wire        [`DW-1:0]       merge_data_i_1_1,
        input       wire                        merge_valid_i_1_1,
        output      wire                        merge_ready_o_1_1,

        output      wire        [`DW-1:0]       merge_data_o_1_1,
        output      wire                        merge_valid_o_1_1,
        input       wire                        merge_ready_i_1_1,
        input       wire        [`DW-1:0]       merge_data_i_1_2,
        input       wire                        merge_valid_i_1_2,
        output      wire                        merge_ready_o_1_2,

        output      wire        [`DW-1:0]       merge_data_o_1_2,
        output      wire                        merge_valid_o_1_2,
        input       wire                        merge_ready_i_1_2,
        input       wire        [`DW-1:0]       merge_data_i_1_3,
        input       wire                        merge_valid_i_1_3,
        output      wire                        merge_ready_o_1_3,

        output      wire        [`DW-1:0]       merge_data_o_1_3,
        output      wire                        merge_valid_o_1_3,
        input       wire                        merge_ready_i_1_3,
        input       wire        [`DW-1:0]       merge_data_i_1_4,
        input       wire                        merge_valid_i_1_4,
        output      wire                        merge_ready_o_1_4,

        output      wire        [`DW-1:0]       merge_data_o_1_4,
        output      wire                        merge_valid_o_1_4,
        input       wire                        merge_ready_i_1_4,
        input       wire        [`DW-1:0]       merge_data_i_1_5,
        input       wire                        merge_valid_i_1_5,
        output      wire                        merge_ready_o_1_5,

        output      wire        [`DW-1:0]       merge_data_o_1_5,
        output      wire                        merge_valid_o_1_5,
        input       wire                        merge_ready_i_1_5,
        input       wire        [`DW-1:0]       merge_data_i_1_6,
        input       wire                        merge_valid_i_1_6,
        output      wire                        merge_ready_o_1_6,

        output      wire        [`DW-1:0]       merge_data_o_1_6,
        output      wire                        merge_valid_o_1_6,
        input       wire                        merge_ready_i_1_6,
        input       wire        [`DW-1:0]       merge_data_i_1_7,
        input       wire                        merge_valid_i_1_7,
        output      wire                        merge_ready_o_1_7,

        output      wire        [`DW-1:0]       merge_data_o_1_7,
        output      wire                        merge_valid_o_1_7,
        input       wire                        merge_ready_i_1_7,
        input       wire        [`DW-1:0]       merge_data_i_2_0,
        input       wire                        merge_valid_i_2_0,
        output      wire                        merge_ready_o_2_0,

        output      wire        [`DW-1:0]       merge_data_o_2_0,
        output      wire                        merge_valid_o_2_0,
        input       wire                        merge_ready_i_2_0,
        input       wire        [`DW-1:0]       merge_data_i_2_1,
        input       wire                        merge_valid_i_2_1,
        output      wire                        merge_ready_o_2_1,

        output      wire        [`DW-1:0]       merge_data_o_2_1,
        output      wire                        merge_valid_o_2_1,
        input       wire                        merge_ready_i_2_1,
        input       wire        [`DW-1:0]       merge_data_i_2_2,
        input       wire                        merge_valid_i_2_2,
        output      wire                        merge_ready_o_2_2,

        output      wire        [`DW-1:0]       merge_data_o_2_2,
        output      wire                        merge_valid_o_2_2,
        input       wire                        merge_ready_i_2_2,
        input       wire        [`DW-1:0]       merge_data_i_2_3,
        input       wire                        merge_valid_i_2_3,
        output      wire                        merge_ready_o_2_3,

        output      wire        [`DW-1:0]       merge_data_o_2_3,
        output      wire                        merge_valid_o_2_3,
        input       wire                        merge_ready_i_2_3,
        input       wire        [`DW-1:0]       merge_data_i_2_4,
        input       wire                        merge_valid_i_2_4,
        output      wire                        merge_ready_o_2_4,

        output      wire        [`DW-1:0]       merge_data_o_2_4,
        output      wire                        merge_valid_o_2_4,
        input       wire                        merge_ready_i_2_4,
        input       wire        [`DW-1:0]       merge_data_i_2_5,
        input       wire                        merge_valid_i_2_5,
        output      wire                        merge_ready_o_2_5,

        output      wire        [`DW-1:0]       merge_data_o_2_5,
        output      wire                        merge_valid_o_2_5,
        input       wire                        merge_ready_i_2_5,
        input       wire        [`DW-1:0]       merge_data_i_2_6,
        input       wire                        merge_valid_i_2_6,
        output      wire                        merge_ready_o_2_6,

        output      wire        [`DW-1:0]       merge_data_o_2_6,
        output      wire                        merge_valid_o_2_6,
        input       wire                        merge_ready_i_2_6,
        input       wire        [`DW-1:0]       merge_data_i_2_7,
        input       wire                        merge_valid_i_2_7,
        output      wire                        merge_ready_o_2_7,

        output      wire        [`DW-1:0]       merge_data_o_2_7,
        output      wire                        merge_valid_o_2_7,
        input       wire                        merge_ready_i_2_7,
        input       wire        [`DW-1:0]       merge_data_i_3_0,
        input       wire                        merge_valid_i_3_0,
        output      wire                        merge_ready_o_3_0,

        output      wire        [`DW-1:0]       merge_data_o_3_0,
        output      wire                        merge_valid_o_3_0,
        input       wire                        merge_ready_i_3_0,
        input       wire        [`DW-1:0]       merge_data_i_3_1,
        input       wire                        merge_valid_i_3_1,
        output      wire                        merge_ready_o_3_1,

        output      wire        [`DW-1:0]       merge_data_o_3_1,
        output      wire                        merge_valid_o_3_1,
        input       wire                        merge_ready_i_3_1,
        input       wire        [`DW-1:0]       merge_data_i_3_2,
        input       wire                        merge_valid_i_3_2,
        output      wire                        merge_ready_o_3_2,

        output      wire        [`DW-1:0]       merge_data_o_3_2,
        output      wire                        merge_valid_o_3_2,
        input       wire                        merge_ready_i_3_2,
        input       wire        [`DW-1:0]       merge_data_i_3_3,
        input       wire                        merge_valid_i_3_3,
        output      wire                        merge_ready_o_3_3,

        output      wire        [`DW-1:0]       merge_data_o_3_3,
        output      wire                        merge_valid_o_3_3,
        input       wire                        merge_ready_i_3_3,
        input       wire        [`DW-1:0]       merge_data_i_3_4,
        input       wire                        merge_valid_i_3_4,
        output      wire                        merge_ready_o_3_4,

        output      wire        [`DW-1:0]       merge_data_o_3_4,
        output      wire                        merge_valid_o_3_4,
        input       wire                        merge_ready_i_3_4,
        input       wire        [`DW-1:0]       merge_data_i_3_5,
        input       wire                        merge_valid_i_3_5,
        output      wire                        merge_ready_o_3_5,

        output      wire        [`DW-1:0]       merge_data_o_3_5,
        output      wire                        merge_valid_o_3_5,
        input       wire                        merge_ready_i_3_5,
        input       wire        [`DW-1:0]       merge_data_i_3_6,
        input       wire                        merge_valid_i_3_6,
        output      wire                        merge_ready_o_3_6,

        output      wire        [`DW-1:0]       merge_data_o_3_6,
        output      wire                        merge_valid_o_3_6,
        input       wire                        merge_ready_i_3_6,
        input       wire        [`DW-1:0]       merge_data_i_3_7,
        input       wire                        merge_valid_i_3_7,
        output      wire                        merge_ready_o_3_7,

        output      wire        [`DW-1:0]       merge_data_o_3_7,
        output      wire                        merge_valid_o_3_7,
        input       wire                        merge_ready_i_3_7,
        input       wire        [`DW-1:0]       merge_data_i_4_0,
        input       wire                        merge_valid_i_4_0,
        output      wire                        merge_ready_o_4_0,

        output      wire        [`DW-1:0]       merge_data_o_4_0,
        output      wire                        merge_valid_o_4_0,
        input       wire                        merge_ready_i_4_0,
        input       wire        [`DW-1:0]       merge_data_i_4_1,
        input       wire                        merge_valid_i_4_1,
        output      wire                        merge_ready_o_4_1,

        output      wire        [`DW-1:0]       merge_data_o_4_1,
        output      wire                        merge_valid_o_4_1,
        input       wire                        merge_ready_i_4_1,
        input       wire        [`DW-1:0]       merge_data_i_4_2,
        input       wire                        merge_valid_i_4_2,
        output      wire                        merge_ready_o_4_2,

        output      wire        [`DW-1:0]       merge_data_o_4_2,
        output      wire                        merge_valid_o_4_2,
        input       wire                        merge_ready_i_4_2,
        input       wire        [`DW-1:0]       merge_data_i_4_3,
        input       wire                        merge_valid_i_4_3,
        output      wire                        merge_ready_o_4_3,

        output      wire        [`DW-1:0]       merge_data_o_4_3,
        output      wire                        merge_valid_o_4_3,
        input       wire                        merge_ready_i_4_3,
        input       wire        [`DW-1:0]       merge_data_i_4_4,
        input       wire                        merge_valid_i_4_4,
        output      wire                        merge_ready_o_4_4,

        output      wire        [`DW-1:0]       merge_data_o_4_4,
        output      wire                        merge_valid_o_4_4,
        input       wire                        merge_ready_i_4_4,
        input       wire        [`DW-1:0]       merge_data_i_4_5,
        input       wire                        merge_valid_i_4_5,
        output      wire                        merge_ready_o_4_5,

        output      wire        [`DW-1:0]       merge_data_o_4_5,
        output      wire                        merge_valid_o_4_5,
        input       wire                        merge_ready_i_4_5,
        input       wire        [`DW-1:0]       merge_data_i_4_6,
        input       wire                        merge_valid_i_4_6,
        output      wire                        merge_ready_o_4_6,

        output      wire        [`DW-1:0]       merge_data_o_4_6,
        output      wire                        merge_valid_o_4_6,
        input       wire                        merge_ready_i_4_6,
        input       wire        [`DW-1:0]       merge_data_i_4_7,
        input       wire                        merge_valid_i_4_7,
        output      wire                        merge_ready_o_4_7,

        output      wire        [`DW-1:0]       merge_data_o_4_7,
        output      wire                        merge_valid_o_4_7,
        input       wire                        merge_ready_i_4_7,
        input       wire        [`DW-1:0]       merge_data_i_5_0,
        input       wire                        merge_valid_i_5_0,
        output      wire                        merge_ready_o_5_0,

        output      wire        [`DW-1:0]       merge_data_o_5_0,
        output      wire                        merge_valid_o_5_0,
        input       wire                        merge_ready_i_5_0,
        input       wire        [`DW-1:0]       merge_data_i_5_1,
        input       wire                        merge_valid_i_5_1,
        output      wire                        merge_ready_o_5_1,

        output      wire        [`DW-1:0]       merge_data_o_5_1,
        output      wire                        merge_valid_o_5_1,
        input       wire                        merge_ready_i_5_1,
        input       wire        [`DW-1:0]       merge_data_i_5_2,
        input       wire                        merge_valid_i_5_2,
        output      wire                        merge_ready_o_5_2,

        output      wire        [`DW-1:0]       merge_data_o_5_2,
        output      wire                        merge_valid_o_5_2,
        input       wire                        merge_ready_i_5_2,
        input       wire        [`DW-1:0]       merge_data_i_5_3,
        input       wire                        merge_valid_i_5_3,
        output      wire                        merge_ready_o_5_3,

        output      wire        [`DW-1:0]       merge_data_o_5_3,
        output      wire                        merge_valid_o_5_3,
        input       wire                        merge_ready_i_5_3,
        input       wire        [`DW-1:0]       merge_data_i_5_4,
        input       wire                        merge_valid_i_5_4,
        output      wire                        merge_ready_o_5_4,

        output      wire        [`DW-1:0]       merge_data_o_5_4,
        output      wire                        merge_valid_o_5_4,
        input       wire                        merge_ready_i_5_4,
        input       wire        [`DW-1:0]       merge_data_i_5_5,
        input       wire                        merge_valid_i_5_5,
        output      wire                        merge_ready_o_5_5,

        output      wire        [`DW-1:0]       merge_data_o_5_5,
        output      wire                        merge_valid_o_5_5,
        input       wire                        merge_ready_i_5_5,
        input       wire        [`DW-1:0]       merge_data_i_5_6,
        input       wire                        merge_valid_i_5_6,
        output      wire                        merge_ready_o_5_6,

        output      wire        [`DW-1:0]       merge_data_o_5_6,
        output      wire                        merge_valid_o_5_6,
        input       wire                        merge_ready_i_5_6,
        input       wire        [`DW-1:0]       merge_data_i_5_7,
        input       wire                        merge_valid_i_5_7,
        output      wire                        merge_ready_o_5_7,

        output      wire        [`DW-1:0]       merge_data_o_5_7,
        output      wire                        merge_valid_o_5_7,
        input       wire                        merge_ready_i_5_7,
        input       wire        [`DW-1:0]       merge_data_i_6_0,
        input       wire                        merge_valid_i_6_0,
        output      wire                        merge_ready_o_6_0,

        output      wire        [`DW-1:0]       merge_data_o_6_0,
        output      wire                        merge_valid_o_6_0,
        input       wire                        merge_ready_i_6_0,
        input       wire        [`DW-1:0]       merge_data_i_6_1,
        input       wire                        merge_valid_i_6_1,
        output      wire                        merge_ready_o_6_1,

        output      wire        [`DW-1:0]       merge_data_o_6_1,
        output      wire                        merge_valid_o_6_1,
        input       wire                        merge_ready_i_6_1,
        input       wire        [`DW-1:0]       merge_data_i_6_2,
        input       wire                        merge_valid_i_6_2,
        output      wire                        merge_ready_o_6_2,

        output      wire        [`DW-1:0]       merge_data_o_6_2,
        output      wire                        merge_valid_o_6_2,
        input       wire                        merge_ready_i_6_2,
        input       wire        [`DW-1:0]       merge_data_i_6_3,
        input       wire                        merge_valid_i_6_3,
        output      wire                        merge_ready_o_6_3,

        output      wire        [`DW-1:0]       merge_data_o_6_3,
        output      wire                        merge_valid_o_6_3,
        input       wire                        merge_ready_i_6_3,
        input       wire        [`DW-1:0]       merge_data_i_6_4,
        input       wire                        merge_valid_i_6_4,
        output      wire                        merge_ready_o_6_4,

        output      wire        [`DW-1:0]       merge_data_o_6_4,
        output      wire                        merge_valid_o_6_4,
        input       wire                        merge_ready_i_6_4,
        input       wire        [`DW-1:0]       merge_data_i_6_5,
        input       wire                        merge_valid_i_6_5,
        output      wire                        merge_ready_o_6_5,

        output      wire        [`DW-1:0]       merge_data_o_6_5,
        output      wire                        merge_valid_o_6_5,
        input       wire                        merge_ready_i_6_5,
        input       wire        [`DW-1:0]       merge_data_i_6_6,
        input       wire                        merge_valid_i_6_6,
        output      wire                        merge_ready_o_6_6,

        output      wire        [`DW-1:0]       merge_data_o_6_6,
        output      wire                        merge_valid_o_6_6,
        input       wire                        merge_ready_i_6_6,
        input       wire        [`DW-1:0]       merge_data_i_6_7,
        input       wire                        merge_valid_i_6_7,
        output      wire                        merge_ready_o_6_7,

        output      wire        [`DW-1:0]       merge_data_o_6_7,
        output      wire                        merge_valid_o_6_7,
        input       wire                        merge_ready_i_6_7
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
)converter_flee0(
    .clk                      (clk),
    .rstn                     (rstn),
    .valid_i_pe               (1'b0),
    .data_i_pe                ({(`DW){1'b0}}),
    .ready_o_pe               (),
    .valid_o_pe               (valid_o_flee0),
    .data_o_pe                (data_o_flee0),
    .ready_i_pe               (ready_i_flee0),
    .valid_i_nw               (valid_flee0),
    .data_i_nw                (data_flee0),
    .ready_o_nw               (ready_flee0),
    .valid_o_nw               (),
    .data_o_nw                (),
    .ready_i_nw               (1'b0)
);

// from flee1 port to outside
cast_converter #(
    .isCaster                 (0),
    .stream_id                (1022)
)converter_flee1(
    .clk                      (clk),
    .rstn                     (rstn),
    .valid_i_pe               (1'b0),
    .data_i_pe                ({(`DW){1'b0}}),
    .ready_o_pe               (),
    .valid_o_pe               (valid_o_flee1),
    .data_o_pe                (data_o_flee1),
    .ready_i_pe               (ready_i_flee1),
    .valid_i_nw               (valid_flee1),
    .data_i_nw                (data_flee1),
    .ready_o_nw               (ready_flee1),
    .valid_o_nw               (),
    .data_o_nw                (),
    .ready_i_nw               (1'b0)
);

cast_network cast_nw(
    .clk                                               (clk),
    .rstn                                              (rstn),
    .data_i                                            (data_i_cast_nw),
    .valid_i                                           (valid_i_cast_nw),
    .ready_o                                           (ready_o_cast_nw),
    .data_o                                            (data_o_cast_nw),
    .valid_o                                           (valid_o_cast_nw),
    .ready_i                                           (ready_i_cast_nw),
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
    .data_i                                         (data_i_merge_nw),
    .valid_i                                        (valid_i_merge_nw),
    .ready_o                                        (ready_o_merge_nw),
    .data_o                                         (data_o_merge_nw),
    .valid_o                                        (valid_o_merge_nw),
    .ready_i                                        (ready_i_merge_nw)
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
    .valid_i_cast_pe                (cast_valid_i_0_0),
    .data_i_cast_pe                 (cast_data_i_0_0),
    .ready_o_cast_pe                (cast_ready_o_0_0),
    .valid_o_cast_pe                (cast_valid_o_0_0),
    .data_o_cast_pe                 (cast_data_o_0_0),
    .ready_i_cast_pe                (cast_ready_i_0_0),
    .valid_i_merge_pe               (merge_valid_i_0_0),
    .data_i_merge_pe                (merge_data_i_0_0),
    .ready_o_merge_pe               (merge_ready_o_0_0),
    .valid_o_merge_pe               (merge_valid_o_0_0),
    .data_o_merge_pe                (merge_data_o_0_0),
    .ready_i_merge_pe               (merge_ready_i_0_0),
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
    .valid_i_cast_pe                (cast_valid_i_0_1),
    .data_i_cast_pe                 (cast_data_i_0_1),
    .ready_o_cast_pe                (cast_ready_o_0_1),
    .valid_o_cast_pe                (cast_valid_o_0_1),
    .data_o_cast_pe                 (cast_data_o_0_1),
    .ready_i_cast_pe                (cast_ready_i_0_1),
    .valid_i_merge_pe               (merge_valid_i_0_1),
    .data_i_merge_pe                (merge_data_i_0_1),
    .ready_o_merge_pe               (merge_ready_o_0_1),
    .valid_o_merge_pe               (merge_valid_o_0_1),
    .data_o_merge_pe                (merge_data_o_0_1),
    .ready_i_merge_pe               (merge_ready_i_0_1),
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
    .valid_i_cast_pe                (cast_valid_i_0_2),
    .data_i_cast_pe                 (cast_data_i_0_2),
    .ready_o_cast_pe                (cast_ready_o_0_2),
    .valid_o_cast_pe                (cast_valid_o_0_2),
    .data_o_cast_pe                 (cast_data_o_0_2),
    .ready_i_cast_pe                (cast_ready_i_0_2),
    .valid_i_merge_pe               (merge_valid_i_0_2),
    .data_i_merge_pe                (merge_data_i_0_2),
    .ready_o_merge_pe               (merge_ready_o_0_2),
    .valid_o_merge_pe               (merge_valid_o_0_2),
    .data_o_merge_pe                (merge_data_o_0_2),
    .ready_i_merge_pe               (merge_ready_i_0_2),
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
    .valid_i_cast_pe                (cast_valid_i_0_3),
    .data_i_cast_pe                 (cast_data_i_0_3),
    .ready_o_cast_pe                (cast_ready_o_0_3),
    .valid_o_cast_pe                (cast_valid_o_0_3),
    .data_o_cast_pe                 (cast_data_o_0_3),
    .ready_i_cast_pe                (cast_ready_i_0_3),
    .valid_i_merge_pe               (merge_valid_i_0_3),
    .data_i_merge_pe                (merge_data_i_0_3),
    .ready_o_merge_pe               (merge_ready_o_0_3),
    .valid_o_merge_pe               (merge_valid_o_0_3),
    .data_o_merge_pe                (merge_data_o_0_3),
    .ready_i_merge_pe               (merge_ready_i_0_3),
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
    .valid_i_cast_pe                (cast_valid_i_0_4),
    .data_i_cast_pe                 (cast_data_i_0_4),
    .ready_o_cast_pe                (cast_ready_o_0_4),
    .valid_o_cast_pe                (cast_valid_o_0_4),
    .data_o_cast_pe                 (cast_data_o_0_4),
    .ready_i_cast_pe                (cast_ready_i_0_4),
    .valid_i_merge_pe               (merge_valid_i_0_4),
    .data_i_merge_pe                (merge_data_i_0_4),
    .ready_o_merge_pe               (merge_ready_o_0_4),
    .valid_o_merge_pe               (merge_valid_o_0_4),
    .data_o_merge_pe                (merge_data_o_0_4),
    .ready_i_merge_pe               (merge_ready_i_0_4),
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
    .valid_i_cast_pe                (cast_valid_i_0_5),
    .data_i_cast_pe                 (cast_data_i_0_5),
    .ready_o_cast_pe                (cast_ready_o_0_5),
    .valid_o_cast_pe                (cast_valid_o_0_5),
    .data_o_cast_pe                 (cast_data_o_0_5),
    .ready_i_cast_pe                (cast_ready_i_0_5),
    .valid_i_merge_pe               (merge_valid_i_0_5),
    .data_i_merge_pe                (merge_data_i_0_5),
    .ready_o_merge_pe               (merge_ready_o_0_5),
    .valid_o_merge_pe               (merge_valid_o_0_5),
    .data_o_merge_pe                (merge_data_o_0_5),
    .ready_i_merge_pe               (merge_ready_i_0_5),
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
    .valid_i_cast_pe                (cast_valid_i_0_6),
    .data_i_cast_pe                 (cast_data_i_0_6),
    .ready_o_cast_pe                (cast_ready_o_0_6),
    .valid_o_cast_pe                (cast_valid_o_0_6),
    .data_o_cast_pe                 (cast_data_o_0_6),
    .ready_i_cast_pe                (cast_ready_i_0_6),
    .valid_i_merge_pe               (merge_valid_i_0_6),
    .data_i_merge_pe                (merge_data_i_0_6),
    .ready_o_merge_pe               (merge_ready_o_0_6),
    .valid_o_merge_pe               (merge_valid_o_0_6),
    .data_o_merge_pe                (merge_data_o_0_6),
    .ready_i_merge_pe               (merge_ready_i_0_6),
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
    .valid_i_cast_pe                (cast_valid_i_0_7),
    .data_i_cast_pe                 (cast_data_i_0_7),
    .ready_o_cast_pe                (cast_ready_o_0_7),
    .valid_o_cast_pe                (cast_valid_o_0_7),
    .data_o_cast_pe                 (cast_data_o_0_7),
    .ready_i_cast_pe                (cast_ready_i_0_7),
    .valid_i_merge_pe               (merge_valid_i_0_7),
    .data_i_merge_pe                (merge_data_i_0_7),
    .ready_o_merge_pe               (merge_ready_o_0_7),
    .valid_o_merge_pe               (merge_valid_o_0_7),
    .data_o_merge_pe                (merge_data_o_0_7),
    .ready_i_merge_pe               (merge_ready_i_0_7),
    .credit_upd                     (credit_upd[0][7])
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
    .valid_i_cast_pe                (cast_valid_i_1_0),
    .data_i_cast_pe                 (cast_data_i_1_0),
    .ready_o_cast_pe                (cast_ready_o_1_0),
    .valid_o_cast_pe                (cast_valid_o_1_0),
    .data_o_cast_pe                 (cast_data_o_1_0),
    .ready_i_cast_pe                (cast_ready_i_1_0),
    .valid_i_merge_pe               (merge_valid_i_1_0),
    .data_i_merge_pe                (merge_data_i_1_0),
    .ready_o_merge_pe               (merge_ready_o_1_0),
    .valid_o_merge_pe               (merge_valid_o_1_0),
    .data_o_merge_pe                (merge_data_o_1_0),
    .ready_i_merge_pe               (merge_ready_i_1_0),
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
    .valid_i_cast_pe                (cast_valid_i_1_1),
    .data_i_cast_pe                 (cast_data_i_1_1),
    .ready_o_cast_pe                (cast_ready_o_1_1),
    .valid_o_cast_pe                (cast_valid_o_1_1),
    .data_o_cast_pe                 (cast_data_o_1_1),
    .ready_i_cast_pe                (cast_ready_i_1_1),
    .valid_i_merge_pe               (merge_valid_i_1_1),
    .data_i_merge_pe                (merge_data_i_1_1),
    .ready_o_merge_pe               (merge_ready_o_1_1),
    .valid_o_merge_pe               (merge_valid_o_1_1),
    .data_o_merge_pe                (merge_data_o_1_1),
    .ready_i_merge_pe               (merge_ready_i_1_1),
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
    .valid_i_cast_pe                (cast_valid_i_1_2),
    .data_i_cast_pe                 (cast_data_i_1_2),
    .ready_o_cast_pe                (cast_ready_o_1_2),
    .valid_o_cast_pe                (cast_valid_o_1_2),
    .data_o_cast_pe                 (cast_data_o_1_2),
    .ready_i_cast_pe                (cast_ready_i_1_2),
    .valid_i_merge_pe               (merge_valid_i_1_2),
    .data_i_merge_pe                (merge_data_i_1_2),
    .ready_o_merge_pe               (merge_ready_o_1_2),
    .valid_o_merge_pe               (merge_valid_o_1_2),
    .data_o_merge_pe                (merge_data_o_1_2),
    .ready_i_merge_pe               (merge_ready_i_1_2),
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
    .valid_i_cast_pe                (cast_valid_i_1_3),
    .data_i_cast_pe                 (cast_data_i_1_3),
    .ready_o_cast_pe                (cast_ready_o_1_3),
    .valid_o_cast_pe                (cast_valid_o_1_3),
    .data_o_cast_pe                 (cast_data_o_1_3),
    .ready_i_cast_pe                (cast_ready_i_1_3),
    .valid_i_merge_pe               (merge_valid_i_1_3),
    .data_i_merge_pe                (merge_data_i_1_3),
    .ready_o_merge_pe               (merge_ready_o_1_3),
    .valid_o_merge_pe               (merge_valid_o_1_3),
    .data_o_merge_pe                (merge_data_o_1_3),
    .ready_i_merge_pe               (merge_ready_i_1_3),
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
    .valid_i_cast_pe                (cast_valid_i_1_4),
    .data_i_cast_pe                 (cast_data_i_1_4),
    .ready_o_cast_pe                (cast_ready_o_1_4),
    .valid_o_cast_pe                (cast_valid_o_1_4),
    .data_o_cast_pe                 (cast_data_o_1_4),
    .ready_i_cast_pe                (cast_ready_i_1_4),
    .valid_i_merge_pe               (merge_valid_i_1_4),
    .data_i_merge_pe                (merge_data_i_1_4),
    .ready_o_merge_pe               (merge_ready_o_1_4),
    .valid_o_merge_pe               (merge_valid_o_1_4),
    .data_o_merge_pe                (merge_data_o_1_4),
    .ready_i_merge_pe               (merge_ready_i_1_4),
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
    .valid_i_cast_pe                (cast_valid_i_1_5),
    .data_i_cast_pe                 (cast_data_i_1_5),
    .ready_o_cast_pe                (cast_ready_o_1_5),
    .valid_o_cast_pe                (cast_valid_o_1_5),
    .data_o_cast_pe                 (cast_data_o_1_5),
    .ready_i_cast_pe                (cast_ready_i_1_5),
    .valid_i_merge_pe               (merge_valid_i_1_5),
    .data_i_merge_pe                (merge_data_i_1_5),
    .ready_o_merge_pe               (merge_ready_o_1_5),
    .valid_o_merge_pe               (merge_valid_o_1_5),
    .data_o_merge_pe                (merge_data_o_1_5),
    .ready_i_merge_pe               (merge_ready_i_1_5),
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
    .valid_i_cast_pe                (cast_valid_i_1_6),
    .data_i_cast_pe                 (cast_data_i_1_6),
    .ready_o_cast_pe                (cast_ready_o_1_6),
    .valid_o_cast_pe                (cast_valid_o_1_6),
    .data_o_cast_pe                 (cast_data_o_1_6),
    .ready_i_cast_pe                (cast_ready_i_1_6),
    .valid_i_merge_pe               (merge_valid_i_1_6),
    .data_i_merge_pe                (merge_data_i_1_6),
    .ready_o_merge_pe               (merge_ready_o_1_6),
    .valid_o_merge_pe               (merge_valid_o_1_6),
    .data_o_merge_pe                (merge_data_o_1_6),
    .ready_i_merge_pe               (merge_ready_i_1_6),
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
    .valid_i_cast_pe                (cast_valid_i_1_7),
    .data_i_cast_pe                 (cast_data_i_1_7),
    .ready_o_cast_pe                (cast_ready_o_1_7),
    .valid_o_cast_pe                (cast_valid_o_1_7),
    .data_o_cast_pe                 (cast_data_o_1_7),
    .ready_i_cast_pe                (cast_ready_i_1_7),
    .valid_i_merge_pe               (merge_valid_i_1_7),
    .data_i_merge_pe                (merge_data_i_1_7),
    .ready_o_merge_pe               (merge_ready_o_1_7),
    .valid_o_merge_pe               (merge_valid_o_1_7),
    .data_o_merge_pe                (merge_data_o_1_7),
    .ready_i_merge_pe               (merge_ready_i_1_7),
    .credit_upd                     (credit_upd[1][7])
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
    .valid_i_cast_pe                (cast_valid_i_2_0),
    .data_i_cast_pe                 (cast_data_i_2_0),
    .ready_o_cast_pe                (cast_ready_o_2_0),
    .valid_o_cast_pe                (cast_valid_o_2_0),
    .data_o_cast_pe                 (cast_data_o_2_0),
    .ready_i_cast_pe                (cast_ready_i_2_0),
    .valid_i_merge_pe               (merge_valid_i_2_0),
    .data_i_merge_pe                (merge_data_i_2_0),
    .ready_o_merge_pe               (merge_ready_o_2_0),
    .valid_o_merge_pe               (merge_valid_o_2_0),
    .data_o_merge_pe                (merge_data_o_2_0),
    .ready_i_merge_pe               (merge_ready_i_2_0),
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
    .valid_i_cast_pe                (cast_valid_i_2_1),
    .data_i_cast_pe                 (cast_data_i_2_1),
    .ready_o_cast_pe                (cast_ready_o_2_1),
    .valid_o_cast_pe                (cast_valid_o_2_1),
    .data_o_cast_pe                 (cast_data_o_2_1),
    .ready_i_cast_pe                (cast_ready_i_2_1),
    .valid_i_merge_pe               (merge_valid_i_2_1),
    .data_i_merge_pe                (merge_data_i_2_1),
    .ready_o_merge_pe               (merge_ready_o_2_1),
    .valid_o_merge_pe               (merge_valid_o_2_1),
    .data_o_merge_pe                (merge_data_o_2_1),
    .ready_i_merge_pe               (merge_ready_i_2_1),
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
    .valid_i_cast_pe                (cast_valid_i_2_2),
    .data_i_cast_pe                 (cast_data_i_2_2),
    .ready_o_cast_pe                (cast_ready_o_2_2),
    .valid_o_cast_pe                (cast_valid_o_2_2),
    .data_o_cast_pe                 (cast_data_o_2_2),
    .ready_i_cast_pe                (cast_ready_i_2_2),
    .valid_i_merge_pe               (merge_valid_i_2_2),
    .data_i_merge_pe                (merge_data_i_2_2),
    .ready_o_merge_pe               (merge_ready_o_2_2),
    .valid_o_merge_pe               (merge_valid_o_2_2),
    .data_o_merge_pe                (merge_data_o_2_2),
    .ready_i_merge_pe               (merge_ready_i_2_2),
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
    .valid_i_cast_pe                (cast_valid_i_2_3),
    .data_i_cast_pe                 (cast_data_i_2_3),
    .ready_o_cast_pe                (cast_ready_o_2_3),
    .valid_o_cast_pe                (cast_valid_o_2_3),
    .data_o_cast_pe                 (cast_data_o_2_3),
    .ready_i_cast_pe                (cast_ready_i_2_3),
    .valid_i_merge_pe               (merge_valid_i_2_3),
    .data_i_merge_pe                (merge_data_i_2_3),
    .ready_o_merge_pe               (merge_ready_o_2_3),
    .valid_o_merge_pe               (merge_valid_o_2_3),
    .data_o_merge_pe                (merge_data_o_2_3),
    .ready_i_merge_pe               (merge_ready_i_2_3),
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
    .valid_i_cast_pe                (cast_valid_i_2_4),
    .data_i_cast_pe                 (cast_data_i_2_4),
    .ready_o_cast_pe                (cast_ready_o_2_4),
    .valid_o_cast_pe                (cast_valid_o_2_4),
    .data_o_cast_pe                 (cast_data_o_2_4),
    .ready_i_cast_pe                (cast_ready_i_2_4),
    .valid_i_merge_pe               (merge_valid_i_2_4),
    .data_i_merge_pe                (merge_data_i_2_4),
    .ready_o_merge_pe               (merge_ready_o_2_4),
    .valid_o_merge_pe               (merge_valid_o_2_4),
    .data_o_merge_pe                (merge_data_o_2_4),
    .ready_i_merge_pe               (merge_ready_i_2_4),
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
    .valid_i_cast_pe                (cast_valid_i_2_5),
    .data_i_cast_pe                 (cast_data_i_2_5),
    .ready_o_cast_pe                (cast_ready_o_2_5),
    .valid_o_cast_pe                (cast_valid_o_2_5),
    .data_o_cast_pe                 (cast_data_o_2_5),
    .ready_i_cast_pe                (cast_ready_i_2_5),
    .valid_i_merge_pe               (merge_valid_i_2_5),
    .data_i_merge_pe                (merge_data_i_2_5),
    .ready_o_merge_pe               (merge_ready_o_2_5),
    .valid_o_merge_pe               (merge_valid_o_2_5),
    .data_o_merge_pe                (merge_data_o_2_5),
    .ready_i_merge_pe               (merge_ready_i_2_5),
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
    .valid_i_cast_pe                (cast_valid_i_2_6),
    .data_i_cast_pe                 (cast_data_i_2_6),
    .ready_o_cast_pe                (cast_ready_o_2_6),
    .valid_o_cast_pe                (cast_valid_o_2_6),
    .data_o_cast_pe                 (cast_data_o_2_6),
    .ready_i_cast_pe                (cast_ready_i_2_6),
    .valid_i_merge_pe               (merge_valid_i_2_6),
    .data_i_merge_pe                (merge_data_i_2_6),
    .ready_o_merge_pe               (merge_ready_o_2_6),
    .valid_o_merge_pe               (merge_valid_o_2_6),
    .data_o_merge_pe                (merge_data_o_2_6),
    .ready_i_merge_pe               (merge_ready_i_2_6),
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
    .valid_i_cast_pe                (cast_valid_i_2_7),
    .data_i_cast_pe                 (cast_data_i_2_7),
    .ready_o_cast_pe                (cast_ready_o_2_7),
    .valid_o_cast_pe                (cast_valid_o_2_7),
    .data_o_cast_pe                 (cast_data_o_2_7),
    .ready_i_cast_pe                (cast_ready_i_2_7),
    .valid_i_merge_pe               (merge_valid_i_2_7),
    .data_i_merge_pe                (merge_data_i_2_7),
    .ready_o_merge_pe               (merge_ready_o_2_7),
    .valid_o_merge_pe               (merge_valid_o_2_7),
    .data_o_merge_pe                (merge_data_o_2_7),
    .ready_i_merge_pe               (merge_ready_i_2_7),
    .credit_upd                     (credit_upd[2][7])
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
    .valid_i_cast_pe                (cast_valid_i_3_0),
    .data_i_cast_pe                 (cast_data_i_3_0),
    .ready_o_cast_pe                (cast_ready_o_3_0),
    .valid_o_cast_pe                (cast_valid_o_3_0),
    .data_o_cast_pe                 (cast_data_o_3_0),
    .ready_i_cast_pe                (cast_ready_i_3_0),
    .valid_i_merge_pe               (merge_valid_i_3_0),
    .data_i_merge_pe                (merge_data_i_3_0),
    .ready_o_merge_pe               (merge_ready_o_3_0),
    .valid_o_merge_pe               (merge_valid_o_3_0),
    .data_o_merge_pe                (merge_data_o_3_0),
    .ready_i_merge_pe               (merge_ready_i_3_0),
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
    .valid_i_cast_pe                (cast_valid_i_3_1),
    .data_i_cast_pe                 (cast_data_i_3_1),
    .ready_o_cast_pe                (cast_ready_o_3_1),
    .valid_o_cast_pe                (cast_valid_o_3_1),
    .data_o_cast_pe                 (cast_data_o_3_1),
    .ready_i_cast_pe                (cast_ready_i_3_1),
    .valid_i_merge_pe               (merge_valid_i_3_1),
    .data_i_merge_pe                (merge_data_i_3_1),
    .ready_o_merge_pe               (merge_ready_o_3_1),
    .valid_o_merge_pe               (merge_valid_o_3_1),
    .data_o_merge_pe                (merge_data_o_3_1),
    .ready_i_merge_pe               (merge_ready_i_3_1),
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
    .valid_i_cast_pe                (cast_valid_i_3_2),
    .data_i_cast_pe                 (cast_data_i_3_2),
    .ready_o_cast_pe                (cast_ready_o_3_2),
    .valid_o_cast_pe                (cast_valid_o_3_2),
    .data_o_cast_pe                 (cast_data_o_3_2),
    .ready_i_cast_pe                (cast_ready_i_3_2),
    .valid_i_merge_pe               (merge_valid_i_3_2),
    .data_i_merge_pe                (merge_data_i_3_2),
    .ready_o_merge_pe               (merge_ready_o_3_2),
    .valid_o_merge_pe               (merge_valid_o_3_2),
    .data_o_merge_pe                (merge_data_o_3_2),
    .ready_i_merge_pe               (merge_ready_i_3_2),
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
    .valid_i_cast_pe                (cast_valid_i_3_3),
    .data_i_cast_pe                 (cast_data_i_3_3),
    .ready_o_cast_pe                (cast_ready_o_3_3),
    .valid_o_cast_pe                (cast_valid_o_3_3),
    .data_o_cast_pe                 (cast_data_o_3_3),
    .ready_i_cast_pe                (cast_ready_i_3_3),
    .valid_i_merge_pe               (merge_valid_i_3_3),
    .data_i_merge_pe                (merge_data_i_3_3),
    .ready_o_merge_pe               (merge_ready_o_3_3),
    .valid_o_merge_pe               (merge_valid_o_3_3),
    .data_o_merge_pe                (merge_data_o_3_3),
    .ready_i_merge_pe               (merge_ready_i_3_3),
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
    .valid_i_cast_pe                (cast_valid_i_3_4),
    .data_i_cast_pe                 (cast_data_i_3_4),
    .ready_o_cast_pe                (cast_ready_o_3_4),
    .valid_o_cast_pe                (cast_valid_o_3_4),
    .data_o_cast_pe                 (cast_data_o_3_4),
    .ready_i_cast_pe                (cast_ready_i_3_4),
    .valid_i_merge_pe               (merge_valid_i_3_4),
    .data_i_merge_pe                (merge_data_i_3_4),
    .ready_o_merge_pe               (merge_ready_o_3_4),
    .valid_o_merge_pe               (merge_valid_o_3_4),
    .data_o_merge_pe                (merge_data_o_3_4),
    .ready_i_merge_pe               (merge_ready_i_3_4),
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
    .valid_i_cast_pe                (cast_valid_i_3_5),
    .data_i_cast_pe                 (cast_data_i_3_5),
    .ready_o_cast_pe                (cast_ready_o_3_5),
    .valid_o_cast_pe                (cast_valid_o_3_5),
    .data_o_cast_pe                 (cast_data_o_3_5),
    .ready_i_cast_pe                (cast_ready_i_3_5),
    .valid_i_merge_pe               (merge_valid_i_3_5),
    .data_i_merge_pe                (merge_data_i_3_5),
    .ready_o_merge_pe               (merge_ready_o_3_5),
    .valid_o_merge_pe               (merge_valid_o_3_5),
    .data_o_merge_pe                (merge_data_o_3_5),
    .ready_i_merge_pe               (merge_ready_i_3_5),
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
    .valid_i_cast_pe                (cast_valid_i_3_6),
    .data_i_cast_pe                 (cast_data_i_3_6),
    .ready_o_cast_pe                (cast_ready_o_3_6),
    .valid_o_cast_pe                (cast_valid_o_3_6),
    .data_o_cast_pe                 (cast_data_o_3_6),
    .ready_i_cast_pe                (cast_ready_i_3_6),
    .valid_i_merge_pe               (merge_valid_i_3_6),
    .data_i_merge_pe                (merge_data_i_3_6),
    .ready_o_merge_pe               (merge_ready_o_3_6),
    .valid_o_merge_pe               (merge_valid_o_3_6),
    .data_o_merge_pe                (merge_data_o_3_6),
    .ready_i_merge_pe               (merge_ready_i_3_6),
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
    .valid_i_cast_pe                (cast_valid_i_3_7),
    .data_i_cast_pe                 (cast_data_i_3_7),
    .ready_o_cast_pe                (cast_ready_o_3_7),
    .valid_o_cast_pe                (cast_valid_o_3_7),
    .data_o_cast_pe                 (cast_data_o_3_7),
    .ready_i_cast_pe                (cast_ready_i_3_7),
    .valid_i_merge_pe               (merge_valid_i_3_7),
    .data_i_merge_pe                (merge_data_i_3_7),
    .ready_o_merge_pe               (merge_ready_o_3_7),
    .valid_o_merge_pe               (merge_valid_o_3_7),
    .data_o_merge_pe                (merge_data_o_3_7),
    .ready_i_merge_pe               (merge_ready_i_3_7),
    .credit_upd                     (credit_upd[3][7])
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
    .valid_i_cast_pe                (cast_valid_i_4_0),
    .data_i_cast_pe                 (cast_data_i_4_0),
    .ready_o_cast_pe                (cast_ready_o_4_0),
    .valid_o_cast_pe                (cast_valid_o_4_0),
    .data_o_cast_pe                 (cast_data_o_4_0),
    .ready_i_cast_pe                (cast_ready_i_4_0),
    .valid_i_merge_pe               (merge_valid_i_4_0),
    .data_i_merge_pe                (merge_data_i_4_0),
    .ready_o_merge_pe               (merge_ready_o_4_0),
    .valid_o_merge_pe               (merge_valid_o_4_0),
    .data_o_merge_pe                (merge_data_o_4_0),
    .ready_i_merge_pe               (merge_ready_i_4_0),
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
    .valid_i_cast_pe                (cast_valid_i_4_1),
    .data_i_cast_pe                 (cast_data_i_4_1),
    .ready_o_cast_pe                (cast_ready_o_4_1),
    .valid_o_cast_pe                (cast_valid_o_4_1),
    .data_o_cast_pe                 (cast_data_o_4_1),
    .ready_i_cast_pe                (cast_ready_i_4_1),
    .valid_i_merge_pe               (merge_valid_i_4_1),
    .data_i_merge_pe                (merge_data_i_4_1),
    .ready_o_merge_pe               (merge_ready_o_4_1),
    .valid_o_merge_pe               (merge_valid_o_4_1),
    .data_o_merge_pe                (merge_data_o_4_1),
    .ready_i_merge_pe               (merge_ready_i_4_1),
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
    .valid_i_cast_pe                (cast_valid_i_4_2),
    .data_i_cast_pe                 (cast_data_i_4_2),
    .ready_o_cast_pe                (cast_ready_o_4_2),
    .valid_o_cast_pe                (cast_valid_o_4_2),
    .data_o_cast_pe                 (cast_data_o_4_2),
    .ready_i_cast_pe                (cast_ready_i_4_2),
    .valid_i_merge_pe               (merge_valid_i_4_2),
    .data_i_merge_pe                (merge_data_i_4_2),
    .ready_o_merge_pe               (merge_ready_o_4_2),
    .valid_o_merge_pe               (merge_valid_o_4_2),
    .data_o_merge_pe                (merge_data_o_4_2),
    .ready_i_merge_pe               (merge_ready_i_4_2),
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
    .valid_i_cast_pe                (cast_valid_i_4_3),
    .data_i_cast_pe                 (cast_data_i_4_3),
    .ready_o_cast_pe                (cast_ready_o_4_3),
    .valid_o_cast_pe                (cast_valid_o_4_3),
    .data_o_cast_pe                 (cast_data_o_4_3),
    .ready_i_cast_pe                (cast_ready_i_4_3),
    .valid_i_merge_pe               (merge_valid_i_4_3),
    .data_i_merge_pe                (merge_data_i_4_3),
    .ready_o_merge_pe               (merge_ready_o_4_3),
    .valid_o_merge_pe               (merge_valid_o_4_3),
    .data_o_merge_pe                (merge_data_o_4_3),
    .ready_i_merge_pe               (merge_ready_i_4_3),
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
    .valid_i_cast_pe                (cast_valid_i_4_4),
    .data_i_cast_pe                 (cast_data_i_4_4),
    .ready_o_cast_pe                (cast_ready_o_4_4),
    .valid_o_cast_pe                (cast_valid_o_4_4),
    .data_o_cast_pe                 (cast_data_o_4_4),
    .ready_i_cast_pe                (cast_ready_i_4_4),
    .valid_i_merge_pe               (merge_valid_i_4_4),
    .data_i_merge_pe                (merge_data_i_4_4),
    .ready_o_merge_pe               (merge_ready_o_4_4),
    .valid_o_merge_pe               (merge_valid_o_4_4),
    .data_o_merge_pe                (merge_data_o_4_4),
    .ready_i_merge_pe               (merge_ready_i_4_4),
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
    .valid_i_cast_pe                (cast_valid_i_4_5),
    .data_i_cast_pe                 (cast_data_i_4_5),
    .ready_o_cast_pe                (cast_ready_o_4_5),
    .valid_o_cast_pe                (cast_valid_o_4_5),
    .data_o_cast_pe                 (cast_data_o_4_5),
    .ready_i_cast_pe                (cast_ready_i_4_5),
    .valid_i_merge_pe               (merge_valid_i_4_5),
    .data_i_merge_pe                (merge_data_i_4_5),
    .ready_o_merge_pe               (merge_ready_o_4_5),
    .valid_o_merge_pe               (merge_valid_o_4_5),
    .data_o_merge_pe                (merge_data_o_4_5),
    .ready_i_merge_pe               (merge_ready_i_4_5),
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
    .valid_i_cast_pe                (cast_valid_i_4_6),
    .data_i_cast_pe                 (cast_data_i_4_6),
    .ready_o_cast_pe                (cast_ready_o_4_6),
    .valid_o_cast_pe                (cast_valid_o_4_6),
    .data_o_cast_pe                 (cast_data_o_4_6),
    .ready_i_cast_pe                (cast_ready_i_4_6),
    .valid_i_merge_pe               (merge_valid_i_4_6),
    .data_i_merge_pe                (merge_data_i_4_6),
    .ready_o_merge_pe               (merge_ready_o_4_6),
    .valid_o_merge_pe               (merge_valid_o_4_6),
    .data_o_merge_pe                (merge_data_o_4_6),
    .ready_i_merge_pe               (merge_ready_i_4_6),
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
    .valid_i_cast_pe                (cast_valid_i_4_7),
    .data_i_cast_pe                 (cast_data_i_4_7),
    .ready_o_cast_pe                (cast_ready_o_4_7),
    .valid_o_cast_pe                (cast_valid_o_4_7),
    .data_o_cast_pe                 (cast_data_o_4_7),
    .ready_i_cast_pe                (cast_ready_i_4_7),
    .valid_i_merge_pe               (merge_valid_i_4_7),
    .data_i_merge_pe                (merge_data_i_4_7),
    .ready_o_merge_pe               (merge_ready_o_4_7),
    .valid_o_merge_pe               (merge_valid_o_4_7),
    .data_o_merge_pe                (merge_data_o_4_7),
    .ready_i_merge_pe               (merge_ready_i_4_7),
    .credit_upd                     (credit_upd[4][7])
);


network_interface #(
    .isCaster                       (isCaster_5_0),
    .stream_id                      (stream_id_5_0)
)ni_5_0(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[5][0]),
    .data_i_cast_nw                 (data_o_cast_nw[5][0]),
    .ready_o_cast_nw                (ready_i_cast_nw[5][0]),
    .valid_o_cast_nw                (valid_i_cast_nw[5][0]),
    .data_o_cast_nw                 (data_i_cast_nw[5][0]),
    .ready_i_cast_nw                (ready_o_cast_nw[5][0]),
    .valid_i_merge_nw               (valid_o_merge_nw[5][0]),
    .data_i_merge_nw                (data_o_merge_nw[5][0]),
    .ready_o_merge_nw               (ready_i_merge_nw[5][0]),
    .valid_o_merge_nw               (valid_i_merge_nw[5][0]),
    .data_o_merge_nw                (data_i_merge_nw[5][0]),
    .ready_i_merge_nw               (ready_o_merge_nw[5][0]),
    .valid_i_cast_pe                (cast_valid_i_5_0),
    .data_i_cast_pe                 (cast_data_i_5_0),
    .ready_o_cast_pe                (cast_ready_o_5_0),
    .valid_o_cast_pe                (cast_valid_o_5_0),
    .data_o_cast_pe                 (cast_data_o_5_0),
    .ready_i_cast_pe                (cast_ready_i_5_0),
    .valid_i_merge_pe               (merge_valid_i_5_0),
    .data_i_merge_pe                (merge_data_i_5_0),
    .ready_o_merge_pe               (merge_ready_o_5_0),
    .valid_o_merge_pe               (merge_valid_o_5_0),
    .data_o_merge_pe                (merge_data_o_5_0),
    .ready_i_merge_pe               (merge_ready_i_5_0),
    .credit_upd                     (credit_upd[5][0])
);


network_interface #(
    .isCaster                       (isCaster_5_1),
    .stream_id                      (stream_id_5_1)
)ni_5_1(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[5][1]),
    .data_i_cast_nw                 (data_o_cast_nw[5][1]),
    .ready_o_cast_nw                (ready_i_cast_nw[5][1]),
    .valid_o_cast_nw                (valid_i_cast_nw[5][1]),
    .data_o_cast_nw                 (data_i_cast_nw[5][1]),
    .ready_i_cast_nw                (ready_o_cast_nw[5][1]),
    .valid_i_merge_nw               (valid_o_merge_nw[5][1]),
    .data_i_merge_nw                (data_o_merge_nw[5][1]),
    .ready_o_merge_nw               (ready_i_merge_nw[5][1]),
    .valid_o_merge_nw               (valid_i_merge_nw[5][1]),
    .data_o_merge_nw                (data_i_merge_nw[5][1]),
    .ready_i_merge_nw               (ready_o_merge_nw[5][1]),
    .valid_i_cast_pe                (cast_valid_i_5_1),
    .data_i_cast_pe                 (cast_data_i_5_1),
    .ready_o_cast_pe                (cast_ready_o_5_1),
    .valid_o_cast_pe                (cast_valid_o_5_1),
    .data_o_cast_pe                 (cast_data_o_5_1),
    .ready_i_cast_pe                (cast_ready_i_5_1),
    .valid_i_merge_pe               (merge_valid_i_5_1),
    .data_i_merge_pe                (merge_data_i_5_1),
    .ready_o_merge_pe               (merge_ready_o_5_1),
    .valid_o_merge_pe               (merge_valid_o_5_1),
    .data_o_merge_pe                (merge_data_o_5_1),
    .ready_i_merge_pe               (merge_ready_i_5_1),
    .credit_upd                     (credit_upd[5][1])
);


network_interface #(
    .isCaster                       (isCaster_5_2),
    .stream_id                      (stream_id_5_2)
)ni_5_2(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[5][2]),
    .data_i_cast_nw                 (data_o_cast_nw[5][2]),
    .ready_o_cast_nw                (ready_i_cast_nw[5][2]),
    .valid_o_cast_nw                (valid_i_cast_nw[5][2]),
    .data_o_cast_nw                 (data_i_cast_nw[5][2]),
    .ready_i_cast_nw                (ready_o_cast_nw[5][2]),
    .valid_i_merge_nw               (valid_o_merge_nw[5][2]),
    .data_i_merge_nw                (data_o_merge_nw[5][2]),
    .ready_o_merge_nw               (ready_i_merge_nw[5][2]),
    .valid_o_merge_nw               (valid_i_merge_nw[5][2]),
    .data_o_merge_nw                (data_i_merge_nw[5][2]),
    .ready_i_merge_nw               (ready_o_merge_nw[5][2]),
    .valid_i_cast_pe                (cast_valid_i_5_2),
    .data_i_cast_pe                 (cast_data_i_5_2),
    .ready_o_cast_pe                (cast_ready_o_5_2),
    .valid_o_cast_pe                (cast_valid_o_5_2),
    .data_o_cast_pe                 (cast_data_o_5_2),
    .ready_i_cast_pe                (cast_ready_i_5_2),
    .valid_i_merge_pe               (merge_valid_i_5_2),
    .data_i_merge_pe                (merge_data_i_5_2),
    .ready_o_merge_pe               (merge_ready_o_5_2),
    .valid_o_merge_pe               (merge_valid_o_5_2),
    .data_o_merge_pe                (merge_data_o_5_2),
    .ready_i_merge_pe               (merge_ready_i_5_2),
    .credit_upd                     (credit_upd[5][2])
);


network_interface #(
    .isCaster                       (isCaster_5_3),
    .stream_id                      (stream_id_5_3)
)ni_5_3(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[5][3]),
    .data_i_cast_nw                 (data_o_cast_nw[5][3]),
    .ready_o_cast_nw                (ready_i_cast_nw[5][3]),
    .valid_o_cast_nw                (valid_i_cast_nw[5][3]),
    .data_o_cast_nw                 (data_i_cast_nw[5][3]),
    .ready_i_cast_nw                (ready_o_cast_nw[5][3]),
    .valid_i_merge_nw               (valid_o_merge_nw[5][3]),
    .data_i_merge_nw                (data_o_merge_nw[5][3]),
    .ready_o_merge_nw               (ready_i_merge_nw[5][3]),
    .valid_o_merge_nw               (valid_i_merge_nw[5][3]),
    .data_o_merge_nw                (data_i_merge_nw[5][3]),
    .ready_i_merge_nw               (ready_o_merge_nw[5][3]),
    .valid_i_cast_pe                (cast_valid_i_5_3),
    .data_i_cast_pe                 (cast_data_i_5_3),
    .ready_o_cast_pe                (cast_ready_o_5_3),
    .valid_o_cast_pe                (cast_valid_o_5_3),
    .data_o_cast_pe                 (cast_data_o_5_3),
    .ready_i_cast_pe                (cast_ready_i_5_3),
    .valid_i_merge_pe               (merge_valid_i_5_3),
    .data_i_merge_pe                (merge_data_i_5_3),
    .ready_o_merge_pe               (merge_ready_o_5_3),
    .valid_o_merge_pe               (merge_valid_o_5_3),
    .data_o_merge_pe                (merge_data_o_5_3),
    .ready_i_merge_pe               (merge_ready_i_5_3),
    .credit_upd                     (credit_upd[5][3])
);


network_interface #(
    .isCaster                       (isCaster_5_4),
    .stream_id                      (stream_id_5_4)
)ni_5_4(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[5][4]),
    .data_i_cast_nw                 (data_o_cast_nw[5][4]),
    .ready_o_cast_nw                (ready_i_cast_nw[5][4]),
    .valid_o_cast_nw                (valid_i_cast_nw[5][4]),
    .data_o_cast_nw                 (data_i_cast_nw[5][4]),
    .ready_i_cast_nw                (ready_o_cast_nw[5][4]),
    .valid_i_merge_nw               (valid_o_merge_nw[5][4]),
    .data_i_merge_nw                (data_o_merge_nw[5][4]),
    .ready_o_merge_nw               (ready_i_merge_nw[5][4]),
    .valid_o_merge_nw               (valid_i_merge_nw[5][4]),
    .data_o_merge_nw                (data_i_merge_nw[5][4]),
    .ready_i_merge_nw               (ready_o_merge_nw[5][4]),
    .valid_i_cast_pe                (cast_valid_i_5_4),
    .data_i_cast_pe                 (cast_data_i_5_4),
    .ready_o_cast_pe                (cast_ready_o_5_4),
    .valid_o_cast_pe                (cast_valid_o_5_4),
    .data_o_cast_pe                 (cast_data_o_5_4),
    .ready_i_cast_pe                (cast_ready_i_5_4),
    .valid_i_merge_pe               (merge_valid_i_5_4),
    .data_i_merge_pe                (merge_data_i_5_4),
    .ready_o_merge_pe               (merge_ready_o_5_4),
    .valid_o_merge_pe               (merge_valid_o_5_4),
    .data_o_merge_pe                (merge_data_o_5_4),
    .ready_i_merge_pe               (merge_ready_i_5_4),
    .credit_upd                     (credit_upd[5][4])
);


network_interface #(
    .isCaster                       (isCaster_5_5),
    .stream_id                      (stream_id_5_5)
)ni_5_5(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[5][5]),
    .data_i_cast_nw                 (data_o_cast_nw[5][5]),
    .ready_o_cast_nw                (ready_i_cast_nw[5][5]),
    .valid_o_cast_nw                (valid_i_cast_nw[5][5]),
    .data_o_cast_nw                 (data_i_cast_nw[5][5]),
    .ready_i_cast_nw                (ready_o_cast_nw[5][5]),
    .valid_i_merge_nw               (valid_o_merge_nw[5][5]),
    .data_i_merge_nw                (data_o_merge_nw[5][5]),
    .ready_o_merge_nw               (ready_i_merge_nw[5][5]),
    .valid_o_merge_nw               (valid_i_merge_nw[5][5]),
    .data_o_merge_nw                (data_i_merge_nw[5][5]),
    .ready_i_merge_nw               (ready_o_merge_nw[5][5]),
    .valid_i_cast_pe                (cast_valid_i_5_5),
    .data_i_cast_pe                 (cast_data_i_5_5),
    .ready_o_cast_pe                (cast_ready_o_5_5),
    .valid_o_cast_pe                (cast_valid_o_5_5),
    .data_o_cast_pe                 (cast_data_o_5_5),
    .ready_i_cast_pe                (cast_ready_i_5_5),
    .valid_i_merge_pe               (merge_valid_i_5_5),
    .data_i_merge_pe                (merge_data_i_5_5),
    .ready_o_merge_pe               (merge_ready_o_5_5),
    .valid_o_merge_pe               (merge_valid_o_5_5),
    .data_o_merge_pe                (merge_data_o_5_5),
    .ready_i_merge_pe               (merge_ready_i_5_5),
    .credit_upd                     (credit_upd[5][5])
);


network_interface #(
    .isCaster                       (isCaster_5_6),
    .stream_id                      (stream_id_5_6)
)ni_5_6(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[5][6]),
    .data_i_cast_nw                 (data_o_cast_nw[5][6]),
    .ready_o_cast_nw                (ready_i_cast_nw[5][6]),
    .valid_o_cast_nw                (valid_i_cast_nw[5][6]),
    .data_o_cast_nw                 (data_i_cast_nw[5][6]),
    .ready_i_cast_nw                (ready_o_cast_nw[5][6]),
    .valid_i_merge_nw               (valid_o_merge_nw[5][6]),
    .data_i_merge_nw                (data_o_merge_nw[5][6]),
    .ready_o_merge_nw               (ready_i_merge_nw[5][6]),
    .valid_o_merge_nw               (valid_i_merge_nw[5][6]),
    .data_o_merge_nw                (data_i_merge_nw[5][6]),
    .ready_i_merge_nw               (ready_o_merge_nw[5][6]),
    .valid_i_cast_pe                (cast_valid_i_5_6),
    .data_i_cast_pe                 (cast_data_i_5_6),
    .ready_o_cast_pe                (cast_ready_o_5_6),
    .valid_o_cast_pe                (cast_valid_o_5_6),
    .data_o_cast_pe                 (cast_data_o_5_6),
    .ready_i_cast_pe                (cast_ready_i_5_6),
    .valid_i_merge_pe               (merge_valid_i_5_6),
    .data_i_merge_pe                (merge_data_i_5_6),
    .ready_o_merge_pe               (merge_ready_o_5_6),
    .valid_o_merge_pe               (merge_valid_o_5_6),
    .data_o_merge_pe                (merge_data_o_5_6),
    .ready_i_merge_pe               (merge_ready_i_5_6),
    .credit_upd                     (credit_upd[5][6])
);


network_interface #(
    .isCaster                       (isCaster_5_7),
    .stream_id                      (stream_id_5_7)
)ni_5_7(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[5][7]),
    .data_i_cast_nw                 (data_o_cast_nw[5][7]),
    .ready_o_cast_nw                (ready_i_cast_nw[5][7]),
    .valid_o_cast_nw                (valid_i_cast_nw[5][7]),
    .data_o_cast_nw                 (data_i_cast_nw[5][7]),
    .ready_i_cast_nw                (ready_o_cast_nw[5][7]),
    .valid_i_merge_nw               (valid_o_merge_nw[5][7]),
    .data_i_merge_nw                (data_o_merge_nw[5][7]),
    .ready_o_merge_nw               (ready_i_merge_nw[5][7]),
    .valid_o_merge_nw               (valid_i_merge_nw[5][7]),
    .data_o_merge_nw                (data_i_merge_nw[5][7]),
    .ready_i_merge_nw               (ready_o_merge_nw[5][7]),
    .valid_i_cast_pe                (cast_valid_i_5_7),
    .data_i_cast_pe                 (cast_data_i_5_7),
    .ready_o_cast_pe                (cast_ready_o_5_7),
    .valid_o_cast_pe                (cast_valid_o_5_7),
    .data_o_cast_pe                 (cast_data_o_5_7),
    .ready_i_cast_pe                (cast_ready_i_5_7),
    .valid_i_merge_pe               (merge_valid_i_5_7),
    .data_i_merge_pe                (merge_data_i_5_7),
    .ready_o_merge_pe               (merge_ready_o_5_7),
    .valid_o_merge_pe               (merge_valid_o_5_7),
    .data_o_merge_pe                (merge_data_o_5_7),
    .ready_i_merge_pe               (merge_ready_i_5_7),
    .credit_upd                     (credit_upd[5][7])
);


network_interface #(
    .isCaster                       (isCaster_6_0),
    .stream_id                      (stream_id_6_0)
)ni_6_0(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[6][0]),
    .data_i_cast_nw                 (data_o_cast_nw[6][0]),
    .ready_o_cast_nw                (ready_i_cast_nw[6][0]),
    .valid_o_cast_nw                (valid_i_cast_nw[6][0]),
    .data_o_cast_nw                 (data_i_cast_nw[6][0]),
    .ready_i_cast_nw                (ready_o_cast_nw[6][0]),
    .valid_i_merge_nw               (valid_o_merge_nw[6][0]),
    .data_i_merge_nw                (data_o_merge_nw[6][0]),
    .ready_o_merge_nw               (ready_i_merge_nw[6][0]),
    .valid_o_merge_nw               (valid_i_merge_nw[6][0]),
    .data_o_merge_nw                (data_i_merge_nw[6][0]),
    .ready_i_merge_nw               (ready_o_merge_nw[6][0]),
    .valid_i_cast_pe                (cast_valid_i_6_0),
    .data_i_cast_pe                 (cast_data_i_6_0),
    .ready_o_cast_pe                (cast_ready_o_6_0),
    .valid_o_cast_pe                (cast_valid_o_6_0),
    .data_o_cast_pe                 (cast_data_o_6_0),
    .ready_i_cast_pe                (cast_ready_i_6_0),
    .valid_i_merge_pe               (merge_valid_i_6_0),
    .data_i_merge_pe                (merge_data_i_6_0),
    .ready_o_merge_pe               (merge_ready_o_6_0),
    .valid_o_merge_pe               (merge_valid_o_6_0),
    .data_o_merge_pe                (merge_data_o_6_0),
    .ready_i_merge_pe               (merge_ready_i_6_0),
    .credit_upd                     (credit_upd[6][0])
);


network_interface #(
    .isCaster                       (isCaster_6_1),
    .stream_id                      (stream_id_6_1)
)ni_6_1(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[6][1]),
    .data_i_cast_nw                 (data_o_cast_nw[6][1]),
    .ready_o_cast_nw                (ready_i_cast_nw[6][1]),
    .valid_o_cast_nw                (valid_i_cast_nw[6][1]),
    .data_o_cast_nw                 (data_i_cast_nw[6][1]),
    .ready_i_cast_nw                (ready_o_cast_nw[6][1]),
    .valid_i_merge_nw               (valid_o_merge_nw[6][1]),
    .data_i_merge_nw                (data_o_merge_nw[6][1]),
    .ready_o_merge_nw               (ready_i_merge_nw[6][1]),
    .valid_o_merge_nw               (valid_i_merge_nw[6][1]),
    .data_o_merge_nw                (data_i_merge_nw[6][1]),
    .ready_i_merge_nw               (ready_o_merge_nw[6][1]),
    .valid_i_cast_pe                (cast_valid_i_6_1),
    .data_i_cast_pe                 (cast_data_i_6_1),
    .ready_o_cast_pe                (cast_ready_o_6_1),
    .valid_o_cast_pe                (cast_valid_o_6_1),
    .data_o_cast_pe                 (cast_data_o_6_1),
    .ready_i_cast_pe                (cast_ready_i_6_1),
    .valid_i_merge_pe               (merge_valid_i_6_1),
    .data_i_merge_pe                (merge_data_i_6_1),
    .ready_o_merge_pe               (merge_ready_o_6_1),
    .valid_o_merge_pe               (merge_valid_o_6_1),
    .data_o_merge_pe                (merge_data_o_6_1),
    .ready_i_merge_pe               (merge_ready_i_6_1),
    .credit_upd                     (credit_upd[6][1])
);


network_interface #(
    .isCaster                       (isCaster_6_2),
    .stream_id                      (stream_id_6_2)
)ni_6_2(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[6][2]),
    .data_i_cast_nw                 (data_o_cast_nw[6][2]),
    .ready_o_cast_nw                (ready_i_cast_nw[6][2]),
    .valid_o_cast_nw                (valid_i_cast_nw[6][2]),
    .data_o_cast_nw                 (data_i_cast_nw[6][2]),
    .ready_i_cast_nw                (ready_o_cast_nw[6][2]),
    .valid_i_merge_nw               (valid_o_merge_nw[6][2]),
    .data_i_merge_nw                (data_o_merge_nw[6][2]),
    .ready_o_merge_nw               (ready_i_merge_nw[6][2]),
    .valid_o_merge_nw               (valid_i_merge_nw[6][2]),
    .data_o_merge_nw                (data_i_merge_nw[6][2]),
    .ready_i_merge_nw               (ready_o_merge_nw[6][2]),
    .valid_i_cast_pe                (cast_valid_i_6_2),
    .data_i_cast_pe                 (cast_data_i_6_2),
    .ready_o_cast_pe                (cast_ready_o_6_2),
    .valid_o_cast_pe                (cast_valid_o_6_2),
    .data_o_cast_pe                 (cast_data_o_6_2),
    .ready_i_cast_pe                (cast_ready_i_6_2),
    .valid_i_merge_pe               (merge_valid_i_6_2),
    .data_i_merge_pe                (merge_data_i_6_2),
    .ready_o_merge_pe               (merge_ready_o_6_2),
    .valid_o_merge_pe               (merge_valid_o_6_2),
    .data_o_merge_pe                (merge_data_o_6_2),
    .ready_i_merge_pe               (merge_ready_i_6_2),
    .credit_upd                     (credit_upd[6][2])
);


network_interface #(
    .isCaster                       (isCaster_6_3),
    .stream_id                      (stream_id_6_3)
)ni_6_3(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[6][3]),
    .data_i_cast_nw                 (data_o_cast_nw[6][3]),
    .ready_o_cast_nw                (ready_i_cast_nw[6][3]),
    .valid_o_cast_nw                (valid_i_cast_nw[6][3]),
    .data_o_cast_nw                 (data_i_cast_nw[6][3]),
    .ready_i_cast_nw                (ready_o_cast_nw[6][3]),
    .valid_i_merge_nw               (valid_o_merge_nw[6][3]),
    .data_i_merge_nw                (data_o_merge_nw[6][3]),
    .ready_o_merge_nw               (ready_i_merge_nw[6][3]),
    .valid_o_merge_nw               (valid_i_merge_nw[6][3]),
    .data_o_merge_nw                (data_i_merge_nw[6][3]),
    .ready_i_merge_nw               (ready_o_merge_nw[6][3]),
    .valid_i_cast_pe                (cast_valid_i_6_3),
    .data_i_cast_pe                 (cast_data_i_6_3),
    .ready_o_cast_pe                (cast_ready_o_6_3),
    .valid_o_cast_pe                (cast_valid_o_6_3),
    .data_o_cast_pe                 (cast_data_o_6_3),
    .ready_i_cast_pe                (cast_ready_i_6_3),
    .valid_i_merge_pe               (merge_valid_i_6_3),
    .data_i_merge_pe                (merge_data_i_6_3),
    .ready_o_merge_pe               (merge_ready_o_6_3),
    .valid_o_merge_pe               (merge_valid_o_6_3),
    .data_o_merge_pe                (merge_data_o_6_3),
    .ready_i_merge_pe               (merge_ready_i_6_3),
    .credit_upd                     (credit_upd[6][3])
);


network_interface #(
    .isCaster                       (isCaster_6_4),
    .stream_id                      (stream_id_6_4)
)ni_6_4(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[6][4]),
    .data_i_cast_nw                 (data_o_cast_nw[6][4]),
    .ready_o_cast_nw                (ready_i_cast_nw[6][4]),
    .valid_o_cast_nw                (valid_i_cast_nw[6][4]),
    .data_o_cast_nw                 (data_i_cast_nw[6][4]),
    .ready_i_cast_nw                (ready_o_cast_nw[6][4]),
    .valid_i_merge_nw               (valid_o_merge_nw[6][4]),
    .data_i_merge_nw                (data_o_merge_nw[6][4]),
    .ready_o_merge_nw               (ready_i_merge_nw[6][4]),
    .valid_o_merge_nw               (valid_i_merge_nw[6][4]),
    .data_o_merge_nw                (data_i_merge_nw[6][4]),
    .ready_i_merge_nw               (ready_o_merge_nw[6][4]),
    .valid_i_cast_pe                (cast_valid_i_6_4),
    .data_i_cast_pe                 (cast_data_i_6_4),
    .ready_o_cast_pe                (cast_ready_o_6_4),
    .valid_o_cast_pe                (cast_valid_o_6_4),
    .data_o_cast_pe                 (cast_data_o_6_4),
    .ready_i_cast_pe                (cast_ready_i_6_4),
    .valid_i_merge_pe               (merge_valid_i_6_4),
    .data_i_merge_pe                (merge_data_i_6_4),
    .ready_o_merge_pe               (merge_ready_o_6_4),
    .valid_o_merge_pe               (merge_valid_o_6_4),
    .data_o_merge_pe                (merge_data_o_6_4),
    .ready_i_merge_pe               (merge_ready_i_6_4),
    .credit_upd                     (credit_upd[6][4])
);


network_interface #(
    .isCaster                       (isCaster_6_5),
    .stream_id                      (stream_id_6_5)
)ni_6_5(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[6][5]),
    .data_i_cast_nw                 (data_o_cast_nw[6][5]),
    .ready_o_cast_nw                (ready_i_cast_nw[6][5]),
    .valid_o_cast_nw                (valid_i_cast_nw[6][5]),
    .data_o_cast_nw                 (data_i_cast_nw[6][5]),
    .ready_i_cast_nw                (ready_o_cast_nw[6][5]),
    .valid_i_merge_nw               (valid_o_merge_nw[6][5]),
    .data_i_merge_nw                (data_o_merge_nw[6][5]),
    .ready_o_merge_nw               (ready_i_merge_nw[6][5]),
    .valid_o_merge_nw               (valid_i_merge_nw[6][5]),
    .data_o_merge_nw                (data_i_merge_nw[6][5]),
    .ready_i_merge_nw               (ready_o_merge_nw[6][5]),
    .valid_i_cast_pe                (cast_valid_i_6_5),
    .data_i_cast_pe                 (cast_data_i_6_5),
    .ready_o_cast_pe                (cast_ready_o_6_5),
    .valid_o_cast_pe                (cast_valid_o_6_5),
    .data_o_cast_pe                 (cast_data_o_6_5),
    .ready_i_cast_pe                (cast_ready_i_6_5),
    .valid_i_merge_pe               (merge_valid_i_6_5),
    .data_i_merge_pe                (merge_data_i_6_5),
    .ready_o_merge_pe               (merge_ready_o_6_5),
    .valid_o_merge_pe               (merge_valid_o_6_5),
    .data_o_merge_pe                (merge_data_o_6_5),
    .ready_i_merge_pe               (merge_ready_i_6_5),
    .credit_upd                     (credit_upd[6][5])
);


network_interface #(
    .isCaster                       (isCaster_6_6),
    .stream_id                      (stream_id_6_6)
)ni_6_6(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[6][6]),
    .data_i_cast_nw                 (data_o_cast_nw[6][6]),
    .ready_o_cast_nw                (ready_i_cast_nw[6][6]),
    .valid_o_cast_nw                (valid_i_cast_nw[6][6]),
    .data_o_cast_nw                 (data_i_cast_nw[6][6]),
    .ready_i_cast_nw                (ready_o_cast_nw[6][6]),
    .valid_i_merge_nw               (valid_o_merge_nw[6][6]),
    .data_i_merge_nw                (data_o_merge_nw[6][6]),
    .ready_o_merge_nw               (ready_i_merge_nw[6][6]),
    .valid_o_merge_nw               (valid_i_merge_nw[6][6]),
    .data_o_merge_nw                (data_i_merge_nw[6][6]),
    .ready_i_merge_nw               (ready_o_merge_nw[6][6]),
    .valid_i_cast_pe                (cast_valid_i_6_6),
    .data_i_cast_pe                 (cast_data_i_6_6),
    .ready_o_cast_pe                (cast_ready_o_6_6),
    .valid_o_cast_pe                (cast_valid_o_6_6),
    .data_o_cast_pe                 (cast_data_o_6_6),
    .ready_i_cast_pe                (cast_ready_i_6_6),
    .valid_i_merge_pe               (merge_valid_i_6_6),
    .data_i_merge_pe                (merge_data_i_6_6),
    .ready_o_merge_pe               (merge_ready_o_6_6),
    .valid_o_merge_pe               (merge_valid_o_6_6),
    .data_o_merge_pe                (merge_data_o_6_6),
    .ready_i_merge_pe               (merge_ready_i_6_6),
    .credit_upd                     (credit_upd[6][6])
);


network_interface #(
    .isCaster                       (isCaster_6_7),
    .stream_id                      (stream_id_6_7)
)ni_6_7(
    .clk                            (clk),
    .rstn                           (rstn),
    .valid_i_cast_nw                (valid_o_cast_nw[6][7]),
    .data_i_cast_nw                 (data_o_cast_nw[6][7]),
    .ready_o_cast_nw                (ready_i_cast_nw[6][7]),
    .valid_o_cast_nw                (valid_i_cast_nw[6][7]),
    .data_o_cast_nw                 (data_i_cast_nw[6][7]),
    .ready_i_cast_nw                (ready_o_cast_nw[6][7]),
    .valid_i_merge_nw               (valid_o_merge_nw[6][7]),
    .data_i_merge_nw                (data_o_merge_nw[6][7]),
    .ready_o_merge_nw               (ready_i_merge_nw[6][7]),
    .valid_o_merge_nw               (valid_i_merge_nw[6][7]),
    .data_o_merge_nw                (data_i_merge_nw[6][7]),
    .ready_i_merge_nw               (ready_o_merge_nw[6][7]),
    .valid_i_cast_pe                (cast_valid_i_6_7),
    .data_i_cast_pe                 (cast_data_i_6_7),
    .ready_o_cast_pe                (cast_ready_o_6_7),
    .valid_o_cast_pe                (cast_valid_o_6_7),
    .data_o_cast_pe                 (cast_data_o_6_7),
    .ready_i_cast_pe                (cast_ready_i_6_7),
    .valid_i_merge_pe               (merge_valid_i_6_7),
    .data_i_merge_pe                (merge_data_i_6_7),
    .ready_o_merge_pe               (merge_ready_o_6_7),
    .valid_o_merge_pe               (merge_valid_o_6_7),
    .data_o_merge_pe                (merge_data_o_6_7),
    .ready_i_merge_pe               (merge_ready_i_6_7),
    .credit_upd                     (credit_upd[6][7])
);

endmodule
