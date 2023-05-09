# ifndef C_COMM_H
# define C_COMM_H
# include "c_typing.h"
# include "c_token.h"

using namespace std;

namespace toksim{

    class C_Comm{
        public:
            int nc, accum_tokens;
            C_Token token;
            C_Comm();
            C_Comm(int nc);
            void consume_tokens(C_Token token, string pred);
            C_Token produce_tokens();
    };

    class C_MergeComm: public C_Comm{
        public:
            unordered_map<string, C_Token> buf;
            C_MergeComm();
            C_MergeComm(int nc, vector<string> preds);
            void consume_tokens(C_Token token, string pred);
            C_Token produce_tokens();
    };
    
}


# endif