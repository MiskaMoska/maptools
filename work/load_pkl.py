# 加载保存的pkl文件进行观察

import os
import pickle
from maptools import read_results

mapname = 'resnet18'
res = read_results('resnet18', quantize=True)

print(res[(0,0,0,0)]['cast_in'])
# print(res[(0,0,0,0)]['data_out'])

