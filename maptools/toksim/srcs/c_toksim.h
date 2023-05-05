# ifndef C_TOKSIM_H
# define C_TOKSIM_H
# include "c_typing.h"
# include "c_tile.h"
# include "c_comm.h"

using namespace std;

namespace toksim{

    class C_TokSim{
        public:
            int tile_num;
            vector<string> nodes;

            unordered_map<string, C_NodeAttr> node_attr_dict;
            unordered_map<string, C_TileConfig> tile_config_dict;

            unordered_map<string, C_Tile> tile_objects;
            unordered_map<string, C_Comm> comm_objects;

            unordered_map<string, unordered_map<string, int>> need_bufs;

            C_TokSim();
            C_TokSim(
                vector<string> nodes,
                unordered_map<string, C_NodeAttr> node_attr_dict,
                unordered_map<string, C_TileConfig> tile_config_dict
            );

            void _build_objects();
            bool _iter();
            void run();
            void collect_bufs();

        protected:
            bool is_tile(string node);
            bool is_head_tile(string node);
            bool is_tail_tile(string node);
            bool is_comm(string node);
            bool is_cast_comm(string node);
            bool is_merge_comm(string node);
            bool is_gather_comm(string node);
            vector<string> get_preds(string node);
            vector<string> get_succs(string node);
            C_TileConfig get_tile_config(string node);
    };

}

# endif