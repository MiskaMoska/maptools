import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import pickle
from copy import deepcopy
from typing import List, Dict, Optional, Tuple, Any, Union, Callable
from maptools import CTG, OperatorGraph
from maptools.calcusim.utils import *
from maptools.host import HostTask
from maptools import DeviceParams
from maptools.core import QuantConfig
from functools import cached_property, wraps

__all__ = ['CalcuSim']

class _Xbar(object):

    def __init__(self, **kwargs: Any) -> None:
        # for general
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

        # for quantization
        self.merge_node: bool = False
        self.quantize: bool = False
        self.ochan_range: Tuple[int, int] = (0, 0) 
        self.quant_config: Optional[QuantConfig] = None
        self.__dict__.update(kwargs)

        rebuild_pads(self.conv_pads)
        rebuild_pads(self.pool_pads)
    
        # initialize input data
        self.cast_in: Optional[torch.Tensor] = None
        self.merge_in: Optional[torch.Tensor] = None
        self.gather_in: Optional[torch.Tensor] = None

        self.before_pool = None # results before pool
        self._weight_scale = None

    def absorb(self, data: torch.Tensor, pred_type: str) -> None:
        if pred_type == 'Cast':
            self.cast_in = data
        elif pred_type == 'Merge':
            self.merge_in = data
        elif pred_type == 'Gather':
            self.gather_in = data

    def memorize(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args):
            if self._weight_scale is not None:
                return self._weight_scale
            else:
                result = func(self, *args)
                self._weight_scale = result
                return result
        return wrapper

    @memorize
    def weight_scale(self, x: torch.Tensor) -> torch.Tensor:
        shape2d = x.shape[-2:]
        scale = self.quant_config.weight_scale
        to_stack = [torch.ones(shape2d)*scale[i] for i in range(*self.ochan_range)]
        return torch.stack(to_stack).expand(1, -1, -1, -1)

    def forward(self) -> torch.Tensor:
        assert self.cast_in is not None, "cast in data got None"
        x = F.pad(
            self.cast_in, 
            self.conv_pads
        )
        x = F.conv2d(
            x, 
            self.conv_weight,
            bias = self.conv_bias,
            stride = self.conv_strides
        )
        
        if self.is_merge:
            assert self.merge_in is not None, "merge in data got None"
            assert x.shape == self.merge_in.shape, (
                f"got x's shape = {x.shape} but merge's shape = {self.merge_in.shape}, cannot merge")
            x = torch.add(x, self.merge_in)

        # only for merge node where a complete sum should appear
        # quantization converting from input to output, return a int8
        if self.merge_node and self.quantize:
            assert self.quant_config is not None, (
                f"quantize enabled but got no quant_config")
            input_scale = self.quant_config.input_scale
            output_scale = self.quant_config.output_scale
            x = torch.round(torch.mul(x, self.weight_scale(x)) * input_scale / output_scale)

        if self.is_gather:
            assert self.gather_in is not None, "gather in data got None"
            assert x.shape == self.gather_in.shape, (
                f"got x's shape = {x.shape} but gather's shape = {self.gather_in.shape}, cannot gather")
            x = torch.add(x, self.gather_in)

        if self.is_act:
            assert self.act_mode == 'Relu', (
                f"activation mode must be Relu, but got {self.act_mode}")
            x = F.relu(x)

        if self.is_pool:
            self.before_pool = x
            assert self.pool_mode in ['MaxPool', 'AveragePool'], (
                f"got invalid pool mode: {self.pool_mode}")
            x = F.pad(x, self.pool_pads)
            if self.pool_mode == 'MaxPool':
                x = F.max_pool2d(
                    x, 
                    kernel_size = tuple(self.pool_kernel_size),
                    stride = tuple(self.pool_strides)
                )
            elif self.pool_mode == 'AveragePool':
                assert not self.quantize, "quantitized average pooling not supported yet"
                x = F.avg_pool2d(
                    x, 
                    kernel_size = tuple(self.pool_kernel_size),
                    stride = tuple(self.pool_strides)
                )
        
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

    def __init__(
        self, 
        ctg: CTG, 
        host_graph: OperatorGraph, 
        params: DeviceParams,
        **kwargs: Any
    ) -> None:
        '''
        Parameters
        ----------
        ctg : CTG
            communication trace graph
        
        params : DeviceParams
            from `OnnxConverter.param_dict`

        kwargs : Dict
            root_dir : str = os.environ.get('NVCIM_HOME')
                The root directory of the project.

            mapname : str = 'newmap'
                Map name

        Key Members
        -----------
        self.res_dict : Dict[Union[str, Tuple], Dict[str, Optional[torch.Tensor]]]
            Stores the intermediate results of each xbar
            A dictionary with logical xbar as keys and result dictionary as values
            Where the result dictionary = 
            {'cast_in': tensor, 'merge_in': tensor, 'gather_in': tensor, 'data_out': tensor}
        '''
        super().__init__()
        self.ctg = ctg
        self.params = params
        self.root_dir = os.environ.get('NVCIM_HOME')
        self.mapname = 'newmap'
        self.quantize = False
        self.__dict__.update(kwargs)
        self.obj_dict: Dict = dict()
        self._build_device_task()
        self._build_host_task(host_graph)
        self.res_dict: Dict[Union[str, Tuple], Dict[str, Optional[torch.Tensor]]] = dict()

    def _build_device_task(self) -> None:
        for node in self.ctg.node_names:
            if self.ctg.is_comm(node): # is comm
                preds = list(self.ctg.preds(node))
                if self.ctg.is_merge_comm(node): # merge comm
                    self.obj_dict[node] = _MergeComm(preds)
                else: # normal comm
                    self.obj_dict[node] = _Comm()
            else: # is xbar
                cfg = self.ctg.get_xbar_config(node)
                kwargs = get_xbar_kwargs(cfg, self.params)
                is_merge = False
                is_gather = False
                for pred in self.ctg.preds(node):
                    if self.ctg.is_merge_comm(pred):
                        is_merge = True
                    if self.ctg.is_gather_comm(pred):
                        is_gather = True
                self.obj_dict[node] = _Xbar(
                    is_merge=is_merge, 
                    is_gather=is_gather, 
                    **kwargs
                )

    def _build_host_task(self, host_graph: OperatorGraph) -> None:
        self.host_task = HostTask(host_graph)

    def _arrage_output(self, y: List[Tuple]) -> torch.Tensor:
        y.sort(key=lambda x : x[0])
        return torch.cat([v[1] for v in y], dim=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        assert isinstance(x, torch.Tensor), f"input should be torch.Tensor, but got {type(x)}"
        assert len(x.shape) == 4, f"input dimension should be 4 [N, C, H, W], but got {len(x.shape)}"
        print('Launching CalcuSim ....')
        print('Quantization ' + ('Enabled' if self.quantize else 'Disabled'))
        y = []

        #quantizing before performing device task
        if self.quantize:
            x = torch.round(torch.divide(x, self.ctg.input_quant_config.input_scale))

        # device task
        for node in self.ctg.node_names:
            if self.ctg.is_xbar(node): # xbar
                if self.ctg.is_head_xbar(node): # head xbar
                    self.obj_dict[node].absorb(x, 'Cast')
                result = self.obj_dict[node].forward()

                # collect intermediate results
                res = dict()
                for name in ['cast_in', 'merge_in', 'gather_in']:
                    res[name] = self.obj_dict[node].__dict__[name]
                res['before_pool'] = self.obj_dict[node].before_pool
                res['data_out'] = result 
                self.res_dict[node] = res

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
        device_output = self._arrage_output(y)
        self.res_dict['output'] = device_output # the output of device task

        # dequantizing before performing host task
        if self.quantize:
            device_output = torch.mul(device_output, self.ctg.output_quant_config.output_scale)
        print('Finished Device Task')

        # host task
        host_output = self.host_task(device_output)
        print('Finished Host Task')
        print('Finished CalcuSim')
        return device_output, host_output
    
    def save_results(self, file_name: str = 'results'):
        save_dir = os.path.join(self.root_dir, 'mapsave', self.mapname, 'calcusim')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        file_dir = os.path.join(save_dir, file_name+'.pkl')
        with open(file_dir,'wb') as f:
            pickle.dump(self.res_dict, f)
        print(f"\nintermediate results written to {file_dir}")