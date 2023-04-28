from maptools import *

mapinfo = read_mapinfo('xxx')
gather_paths = mapinfo['gather_paths']
cast_paths = mapinfo['cast_paths']
merge_paths = mapinfo['merge_paths']
# for p in gather_paths.values():
#     print(p)

for p in cast_paths.values():
    if p['src'] == [(6,9)]:
        print(p)