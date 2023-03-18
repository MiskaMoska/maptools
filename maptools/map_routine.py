import os
import onnx
from maptools import *

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
        self.xbar_size = (256, 256*5)
        self.noc_size = (5, 10)

        # procedure control
        self.noc_map = True
        self.show_raw_graph = False
        self.show_op_graph = False
        self.save_param = True
        self.simulate = False
        self.show_execu = False
        self.show_ctg = False
        self.save_mapinfo = True
        self.show_cast_path = False
        self.show_gather_path = False

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
        if self.save_param:
            oc.save_params()
        xm = XbarMapper(oc.og, 
                        self.xbar_size[0], 
                        self.xbar_size[1], 
                        **self.config
                        )
        xm.run_map()
        xm.print_config()
        ctg = xm.ctg
        if self.simulate:
            tsim = TokSim(ctg, **self.config)
            tsim.run()
            tsim.save_execu()
            if self.show_execu:
                tsim.plot_execu()
            ctg = tsim.ctg
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
                
        if self.show_ctg:
            if self.noc_map:
                nm.plot_ctg()
            else:
                ctg.plot_ctg()