import torch
import torch.nn as nn
import torch.nn.functional as F
from copy import deepcopy
from typing import Any
from maptools.core import (
    CTG, HostGraph, ModelParams
)
from maptools.calcusim.host import HostTask
from maptools.calcusim.device import DeviceTask

__all__ = ['CalcuSim']

class CalcuSim(nn.Module):

    def __init__(
        self, 
        ctg: CTG, 
        host_graph: HostGraph, 
        params: ModelParams,
        **kwargs: Any
    ) -> None:
        '''
        `CalcuSim` is a calculation simulation engine for post-mapping inference.

        The original AI model is deconstructed to some abstract data structures such
        as `HostGraph`, `DeviceGraph`, and `CTG`, but is reconstructed in `CalcuSim` 
        in the format of `torch.nn.Module`.

        `CalcuSim` is composed of two main parts: the host task and the device task.
        The host task is reconstructed as a `HostTask` according to `HostGraph`.
        The device task is reconstructed by multiple tiles executors according to `CTG`.

        Parameters
        ----------
        ctg : CTG
            communication trace graph, obtained from `TileMapper.ctg`
        
        params : ModelParams
            device param dictionary, with operator name as keys and the parameters as
            values, obtained from `OnnxConverter.params`.

        kwargs : Dict
            mapname : str = 'newmap'
                map name

        Examples
        --------
        Users can treat `CalcuSim` as a complete replacement of the torch model.
        For example, if we have an AI model with the format of `torch.nn.Module`, 
        we can perform inference by calling the model object:

        >>> model = .... # my torch model
        >>> x = torch.Tensor(...) # input data
        >>> y = model(x)

        Now suppose we have our torch model exported to an .onnx file and then mapped
        to `CTG` and `HostGraph`, to reconstruct the inference task of the original 
        AI model, we can instantiate a CalcuSim object and call it:

        >>> csim = CalcuSim(...) # instantiate a CalcuSim object
        >>> y = csim(x)

        That means, `CalcuSim` expose the same software interface as the torch model, 
        and we can perform post-mapping inference as if we are operating the torch model.

        Besides, `CalcuSim` supports cuda acceleration, which can be enabled by calling
        the method `CalcuSim.cuda()`:

        >>> csim.cuda()
        >>> y = csim(x)

        Key Members
        -----------
        self.obj_dict : Dict[Union[PhysicalTile, str], Union[_Tile, torch.Tensor]]
            A dictionary with physical tile id as keys and its corrensponding tile
            executors and values. The tile executors are the submodules of CalcuSim.

        self.res_dict : Dict[Union[str, Tuple], Dict[str, Optional[torch.Tensor]]]
            Stores the intermediate results of each tile.
            A dictionary with logical tile as keys and result dictionary as values
            Where the result dictionary has keys in `OBSERVE_VARS`.
        '''
        super().__init__()
        self.ctg = ctg
        self.host_graph = host_graph
        self.params = params
        self.mapname: str = 'newmap'
        self.quantize: bool = False
        self.observe: bool = False
        self.physical: bool = False
        self.__dict__.update(kwargs)

        self.device_task = DeviceTask(
            self.ctg, 
            self.params,
            mapname=self.mapname,
            quantize=self.quantize,
            observe=self.observe,
            physical=self.physical
        )
        self.host_task = HostTask(
            self.host_graph, 
            self.params
        )

    def cuda(self) -> None:
        self.host_task.cuda()
        self.device_task.cuda()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.host_task(self.device_task(x))

    def save_results(self, file_name: str = 'results'):
        self.device_task.save_results(file_name=file_name)