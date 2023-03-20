import pickle
from maptools import MapRoutine
from maptools import read_mapinfo, read_params, read_results
from maptools import get_input
import os

mapname = 'xxx'

img = get_input('work/test.jpg')
routine = MapRoutine(mapname='xxx',input=img,show_ctg=False)
routine.run()

mapinfo = read_mapinfo(mapname)
params = read_params(mapname)
results = read_results(mapname)

# print(results['output'].shape)'

for (i,j), cfg in mapinfo['xbar_config'].items():
    if (i,j) == (0,0):
        print(cfg['conv_pads'],cfg['pool_pads'])
