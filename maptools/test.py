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
    

# import networkx as nx

# g = nx.MultiDiGraph()

# g.add_node(1, color='red')

# print(g.nodes[1])

def add(x):
    return x+1

a = ([1,2,3],[4,5,6])

print(list(zip(*a)))


def set_precall_method(callee=lambda x:x):
    def precall_method(func):

        def wrapper(*args, **kwargs):
            callee()
            return func(*args, **kwargs)

        return wrapper
    return precall_method



def echo():
    print("fuck")

def add(x, y):
    return x+y

print(add(3,4))
