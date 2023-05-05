# ifndef C_COMM_H
# define C_COMM_H
# include <iostream>
# include <vector>
# include <unordered_map>
# include <string>
# include <algorithm>
# include <unistd.h>

using namespace std;

namespace toksim{

    class C_Comm{
        public:
            int nc, token, accum_tokens;
            C_Comm();
            C_Comm(int nc);
            void consume_tokens(int token, string pred);
            int produce_tokens();
    };

    class C_MergeComm: public C_Comm{
        public:
            unordered_map<string, int> buf;
            C_MergeComm();
            C_MergeComm(int nc, vector<string> preds);
            void consume_tokens(int token, string pred);
            int produce_tokens();
    };
    
}


# endif