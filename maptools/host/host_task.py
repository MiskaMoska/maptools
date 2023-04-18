import torch
import torch.nn as nn
from typing import Dict, List, Tuple, Iterator
from maptools.core import HostGraph
from maptools.host.host_operator import HostOperator

__all__ = ['HostTask']

class HostTask(nn.Module):

    def __init__(self, host_graph: HostGraph) -> None:
        super().__init__()
        self.host_graph = host_graph
        self._modules: Dict[str, nn.Module] = {}
        self._buffers: Dict[str, torch.Tensor] = {}
        self._construct_operators()

    def _construct_operators(self) -> None:
        for n in self.host_graph.nodes:
            self._modules[n] = HostOperator(self.host_graph.config(n))

    def forward(self, x: Tuple[torch.Tensor, ...]) -> torch.Tensor:
        for n in self.host_graph.nodes:
            if self.host_graph.is_input(n): ...

            x = self._modules[n](x)


        return x


