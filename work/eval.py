# 对比量化前的calcusim、量化后的calcusim和pytorch三者的推理的结果

import torch
import torchvision as tv
import torchvision.transforms as transforms
from torchvision.models import resnet18, resnet50
from torch.utils.data import DataLoader
from typing import List, Tuple, Dict
from maptools import OnnxConverter, TileMapper
from maptools.calcusim import CalcuSim
from maptools import read_quantparams
import onnx

K = 3
MAPNAME = 'resnet18'
ONNXDIR = 'onnx_models/simp-resnet18.onnx'
QUANTIZE = True
DEVICE = 'cuda'
BATCHSIZE = 32
PHYSICAL = False

########################## CalcuSim Model Begin ############################################
model = onnx.load(ONNXDIR)
oc = OnnxConverter(model, mapname=MAPNAME, quantize=QUANTIZE)
oc.run_conversion()

xm = TileMapper(
    oc.device_graph, 
    256, 
    256*5, 
    mapname=MAPNAME
)
xm.run_map()
params = read_quantparams(MAPNAME) if QUANTIZE else oc.params
model = CalcuSim(xm.ctg, oc.host_graph, params, mapname=MAPNAME, quantize=QUANTIZE, physical=PHYSICAL)
########################## CalcuSim Model End ############################################


########################## Pytorch Model Begin ############################################
# model = resnet18(pretrained=True)
model.eval()
########################## Pytorch Model End ############################################

device = torch.device(DEVICE)
if DEVICE == 'cuda':
    model.cuda()

trans = transforms.Compose([
    transforms.Resize([224, 224]),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
])

testset = tv.datasets.ImageFolder(root=r'C:\Users\wx98\Downloads\val', transform=trans)

test_loader = DataLoader(
    testset,
    batch_size=BATCHSIZE,
    num_workers=0,
    shuffle=False
)

loader_len = len(test_loader)

total_samples = 0
true_samples = 0

def get_true_number(outputs: List[torch.Tensor], labels: List[int], k: int) -> int:
    preds = [output.topk(k)[1] for output in outputs]
    lst = [1 if labels[i] in preds[i] else 0 for i in range(len(labels))]
    return sum(lst)

for i, (inputs, labels) in enumerate(test_loader, 1):
    print(f'Evaluating batches: {i}/{loader_len}')
    inputs, labels = inputs.to(device), labels.to(device)
    outputs = model(inputs)
    total_samples += len(labels)
    true_samples += get_true_number(outputs, labels, K)

print("\ntotal samples:", total_samples)
print("true samples:", true_samples)
print("accuracy:%f%%" % (true_samples / total_samples * 100))

