import torch
import torch.nn.functional as F
import torch.nn as nn
from typing import Generator

class A(nn.Module):

    def __init__(self) -> None:
        super().__init__()
        self.b = nn.Conv2d(31,32,[3,3])
        self.c = nn.Conv2d(32,32,[3,3])
        self.dict = {}
        self.dict['d'] = nn.Conv2d(33,32,[3,3])
        self.dict['e'] = nn.Conv2d(34,32,[3,3])
        for k, v in self.dict.items():
            self.add_module(k, v)

    # def children(self) -> Generator:
    #     yield from iter([self.b, self.c])
    #     yield from self.dict.values()


a= A()
for i in a.children():
    print(i)


class Gemm(nn.Module):
    
    def __init__(self, weight: torch.Tensor) -> None:
        super().__init__()
        self.weight = torch.tensor(weight)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.linear(x, self.weight)
    


class B():

    def __init__(self) -> None:
        self._var = 0
    
    @property
    def var(self):
        return self._var
    
    @var.setter
    def var(self, value):
        self._var = value
    

b = B()
print(b.var)
b.var = 1
print(b.var)

