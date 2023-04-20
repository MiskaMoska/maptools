import torch
import torch.nn as nn
import torch.nn.functional as F
from functools import wraps
from typing import List, Tuple, Dict
from maptools.core import OperatorConfig, ModelParams, VALID_OPS

__all__ = ['HostOperator']

class Conv(nn.Conv2d):

    def __init__(self, config: OperatorConfig, params: ModelParams) -> None:
        pads = config['conv_pads']
        super().__init__(
            config['conv_num_ichan'],
            config['conv_num_ochan'],
            config['conv_kernel_size'],
            config['conv_strides'],
            [pads[3], pads[1], pads[0], pads[2]]
        )

        weight_ptr = config['conv_weight']
        self.weight.data = torch.tensor(params[weight_ptr])

        bias_ptr = config['conv_bias']
        if params[bias_ptr] is None:
            self.bias.data = torch.zeros(self.out_channels)
        else: self.bias.data = torch.tensor(params[bias_ptr])

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return super().forward(x[0])


class Relu(nn.ReLU):

    def __init__(self, *args) -> None:
        super().__init__()

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return super().forward(x[0])


class Resize(nn.Module):

    def __init__(self) -> None:
        super().__init__()


class GlobalAveragePool(nn.Module):

    def __init__(self, *args) -> None:
        super().__init__()

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return F.adaptive_avg_pool2d(x[0], 1)


class Flatten(nn.Flatten):

    def __init__(self, *args) -> None:
        super().__init__()

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return super().forward(x[0])


class Gemm(nn.Linear): 

    def __init__(self, config: OperatorConfig, params: ModelParams) -> None:
        super().__init__(config['gemm_len_inv'], config['gemm_len_outv'])

        weight_ptr = config['gemm_weight']
        self.weight.data = torch.tensor(params[weight_ptr])

        bias_ptr = config['gemm_bias']
        if params[bias_ptr] is None:
            self.bias.data = torch.zeros(self.out_features)
        else: self.bias.data = torch.tensor(params[bias_ptr])

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return super().forward(x[0])


class Add(nn.Module):

    def __init__(self, *args) -> None:
        super().__init__()

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.add(x[0], x[1])


class Mul(nn.Module):

    def __init__(self, *args) -> None:
        super().__init__()

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.mul(x[0], x[1])


class Reshape(nn.Module):

    def __init__(self, config: OperatorConfig, *args) -> None:
        super().__init__()
        self.shape = config['reshape_shape']

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.reshape(x[0], self.shape)


class Concat(nn.Module):

    def __init__(self, *args) -> None:
        super().__init__()

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.concat(x, dim=1)


class Transpose(nn.Module):
    
    def __init__(self, config: OperatorConfig, *args) -> None:
        super().__init__()
        self.perm = config['tranpose_perm']

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.permute(x[0], self.perm)


class HostOperator(nn.Module):

    def __init__(self, config: OperatorConfig, params: ModelParams) -> None:
        super().__init__()
        self.op_type = config['op_type']
        assert self.op_type in VALID_OPS, (
            f"unsupported op_type {self.op_type} when building host operation")
        self.operation = __HOST_OPERATOR_ACCESS_TABLE__[self.op_type](config, params)

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return self.operation(x)


__HOST_OPERATOR_ACCESS_TABLE__ = {
    'GlobalAveragePool'         : GlobalAveragePool,
    'Flatten'                   : Flatten,
    'Conv'                      : Conv,
    'Relu'                      : Relu,
    'Gemm'                      : Gemm,
    'Add'                       : Add,
    'Mul'                       : Mul,
    'Reshape'                   : Reshape,
    'Transpose'                 : Transpose
}
