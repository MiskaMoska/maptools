
`ifndef         __PARAMS_SVH__
`define         __PARAMS_SVH__

// data width
// identical to cast, merge, and gather
`define         DW                                          34 

// channel number
// for cast router:     0:local 1:west 2:east 3:vert0 4:vert1
// for gather router:   0:local 1:west 2:east 3:north 5:south
// merge router does not use parametric channel id
`define         CN                                          5 

// network size
// identical to cast, merge, and gather
`define         NOC_WIDTH                                   10
`define         NOC_HEIGHT                                  25

// buffer allocated for credit-based flow control
// identical to both cast and gather
`define         BUFFER_ALLOC                                256
`define         BUFFER_ALLOC_LOG                            8

// routing table depth, identical to both cast and gather
// merge network does not use routing table
// determined by how many streams one channel can support
`define         ROUTE_TABLE_DEPTH                           16

// packet length
// identical to both cast and gather 
// merge network transfers data without packets
`define         PKT_LEN                                     18
`define         PKT_LEN_LOG                                 5

// intra-router fifo depth
`define         CAST_ROUTER_BUFFER_DEPTH_LOG                6
`define         MERGE_ROUTER_BUFFER_DEPTH_LOG               4
`define         GATHER_ROUTER_BUFFER_DEPTH_LOG              4

// stream-id zone in packet header
// identical to both cast and gather
// merge network does not need stream-id 
`define         STREAM_ID_H                                 9
`define         STREAM_ID_L                                 0            

// packet type define
`define         HEAD                                        2'b00
`define         BODY                                        2'b01
`define         TAIL                                        2'b11

`endif

