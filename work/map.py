import pickle
from maptools import CTG
from maptools import MapRoutine
from maptools import read_cfginfo, read_mapinfo
from maptools.calcusim import get_input
import os

root_dir = os.environ.get('NVCIM_HOME')
mapname = 'resnet18'
test = os.path.join(root_dir, 'onnx_models', 'simp-resnet18.onnx')
img = get_input('work/test4.png')

routine = MapRoutine(   
    mapname=mapname,
    noc_map=False,
    calcusim=True,
    save_cfginfo=True,
    show_ctg=False,
    show_origin_graph=False,
    xbar_size = (256, 256*5),
    noc_size=(5, 10),
    model_dir=test,
    show_cast_path=True,
    show_merge_path=True,
    show_gather_path=True,
    toksim=False,
    toksim_latency = 4,
    input=img,
    quantize=True
)

ctg = routine.run()

# for xbar in ctg.xbars:
#     print(xbar, ctg.dicts[xbar].keys())
