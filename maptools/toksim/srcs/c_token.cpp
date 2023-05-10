# include "c_token.h"

namespace toksim{

    C_Token::C_Token(){}
    C_Token::C_Token(
        int token_num
    ):
        token_num(token_num),
        mode(SINGLE),
        upsample_h(1),
        upsample_w(1)
    {}

    void C_Token::set_mode(C_TokenMode token_mode){
        this->mode = token_mode;
    }

    void C_Token::set_upsample(int upsample_h, int upsample_w){
        this->upsample_h = upsample_h;
        this->upsample_w = upsample_w;
    }

    void C_Token::merge(C_Token token){
        if(token.mode == UPSAMPLE){
            this->mode = token.mode;
            this->upsample_h = token.upsample_h;
            this->upsample_w = token.upsample_w;
        }
        this->token_num += token.token_num;
    }

    void C_Token::pop(C_Token token){
        this->token_num -= token.token_num;
    }
}
