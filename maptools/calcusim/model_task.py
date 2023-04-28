import torch
import torch.nn as nn
from typing import Dict
from maptools.core import ModelParams, OriginGraph
from maptools.calcusim.host import HostOperator

__all__ = ['ModelTask']    

class ModelTask(nn.Module):

    def __init__(
        self,
        origin_graph: OriginGraph,
        params: ModelParams
    ) -> None:
        super().__init__()
        self.origin_graph = origin_graph
        self.params = params
        self._modules: Dict[str, nn.Module] = {}
        self._buffers: Dict[str, torch.Tensor] = {}
        self._construct_operators()

    def _construct_operators(self) -> None:
        for n in self.origin_graph.nodes:
            config = self.origin_graph.config(n)
            self._modules[n] = HostOperator(config, self.params)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for n in self.origin_graph.nodes:
            if self.origin_graph.is_input(n):
                self._buffers[n] = self._modules[n]([x])
            
            else:
                input_list = [self._buffers[pred] \
                    for pred in self.origin_graph.preds(n)]
                res = self._modules[n](input_list)
                if self.origin_graph.is_output(n):
                    return res
                self._buffers[n] = res

    def cuda(self) -> None:
        for module in self._modules.values():
            module.cuda()
