import torch
from maptools.utils import read_quantparams


params = read_quantparams('resnet18')

for i,v in enumerate(params.values()):
    print(torch.tensor(v).float())