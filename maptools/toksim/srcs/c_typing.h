# ifndef C_TYPING_H
# define C_TYPING_H
# include <iostream>
# include <vector>
# include <unordered_map>
# include <string>
# include <algorithm>
# include <unistd.h>

using namespace std;

namespace toksim{
    enum C_PredType{
        CAST, MERGE, GATHER
    };

    struct C_TileConfig{
        bool 
            has_conv,
            has_pool,
            has_resize;

        bool 
            is_merge, 
            is_gather;

        int 
            xbar_num_ichan, 
            xbar_num_ochan;
        
        vector<int> 
            conv_input_size,
            conv_output_size,
            conv_kernel_size,
            conv_strides,
            conv_pads,
            pool_input_size,
            pool_output_size,
            pool_kernel_size,
            pool_strides,
            pool_pads,
            resize_scales;          
    };

    struct C_NodeAttr{
        bool
            is_tile,
            is_head_tile,
            is_tail_tile,
            is_comm,
            is_cast_comm,
            is_merge_comm,
            is_gather_comm;

        vector<string> preds, succs;
    };

}
# endif