import torch
from torchvision import transforms
from PIL import Image
from typing import Tuple
from copy import deepcopy
from typing import List, Tuple, Dict
from maptools.core import ModelParams, TileConfig

__all__ = [
    'get_tile_kwargs'
]

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
    _weight_ = torch.zeros_like(_weight)
    kw = weight.shape[3]
    for i in [m[0] for m in icfg]:
        y = i // kw
        x = i % kw
        _weight_[:, :, y, x] = _weight[:, :, y, x] # mask
    return _weight_


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
        bias = rebuild_conv_bias(
            cfg['xbar_ocfg'],
            torch.tensor(params[bias_ptr]).float()
        )
        kwargs['conv_bias'] = bias
    
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
    
    # get output channel range
    kwargs['ochan_range'] = cfg['xbar_ocfg']

    # get quant config
    config_names = {
        'conv_quant_config', 
        'add_quant_config',
        'relu_quant_config'
    }
    for name in config_names:
        if name in cfg:
            kwargs[name] = cfg[name]

    # get connection attributes
    if not cfg['merge_out']:
        kwargs['merge_node'] = True
    return kwargs
