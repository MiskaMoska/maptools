import os
import onnx
from maptools import OnnxConverter
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
mapname = 'yolo'
model = os.path.join(root_dir, 'onnx_models', 'simp-yolo.onnx')
imgs = []
for i in range(16):
    imgs.append(get_input('work/test8.png', resize=(768, 768)))
img = torch.cat(imgs, dim=0)

m = onnx.load(model)
oc = OnnxConverter(m, arch=NNModelArch.YOLO_V3)
oc.run_conversion()
# oc.origin_graph.plot_graph()
task = ModelTask(oc.origin_graph, oc.params)
task.cuda()
while True:
    y = task(img)
    print('aaaa')
print(y.shape)
