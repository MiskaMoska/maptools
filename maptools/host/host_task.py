import torch
import torch.nn as nn
from maptools import OperatorGraph
from maptools.host.host_operator import HostOperator

__all__ = ['HostTask']

class HostTask(nn.Module):

    def __init__(self, host_graph: OperatorGraph) -> None:
        super().__init__()
        self.host_graph = host_graph

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for n in self.host_graph.nodes:
            operator = HostOperator(self.host_graph.config(n))
            x = operator(x)
            del operator
        return x

