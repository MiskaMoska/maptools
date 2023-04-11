import torch
import torch.nn as nn
import torch.nn.functional as F
from  maptools.maptype import OperatorConfig

__all__ = ['HostOperator']

class GlobalAveragePool(nn.Module):

    def __init__(self) -> None:
        super().__init__()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.adaptive_avg_pool2d(x, 1)


class Gemm(nn.Module):
    
    def __init__(self, weight: torch.Tensor) -> None:
        super().__init__()
        self.weight = weight
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.linear(x, torch.tensor(self.weight))


class HostOperator(nn.Module):

    legal_ops = ['GlobalAveragePool', 'Flatten', 'Gemm']

    def __init__(self, config: OperatorConfig) -> None:
        super().__init__()
        self.build_operation(config)

    def build_operation(self, config):
        op_type = config['op_type']
        assert op_type in self.legal_ops, (
            f"usupported op_type {op_type} when building host operation")
        
        if op_type == 'GlobalAveragePool':
            self.operation = GlobalAveragePool()
        
        elif op_type == 'Flatten':
            self.operation = nn.Flatten()

        elif op_type == 'Gemm':
            self.operation = Gemm(config['fc_weight'])

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.operation(x)