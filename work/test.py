import pickle
from maptools import MapRoutine
from maptools import read_cfginfo, read_mapinfo
from maptools import get_input
import os

mapname = 'xxx'

img = get_input('work/test.jpg')
routine = MapRoutine(mapname='xxx',calcusim=False,show_ctg=False,save_cfginfo=True)
routine.run()

cfginfo = read_cfginfo(mapname)
mapinfo = read_mapinfo(mapname)
# mapinfo = read_mapinfo(mapname)
# params = read_params(mapname)
# results = read_results(mapname)

for k,v in mapinfo['xbar_config'].items():
    print(k, v.keys())

# print(results['output'].shape)'

