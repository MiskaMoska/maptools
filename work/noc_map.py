import os
import onnx
from maptools import OnnxConverter, TileMapper, NocMapper
from maptools.core import NNModelArch, CTG, ACG
from maptools import MapPlotter
from maptools import (
    LayoutDesigner, RoutingDesigner, RoutingPatternCode, 
    LayoutResult, DLEMethod, DREMethod, MapPlotter
)
import pickle
import matplotlib
from matplotlib import pyplot as plt

# 读取onnx模型，注意你自己的路径
nvcim_root = os.environ.get('NVCIM_HOME')
model_path = os.path.join(nvcim_root, "onnx_models/simp-squeezenet.onnx")
model = onnx.load(model_path)

# 创建onnx转换器
oc = OnnxConverter(model, arch=NNModelArch.SQUEEZENET)

# 执行转换
oc.run_conversion()

# oc.plot_host_graph() # 查看主机算子图
# oc.plot_device_graph() # 查看设备算子图


# 获得转换得到的设备算子图
og = oc.device_graph

# 创建xbar映射器
tm = TileMapper(og, 128, 128*5)

# 执行映射
tm.run_map()

# 打印映射信息
tm.print_config()

# 获得映射得到的CTG
ctg = tm.ctg

# ctg.plot_ctg()

acg = ACG(9, 9)

nm = NocMapper(ctg, acg, dle=None, dre=None, dummy_sa=False)
nm.run_layout()
nm.run_routing()
nm.layout.draw()
nm.routing.draw()

mplt = MapPlotter(
    acg.w, acg.h, 
    nm.cast_paths, 
    nm.merge_paths, 
    nm.cast_paths, 
    show_path=True, 
    mapname='newmap'
)

mplt.plot_cast_map()
mplt.plot_merge_map()


# rd.run_routing()

# routing = rd.routing_result
# print(routing.max_conflicts)

# # layout.draw()
# routing.draw()

# ys = rd.routing_engine.generation_best_Y
# with open('data/total_real_1.pkl', 'wb') as f:
#     pickle.dump(ys, f)


########################################################
# rd = RoutingDesigner(ctg, acg, layout, dre=DREMethod.DYXY)

# max = 1000
# cnt = 0
# res = []
# while True:
#     rd.run_routing()
#     now_max = rd.obj_func(rd.rpc)
#     if now_max < max:
#         max = now_max
#     print(cnt, '\t', max)
#     rd.reset()

#     if cnt % 10 == 0:
#         res.append(max)

#     cnt += 1
#     if cnt == 10000:
#         break

# with open('data/total_rand_4.pkl', 'wb') as f:
#     pickle.dump(res, f)


