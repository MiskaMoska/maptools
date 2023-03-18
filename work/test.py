import pickle
from maptools import MapRoutine
from maptools import get_map
import os

mapname = 'xxx'
# os.environ.get('NVCIM_HOME')
routine = MapRoutine(mapname=mapname,noc_map=True,simulate=False,show_ctg=True)
routine.run()

params, mapinfo = get_map(mapname)

for item in mapinfo['p2p_gathers']:
    print(item[0],item[1])
