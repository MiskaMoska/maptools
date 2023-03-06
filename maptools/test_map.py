'''
Test the function of mapper
'''
import onnx
from onnx_converter import *
from operator_graph import *
from xbar_mapper import *
from ctg import *
from noc_mapper import *
from inferator import *

if __name__ == "__main__":
    model = onnx.load("../onnx_models/simp-resnet50.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    og = oc.og
    xm = XbarMapper(og, 512, 512*5)
    xm._xbar_map_resnet()
    xm.print_config()
    # for v in xm.map_dict.values():
    #     if 'Pool' in v['op_type'] or True:
    #         print('\nXbar')
    #         print(v['conv_input_size'])

    ctg = xm.ctg
    # ctg.plot_ctg()
    inf = Inferator(ctg)
    inf.run()
    # inf.echo_xbar()
    # inf.echo_comm()
    # for n in inf.ctg.node_names:
    #     print(n)
    ctg = inf.ctg
    ctg.plot_ctg()

    # nm = NocMapper(ctg,10,25)
    # nm.map_xbars()
    # nm._cast_plan()
    # # nm._merge_plan()
    # # nm._gather_plan()
    # # nm.plot_map()
    # print('contention_coefficient:',nm.contention_coefficient)
    # for i in nm.merge_paths:
    #     print(i)
    # # for k,v in nm.cast_paths.items():
    # #     print(k,v)
    
