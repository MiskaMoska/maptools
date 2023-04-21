import torch
import torch.nn as nn
import torch.nn.functional as F
from functools import wraps
from typing import List, Tuple, Dict, Callable
from functools import wraps
from maptools.core import OperatorConfig, ModelParams, VALID_OPS

__all__ = ['HostOperator']

def record_name(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, config, *args):
        self.name = config['name']
        self.op_type = config['op_type']
        return func(self, config, *args)
    return wrapper


def echo_input(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, x):
        res = func(self, x)
        # print(f"output_size: {res.shape}")
        return res
    return wrapper


class Conv(nn.Module):

    @record_name
    def __init__(self, config: OperatorConfig, params: ModelParams) -> None:
        super().__init__()
        weight_ptr = config['conv_weight']
        self.weight = torch.tensor(params[weight_ptr])

        bias_ptr = config['conv_bias']
        if params[bias_ptr] is None:
            self.bias = torch.zeros(config['conv_num_ochan'])
        else: self.bias = torch.tensor(params[bias_ptr])

        pads = config['conv_pads']
        self.pads = [pads[3], pads[1], pads[0], pads[2]]
        self.stride = config['conv_strides']

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        x = F.pad(x[0], self.pads)
        return F.conv2d(x, self.weight, bias=self.bias, stride=self.stride)

    def cuda(self) -> None:
        self.weight = self.weight.cuda()
        self.bias = self.bias.cuda()


class Relu(nn.ReLU):

    @record_name
    def __init__(self, *args) -> None:
        super().__init__()

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return super().forward(x[0])


class Resize(nn.Module):

    @record_name
    def __init__(self) -> None:
        super().__init__()

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return super().forward(x[0])


class GlobalAveragePool(nn.Module):

    @record_name
    def __init__(self, *args) -> None:
        super().__init__()

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return F.adaptive_avg_pool2d(x[0], 1)


class Flatten(nn.Flatten):

    @record_name
    def __init__(self, *args) -> None:
        super().__init__()

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return super().forward(x[0])


class Gemm(nn.Linear): 

    @record_name
    def __init__(self, config: OperatorConfig, params: ModelParams) -> None:
        super().__init__(config['gemm_len_inv'], config['gemm_len_outv'])

        weight_ptr = config['gemm_weight']
        self.weight.data = torch.tensor(params[weight_ptr])

        bias_ptr = config['gemm_bias']
        if params[bias_ptr] is None:
            self.bias.data = torch.zeros(self.out_features)
        else: self.bias.data = torch.tensor(params[bias_ptr])

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return super().forward(x[0])


class Add(nn.Module):

    @record_name
    def __init__(self, *args) -> None:
        super().__init__()

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.add(x[0], x[1])


class Mul(nn.Module):

    @record_name
    def __init__(self, *args) -> None:
        super().__init__()

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.mul(x[0], x[1])


class Reshape(nn.Module):

    @record_name
    def __init__(self, config: OperatorConfig, *args) -> None:
        super().__init__()
        self.shape = config['reshape_shape']

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        # adapt to input batch size
        self.shape[0] = x[0].shape[0]
        return torch.reshape(x[0], self.shape)


class Concat(nn.Module):

    @record_name
    def __init__(self, *args) -> None:
        super().__init__()

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.concat(x, dim=1)


class Transpose(nn.Module):

    @record_name
    def __init__(self, config: OperatorConfig, *args) -> None:
        super().__init__()
        self.perm = config['transpose_perm']

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return torch.permute(x[0], self.perm)


class Resize(nn.Upsample):

    @record_name
    def __init__(self, config: OperatorConfig, *args) -> None:
        super().__init__()
        scales = config['resize_scales']
        scales = (scales[2], scales[3])
        self.scale_factor = tuple(float(scale) for scale in scales)

    @echo_input
    def forward(self, x: List[torch.Tensor]) -> torch.Tensor:
        return super().forward(x[0])


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
    'Concat'                    : Concat,
    'Transpose'                 : Transpose,
    'Resize'                    : Resize
}
