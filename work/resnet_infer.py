import os
import onnx
from maptools import OnnxConverter, TileMapper, CalcuSim
from maptools.core import ROOT_DIR
from maptools import NNModelArch
from maptools.host import ModelTask

ONNXDIR = os.path.join(ROOT_DIR, 'onnx_models', 'simp-yolo.onnx')
MAPNAME = 'yolo'

import pickle
import torch
from maptools import CTG
from maptools import MapRoutine
from maptools import read_cfginfo, read_mapinfo, get_input
import os

root_dir = os.environ.get('NVCIM_HOME')
mapname = 'resnet18'
model = os.path.join(root_dir, 'onnx_models', 'simp-resnet18.onnx')
imgs = []
# for i in range(16):
#     imgs.append(get_input('work/test8.png', resize=(768, 768)))
# img = torch.cat(imgs, dim=0)
img = get_input('work/test8.png', resize=(224, 224))

m = onnx.load(model)
oc = OnnxConverter(m, arch=NNModelArch.RESNET)
oc.run_conversion()
oc.device_graph.plot_graph()


tm = TileMapper(oc.device_graph, 256, 256*5)
tm.run_map()

csim = CalcuSim(tm.ctg, oc.host_graph, oc.params)
y = csim(img)
print(y)

task = ModelTask(oc.origin_graph, oc.params)
# img = img.cuda()
# task.cuda()
m = task(img)
print(torch.argmax(y))
print(torch.argmax(m))