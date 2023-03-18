import pickle
from maptools import MapRoutine
from maptools import get_map
import os

mapname = 'xxx'
# os.environ.get('NVCIM_HOME')
routine = MapRoutine(mapname=mapname,noc_map=True,simulate=False,show_ctg=True)
routine.run()

params, mapinfo = get_map(mapname)

for xbar, cfg in mapinfo['xbar_config'].items():
    if 'Bias' in cfg['op_type']:
        bias = params[cfg['conv_bias']]
        break

print(bias.shape)
