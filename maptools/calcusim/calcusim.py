import torch
import torch.nn as nn
import torch.nn.functional as F
from copy import deepcopy
from typing import Any, Optional, Dict
from maptools.core import (
    CTG, HostGraph, ModelParams, LogicalTile,
    ADC_POWER_PER_TRANSFER
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
        self.hardtrans: bool = True
        self.ivcf: Optional[float] = None
        self.first_layer_ivcf: Optional[float] = None
        self.stats: bool = False
        self.eval_power: bool = False
        self.__dict__.update(kwargs)

        self.done: bool = False

        self.device_task = DeviceTask(
            self.ctg, 
            self.params,
            mapname=self.mapname,
            quantize=self.quantize,
            observe=self.observe,
            physical=self.physical,
            hardtrans=self.hardtrans,
            ivcf=self.ivcf,
            first_layer_ivcf=self.first_layer_ivcf,
            stats=self.stats,
            eval_power=self.eval_power
        )
        self.host_task = HostTask(
            self.host_graph, 
            self.params
        )

    def cuda(self) -> None:
        self.host_task.cuda()
        self.device_task.cuda()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        self.device_output = self.device_task(x)
        self.host_output = self.host_task(self.device_output)
        self.done = True
        return self.host_output

    def save_results(self, file_name: str = 'results'):
        self.device_task.save_results(file_name=file_name)

    def report_results(self) -> None:
        print('\n'+'-'*70)
        print('\t\tCalcuSim Results')
        print('-'*70)
        print('device output shape: ', [v.shape for v in self.device_output])
        print('host output shape: ', self.host_output.shape)
        print('host output max: ', torch.max(self.host_output))
        print('host output max index: ', torch.argmax(self.host_output))

    def report_power(self) -> None:
        if not self.eval_power:
            raise AssertionError("please enable eval_power")
        if not self.done:
            raise AssertionError("please run self.forward() before reporting power")
        if not self.quantize:
            raise AssertionError("please enable quantize before reporting power")
        if not self.physical:
            raise AssertionError("please enable physical before reporting power")
        if self.stats:
            raise AssertionError("please disable stats before reporting power")
            
        power_dict = self.device_task.power_dict
        self._calcu_adc_power(power_dict)

        print('\n'+'-'*70)
        print('\t\tPower Evaluation Reports')
        print('-'*70)
        for tile, dict in power_dict.items():
            print(f"tile: {tile}\txbar_power: {dict['xbar']}\tadc_power: {dict['adc']}")

        xbar_powers = [p['xbar'] for p in power_dict.values()]
        adc_powers = [p['adc'] for p in power_dict.values()]
        print(f"total power (J/Frame): {sum(xbar_powers)+sum(adc_powers)}")

    def _calcu_adc_power(self, power_dict: Dict[LogicalTile, Dict[str, float]]) -> None:
        for tile in self.ctg.tile_nodes:
            config = self.ctg.get_tile_config(tile)
            osize = config['conv_output_size']
            ochan = config['xbar_num_ochan']
            power = osize[0] * osize[1] * ochan * 8 * ADC_POWER_PER_TRANSFER / 16 # considering adc sharing
            power_dict[tile]['adc'] = power

