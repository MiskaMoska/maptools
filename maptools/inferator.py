import time
from ctg import *
from utils import *
import numpy as np
from typing import Tuple, List, Any, Optional, Dict
from functools import cached_property

__all__ = ['Inferator']

class _WindowBuf(object):

    def __init__(self, input_size: Tuple[int, int], output_size: Tuple[int, int],
                    kernel_size: List[int], strides: List[int], pads: List[int]) -> None:
        '''
        
        '''
        self.size_i = input_size
        self.size_o = output_size
        self.ks = kernel_size
        self.strides = strides
        self.pads = pads
        self.buf = np.zeros(input_size, dtype=int)
        self.rptr = 0 # results ptr
        self.wptr = 0 # write ptr

    def add_token(self, token: int) -> None:
        for i in range(token):
            self.buf[(self.wptr+i)//self.size_i[1], (self.wptr+i)%self.size_i[1]] = 1
        self.wptr += token
        assert self.wptr <= self.size_i[0] * self.size_i[1], "wptr overflow"

    @property
    def win_pos(self) -> Tuple[int, int, int, int]:
        # [dy, dx] is the position of the results
        dy = self.rptr // self.size_o[1]
        dx = self.rptr % self.size_o[1]
        # [win_y, win_x] is the position of the window
        win_y = dy * self.strides[0]
        win_x = dx * self.strides[1]
        return (win_y, win_x, win_y+self.ks[0], win_x+self.ks[1])

    def _release_data(self) -> None:
        # release data from buffer
        if self.rptr // self.size_o[1] == self.size_o[0] - 1: # on the down edge
            rele_y = self.ks[0]
        else:
            rele_y = self.strides[0]
        if self.rptr % self.size_o[1] == self.size_o[1] - 1: # on the right edge
            rele_x = self.ks[1]
        else:
            rele_x = self.strides[1]
        self.buf[self.win_pos[0]:self.win_pos[0]+rele_y, self.win_pos[1]:self.win_pos[1]+rele_x] *= 0

    def try_slide(self) -> int:
        # the window block in the buffer
        window = self.buf[self.win_pos[0]:self.win_pos[2],self.win_pos[1]:self.win_pos[3]]
        if np.sum(window) == self.ks[0] * self.ks[1]: # all data in window is available
            self._release_data()
            self.rptr += 1 # slide window
            return 1 # return a token
        else: # needed data is not prepared well
            return 0 # return no token


class _Xbar(object):

    def __init__(self, config: Dict, is_merge: bool, is_gather: bool) -> None:
        '''
        Xbar abstract model designed for inferator
        
        Parameters
        ----------
        config : Dict
            xbar config dictionary
        
        is_merge : bool
            whether is a merge destination node

        is_gather : bool
            whether is a gather destination node
        '''
        self.__dict__.update(config)
        self.is_merge = is_merge
        self.is_gather = is_gather
        self.conv_buf = _WindowBuf(self.sizes[0], self.sizes[1],
                                    self.conv_kernel_size, self.conv_strides, self.conv_pads)
        self.inter_buf = 0
        if 'Pool' in self.op_type: # has pooling
            self.pool_buf = _WindowBuf(self.sizes[2], self.sizes[3],
                                    self.pool_kernel_size, self.pool_strides, self.pool_pads)
        self.merge_buf = 0
        self.gather_buf = 0

    @cached_property
    def sizes(self) -> Tuple[Tuple, Tuple, Tuple, Tuple]:
        # calculate the convolution and pooling input and output size
        return self.calcu_sizes()

    def _consume_tokens_cast(self, token: int) -> None:
        self.conv_buf.add_token(token)
        res = self.conv_buf.try_slide() # number of results
        self.inter_buf += res # put the results to inter buffer

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
                return self.pool_buf.try_slide()
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
        self.merge_buf -= token if self.is_merge else 0
        self.gather_buf -= token if self.is_gather else 0

        if 'Pool' in self.op_type: # has pooling
            self.pool_buf.add_token(token)
            return self.pool_buf.try_slide()
        else: # no pooling
            return token
        
    def calcu_sizes(self) -> Tuple[Tuple, Tuple, Tuple, Tuple]:
        '''
        Calculate convolution and pooling input and output size
        '''
        conv_in_h = self.input_size[0] + self.conv_pads[0] + self.conv_pads[2]
        conv_in_w = self.input_size[1] + self.conv_pads[1] + self.conv_pads[3]
        print('conv_in_h:',conv_in_h)
        print('kernel_size:',self.conv_kernel_size)
        print('strides:',self.conv_strides)
        assert (conv_in_h - self.conv_kernel_size[0]) % self.conv_strides[0] == 0, "conv size dismatch"
        assert (conv_in_w - self.conv_kernel_size[1]) % self.conv_strides[1] == 0, "conv size dismatch"
        conv_out_h = (conv_in_h - self.conv_kernel_size[0]) // self.conv_strides[0] + 1
        conv_out_w = (conv_in_w - self.conv_kernel_size[1]) // self.conv_strides[1] + 1
        if 'Pool' in self['op_type']:
            pool_in_h = conv_out_h + self.pool_pads[0] + self.pool_pads[2]
            pool_in_w = conv_out_w + self.pool_pads[1] + self.pool_pads[3]
            assert (pool_in_h - self.pool_kernel_size[0]) % self.pool_strides[0] == 0, "pool size dismatch"
            assert (pool_in_w - self.pool_kernel_size[1]) % self.pool_strides[1] == 0, "pool size dismatch"
            pool_out_h = (pool_in_h - self.pool_kernel_size[0]) // self.pool_strides[0] + 1
            pool_out_w = (pool_in_w - self.pool_kernel_size[1]) // self.pool_strides[1] + 1
            return (conv_in_h, conv_in_w), (conv_out_h, conv_out_w), (pool_in_h, pool_in_w), (pool_out_h, pool_out_w)
        else:
            return (conv_in_h, conv_in_w), (conv_out_h, conv_out_w), (0, 0), (0, 0)


class _Comm(object):
    
    def __init__(self) -> None:
        self.accum_tokens = 0

    def consume_tokens(self, token: int, pred: Any) -> None:
        self.token = token

    def produce_tokens(self) -> int:
        self.accum_tokens += self.token
        return self.token


class _MergeComm(_Comm):

    def __init__(self, preds: List[Any]) -> None:
        super().__init__()
        self.buf = {k: 0 for k in preds}

    def consume_tokens(self, token: int, pred: Any) -> None:
        self.buf[pred] += token
    
    def produce_tokens(self) -> int:
        token = min([v for v in self.buf.values()])
        self.accum_tokens += token
        for k in self.buf.keys():
            self.buf[k] -= token
        return token


class Inferator(object):

    def __init__(self, ctg: CTG) -> None:
        self.ctg = ctg
        self._build_obj_dict()

    def _build_obj_dict(self) -> None:
        # build `self.obj_dict` according to ctg
        self.obj_dict = dict()
        for node in self.ctg.node_names:
            if self.ctg.is_comm(node): # comm
                if self.ctg.is_merge_comm(node): # merge comm
                    preds = list(self.ctg.preds(node))
                    self.obj_dict[node] = _MergeComm(preds)
                else: # normal comm
                    self.obj_dict[node] = _Comm()
            elif self.ctg.is_xbar(node): # xbar
                config = self.ctg.get_xbar_config(node)
                is_merge = False
                is_gather = False
                for pred in self.ctg.preds(node):
                    if self.ctg.is_merge_comm(pred):
                        is_merge = True
                    if self.ctg.is_gather_comm(pred):
                        is_gather = True
                self.obj_dict[node] = _Xbar(config, is_merge, is_gather)

    def run(self) -> None:
        for i in range(224*224):
            print(i)
            self.iter()
        
    def iter(self) -> None:
        for node in self.ctg.node_names:
            if self.ctg.is_xbar(node): # xbar
                if self.ctg.is_head_xbar(node): # head xbar
                    self.obj_dict[node].consume_tokens(1, 'Cast')
                token = self.obj_dict[node].produce_tokens()
                # xbar must have only one successor typed "comm"
                if token == 0: # produced 0 token
                    continue
                succs = list(self.ctg.succs(node))
                if len(succs) == 0: # tail xbar
                    continue
                succ = list(succs)[0]
                self.obj_dict[succ].consume_tokens(token)
                
            elif self.ctg.is_comm(node): # comm
                token = self.obj_dict[node].produce_tokens()
                if token == 0:
                    continue
                for succ in self.ctg.succs(node): # comm successors must be xbar
                    self.obj_dict[succ].consume_tokens(token)

def test_window_slide():
    buf = _WindowBuf((8,8), (4,4), [2,2], [2,2], [0,0,0,0])
    while True:
        buf.add_token(1)
        buf.try_slide()
        print(buf.buf,end='\n\n')
        time.sleep(0.5)

if __name__ == "__main__":
    test_window_slide()