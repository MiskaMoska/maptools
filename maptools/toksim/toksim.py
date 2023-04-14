'''
To use TokSim to perform evaluation, the precondition is that the bottlenck does not happen at communication.
In other words, the rate the communication link transports data matches the rate the Xbar produces data.  
TODO support finite bandwidth
TODO support linear layer
'''
import os
import time
import pickle
from maptools.ctg import *
from maptools.utils import *
from maptools.core import ROOT_DIR
import numpy as np
from typing import Tuple, List, Any, Optional, Dict

__all__ = ['TokSim']

class _WindowBuf(object):

    def __init__(
        self, 
        input_size: List[int], 
        output_size: List[int],
        kernel_size: List[int], 
        strides: List[int], 
        pads: List[int], 
        ni: int, 
        slide_once: bool = True
    ) -> None:
        '''
        Window buffer

        Parameters
        ----------
        input_size : Tuple[int, int]
            input feture map size [H, W] without pads
        
        output_size : Tuple[int, int]
            output feature map size [H, W]

        kernel_size : List[int]
            convolution or pooling kernel size [H, W]

        strides : List[int]
            pads before convolution or pooling [U, R, D, L]
        
        ni : int
            number of conv input channel
        
        slide_once : bool
            when True, the window slides only once in each iteration,
            when False, the window slides as much as possible in each iteration
        '''
        self.size_i_np = input_size
        self.size_i = [
            input_size[0] + pads[0] + pads[2],
            input_size[1] + pads[1] + pads[3]
        ]
        self.size_o = output_size
        self.ks = kernel_size
        self.strides = strides
        self.pads = pads
        self.ni = ni
        self.slide_once = slide_once

        self.buf = np.zeros(self.size_i, dtype=int)
        self._init_pads()
        self.rptr = 0 # results ptr
        self.wptr = 0 # write ptr

        self.close = False # close == True means all input data is arrived
        self.done = False # done == True means all windows are processed

        # for buffer size analysis
        self.max_buf = 0 # maximum buffer occupied

    def _init_pads(self) -> None:
        # add pads to input feature map by setting the bits to 1
        if self.pads[0] > 0:
            self.buf[0:self.pads[0],:] = 1
        if self.pads[1] > 0:
            self.buf[:,self.size_i[1]-self.pads[1]:self.size_i[1]] = 1
        if self.pads[2] > 0:
            self.buf[self.size_i[0]-self.pads[2]:self.size_i[0],:] = 1
        if self.pads[3] > 0:
            self.buf[:,0:self.pads[3]] = 1

    @property
    def now_buf(self) -> int:
        # now occupied buffer size
        sy = self.pads[0]
        sx = self.pads[3]
        dy = self.size_i[0] - self.pads[2]
        dx = self.size_i[1] - self.pads[1]
        return np.sum(self.buf[sy:dy, sx:dx]) * self.ni
    
    def _update_max_buf(self) -> None:
        if self.now_buf > self.max_buf:
            self.max_buf = self.now_buf

    def add_token(self, token: int) -> None:
        if token == 0:
            return
        for i in range(token):
            if self.close:
                return
            # position on no-pad input feature map
            y = self.wptr // self.size_i_np[1]
            x = self.wptr % self.size_i_np[1]
            # position on padded input feature map
            pos_y = y + self.pads[0]
            pos_x = x + self.pads[3]
            self.buf[pos_y, pos_x] = 1
            self.wptr += 1
            if y + 1 >= self.size_i_np[0] and x + 1 >= self.size_i_np[1]:
                self.close = True
                return

    @property
    def win_pos(self) -> Tuple[int, int, int, int]:
        # [dy, dx] is the position of the results
        dy = self.rptr // self.size_o[1]
        dx = self.rptr % self.size_o[1]
        # [win_y, win_x] is the position of the window
        win_y = dy * self.strides[0]
        win_x = dx * self.strides[1]
        # [win_h, win_w] is the size of the window
        win_h = max([self.strides[0], self.ks[0]])
        win_w = max([self.strides[1], self.ks[1]])
        return (win_y, win_x, win_y+win_h, win_x+win_w)

    def _release_data(self) -> None:
        # release data from buffer
        if self.rptr // self.size_o[1] == self.size_o[0] - 1: # on the down edge
            rele_y = max([self.strides[0], self.ks[0]])
        else:
            rele_y = self.strides[0]
        if self.rptr % self.size_o[1] == self.size_o[1] - 1: # on the right edge
            rele_x = max([self.strides[1], self.ks[1]])
        else:
            rele_x = self.strides[1]
        self.buf[
            self.win_pos[0]:self.win_pos[0]+rele_y,
            self.win_pos[1]:self.win_pos[1]+rele_x
        ] *= 0

    def try_slide(self) -> int:
        if self.done:
            return 0
        token = 0
        while True:
            # the window block in the buffer
            window = self.buf[
                self.win_pos[0] : self.win_pos[2],
                self.win_pos[1] : self.win_pos[3]
            ]
            need_token = max([
                self.ks[0] * self.ks[1], 
                self.strides[0] * self.strides[1]
            ])
            if np.sum(window) == need_token: # all data in window is available
                self._release_data()
                self.rptr += 1 # slide window
                if self.rptr == self.size_o[0] * self.size_o[1]:
                    self.done = True
                token += 1 # return a token
                if self.slide_once:
                    break
            else: # data not prepared
                break
        self._update_max_buf()
        return token


class _Xbar(object):

    def __init__(
        self, 
        config: Dict, 
        is_merge: bool, 
        is_gather: bool, 
        slide_once: bool = True,
        **kwargs: Any
    ) -> None:
        '''
        Xbar abstract model designed for TokSim
        
        Parameters
        ----------
        config : Dict
            xbar config dictionary
        
        is_merge : bool
            whether is a merge destination node

        is_gather : bool
            whether is a gather destination node
        
        slide_once : bool
            when True, the window slides only once in each iteration,
            when False, the window slides as much as possible in each iteration.
        '''
        self.__dict__.update(config)
        assert 'Conv' in self.__dict__['op_type'], \
            f"Xbar must perform convolution, now op_type: {self.__dict__['op_type']}"
        self.is_merge = is_merge
        self.is_gather = is_gather
        self.conv_buf = _WindowBuf(
            self.conv_input_size, 
            self.conv_output_size,
            self.conv_kernel_size, 
            self.conv_strides, 
            self.conv_pads, 
            self.xbar_num_ichan,
            slide_once = slide_once
        )
        if 'Pool' in self.op_type: # has pooling
            self.pool_buf = _WindowBuf(
                self.pool_input_size, 
                self.pool_output_size,
                self.pool_kernel_size, 
                self.pool_strides, 
                self.pool_pads, 
                self.xbar_num_ochan,
                slide_once = slide_once
            ) # pooling input channel is conv output channel
        
        # buffers for results merging
        self.inter_buf = 0
        self.merge_buf = 0
        self.gather_buf = 0
        self.done = False

        # for buffer size analysiz
        self.max_inter_buf = 0 # maximum inter buffer occupied
        self.max_merge_buf = 0 # maximum merge buffer occupied
        self.max_gather_buf = 0 # maximum gather buffer occupied

    def _update_max_buf(self, buf_name: str) -> None:
        max_buf_name = 'max_' + buf_name
        now_buf = self.__dict__[buf_name] * self.conv_num_ochan
        if  now_buf > self.__dict__[max_buf_name]:
            self.__dict__[max_buf_name] = now_buf

    def _consume_tokens_cast(self, token: int) -> None:
        if token > 0:
            self.conv_buf.add_token(token)
        res = self.conv_buf.try_slide() # number of results
        self.inter_buf += res # put the results to inter buffer

        if 'Pool' not in self.op_type:
            self.done = self.conv_buf.done

    def _consume_tokens_merge(self, token: int) -> None:
        self.merge_buf += token

    def _consume_tokens_gather(self, token: int) -> None:
        self.gather_buf += token

    def consume_tokens(self, token: int, pred_type: str) -> None:
        if pred_type == 'Cast':
            self._consume_tokens_cast(token)
        elif pred_type == 'Merge':
            self._consume_tokens_merge(token)
        elif pred_type == 'Gather':
            self._consume_tokens_gather(token)

    def produce_tokens(self) -> int:
        if not self.is_merge and not self.is_gather: # no merge and no gather
            if 'Pool' in self.op_type: # has pooling
                self.pool_buf.add_token(self.inter_buf)
                self.inter_buf = 0 
                token = self.pool_buf.try_slide()
                self.done = self.pool_buf.done
            else: # no pooling
                token = self.inter_buf
                self.inter_buf = 0
            return token

        cmp_list = [self.inter_buf]
        if self.is_merge:
            cmp_list.append(self.merge_buf)
        if self.is_gather:
            cmp_list.append(self.gather_buf)
        token = min(cmp_list)
        self.inter_buf -= token
        self.merge_buf -= (token if self.is_merge else 0)
        self.gather_buf -= (token if self.is_gather else 0)

        # update max buf
        for name in ['inter_buf', 'merge_buf', 'gather_buf']:
            self._update_max_buf(name)

        if 'Pool' in self.op_type: # has pooling
            self.pool_buf.add_token(token)
            token = self.pool_buf.try_slide()
            self.done = self.pool_buf.done

        return token


class _ShiftReg(object):

    def __init__(self, depth: int = 8) -> None:
        '''
        Shift register to simulate communication latency.
        '''
        self.depth = depth
        self.buf = [0] * depth
        self.valid = [False] * depth
    
    def step(self, token: int) -> int:
        data = self.buf[-1]
        valid = self.valid[-1]
        for i in range(1, self.depth):
            self.buf[-i] = self.buf[-(i+1)]
            self.valid[-i] = self.valid[-(i+1)]
        self.buf[0] = token
        self.valid[0] = True
        return data if valid else 0


class _Comm(object):
    
    def __init__(self, nc: int, 
                    latency: Optional[int] = None) -> None:
        '''
        nc : number of channels
        '''
        self.accum_tokens = 0
        self.token = 0
        self.nc = nc
        self.latency = latency
        if self.latency is not None:
            self.shiftreg = _ShiftReg(depth=latency)

    def consume_tokens(self, token: int, pred: Any) -> None:
        self.token = token

    def produce_tokens(self) -> int:
        self.accum_tokens += self.token * self.nc
        token = self.token
        self.token = 0
        if self.latency is None:
            return token
        else:
            return self.shiftreg.step(token)


class _MergeComm(_Comm):

    def __init__(
        self, 
        nc: int, 
        preds: List[Any], 
        latency: Optional[int] = None
    ) -> None:
        '''
        nc : number of channels
        '''
        super().__init__(nc, latency=latency)
        self.buf = {k: 0 for k in preds}

    def consume_tokens(self, token: int, pred: Any) -> None:
        self.buf[pred] += token
    
    def produce_tokens(self) -> int:
        token = min([v for v in self.buf.values()])
        self.accum_tokens += token * self.nc
        for k in self.buf.keys():
            self.buf[k] -= token
        if self.latency is None:
            return token
        else:
            return self.shiftreg.step(token)


class TokSim(object):

    def __init__(
        self, 
        ctg: CTG, 
        slide_once: bool = True, 
        latency: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        '''
        Token simulation machine designed for buffer size and communication load analysis.
        Buffer allocation is important in AI accelerators, especially NVCIM systems, because in
        CNN computing, a certain amount of data should be prepared well before the processing
        unit can perform computing once.

        This implies a producer-consumer model (PCM). In traditional PCMs, the number
        of tokens that should be consumed to produce one token is a constant, 
        to keep the operation flow from deadlock, we only need to set the input buffer
        size larger than the constant value. 

        However, in NVCIM, the number of tokens that should be consumed to produce one token 
        varies under differnet operation states, making it difficult to determine the buffer size threshold. 
        
        Besides, for synchronous data flow graph containing merge-in branches, especially bypass-structured
        branches in NVCIM, the token unbalance between different branches can lead to larger buffer need.
        `TokSim` is an inference-based simulator, it gives designers a simulated value of the lower bound
        of the buffer size that should be allocated for each xbar.

        Besides, `TokSim` helps designers to evaluate the communication load on each connection,
        this is valuable for network bandwidth allocation while running network mapping.
        
        Examples
        --------
        >>> inf = TokSim(ctg)
        >>> inf.run()

        Parameters
        ----------
        ctg : CTG
            the communication trace graph that contains the xbars and communication relationship
            run xbar mapping to get the CTG

        slide_once : bool
            when True, the window slides only once in each iteration,
            when False, the window slides as much as possible in each iteration. 

        latency : Optional[int]
            communication latency for each connection in CTG.
            when None, indicate no communication latency,
            when int, indicate communication latency is `latency`, `latency` must > 0

        kwargs : Dict
            mapname : str = 'newmap'
                Map name

        Key Members
        -----------
        self.obj_dict : Dict
            A dictionary with key = [CTG.graph.nodes] and value = [_Xbar, _Comm, _MergeComm]
            Stores all the objects in `TokSim`.

        self.execu_dict : Dict
            A dictionary with key = [CTG.graph.nodes] and value = execu list
        '''
        self.ctg = ctg
        self.slide_once = slide_once
        self.latency = latency
        self.mapname = 'newmap'
        self.__dict__.update(kwargs)
        self.execu_dict = dict()
        self._build_obj_dict()

    def _build_obj_dict(self) -> None:
        # build `self.obj_dict` according to ctg
        self.obj_dict = dict()
        for node in self.ctg.node_names:
            if self.ctg.is_comm(node): # comm
                preds = list(self.ctg.preds(node))
                pred = preds[0]
                cfg = self.ctg.get_xbar_config(pred)
                if self.ctg.is_merge_comm(node): # merge comm
                    self.obj_dict[node] = _MergeComm(
                        cfg['xbar_num_ochan'], 
                        preds, 
                        latency=self.latency
                    )
                else: # normal comm
                    self.obj_dict[node] = _Comm(
                        cfg['xbar_num_ochan'],
                        latency=self.latency
                    )
            elif self.ctg.is_xbar(node): # xbar
                config = self.ctg.get_xbar_config(node)
                is_merge = False
                is_gather = False
                for pred in self.ctg.preds(node):
                    if self.ctg.is_merge_comm(pred):
                        is_merge = True
                    if self.ctg.is_gather_comm(pred):
                        is_gather = True
                self.obj_dict[node] = _Xbar(
                    config, 
                    is_merge, 
                    is_gather, 
                    slide_once=self.slide_once
                )
                self.execu_dict[node] = []

    def iter(self) -> bool:
        done_cnt = 0
        for node in self.ctg.node_names:
            if self.ctg.is_xbar(node): # xbar
                if self.ctg.is_head_xbar(node): # head xbar
                    self.obj_dict[node].consume_tokens(1, 'Cast')
                token = self.obj_dict[node].produce_tokens()
                self.execu_dict[node].append(token) # record executed or not
                
                if self.obj_dict[node].done:
                    done_cnt += 1

                # xbar may have multiple successors typed "comm"
                # it may be any one of cast, merge, and gather
                if token == 0: # produced 0 token
                    continue
                succs = list(self.ctg.succs(node))
                if len(succs) == 0: # tail xbar
                    continue
                for succ in succs:
                    self.obj_dict[succ].consume_tokens(token, node)
                
            elif self.ctg.is_comm(node): # comm
                token = self.obj_dict[node].produce_tokens()
                if self.ctg.is_cast_comm(node):
                    pred_type = 'Cast'
                elif self.ctg.is_merge_comm(node):
                    pred_type = 'Merge'
                else:
                    pred_type = 'Gather'
                for succ in self.ctg.succs(node): # comm successors must be xbar
                    self.obj_dict[succ].consume_tokens(token, pred_type)

        print(f'process: {done_cnt}/{self.ctg.xbar_num} xbars')
        if done_cnt == self.ctg.xbar_num:
            return True
        return False

    def run(self) -> None:
        cnt = 0
        done = False
        while not done:
            cnt += 1
            done = self.iter()
            print(f"iteration: {cnt}", end='  ')
        # write the buffer and communication info to `self.ctg`
        self._write_back()

    def _write_back(self) -> None:
        '''
        Write back the information about the buffer size and communication load
        Xbar : {conv_buf, pool_buf, gather_buf}
        Comm : {load, load_ratio}
        '''
        # maximum communication load
        self.max_comm_load = max([
            self.obj_dict[n].accum_tokens for n in self.ctg.comms
        ])
        for n in self.ctg.node_names:
            local = dict()
            node = self.obj_dict[n]
            if self.ctg.is_xbar(n): # xbar node
                local['conv_buf'] = node.conv_buf.max_buf
                local['pool_buf'] = 0
                if 'Pool' in node.op_type:
                    local['pool_buf'] = node.pool_buf.max_buf
                local['gather_buf'] = node.max_gather_buf
            else: # comm node
                local['load'] = node.accum_tokens
                local['load_ratio'] = local['load'] / self.max_comm_load
            self.ctg.update_dict(n, local)

    def echo_xbar(self) -> str:
        log = ""
        for node in self.ctg.node_names:
            if self.ctg.is_xbar(node):
                xbar = self.obj_dict[node]
                conv_buf = xbar.conv_buf.max_buf
                pool_buf = '--'
                if 'Pool' in xbar.op_type:
                    pool_buf = xbar.pool_buf.max_buf
                inter_buf = xbar.max_inter_buf
                merge_buf = xbar.max_merge_buf
                gather_buf = xbar.max_gather_buf
                log += '%-5s%-20s%-9s%-20s%-9s%-20s%-10s%-20s%-10s%-20s%-11s%-20s\n' % (
                    'xbar:', node,
                    'conv_buf:', conv_buf,
                    'pool_buf:', pool_buf,
                    'inter_buf:', inter_buf,
                    'merge_buf:', merge_buf,
                    'gather_buf:', gather_buf
                )
        return log

    def echo_comm(self) -> str:
        log = ""
        for node in self.ctg.node_names:
            if self.ctg.is_comm(node):
                comm = self.obj_dict[node]
                log += '%-11s%-30s%-5s%-20s%-9s%-20s\n' % (
                    'connection:', node,
                    'load:', comm.accum_tokens,
                    '#channel:', comm.nc
                )
        return log

    def save_execu(self, file_name: str = 'token'):
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'toksim')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # save token information
        file_dir = os.path.join(save_dir, file_name+'.pkl')
        with open(file_dir,'wb') as f:
            pickle.dump(self.execu_dict, f)
        print(f"\ntoken info written to {file_dir}")

        # save buffer log
        file_dir = os.path.join(save_dir, 'buffer.log')
        log = self.echo_xbar() + "\n\n" + self.echo_comm()
        with open(file_dir, 'w') as f:
            f.write(log)
        print(f"\nbuffer log written to {file_dir}")


def test_window_slide():
    buf = _WindowBuf([11,10], [7,7], [3,3], [2,2], [1,3,3,2], 64, slide_once=False)
    while True:
        buf.add_token(100)
        buf.try_slide()
        print(buf.buf,end='\n\n')
        time.sleep(0.5)
        if buf.done:
            break

if __name__ == "__main__":
    test_window_slide()