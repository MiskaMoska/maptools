import pickle
from maptools import MapRoutine
from maptools import read_mapinfo, read_params, read_results
from maptools import get_input
import os

mapname = 'xxx'

img = get_input('work/test.jpg')
routine = MapRoutine(mapname=mapname,calcusim=True,show_ctg=True,input=img)
routine.run()

mapinfo = read_mapinfo(mapname)
params = read_params(mapname)
results = read_results(mapname)

print(results['output'].shape)

# for xbar, cfg in mapinfo['xbar_config'].items():
#     if 'Bias' in cfg['op_type']:
#         bias = params[cfg['conv_bias']]
#         break
