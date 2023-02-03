
`ifndef         __PARAMS_SVH__
`define         __PARAMS_SVH__

`define         DW                              16 //data width
`define         CN                              5 //channel number 0:local 1:west 2:east 3:verti0 4:verti1
`define         NOC_WIDTH                       5
`define         NOC_HEIGHT                      11

`define         BUFFER_ALLOC                    32
`define         BUFFER_ALLOC_LOG                5

`define         ROUTE_TABLE_DEPTH               16
`define         CAST_ROUTER_BUFFER_DEPTH_LOG    4

`define         PKT_LEN                         16
`define         PKT_LEN_LOG                     4


//packet contents begin

`define         STREAM_ID_H                     9
`define         STREAM_ID_L                     0

`define         PKT_LEN_H                       `STREAM_ID_H+8
`define         PKT_LEN_L                       `STREAM_ID_H+1

//packet contents end

`define         HEAD                            2'b00
`define         BODY                            2'b01
`define         TAIL                            2'b11

`endif
