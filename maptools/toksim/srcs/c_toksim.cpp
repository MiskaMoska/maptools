# include <iostream>
# include <vector>
# include <unordered_map>
# include <string>
# include <algorithm>
# include <unistd.h>
# include "c_toksim.h"

namespace toksim{

    C_TokSim::C_TokSim(){}

    C_TokSim::C_TokSim(
        vector<string> nodes,
        unordered_map<string, C_NodeAttr> node_attr_dict,
        unordered_map<string, C_TileConfig> tile_config_dict
    ):
        nodes(nodes),
        node_attr_dict(node_attr_dict), 
        tile_config_dict(tile_config_dict)
    {
        this->_build_objects();
        this->tile_num = (int)(tile_objects.size());
    }

    void C_TokSim::_build_objects(){
        for(auto &node : nodes){
            if(is_comm(node)){
                auto preds = get_preds(node);
                auto pred = preds[0];
                auto cfg = get_tile_config(node);

                if(is_merge_comm(node)){ // merge comm
                    this->comm_objects[node] = C_MergeComm(
                        cfg.xbar_num_ochan, preds
                    );
                }else{ // normal comm
                    this->comm_objects[node] = C_Comm(
                        cfg.xbar_num_ochan 
                    );
                }
            }
            else if(is_tile(node)){
                auto cfg = get_tile_config(node);
                this->tile_objects[node] = C_Tile(cfg);
            }
        }
    }

    bool C_TokSim::_iter(){
        int token, done_cnt = 0;
        for(auto &node : nodes){
            if(is_tile(node)){
                auto &tile = tile_objects[node];
                if(is_head_tile(node))
                    tile.consume_tokens(1, CAST);
                token = tile.produce_tokens();

                if(tile.done) done_cnt++;
                if(!token) continue;
                if(is_tail_tile(node)) continue;
                auto succs = get_succs(node);
                for(auto &succ : succs){
                    auto &comm = comm_objects[succ];
                    comm.consume_tokens(token, node);
                }
            }
            else if(is_comm(node)){
                auto &comm = comm_objects[node];
                token = comm.produce_tokens();
                auto pred_type = is_cast_comm(node) ? CAST : (
                                 is_merge_comm(node) ? MERGE : GATHER);
                for(auto &succ : get_succs(node)){
                    auto &tile = tile_objects[succ];
                    tile.consume_tokens(token, pred_type);
                }
            }
        }
        cout << "process: " << done_cnt << "/" << tile_num << " tiles" << endl;
        if(done_cnt == tile_num) return true;
        return false;
    }

    void C_TokSim::run(){
        int cnt = 0;
        bool done = false;
        while(!done){
            cnt++;
            cout << "iteration: " << cnt << " ";
            done = this->_iter();
        }
        collect_bufs();
    }

    void C_TokSim::collect_bufs(){
        for(auto &node : nodes){
            if(is_tile(node)){
                auto &tile = tile_objects[node];
                unordered_map<string, int> tile_bufs{};
                tile_bufs["conv_buf"] = tile.conv_buf.max_buf * tile.conv_buf.ni;
                if(tile.config.has_pool){
                    tile_bufs["pool_buf"] = tile.pool_buf.max_buf * tile.pool_buf.ni;
                }else{
                    tile_bufs["pool_buf"] = 0;
                }
                tile_bufs["inter_buf"] = tile.max_inter_buf * tile.config.xbar_num_ochan;
                tile_bufs["merge_buf"] = tile.max_merge_buf * tile.config.xbar_num_ochan;
                tile_bufs["gather_buf"] = tile.max_gather_buf * tile.config.xbar_num_ochan;
                need_bufs[node] = tile_bufs;
            }
        }
    }

    bool C_TokSim::is_tile(string node){
        return node_attr_dict[node].is_tile;
    }

    bool C_TokSim::is_head_tile(string node){
        return node_attr_dict[node].is_head_tile;
    }

    bool C_TokSim::is_tail_tile(string node){
        return node_attr_dict[node].is_tail_tile;
    }

    bool C_TokSim::is_comm(string node){
        return node_attr_dict[node].is_comm;
    }

    bool C_TokSim::is_cast_comm(string node){
        return node_attr_dict[node].is_cast_comm;
    }

    bool C_TokSim::is_merge_comm(string node){
        return node_attr_dict[node].is_merge_comm;
    }

    bool C_TokSim::is_gather_comm(string node){
        return node_attr_dict[node].is_gather_comm;
    }

    vector<string> C_TokSim::get_preds(string node){
        return node_attr_dict[node].preds;
    }

    vector<string> C_TokSim::get_succs(string node){
        return node_attr_dict[node].succs;
    }

    C_TileConfig C_TokSim::get_tile_config(string node){
        return tile_config_dict[node];
    }

}