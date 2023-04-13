import torch
import torch.nn.functional as F
import torch.nn as nn
from typing import Generator

class A(nn.Module):

    def __init__(self) -> None:
        super().__init__()
        self.b = nn.Conv2d(32,32,[3,3])
        self.c = nn.Conv2d(32,32,[3,3])
        self.dict = {}
        self.dict['d'] = nn.Conv2d(32,32,[3,3])
        self.dict['e'] = nn.Conv2d(32,32,[3,3])

    def children(self) -> Generator:
        yield from iter([self.b, self.c])
        yield from self.dict.values()

device = torch.device('cuda')


class Gemm(nn.Module):
    
    def __init__(self, weight: torch.Tensor) -> None:
        super().__init__()
        self.weight = torch.tensor(weight)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.linear(x, self.weight)
    

gemm = torch.nn.Linear(10,20)

print(gemm.weight.device)
gemm.to(device)

print(gemm.weight.device)
