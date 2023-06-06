# 执行全流程映射

import pickle
from maptools import CTG
from maptools import MapRoutine
from maptools import read_cfginfo, read_mapinfo, get_input
import os

root_dir = os.environ.get('NVCIM_HOME')
mapname = '58'
test = os.path.join(root_dir, 'onnx_models', 'simp-58.onnx')
img = get_input('work/test8.png', resize=(32, 32))

routine = MapRoutine(   
    mapname=mapname,
    noc_map=False,
    calcusim=True,
    save_results=True,
    save_cfginfo=False,
    show_ctg=True,
    show_origin_graph=True,
    show_host_graph=True,
    show_device_graph=True,
    xbar_size=(256, 256*5),
    noc_size=(5, 10),
    model_dir=test,
    show_cast_path=True,
    show_merge_path=True,
    show_gather_path=True,
    toksim=False,
    toksim_latency = None,
    input=img,
    quantize=True,
    physical=True,
    hardtrans=True,
    ivcf=4000/128,
    stats=True
)

ctg = routine.run()

# for xbar in ctg.xbars:
#     print(xbar, ctg.dicts[xbar].keys())
