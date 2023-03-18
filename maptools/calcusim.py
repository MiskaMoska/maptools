
import torch
import torch.nn as nn
import torch.nn.functional as F
from copy import deepcopy
from typing import List, Dict, Optional, Tuple, Any
from maptools import CTG

__all__ = ['CalcuSim']

def _rebuild_pads(pads: List):
    if pads is not None:
        _pads = deepcopy(pads)
        pads[0] = _pads[3]
        pads[1] = _pads[1]
        pads[2] = _pads[0]
        pads[3] = _pads[2]

def _rebuild_conv_weight(icfg: List[Tuple], 
                        ocfg: Tuple, 
                        weight: torch.Tensor
                        ) -> torch.Tensor:
    '''
    Rebuild convolution weight according to vector slicing information
    '''
    assert len(weight.shape) == 4, f"dimension of weight should be 4, but got {len(weight.shape)}"
    ichan_s = icfg[0][1]
    ichan_d = icfg[0][2]
    ochan_s = ocfg[0]
    ochan_d = ocfg[1]
    _weight = weight[ochan_s:ochan_d, ichan_s:ichan_d, :, :]
    _weight_ = torch.zeros_like(_weight)
    kw = weight.shape[3]
    for i in [m[0] for m in icfg]:
        y = i // kw
        x = i % kw
        _weight_[:, :, y, x] = _weight[:, :, y, x] # mask
    return _weight_

def _rebuild_conv_bias(ocfg: Tuple, bias: torch.Tensor) -> torch.Tensor:
    '''
    Rebuild convolution bias according to vector slicing information
    '''
    assert len(bias.shape) == 1, f"dimension of weight should be 1, but got {len(bias.shape)}"
    return bias[ocfg[0]:ocfg[1]]

def _get_xbar_kwargs(cfg: Dict, params: Dict) -> Dict:
    kwargs = dict()
    kwargs['conv_pads'] = cfg['conv_pads']
    weight_ptr = cfg['conv_weight']
    weight = _rebuild_conv_weight(cfg['xbar_icfg'], cfg['xbar_ocfg'], 
                                    torch.tensor(params[weight_ptr]))
    kwargs['conv_weight'] = weight
    if 'Bias' in cfg['op_type']:
        bias_ptr = cfg['conv_bias']
        bias = _rebuild_conv_bias(cfg['xbar_ocfg'],torch.tensor(params[bias_ptr]))
        kwargs['conv_bias'] = bias
    kwargs['conv_strides'] = cfg['conv_strides']
    if 'Pool' in cfg['op_type']:
        kwargs['is_pool'] = True
        kwargs['pool_mode'] = cfg['pool_mode']
        kwargs['pool_pads'] = cfg['pool_pads']
        kwargs['pool_kernel_size'] = cfg['pool_kernel_size']
        kwargs['pool_strides'] = cfg['pool_strides']
    if 'Act' in cfg['op_type']:
        kwargs['is_act'] = True
        kwargs['act_mode'] = cfg['act_mode']
    return kwargs

class _Xbar(object):

    def __init__(self, *args, **kwargs) -> None:
        self.conv_pads: Optional[List] = None
        self.conv_weight: Optional[torch.Tensor] = None
        self.conv_bias: Optional[torch.Tensor] = None
        self.conv_strides: Optional[List] = None
        self.pool_mode: Optional[str] = None
        self.pool_pads: Optional[List] = None
        self.pool_kernel_size: Optional[List] = None
        self.pool_strides: Optional[List] = None
        self.act_mode: Optional[str] = None
        self.is_pool: bool = False
        self.is_act: bool = False
        self.is_merge: bool = False
        self.is_gather: bool = False
        self.__dict__.update(kwargs)

        _rebuild_pads(self.conv_pads)
        _rebuild_pads(self.pool_pads)
    
        # initialize input data
        self.cast_in: Optional[torch.Tensor] = None
        self.merge_in: Optional[torch.Tensor] = None
        self.gather_in: Optional[torch.Tensor] = None

    def absorb(self, data: torch.Tensor, pred_type: str) -> None:
        if pred_type == 'Cast':
            self.cast_in = data
        elif pred_type == 'Merge':
            self.merge_in = data
        elif pred_type == 'Gather':
            self.gather_in = data

    def forward(self) -> torch.Tensor:
        assert self.cast_in is not None, "cast in data got None"
        x = F.pad(self.cast_in, self.conv_pads)
        x = F.conv2d(x, self.conv_weight,
                        bias = self.conv_bias,
                        stride = self.conv_strides)
        
        if self.is_merge:
            assert self.merge_in is not None, "merge in data got None"
            assert x.shape == self.merge_in.shape, f"got x's shape = {x.shape} but merge's shape = {self.merge_in.shape}, cannot merge"
            x = torch.add(x, self.merge_in)
            
        if self.is_gather:
            assert self.gather_in is not None, "gather in data got None"
            assert x.shape == self.gather_in.shape, f"got x's shape = {x.shape} but gather's shape = {self.gather_in.shape}, cannot gather"
            x = torch.add(x, self.gather_in)

        if self.is_act:
            assert self.act_mode == 'Relu', f"activation mode must be Relu, but got {self.act_mode}"
            x = F.relu(x)

        if self.is_pool:
            assert self.pool_mode in ['MaxPool', 'AveragePool'], f"got invalid pool mode: {self.pool_mode}"
            x = F.pad(x, self.pool_pads)
            if self.pool_mode == 'MaxPool':
                x = F.max_pool2d(x, kernel_size = tuple(self.pool_kernel_size),
                                        stride = tuple(self.pool_strides))
            elif self.pool_mode == 'AveragePool':
                x = F.avg_pool2d(x, kernel_size = tuple(self.pool_kernel_size),
                                        stride = tuple(self.pool_strides))
        
        return x


class _Comm(object):

    def __init__(self) -> None:
        self.data: Optional[torch.Tensor] = None

    def absorb(self, data: torch.Tensor, pred: Any) -> None:
        self.data = data

    def forward(self) -> torch.Tensor:
        assert self.data is not None, f"data_in is None"
        return self.data

class _MergeComm(object):

    def __init__(self, preds: List[Any]) -> None:
        self.datapool: Dict[Any, Optional[torch.Tensor]] = {k: None for k in preds}

    def absorb(self, data: torch.Tensor, pred: Any) -> None:
        self.datapool[pred] = data

    def forward(self) -> torch.Tensor:
        for tensor in self.datapool.values():
            assert tensor is not None, f"datapool still has None value(s)"
        return torch.sum(torch.stack([v for v in self.datapool.values()]), dim=0)


class CalcuSim(nn.Module):

    def __init__(self, ctg: CTG, params: Dict) -> None:
        '''
        Parameters
        ----------
        ctg : CTG
            communication trace graph
        
        params : Dict
            from `OnnxConverter.param_dict`
        '''
        super().__init__()
        self.ctg = ctg
        self.params = params
        self.obj_dict: Dict = dict()
        self._build_obj_dict()

    def _build_obj_dict(self) -> None:
        for node in self.ctg.node_names:
            if self.ctg.is_comm(node): # is comm
                preds = list(self.ctg.preds(node))
                if self.ctg.is_merge_comm(node): # merge comm
                    self.obj_dict[node] = _MergeComm(preds)
                else: # normal comm
                    self.obj_dict[node] = _Comm()
            else: # is xbar
                cfg = self.ctg.get_xbar_config(node)
                kwargs = _get_xbar_kwargs(cfg, self.params)
                is_merge = False
                is_gather = False
                for pred in self.ctg.preds(node):
                    if self.ctg.is_merge_comm(pred):
                        is_merge = True
                    if self.ctg.is_gather_comm(pred):
                        is_gather = True
                self.obj_dict[node] = _Xbar(is_merge=is_merge, is_gather=is_gather, **kwargs)

    def _arrage_output(self, y: List[Tuple]) -> torch.Tensor:
        y.sort(key=lambda x : x[0])
        return torch.cat([v[1] for v in y], dim=1)

    def forward(self, x: torch.Tensor):
        assert isinstance(x, torch.Tensor), f"input should be torch.Tensor, but got {type(x)}"
        assert len(x.shape) == 4, f"input dimension should be 4 [N, C, H, W], but got {len(x.shape)}"
        y = []
        for node in self.ctg.node_names:
            if self.ctg.is_xbar(node): # xbar
                if self.ctg.is_head_xbar(node): # head xbar
                    self.obj_dict[node].absorb(x, 'Cast')
                result = self.obj_dict[node].forward()

                if node == (0,0,0,0):
                    self.tp = result

                # xbar may have multiple successors typed "comm"
                # it may be any one of cast, merge, and gather
                succs = list(self.ctg.succs(node))
                if len(succs) == 0: # tail xbar (must be merge xbar)
                    y.append((node[1], result))
                    continue
                for succ in succs:
                    self.obj_dict[succ].absorb(result, node)
                
            elif self.ctg.is_comm(node): # comm
                result = self.obj_dict[node].forward()
                if self.ctg.is_cast_comm(node):
                    pred_type = 'Cast'
                elif self.ctg.is_merge_comm(node):
                    pred_type = 'Merge'
                else:
                    pred_type = 'Gather'
                for succ in self.ctg.succs(node): # comm successors must be xbar
                    self.obj_dict[succ].absorb(result, pred_type)
        return self._arrage_output(y)







