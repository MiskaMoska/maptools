# include "c_comm.h"

namespace toksim{
    C_Comm::C_Comm(){}
    C_Comm::C_Comm(int nc): 
        nc(nc),
        accum_tokens(0),
        token(C_Token(0)){}

    void C_Comm::consume_tokens(C_Token token, string pred){
        this->token = token;
    }
    C_Token C_Comm::produce_tokens(){
        this->accum_tokens += token.token_num * nc;
        auto _token = this->token;
        this->token = C_Token(0);
        return _token;
    }

    C_MergeComm::C_MergeComm(){}
    C_MergeComm::C_MergeComm(int nc, vector<string> preds):C_Comm(nc){
        this->buf = unordered_map<string, C_Token>();
        for(auto it : preds) this->buf[it] = C_Token(0);
    }

    void C_MergeComm::consume_tokens(C_Token token, string pred){
        this->buf[pred].merge(token);
    }

    C_Token C_MergeComm::produce_tokens(){
        auto p = min_element(
            buf.begin(), buf.end(),
            [](const pair<string, C_Token> &left, const pair<string, C_Token> &right){
                return left.second.token_num < right.second.token_num;
            }
        );
        C_Token _token((*p).second);
        for(auto &it : this->buf){
            it.second.pop(_token);
        }
        return _token;
    }
}