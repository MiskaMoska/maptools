import torch
from typing import Tuple, Union
from copy import deepcopy
from typing import List, Tuple, Dict
from maptools.core import ModelParams, TileConfig

__all__ = ['get_tile_kwargs']

def rebuild_conv_weight(icfg: List[Tuple], ocfg: Tuple, weight: torch.Tensor) -> torch.Tensor:
    '''
    Rebuild convolution weight according to vector slicing information
    '''
    assert len(weight.shape) == 4, f"dimension of weight should be 4, but got {len(weight.shape)}"
    ichan_s = icfg[0][1]
    ichan_d = icfg[0][2]
    ochan_s = ocfg[0]
    ochan_d = ocfg[1]
    _weight = deepcopy(weight[ochan_s:ochan_d, ichan_s:ichan_d, :, :])
    partial_weight = torch.zeros_like(_weight)
    kw = weight.shape[3]
    for i in [m[0] for m in icfg]:
        y = i // kw
        x = i % kw
        partial_weight[:, :, y, x] = _weight[:, :, y, x] # mask
    return partial_weight


def rebuild_conv_bias(ocfg: Tuple, bias: torch.Tensor) -> torch.Tensor:
    '''
    Rebuild convolution bias according to vector slicing information
    '''
    assert len(bias.shape) == 1, f"dimension of weight should be 1, but got {len(bias.shape)}"
    return deepcopy(bias[ocfg[0]:ocfg[1]])


def get_tile_kwargs(cfg: TileConfig, params: ModelParams) -> Dict:
    kwargs = dict()

    # get conv pads
    pads = cfg['conv_pads'].copy()
    kwargs['conv_pads'] = [pads[3], pads[1], pads[0], pads[2]]

    # get conv weight
    weight_ptr = cfg['conv_weight']
    weight = rebuild_conv_weight(
        cfg['xbar_icfg'], cfg['xbar_ocfg'], 
        torch.tensor(params[weight_ptr]).float()
    )
    kwargs['conv_weight'] = weight

    # get conv bias
    if 'Bias' in cfg['op_type']:
        bias_ptr = cfg['conv_bias']
        if params[bias_ptr] is None:
            kwargs['conv_bias'] = None
        else:
            kwargs['conv_bias'] = rebuild_conv_bias(
                cfg['xbar_ocfg'],
                torch.tensor(params[bias_ptr]).float()
            )
    
    # get conv strides
    kwargs['conv_strides'] = cfg['conv_strides'].copy()

    # get pool config
    if 'Pool' in cfg['op_type']:
        kwargs['is_pool'] = True
        kwargs['pool_mode'] = deepcopy(cfg['pool_mode'])
        pads = cfg['pool_pads'].copy()
        kwargs['pool_pads'] = [pads[3], pads[1], pads[0], pads[2]]
        kwargs['pool_kernel_size'] = cfg['pool_kernel_size'].copy()
        kwargs['pool_strides'] = cfg['pool_strides'].copy()

    # get act config
    if 'Act' in cfg['op_type']:
        kwargs['is_act'] = True
        kwargs['act_mode'] = deepcopy(cfg['act_mode'])

    # get resize config
    if 'Rsz' in cfg['op_type']:
        kwargs['is_resize'] = True
        kwargs['resize_scales'] = deepcopy(cfg['resize_scales'])

    # get connection attributes
    if not cfg['merge_out']:
        kwargs['merge_node'] = True

    return kwargs