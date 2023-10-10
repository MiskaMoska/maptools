import torch
from typing import Tuple, Union
from copy import deepcopy
from typing import List, Tuple, Dict
from maptools.core import ModelParams, TileConfig

__all__ = ['get_tile_kwargs']

def rebuild_conv_weight(icfg: List[Tuple], ocfg: Tuple, xbar_num_ichan: int, weight: torch.Tensor) -> torch.Tensor:
    '''
    Rebuild convolution weight according to vector slicing information
    '''
    assert len(weight.shape) == 4, f"dimension of weight should be 4, but got {len(weight.shape)}"
    ichan_ss = list(zip(*icfg))[1]
    ichan_ds = list(zip(*icfg))[2]
    ichan_s = min(ichan_ss)
    ichan_d = max(ichan_ds)
    assert ichan_d - ichan_s == xbar_num_ichan, (
        f"input channel not matched, got slice ({ichan_s}, {ichan_d}, but got xbar_num_ichan: {xbar_num_ichan})"
    )
    ochan_s = ocfg[0]
    ochan_d = ocfg[1]
    _weight = deepcopy(weight[ochan_s:ochan_d, ichan_s:ichan_d, :, :])
    partial_weight = torch.zeros_like(_weight)
    kw = weight.shape[3]
    for i, s, d in icfg:
        y = i // kw
        x = i % kw
        b = s - ichan_s
        e = d - ichan_s
        partial_weight[:, b:e, y, x] = _weight[:, b:e, y, x] # mask
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
        cfg['xbar_num_ichan'],
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