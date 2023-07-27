# 对比量化前的calcusim、量化后的calcusim和pytorch三者的推理的结果

import torch
import torchvision as tv
import torchvision.transforms as transforms
from torchvision.models import resnet18, resnet50
from torch.utils.data import DataLoader
from typing import List, Tuple, Dict
from maptools import OnnxConverter, TileMapper
from maptools.calcusim import CalcuSim, ModelTask
from maptools import read_quantparams
import onnx

K = 3 # 准确率指标为 K-ACC
MAPNAME = 'resnet18' 
ONNXDIR = 'onnx_models/simp-resnet18.onnx'
QUANTIZE = True # 是否进行量化
DEVICE = 'cuda' # 是否使用CUDA加速
BATCHSIZE = 32 # Batch 大小
PHYSICAL = False # 是否模拟真实的Xbar和ADC计算
HARDTRANS = True # 是否模拟真实的定点数乘法
IVCF = 4000/128 # ADC电流-电压转换系数

########################## 以下是 CalcuSim 模型 ############################################
model = onnx.load(ONNXDIR)
oc = OnnxConverter(model, mapname=MAPNAME, quantize=QUANTIZE)
oc.run_conversion()

xm = TileMapper(
    oc.device_graph, 
    256, 
    256*5, 
    mapname=MAPNAME,
    quantize=QUANTIZE
)
xm.run_map()
params = read_quantparams(MAPNAME) if QUANTIZE else oc.params
model = CalcuSim(
    xm.ctg, 
    oc.host_graph, 
    params, 
    mapname=MAPNAME, 
    quantize=QUANTIZE, 
    physical=PHYSICAL, 
    hardtrans=HARDTRANS,
    ivcf=IVCF
)
########################## 以上是 CalcuSim 模型 ############################################



########################## 以下是 Pytorch 原始模型 ############################################
# model = resnet18(pretrained=True)
# model.eval()
########################## 以上是 Pytorch 原始模型 ############################################



########################## 以下是 测试集构建 ############################################
device = torch.device(DEVICE)
if DEVICE == 'cuda':
    model.cuda()

trans = transforms.Compose([
    transforms.Resize([224, 224]),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
])

testset = tv.datasets.ImageFolder(root='/mnt/c/Users/wx98/Downloads/val', transform=trans)

test_loader = DataLoader(
    testset,
    batch_size=BATCHSIZE,
    num_workers=0,
    shuffle=False
)
########################## 以上是 测试集构建 ############################################


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

