# include "c_tile.h"

namespace toksim{
    C_Tile::C_Tile(){}
    C_Tile::C_Tile(C_TileConfig config): 
        config(config), 
        inter_buf(0),
        merge_buf(0),
        gather_buf(0),
        max_inter_buf(0),
        max_merge_buf(0),
        max_gather_buf(0),
        done(false)
    {
        this->conv_buf = C_WindowBuf(
            config.xbar_num_ichan,
            config.conv_input_size,
            config.conv_output_size,
            config.conv_kernel_size,
            config.conv_strides,
            config.conv_pads
        );

        if(config.has_pool){
            this->pool_buf = C_WindowBuf(
                config.xbar_num_ochan,
                config.pool_input_size,
                config.pool_output_size,
                config.pool_kernel_size,
                config.pool_strides,
                config.pool_pads
            );
        }
    }

    void C_Tile::_update_max_buf(){
        if(inter_buf > max_inter_buf)
            this->max_inter_buf = inter_buf;

        if(merge_buf > max_merge_buf)
            this->max_merge_buf = merge_buf;

        if(gather_buf > max_gather_buf)
            this->max_gather_buf = gather_buf;
    }

    void C_Tile::_consume_tokens_cast(int token){
        if(token > 0)
            conv_buf.add_token(token);
        auto res = conv_buf.try_slide();
        this->inter_buf += res;

        if(!config.has_pool)
            this->done = conv_buf.done;
    }
    void C_Tile::_consume_tokens_merge(int token){
        merge_buf += token;
    }
    void C_Tile::_consume_tokens_gather(int token){
        gather_buf += token;
    }
    void C_Tile::consume_tokens(int token, C_PredType pred_type){
        if(pred_type == CAST)
            this->_consume_tokens_cast(token);
        else if(pred_type == MERGE)
            this->_consume_tokens_merge(token);
        else if(pred_type == GATHER)
            this->_consume_tokens_gather(token);
    }
    int C_Tile::produce_tokens(){
        int token = 0;
        if(!config.is_merge && !config.is_gather){
            if(config.has_pool){
                pool_buf.add_token(inter_buf);
                token = pool_buf.try_slide();
                this->done = pool_buf.done;
            }else{
                token = inter_buf;
            }
            this->inter_buf = 0;
        }else{
            vector<int> cmp_list{inter_buf};
            if(config.is_merge)
                cmp_list.push_back(merge_buf);
            if(config.is_gather)
                cmp_list.push_back(gather_buf);
            token = *min_element(cmp_list.begin(), cmp_list.end());
            this->inter_buf -= token;
            this->merge_buf -= (config.is_merge ? token : 0);
            this->gather_buf -= (config.is_gather ? token : 0);

            this->_update_max_buf();

            if(config.has_pool){
                pool_buf.add_token(token);
                token = pool_buf.try_slide();
                this->done = pool_buf.done;
            }
        }
        if(config.has_resize){
            token *= (config.resize_scales[2] * config.resize_scales[3]);
        }

        return token;
    }
} 
