from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map

cdef extern from "srcs/c_typing.h" namespace "toksim":
    cdef enum C_PredType:
        CAST, MERGE, GATHER

    # this structure must be declared for parameter typing parsing
    cdef struct C_TileConfig:
        bint has_conv, has_pool, has_resize;
        bint is_merge, is_gather;
        int xbar_num_ichan, xbar_num_ochan;
        vector[int] conv_input_size;
        vector[int] conv_output_size;
        vector[int] conv_kernel_size;
        vector[int] conv_strides;
        vector[int] conv_pads;
        vector[int] pool_input_size;
        vector[int] pool_output_size;
        vector[int] pool_kernel_size;
        vector[int] pool_strides;
        vector[int] pool_pads;
        vector[int] resize_scales;

    # this structure must be declared for parameter typing parsing
    cdef struct C_NodeAttr:
        bint is_tile;
        bint is_head_tile;
        bint is_tail_tile;
        bint is_comm;
        bint is_cast_comm;
        bint is_merge_comm;
        bint is_gather_comm;
        vector[string] preds, succs;

cdef extern from "srcs/c_token.h" namespace "toksim":
    cdef cppclass C_Token

cdef extern from "srcs/c_windowbuf.h" namespace "toksim":
    cdef cppclass C_WindowBuf

cdef extern from "srcs/c_tile.h" namespace "toksim":
    cdef cppclass C_Tile

cdef extern from "srcs/c_comm.h" namespace "toksim":
    cdef cppclass C_Comm
    cdef cppclass C_MergeComm

cdef extern from "srcs/c_toksim.h" namespace "toksim":
    cdef cppclass C_TokSim:
        vector[string] nodes;

        unordered_map[string, C_NodeAttr] node_attr_dict;
        unordered_map[string, C_TileConfig] tile_config_dict;

        unordered_map[string, C_Tile] tile_objects;
        unordered_map[string, C_Comm] comm_objects;

        unordered_map[string, unordered_map[string, int]] need_bufs;

        C_TokSim() except +
        C_TokSim(
            vector[string] nodes,
            unordered_map[string, C_NodeAttr] node_attr_dict,
            unordered_map[string, C_TileConfig] tile_config_dict
        ) except +

        void _build_objects();
        bint _iter();
        void run();
        void collect_bufs();