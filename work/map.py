import pickle
from maptools import MapRoutine
from maptools import read_cfginfo, read_mapinfo
from maptools.calcusim import get_input
import os

root_dir = os.environ.get('NVCIM_HOME')
mapname = 'resnet50'
test = os.path.join(root_dir, 'onnx_models', 'simp-resnet50.onnx')
img = get_input('work/test.jpg')
routine = MapRoutine(   
                        mapname=mapname,
                        noc_map=True,
                        calcusim=True,
                        input=img,
                        save_cfginfo=True,
                        show_ctg=True,
                        noc_size=(10, 25),
                        model_dir=test,
                        show_gather_path=True,
                        toksim=False,
                        toksim_latency = 16
                    )
routine.run()

# cfginfo = read_cfginfo(mapname)
# mapinfo = read_mapinfo(mapname)
# mapinfo = read_mapinfo(mapname)
# params = read_params(mapname)
# results = read_results(mapname)

# for k,v in mapinfo['xbar_config'].items():
#     print(k, v.keys())

# print(results['output'].shape)'