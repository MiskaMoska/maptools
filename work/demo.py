# 导入我们所开发的映射仿真工具包——Maptools
from maptools import *
import onnx

# 读取onnx模型
config = {
    'mapname': 'resnet18',
    'quantize': False,
    'dre': DREMethod.DYXY,
    # 'dle': DLEMethod.REVERSE_S,
    'slice_align': False
}

model = onnx.load("onnx_models/simp-resnet18.onnx")

# 创建onnx转换器
oc = OnnxConverter(model, arch=NNModelArch.RESNET, **config)

# 执行模型转换
oc.run_conversion()

# 显示转换得到的设备算子图
oc.plot_device_graph()

# 获得转换得到的设备算子图
og = oc.device_graph

# 创建逻辑映射器，设置Xbar尺寸
xm = TileMapper(og, 256, int(256*4.5), **config)

# 执行映射
xm.run_map()

# 打印映射信息
xm.report_config()

import sys
sys.exit()

# 获得映射得到的CTG
ctg = xm.ctg

# 创建Tile阵列拓扑图，设置阵列规模
acg = ACG(6, 8)

# 创建物理映射器
nm = NocMapper(ctg, acg, **config)

# 执行智能布局布线
nm.run_layout()
# nm.run_routing(omit_merge=False)

# 保存布局布线图
nm.save_layout()
# nm.save_routing(omit_merge=False)

# # 创建硬件部署器
# hd = HardwareDeployer(nm.cast_trails, nm.merge_trails, acg, ctg, nm.layout, **config)

# # 保存硬件配置信息
# hd.save_config()





