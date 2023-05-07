# ifndef C_TOKEN_H
# define C_TOKEN_H
# include "c_typing.h"

namespace toksim{

    class C_Token{
        public:
            int token_num;
            C_TokenMode mode;
            int upsample_h, upsample_w;
            C_Token();
            C_Token(int token_num);
            void merge(C_Token token);
    };

}


# endif