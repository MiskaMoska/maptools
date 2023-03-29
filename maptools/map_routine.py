import os
import onnx
from typing import Optional, List, Dict, Tuple, Any
from maptools import *
from maptools.toksim import *
from maptools.hardware import *

__all__ = ['MapRoutine']

class MapRoutine(object):

    def __init__(self, *args, **kwargs) -> None:
        # global defination
        self.root_dir = os.environ.get('NVCIM_HOME')
        self.model_dir = os.path.join(self.root_dir, 'onnx_models', 'simp-resnet18.onnx')
        self.mapname = 'newmap'
        self.arch = 'resnet'
        self.config = kwargs

        # hardware configuration
        self.xbar_size: Tuple[2] = (256, 256*5)
        self.noc_size: Tuple[2] = (5, 10)

        # data input    
        self.input: Optional[Any] = None

        # procedure control
        self.noc_map: bool = True

        self.show_raw_graph: bool = False
        self.show_op_graph: bool = False
        self.show_ctg: bool = False

        self.toksim: bool = False
        self.toksim_latency: Optional[int] = None 
        self.calcusim: bool = True

        self.show_cast_path: bool = False
        self.show_gather_path: bool = False

        self.save_params: bool = True
        self.save_mapinfo: bool = True
        self.save_cfginfo: bool = False

        self.__dict__.update(kwargs)
        assert isinstance(self.mapname, str),\
            f"mapname should be <class 'str'>, but got {type(self.mapname)}"

    def run(self) -> None:
        model = onnx.load(self.model_dir)
        oc = OnnxConverter(model, **self.config)
        oc.run_conversion()
        if self.show_raw_graph:
            oc.plot_raw_graph()
        if self.show_op_graph:
            oc.plot_op_graph()
        if self.save_params:
            oc.save_params()
        xm = XbarMapper(oc.og, 
                        self.xbar_size[0], 
                        self.xbar_size[1], 
                        **self.config
                        )
        xm.run_map()
        xm.print_config()
        ctg = xm.ctg
        if self.toksim:
            tsim = TokSim(ctg, latency=self.toksim_latency, **self.config)
            tsim.run()
            tsim.save_execu()
            ctg = tsim.ctg
        if self.calcusim:
            import torch
            from maptools.calcusim import CalcuSim
            assert self.input is not None, "calcusim enabled but got input is None"
            assert isinstance(self.input, torch.Tensor), f"input must be torch.Tensor. but got {type(self.input)}"
            assert len(self.input.shape) == 4, f"input dimension must be 4 [N, C, H, W]. but got {len(self.input.shape)}"
            csim = CalcuSim(ctg, oc.param_dict, **self.config)
            _ = csim(self.input)
            csim.save_results()
        if self.noc_map:
            assert xm.total_xbar <= self.noc_size[0] * self.noc_size[1],\
                f"Need larger networks, number of total xbars: {xm.total_xbar}"
            nm = NocMapper(ctg, 
                            self.noc_size[0], 
                            self.noc_size[1],
                            **self.config
                            )
            nm.run_map()
            if self.save_mapinfo:
                nm.save_map()
            if self.show_cast_path or self.show_gather_path:
                plt = MapPlotter(self.noc_size[0], 
                                    self.noc_size[1], 
                                    nm.cast_paths, 
                                    nm.merge_paths, 
                                    nm.gather_paths, 
                                    show_path=True,
                                    **self.config
                                    )
                if self.show_cast_path:
                    plt.plot_cast_map()
                if self.show_gather_path:
                    plt.plot_gather_map()
            if self.save_cfginfo:
                nc = NocConfig(self.noc_size[0], 
                                self.noc_size[1],
                                nm.cast_paths,
                                nm.merge_paths,
                                nm.gather_paths,
                                **self.config
                                )
                nc.run_config()
                nc.save_config()
                
        if self.show_ctg:
            if self.noc_map:
                nm.plot_ctg()
            else:
                ctg.plot_ctg()