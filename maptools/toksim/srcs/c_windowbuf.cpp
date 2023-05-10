# include <cassert>
# include "c_windowbuf.h"

namespace toksim{
    C_WindowBuf::C_WindowBuf(){}
    C_WindowBuf::C_WindowBuf(
        int xbar_num_ichan,
        vector<int> input_size,
        vector<int> output_size,
        vector<int> kernel_size,
        vector<int> strides,
        vector<int> pads
    ):
        size_i_np(input_size), 
        size_o(output_size), 
        ks(kernel_size),
        strides(strides),
        pads(pads),
        ni(xbar_num_ichan),
        rptr(0),
        wptr(0),
        size_config_flag(true),
        size_i_before_resize(vector<int>{0, 0}),
        released_token(0),
        max_buf(0),
        close(false),
        done(false)
    {
        this->size_i = {
            input_size[0] + pads[0] + pads[2],
            input_size[1] + pads[1] + pads[3]
        };

        this->buf = vector<vector<int>>(
            this->size_i[0], 
            vector<int>(this->size_i[1], 0)
        );

        this->need_token = max(
            ks[0] * ks[1],
            strides[0] * strides[1]
        );

        this->_init_pads();
    }

    void C_WindowBuf::_init_pads(){
        int start, end;
        if(pads[0] > 0){
            start = 0;
            end = pads[0];
            for(int i=start; i<end; i++){
                for(auto it=buf[i].begin(); it!=buf[i].end(); it++){
                    *it = 1;
                }
            }
        }
        if(pads[1] > 0){
            start = size_i[1] - pads[1];
            end = size_i[1];
            for(auto it=buf.begin(); it!=buf.end(); it++){
                for(int i=start; i<end; i++){
                    (*it)[i] = 1;
                }
            }
        }
        if(pads[2] > 0){
            start = size_i[0] - pads[2];
            end = size_i[0];
            for(int i=start; i<end; i++){
                for(auto it=buf[i].begin(); it!=buf[i].end(); it++){
                    *it = 1;
                }
            }
        }
        if(pads[3] > 0){
            start = 0;
            end = pads[3];
            for(auto it=buf.begin(); it!=buf.end(); it++){
                for(int i=start; i<end; i++){
                    (*it)[i] = 1;
                }
            }
        }
    }

    tuple<int, int> C_WindowBuf::coord_trans(int coord_y, int coord_x){
        int np_coord_y = coord_y <= pads[0]-1 ? 0 : (
                            coord_y > size_i[0] - pads[2]-1 ? (size_i_np[0]-1) : 
                            coord_y - pads[0]);
        
        int np_coord_x = coord_x <= pads[3]-1 ? 0 : (
                            coord_x > size_i[1]-pads[1]-1 ? (size_i_np[1]-1) : 
                            coord_x - pads[3]);

        return make_tuple(np_coord_y, np_coord_x);
    }

    void C_WindowBuf::_update_max_buf(){
        auto np_winstart = coord_trans(get<0>(winpos), get<1>(winpos));
        auto np_winend = coord_trans(get<2>(winpos)-1, get<3>(winpos)-1);

        int start_ptr = get<0>(np_winstart) * size_i_np[1] + get<1>(np_winstart);
        int end_ptr = get<0>(np_winend) * size_i_np[1] + get<1>(np_winend);
        int buffered = end_ptr + 1 - start_ptr;
        
        if(buffered > max_buf){
            this->max_buf = buffered;
        }
    }

    void C_WindowBuf::add_token(C_Token token){
        int y, x, pos_y, pos_x, bf_y, bf_x;
        if(!token.token_num) return;
        for(int k=0; k<token.token_num; k++){
            if(close) return;

            if(token.mode == SINGLE){
                y = wptr / size_i_np[1];
                x = wptr % size_i_np[1];
                pos_y = y + pads[0];
                pos_x = x + pads[3];
                buf[pos_y][pos_x] = 1;
            }

            else{
                if(size_config_flag){
                    size_config_flag = false;
                    size_i_before_resize[0] = size_i_np[0] / token.upsample_h;
                    size_i_before_resize[1] = size_i_np[1] / token.upsample_w;
                }

                bf_y = wptr / size_i_before_resize[1];
                bf_x = wptr % size_i_before_resize[1];

                for(int i=0; i<token.upsample_h; i++){
                    y = bf_y * token.upsample_h + i;
                    pos_y = y + pads[0];

                    for(int j=0; j<token.upsample_w; j++){
                        x = bf_x * token.upsample_w + j;
                        pos_x = x + pads[3];
                        buf[pos_y][pos_x] = 1;
                    }
                }
            }

            wptr++;

            if(y + 1 >= size_i_np[0] && x + 1 >= size_i_np[1]){
                this->close = true;
                return;
            }
        }
    }

    tuple<int, int, int, int> C_WindowBuf::win_pos(){
        int dy, dx, win_y, win_x, win_h, win_w;
        dy = rptr / size_o[1];
        dx = rptr % size_o[1];
        win_y = dy * strides[0];
        win_x = dx * strides[1];
        win_h = max(strides[0], ks[0]);
        win_w = max(strides[1], ks[1]);
        return make_tuple(win_y, win_x, win_y+win_h, win_x+win_w);
    }

    bool C_WindowBuf::is_pad(int buf_y, int buf_x){
        if(buf_y < pads[0]) return true;
        else if(buf_y >= size_i[0]-pads[2]) return true;
        else if(buf_x < pads[3]) return true;
        else if(buf_x >= size_i[1]-pads[1]) return true;
        return false;
    }

    void C_WindowBuf::_release_data(){
        int rele_y, rele_x;
        if(rptr / size_o[1] == size_o[0] - 1){
            rele_y = max(strides[0], ks[0]);
        }else{
            rele_y = strides[0];
        }
        if(rptr % size_o[1] == size_o[1] - 1){
            rele_x = max(strides[1], ks[1]);
        }else{
            rele_x = strides[1];
        }
        for(int i=get<0>(winpos); i<get<0>(winpos)+rele_y; i++){
            for(int j=get<1>(winpos); j<get<1>(winpos)+rele_x; j++){
                buf[i][j] = 0;
                if(!is_pad(i, j)) released_token++;
            }
        }
    }
    
    C_Token C_WindowBuf::try_slide(){
        if(done) return C_Token(0);
        int token = 0;
        while(true){
            int sum = 0;
            this->winpos = this->win_pos();
            for(int i=get<0>(winpos); i<get<2>(winpos); i++){
                for(int j=get<1>(winpos); j<get<3>(winpos); j++){
                    sum += buf[i][j];
                }
            }
            if(sum == need_token){
                // each time before sliding, record the max buf
                this->_update_max_buf();
                this->_release_data();
                this->rptr++;
                if(rptr == size_o[0] * size_o[1]){
                    this->done = true;
                }
                token++;
            }
            else break;
            if(done) break;
        }
        return C_Token(token);
    }

    void C_WindowBuf::echo_buf(){
        for(auto it1=buf.begin(); it1!=buf.end(); it1++){
            for(auto it2=(*it1).begin(); it2!=(*it1).end(); it2++){
                cout << *it2 << " ";
            }
            cout << endl;
        }
        cout << endl;
    }
}