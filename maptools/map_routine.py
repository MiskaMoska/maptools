import os
import sys
import onnx
import torch
from typing import Optional, Tuple, Any
if os.name == 'posix':
    from maptools.toksim import TokSim
from maptools.utils import read_quantparams
from maptools.core import CTG, NNModelArch, ROOT_DIR
from maptools.mapper import OnnxConverter, TileMapper, NocMapper
from maptools.calcusim import CalcuSim

__all__ = ['MapRoutine']

class MapRoutine(object):

    def __init__(self, **kwargs: Any) -> None:
        # global defination
        self.model_dir = os.path.join(ROOT_DIR, 'onnx_models', 'simp-resnet18.onnx')
        self.mapname = 'newmap'
        self.arch = NNModelArch.RESNET

        # hardware configuration
        self.xbar_size: Tuple[int, int] = (256, 256*5)
        self.noc_size: Tuple[int, int] = (5, 10)

        # data input    
        self.input: Optional[torch.Tensor] = None

        # procedure control
        self.noc_map: bool = True
        self.quantize: bool = False
        self.physical: bool = False
        self.hardtrans: bool = False
        self.ivcf: Optional[float] = None
        self.stats: bool = False

        self.show_origin_graph: bool = False
        self.show_host_graph: bool = False
        self.show_device_graph: bool = False
        self.show_ctg: bool = False

        self.toksim: bool = False
        self.calcusim: bool = False
        self.save_results: bool = False

        self.show_cast_path: bool = False
        self.show_merge_path: bool = False
        self.show_gather_path: bool = False

        self.save_params: bool = True
        self.save_mapinfo: bool = True
        self.save_cfginfo: bool = False

        config_keys = ['mapname', 'arch', 'quantize']
        self.config = {k: kwargs[k] for k in config_keys if k in kwargs}
        self.__dict__.update(kwargs)

        assert isinstance(self.mapname, str),\
            f"mapname should be {str}, but got {type(self.mapname)}"

    def run(self) -> CTG:
        model = onnx.load_model(self.model_dir)
        oc = OnnxConverter(model, **self.config)
        oc.run_conversion()

        if self.show_origin_graph: oc.plot_origin_graph()
        if self.show_host_graph: oc.plot_host_graph()
        if self.show_device_graph: oc.plot_device_graph()
        if self.save_params: oc.save_params()

        xm = TileMapper(
            oc.device_graph, 
            self.xbar_size[0], 
            self.xbar_size[1], 
            **self.config
        )

        xm.run_map()
        xm.print_config()
        ctg = xm.ctg
        if self.toksim:
            tsim = TokSim(
                ctg,
                mapname=self.mapname
            )
            tsim.run()
            tsim.save_execu()
            # ctg = tsim.ctg

        if self.calcusim:
            assert self.input is not None, "calcusim enabled but got input is None"
            assert isinstance(self.input, torch.Tensor), f"input must be {torch.Tensor}, but got {type(self.input)}"
            assert len(self.input.shape) == 4, f"input dimension must be 4 [N, C, H, W], but got {len(self.input.shape)}"

            params = read_quantparams(self.mapname) if self.quantize else oc.params
            csim = CalcuSim(
                ctg, 
                oc.host_graph, 
                params, 
                observe=self.save_results, 
                physical=self.physical,
                hardtrans=self.hardtrans,
                ivcf=self.ivcf,
                stats=self.stats,
                **self.config
            )
            _ = csim(self.input)
            csim.report_results()
            
            if self.save_results:
                csim.save_results(file_name='quantres' if self.quantize else 'res')

        if self.noc_map:
            assert xm.total_tile <= self.noc_size[0] * self.noc_size[1],\
                f"Need larger networks, number of total tiles: {xm.total_tile}"
            nm = NocMapper(
                ctg, 
                self.noc_size[0],
                self.noc_size[1],
                **self.config
            )
            nm.run_layout()
            nm.run_routing()

            if self.save_mapinfo: nm.save_config()
                
        if self.show_ctg:
            if self.noc_map: nm.plot_ctg()
            else: ctg.plot_ctg()

        return ctg