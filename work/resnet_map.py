# 执行全流程映射

import pickle
from maptools import CTG
from maptools import MapRoutine
from maptools.core import  NNModelArch
from maptools import read_cfginfo, read_mapinfo, get_input
import os

root_dir = os.environ.get('NVCIM_HOME')
mapname = 'renet18'
test = os.path.join(root_dir, 'onnx_models', 'simp-resnet18.onnx')
img = get_input('work/test8.png', resize=(224, 224))

routine = MapRoutine(   
    mapname=mapname,
    arch=NNModelArch.RESNET,
    noc_map=True,
    calcusim=False,
    save_results=True,
    save_cfginfo=False,
    show_ctg=True,
    show_origin_graph=True,
    show_host_graph=True,
    show_device_graph=True,
    xbar_size=(256, 256*4),
    noc_size=(8, 9),
    model_dir=test,
    show_cast_path=True,
    show_merge_path=True,
    show_gather_path=True,
    toksim=False,
    toksim_latency = None,
    input=img,
    quantize=False,
    physical=True,
    hardtrans=True,
    ivcf=1500/128,
    stats=False
)

ctg = routine.run()

# for xbar in ctg.xbars:
#     print(xbar, ctg.dicts[xbar].keys())
