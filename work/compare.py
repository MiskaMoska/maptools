import os
from maptools import read_results
root_dir = os.environ.get('NVCIM_HOME')
save_dir = os.path.join(root_dir, 'mapsave', 'resnet18', 'calcusim')
mapname = 'resnet18'
quantres = read_results(mapname, quantize=True)
res = read_results(mapname, quantize=False)

for k in quantres:
    if k == (2, 0, 0, 0):
        print(quantres[k]['data_out_float'])
        print(res[k]['data_out'])
        # print(res[k].shape)


