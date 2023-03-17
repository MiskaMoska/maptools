'''
Test the function of mapper
'''
import onnx
from maptools import *
import sys

if __name__ == "__main__":
    # 获得onnx原生模型
    model = onnx.load("../onnx_models/simp-resnet18.onnx")

    # 创建onnx转换器
    oc = OnnxConverter(model,arch='resnet')

    # 执行转换
    oc.run_conversion()

    # 获得转换得到的算子图
    og = oc.og
    # oc.plot_op_graph()
    # 创建xbar映射器
    xm = XbarMapper(og, 256, 256*5)

    # 执行映射
    xm.run_map()

    # 打印映射信息
    xm.print_config()

    # 获得映射得到的CTG
    ctg = xm.ctg
    # for xbar, cfg in xm.xbar_config_info:
    #     if xbar == (0,0,0,0):
    #         print(cfg['conv_weight'][0,0])
    # ctg.plot_ctg()
    # sys.exit()

    # inf = Inferator(ctg)
    # # inf.run()
    # # inf.save_execu(file_name='this')
    # inf.plot_execu(load_file='this')

    # ctg.plot_ctg()
    # ctg.comm_load_analysis()

    # 创建NoC映射器
    nm = NocMapper(ctg,5,10)

    # 执行映射
    nm.run_map()

    # nm.save_map()

    # for k,v in nm.xbar_config_info:
    #     print(k,'\t\t',v['op_type'])
    # # for k,v in nm.xbar_config_info:
    # #     print(k,v['op_type'])
    # # nm.save_map(file_name='this.pkl')
    plt = MapPlotter(5,10,nm.cast_paths, nm.merge_paths, nm.gather_paths, show_path=True)
    plt.plot_gather_map()

