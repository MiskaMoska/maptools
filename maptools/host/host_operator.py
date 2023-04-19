import torch
import torch.nn as nn
import torch.nn.functional as F
from functools import wraps
from typing import List, Tuple, Dict
from maptools.core import OperatorConfig, VALID_OPS

__all__ = ['HostOperator']

class GlobalAveragePool(nn.Module):

    def __init__(self, config: OperatorConfig) -> None:
        super().__init__()

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return F.adaptive_avg_pool2d(x[0], 1)


class Flatten(nn.Flatten):

    def __init__(self, config: OperatorConfig) -> None:
        super().__init__()

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return super().forward(x[0])


class Gemm(nn.Linear): 

    def __init__(self, config: OperatorConfig) -> None:
        super().__init__(config['gemm_len_inv'], config['gemm_len_outv'])
        self.weight.data = torch.tensor(config['gemm_weight'])
        self.bias.data = torch.tensor(config['gemm_bias'])

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return super().forward(x[0])


class Add(nn.Module):

    def __init__(self, config: OperatorConfig) -> None:
        super().__init__()

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.add(x[0], x[1])


class Mul(nn.Module):

    def __init__(self, config: OperatorConfig) -> None:
        super().__init__()

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.mul(x[0], x[1])


class Reshape(nn.Module):

    def __init__(self, config: OperatorConfig) -> None:
        super().__init__()
        self.shape = config['reshape_shape']

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.reshape(x[0], self.shape)


class Concat(nn.Module):

    def __init__(self, config: OperatorConfig) -> None:
        super().__init__()

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.concat(x, dim=1)


class Transpose(nn.Module):
    
    def __init__(self, config: OperatorConfig) -> None:
        super().__init__()
        self.perm = config['tranpose_perm']

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.permute(x[0], self.perm)


class HostOperator(nn.Module):

    def __init__(self, config: OperatorConfig) -> None:
        super().__init__()
        self.op_type = config['op_type']
        assert self.op_type in VALID_OPS, (
            f"unsupported op_type {self.op_type} when building host operation")
        self.operation = __HOST_OPERATOR_ACCESS_TABLE__[self.op_type](config)

    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return self.operation(x)


__HOST_OPERATOR_ACCESS_TABLE__ = {
    'GlobalAveragePool'         : GlobalAveragePool,
    'Flatten'                   : Flatten,
    'Gemm'                      : Gemm,
    'Add'                       : Add,
    'Mul'                       : Mul,
    'Reshape'                   : Reshape,
    'Transpose'                 : Transpose
}
