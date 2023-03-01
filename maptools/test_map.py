'''
Test the function of mapper
'''
import onnx
from onnx_converter import *
from operator_graph import *
from xbar_mapper import *
from ctg import *
from noc_mapper import *

if __name__ == "__main__":
    model = onnx.load("../onnx_models/simp-resnet50.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    og = oc.og
    xm = XbarMapper(og, 256, 256*5)
    xm._xbar_map_resnet()
    xm.print_config()
    ctg = xm.ctg
    # ctg.plot_ctg()

    nm = NocMapper(ctg,10,25)
    nm.map_xbars()
    nm._cast_plan()
    # nm._merge_plan()
    # nm._collect_plan()
    # nm.plot_map()
    print('contention_coefficient:',nm.contention_coefficient)
    # for i in nm.merge_paths:
    #     print(i)
    # # for k,v in nm.cast_paths.items():
    # #     print(k,v)
    
