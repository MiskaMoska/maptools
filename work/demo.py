# 现在这个配置就是能够用来获得tree based和path based的通信冲突值的区别
from maptools import *
from maptools.toksim import TokSim
import onnx
import networkx as nx

import torch
import onnxruntime as rt

# 读取onnx模型
config = {
    'mapname': 'squeezenet',
    'quantize': False,
    # 'dre': DREMethod.SP_PART,
    'dle': DLEMethod.REVERSE_S
}

model = onnx.load("onnx_models/simp-squeezenet.onnx")

# 创建onnx转换器
oc = OnnxConverter(model, arch=NNModelArch.SQUEEZENET, **config)

# 执行模型转换
oc.run_conversion()
oc.save_params()
# oc.plot_device_graph()
# oc.plot_host_graph()
# oc.plot_origin_graph()
# oc.save_params()

# 获得转换得到的设备算子图
dg = oc.device_graph

print('GOPS:', dg.op_num)
print('M weights', dg.param_num)
print(oc.quantize)

# 创建逻辑映射器，设置Xbar尺寸
xm = TileMapper(dg, 128, 128*4+64, **config)

# 执行映射
xm.run_map()

# 打印映射信息
xm.report_config()

# 获得映射得到的CTG
ctg = xm.ctg

# toksim = TokSim(ctg)
# toksim.run()

# mtsk = ModelTask(oc.origin_graph, oc.params)

# print(oc.origin_graph.dicts['_174'])
# print(oc.origin_graph.dicts['_177'])
# print(oc.origin_graph.dicts['_180'])


# 获取输入图片数据, 缩放至 224 × 224
# input = get_input('work/test.jpg', resize=(224, 224))
# output = mtsk(input)
# print(output)
# params = read_quantparams(config['mapname'])

# 创建CalcuSim仿真器, tm是TileMapper, oc是OnnxConverter
# model_params = read_params(config['mapname'])
# csim = CalcuSim(
#     xm.ctg, oc.host_graph, model_params,
#     physical=False, stats=False,
#     eval_power=False, observe=True, **config
# )
# csim.cuda()
# # 运行CalcuSim仿真, 获得输出结果
# output: torch.Tensor = csim(input.cuda())
# csim.save_results()
# print(output.size())
# csim.report_power()


# 创建Tile阵列拓扑图，设置阵列规模
acg = ACG(8, 10)

# 创建物理映射器
nm = NocMapper(ctg, acg, **config)

# 执行智能布局布线
nm.run_layout()
nm.run_routing(omit_merge=False)
# nm.plot_ctg()

# 保存布局布线图
nm.save_layout()
nm.save_routing(omit_merge=False)
nm.plot_ctg()
nm.report_routing()

routing = nm.routing

# hd = HardwareDeployer(nm.cast_trails, nm.merge_trails, acg, ctg, nm.layout, **config)

# hd.save_config()
# toksim = TokSim(ctg, **config)
# toksim.run()

# trails = list(nm.cast_trails.values())

# draw_heatmap(acg, trails, mapfunc='lg', mapname=config['mapname'])

# plot_tokens(config['mapname'])



