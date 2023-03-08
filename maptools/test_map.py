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
from map_plotter import *

def opgraph_vgg16():
    model = onnx.load("../onnx_models/simp-vgg16.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    oc.plot_op_graph()

def opgraph_resnet18():
    model = onnx.load("../onnx_models/simp-resnet18.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    oc.plot_op_graph()

def opgraph_resnet50():
    model = onnx.load("../onnx_models/simp-resnet50.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    oc.plot_op_graph()

def opgraph_googlenet():
    model = onnx.load("../onnx_models/simp-googlenet.onnx")
    oc = OnnxConverter(model,arch='googlenet')
    oc.run_conversion()
    oc.plot_op_graph()

def ctg_vgg16():
    model = onnx.load("../onnx_models/simp-vgg16.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    og = oc.og
    xm = XbarMapper(og, 256, 256*5)
    xm._xbar_map_resnet()
    xm.print_config()
    ctg = xm.ctg
    ctg.plot_ctg()

def ctg_resnet18():
    model = onnx.load("../onnx_models/simp-resnet18.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    oc.plot_op_graph()
    og = oc.og
    xm = XbarMapper(og, 256, 256*5)
    xm._xbar_map_resnet()
    xm.print_config()
    ctg = xm.ctg
    ctg.plot_ctg()

def ctg_resnet50():
    model = onnx.load("../onnx_models/simp-resnet50.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    og = oc.og
    xm = XbarMapper(og, 256, 256*5)
    xm._xbar_map_resnet()
    xm.print_config()
    ctg = xm.ctg
    ctg.plot_ctg()

def network_vgg16():
    model = onnx.load("../onnx_models/simp-vgg16.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    og = oc.og
    xm = XbarMapper(og, 256, 256*5)
    xm._xbar_map_resnet()
    xm.print_config()
    ctg = xm.ctg
    ctg.comm_load_analysis()
    nm = NocMapper(ctg,5,11)
    nm.map_xbars()
    nm._cast_plan()
    nm._merge_plan()
    nm._gather_plan()
    mp = MapPlotter(5,11, nm.cast_paths, nm.merge_paths, nm.gather_paths, show_path=True)
    mp.plot_cast_map()

def network_resnet50():
    model = onnx.load("../onnx_models/simp-resnet50.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    og = oc.og
    xm = XbarMapper(og, 256, 256*5)
    xm._xbar_map_resnet()
    xm.print_config()
    ctg = xm.ctg
    ctg.comm_load_analysis()
    nm = NocMapper(ctg,10,25)
    nm.map_xbars()
    nm._cast_plan()
    nm._merge_plan()
    nm._gather_plan()
    mp = MapPlotter(10,25, nm.cast_paths, nm.merge_paths, nm.gather_paths, show_path=True)
    mp.plot_cast_map()

def analysis_resnet18():
    model = onnx.load("../onnx_models/simp-resnet18.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    og = oc.og
    xm = XbarMapper(og, 256, 256*5)
    xm._xbar_map_resnet()
    xm.print_config()
    ctg = xm.ctg
    inf = Inferator(ctg)
    inf.run()
    inf.echo_xbar()
    inf.echo_comm()
    ctg = inf.ctg
    ctg.plot_ctg()

if __name__ == "__main__":
    model = onnx.load("../onnx_models/simp-resnet18.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.run_conversion()
    og = oc.og
    xm = XbarMapper(og, 256, 256*5)
    xm._xbar_map_resnet()
    xm.print_config()
    ctg = xm.ctg

    inf = Inferator(ctg, slide_once=False, latency=16)
    inf.run()
    inf.echo_xbar()
    inf.echo_comm()
    inf.save_execu()

    # ctg.comm_load_analysis()
    # nm = NocMapper(ctg,5,10)
    # nm.map_xbars()
    # nm._cast_plan()
    # nm._merge_plan()
    # nm._gather_plan()
    # mp = MapPlotter(5,10, nm.cast_paths, nm.merge_paths, nm.gather_paths)
    # mp.plot_gather_map()
    
