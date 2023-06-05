import os
import onnx
from maptools import OnnxConverter, TileMapper
from maptools.core import ROOT_DIR
from maptools import NNModelArch

ONNXDIR = os.path.join(ROOT_DIR, 'onnx_models', 'simp-yolo.onnx')
MAPNAME = 'yolo'

import pickle
from maptools import CTG
from maptools import MapRoutine
from maptools import read_cfginfo, read_mapinfo, get_input
import os

root_dir = os.environ.get('NVCIM_HOME')
mapname = 'yolo'
model = os.path.join(root_dir, 'onnx_models', 'simp-yolo.onnx')
img = get_input('work/test8.png', resize=(768, 768))

# m = onnx.load(model)
# oc = OnnxConverter(m, arch=NNModelArch.YOLO_V3)
# oc.run_conversion()

# hg = oc.host_graph

# for node in hg.nodes:
#     if hg.op_type(node) == 'Concat':
#         for n in hg.preds(node):
#             print(n)


routine = MapRoutine(   
    mapname=mapname,
    arch=NNModelArch.YOLO_V3,
    noc_map=False,
    input=img,
    calcusim=True,
    save_results=False,
    save_cfginfo=False,
    show_ctg=False,
    show_device_graph=False,
    xbar_size = (128, 256),
    noc_size=(8, 10),
    model_dir=model,
    show_cast_path=True,
    show_merge_path=True,
    show_gather_path=True,
    toksim=False,
    toksim_latency = 4,
    quantize=True,
    physical=True,
    hardtrans=False,
    ivcf=4000/128,
    stats=True
)

ctg = routine.run()

