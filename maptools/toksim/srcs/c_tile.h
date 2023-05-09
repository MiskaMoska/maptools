# ifndef C_TILE_H
# define C_TILE_H
# include "c_typing.h"
# include "c_windowbuf.h"
# include "c_token.h"

using namespace std;

namespace toksim{

    class C_Tile{
        public:
            C_TileConfig config;
            C_WindowBuf conv_buf, pool_buf;
            
            int inter_buf, merge_buf, gather_buf;
            int max_inter_buf, max_merge_buf, max_gather_buf;
            bool done;
            
            C_Tile();
            C_Tile(C_TileConfig config);
            void _update_max_buf();
            void _consume_tokens_cast(C_Token token);
            void _consume_tokens_merge(C_Token token);
            void _consume_tokens_gather(C_Token token);
            void consume_tokens(C_Token token, C_PredType pred_type);
            C_Token produce_tokens();
    };

}

# endif