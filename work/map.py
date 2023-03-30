import pickle
from maptools import MapRoutine
from maptools import read_cfginfo, read_mapinfo
from maptools.calcusim import get_input
import os

root_dir = os.environ.get('NVCIM_HOME')
mapname = 'newmap'
test = os.path.join(root_dir, 'onnx_models', 'simp-resnet18.onnx')
# img = get_input('work/test.jpg')

routine = MapRoutine(   
    mapname=mapname,
    noc_map=True,
    calcusim=False,
    save_cfginfo=True,
    show_ctg=True,
    noc_size=(5, 11),
    model_dir=test,
    show_cast_path = True,
    show_gather_path=True,
    toksim=True,
    toksim_latency = None
)

routine.run()
