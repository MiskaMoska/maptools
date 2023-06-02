import onnx
from maptools import OnnxConverter, TileMapper, NocMapper
from maptools.core import NNModelArch
from maptools import MapPlotter

# 读取onnx模型，注意你自己的路径
model = onnx.load("onnx_models/simp-resnet18.onnx")

# 创建onnx转换器
oc = OnnxConverter(model, arch=NNModelArch.RESNET)

# 执行转换
oc.run_conversion()

# oc.plot_host_graph() # 查看主机算子图
# oc.plot_device_graph() # 查看设备算子图


# 获得转换得到的设备算子图
og = oc.device_graph

# 创建xbar映射器
xm = TileMapper(og, 256, 256*5)

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

nm.plot_ctg()

mp = MapPlotter(
    5,
    10,
    nm.cast_paths,
    nm.merge_paths,
    nm.gather_paths,
    show_path=True
)
mp.plot_cast_map()
mp.plot_merge_map()
mp.plot_gather_map()