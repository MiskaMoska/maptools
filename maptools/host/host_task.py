import torch
import torch.nn as nn
from maptools import OperatorGraph
from maptools.host.host_operator import HostOperator
from typing import Dict, List, Tuple, Iterator

__all__ = ['HostTask']

class HostTask(nn.Module):

    def __init__(self, host_graph: OperatorGraph) -> None:
        super().__init__()
        self.host_graph = host_graph
        self._modules: Dict[str, nn.Module] = {}
        self._construct_operators()

    def _construct_operators(self) -> None:
        for n in self.host_graph.nodes:
            self._modules[n] = HostOperator(self.host_graph.config(n))
    
    ## The following codes are dangerous, not recommended
    # def children(self) -> Iterator[nn.Module]:
    #     '''
    #     To support recursive children configuration
    #     This method is used to support cuda acceleration
    #     '''
    #     yield from self.operators.values()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for n in self.host_graph.nodes:
            x = self._modules[n](x)
        return x


