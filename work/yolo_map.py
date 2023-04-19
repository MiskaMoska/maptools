import os
import onnx
from maptools import OnnxConverter, XbarMapper
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
# img = get_input('work/test8.png')

m = onnx.load(model)
oc = OnnxConverter(m, arch=NNModelArch.YOLO_V3)
oc.run_conversion()

hg = oc.host_graph

for node in hg.nodes:
    if hg.op_type(node) == 'Concat':
        for n in hg.preds(node):
            print(n)


routine = MapRoutine(   
    mapname=mapname,
    arch=NNModelArch.YOLO_V3,
    noc_map=False,
    calcusim=False,
    save_results=True,
    save_cfginfo=True,
    show_ctg=True,
    show_device_graph=True,
    xbar_size = (128, 256),
    noc_size=(8, 10),
    model_dir=model,
    show_cast_path=True,
    show_merge_path=True,
    show_gather_path=True,
    toksim=True,
    toksim_latency = 4,
    quantize=False,
    physical=False
)

# ctg = routine.run()

