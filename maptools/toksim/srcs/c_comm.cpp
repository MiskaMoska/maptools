# include "c_comm.h"

namespace toksim{
    C_Comm::C_Comm(){}
    C_Comm::C_Comm(int nc): 
        nc(nc),
        token(0),
        accum_tokens(0){}

    void C_Comm::consume_tokens(int token, string pred){
        this->token = token;
    }
    int C_Comm::produce_tokens(){
        this->accum_tokens += token * nc;
        auto _token = this->token;
        this->token = 0;
        return _token;
    }

    C_MergeComm::C_MergeComm(){}
    C_MergeComm::C_MergeComm(int nc, vector<string> preds):C_Comm(nc){
        this->buf = unordered_map<string, int>();
        for(auto it : preds) this->buf[it] = 0;
    }

    void C_MergeComm::consume_tokens(int token, string pred){
        this->buf[pred] += token;
    }

    int C_MergeComm::produce_tokens(){
        auto p = min_element(
            buf.begin(), buf.end(),
            [](const pair<string, int> &left, const pair<string, int> &right){
                return left.second < right.second;
            }    
        );
        auto token = (*p).second;
        for(auto &it : this->buf){
            it.second -= token;
        }
        return token;
    }
}