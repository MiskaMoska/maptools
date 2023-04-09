import pickle
from maptools import MapRoutine
from maptools import read_cfginfo, read_mapinfo
from maptools.calcusim import get_input
import os

root_dir = os.environ.get('NVCIM_HOME')
mapname = 'example'
test = os.path.join(root_dir, 'onnx_models', 'simp-example.onnx')
# img = get_input('work/test.jpg')

routine = MapRoutine(   
    mapname=mapname,
    noc_map=True,
    calcusim=False,
    save_cfginfo=True,
    show_ctg=True,
    show_op_graph=False,
    xbar_size = (128, 128*5),
    noc_size=(4, 6),
    model_dir=test,
    show_cast_path=True,
    show_merge_path=True,
    show_gather_path=True,
    toksim=False,
    toksim_latency = None
)

routine.run()
