import os
import sys
import torch
import torch.nn as nn
import pickle
from functools import wraps
from typing import List, Dict, Optional, Tuple, Any, Union, Callable
from maptools.core import CTG, ModelParams, ROOT_DIR, PhysicalTile
from maptools.calcusim.device.utils import *
from maptools.calcusim.device.tile_task import TileTask, OBSERVE_VARS

__all__ = ['DeviceTask']

class DeviceTask(nn.Module):

    def __init__(
        self, 
        ctg: CTG,
        params: ModelParams,
        **kwargs: Any
    ) -> None:
        super().__init__()
        self.ctg = ctg
        self.params = params
        self.mapname: str = 'newmap'
        self.quantize: bool = False
        self.observe: bool = False
        self.physical: bool = False
        self.hardtrans: bool = True
        self.ivcf: Optional[float] = None
        self.first_layer_ivcf: Optional[float] = None
        self.__dict__.update(kwargs)

        if self.physical and not self.quantize:
            raise AssertionError ("to use physical CIMU, quantize must be enabled")
        
        self.obj_dict: Dict[Union[PhysicalTile, str], torch.Tensor] = dict()
        self.res_dict: Dict[Union[PhysicalTile, str], Dict[str, Optional[torch.Tensor]]] = dict()

        self._construct_tile_tasks()

    def _construct_tile_tasks(self) -> None:
        for node in self.ctg.node_names:
            if self.ctg.is_comm(node): # is comm
                self.obj_dict[node] = 0
                
            else: # is tile
                cfg = self.ctg.get_tile_config(node)
                kwargs = get_tile_kwargs(cfg, self.params)
                is_merge = False
                is_gather = False
                for pred in self.ctg.preds(node):
                    if self.ctg.is_merge_comm(pred):
                        is_merge = True
                    if self.ctg.is_gather_comm(pred):
                        is_gather = True
                self.obj_dict[node] = TileTask(
                    tile=node,
                    is_merge=is_merge, 
                    is_gather=is_gather,
                    quantize=self.quantize,
                    tqc=cfg['tqc'] if self.quantize else None,
                    physical=self.physical,
                    observe=self.observe,
                    hardtrans=self.hardtrans,
                    ivcf=self.ivcf,
                    first_layer_ivcf=self.first_layer_ivcf,
                    **kwargs
                )

    def _arrage_output(self, y: List[Tuple]) -> torch.Tensor:
        y.sort(key=lambda x : x[0])
        return torch.cat([v[1] for v in y], dim=1)

    def cuda(self) -> None:
        for node in self.obj_dict.keys():
            if self.ctg.is_tile(node):
                self.obj_dict[node].cuda()

    def empty_device_buffer(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for comm in self.ctg.comms:
                self.obj_dict[comm] = 0
            return func(self, *args, **kwargs)
        return wrapper

    @empty_device_buffer
    def forward(self, x: torch.Tensor) -> List[torch.Tensor]:
        assert isinstance(x, torch.Tensor), f"input should be torch.Tensor, but got {type(x)}"
        assert len(x.shape) == 4, f"input dimension should be 4 [N, C, H, W], but got {len(x.shape)}"

        # to store the raw output
        # the length of `output_list` equals the number of output layers in device task
        # each sublist of `output_list` stores the output of all tiles in one output layer
        # the arrangement of the sublists follows the order of bridge index
        # each member of the sublist is a tuple with the tile output tensor as the second 
        # element and the corresponding region index of the tile as the first element
        output_list = []
        for i in range(self.ctg.output_num):
            output_list.append([])

        # device task
        for node in self.ctg.tiles:
            # get input data
            cast_in, merge_in, gather_in = None, None, None
            if self.ctg.is_head_tile(node):
                # quantizing before the head tile
                if self.quantize:
                    i_scale = self.ctg.dicts[node]['tqc'].i_scale
                    x = torch.round(torch.divide(x, i_scale))
                    x = torch.clamp(x, -128, 127)
                cast_in = x
            else:
                if self.ctg.has_cast_in(node):
                    cast_in = self.obj_dict[self.ctg.cast_pred_comm(node)]
                if self.ctg.has_merge_in(node):
                    merge_in = self.obj_dict[self.ctg.merge_pred_comm(node)]
                if self.ctg.has_gather_in(node):
                    gather_in = self.obj_dict[self.ctg.gather_pred_comm(node)]
            
            # perform tile execution
            temp_y = self.obj_dict[node](cast_in, merge_in, gather_in)
            
            # store output data
            if self.ctg.is_tail_tile(node):
                # quantizing after the tail tile
                if self.quantize:
                    o_scale = self.ctg.dicts[node]['tqc'].o_scale
                    temp_y *= o_scale

                bridge_idx = self.ctg.dicts[node]['bridge_idx']
                output_list[bridge_idx].append((node[1], temp_y))

            else:
                if self.ctg.has_cast_out(node):
                    self.obj_dict[self.ctg.cast_succ_comm(node)] = temp_y
                if self.ctg.has_merge_out(node):
                    self.obj_dict[self.ctg.merge_succ_comm(node)] += temp_y
                if self.ctg.has_gather_out(node):
                    self.obj_dict[self.ctg.gather_succ_comm(node)] = temp_y
            
            # collect intermediate results
            # execute only when observing is enabled
            if self.observe:
                res = dict()
                for name in OBSERVE_VARS:
                    res[name] = self.obj_dict[node].__dict__[name]
                self.res_dict[node] = res

        device_output = [self._arrage_output(y) for y in output_list]
        self.res_dict['output'] = device_output # the output of device task

        return device_output

    def save_results(self, file_name: str = 'results'):
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'calcusim')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        file_dir = os.path.join(save_dir, file_name+'.pkl')
        with open(file_dir,'wb') as f:
            pickle.dump(self.res_dict, f)
        print(f"\nintermediate results written to {file_dir}")