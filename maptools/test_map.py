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

if __name__ == "__main__":
    # model = onnx.load("../onnx_models/simp-resnet18.onnx")
    # oc = OnnxConverter(model,arch='resnet')
    # oc.run_conversion()
    # og = oc.og
    # xm = XbarMapper(og, 256, 256*5)
    # xm.run_map()
    # xm.print_config()
    # ctg = xm.ctg

    # # inf = Inferator(ctg, slide_once=True, latency=16)
    # # inf.run()
    # # inf.echo_xbar()
    # # inf.echo_comm()
    # # inf.save_execu()

    # # ctg.comm_load_analysis()
    # nm = NocMapper(ctg,5,10)
    # nm.run_map()
    # mp = MapPlotter(5,10, nm.cast_paths, nm.merge_paths, nm.gather_paths)
    # mp.plot_gather_map()

    # 获得onnx原生模型
    model = onnx.load("../onnx_models/simp-resnet18.onnx")

    # 创建onnx转换器
    oc = OnnxConverter(model,arch='resnet')

    # 执行转换
    oc.run_conversion()

    # 获得转换得到的算子图
    og = oc.og

    # 创建xbar映射器
    xm = XbarMapper(og, 256, 256*5)

    # 执行映射
    xm.run_map()

    # 打印映射信息
    xm.print_config()

    # 获得映射得到的CTG
    ctg = xm.ctg

    ctg.plot_ctg()

    # 创建NoC映射器
    nm = NocMapper(ctg,5,10)

    # 执行映射
    nm.run_map()
