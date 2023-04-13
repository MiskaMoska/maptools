# 加载保存的pkl文件进行观察

import os
import pickle
from maptools import *

mapname = 'resnet18'
root_dir = os.environ.get('NVCIM_HOME')
quantinfo_path = os.path.join(root_dir, 'mapsave', mapname, 'quantinfo.pkl')
graph_path = os.path.join(root_dir, 'mapsave', mapname, 'quantized_graph.pkl')

with open(quantinfo_path, 'rb') as f:
    quantinfo = pickle.load(f)

for i in quantinfo.values():
    print(i.__dict__)

# qparams = read_quantparams(mapname)
# params = read_params(mapname)
