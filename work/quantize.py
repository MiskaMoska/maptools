# 执行量化
import torch
from ppq import TargetPlatform
from maptools.quantization import quantize

# generate calibration dataset begin
import torchvision.transforms as transforms
from torchvision.io import image
import torchvision as tv

trans = transforms.Compose([
    transforms.Resize([224, 224]),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
])

print("Preparing calibration dataset ...")
dataset = tv.datasets.ImageFolder(root='/mnt/c/Users/wx98/Downloads/calib', transform=trans)
calibset = [{'input': torch.unsqueeze(sample, dim=0)} for sample, _ in dataset]
print(f"Calibration dataset prepared, number of samples: {len(calibset)}")
# generate calibration datset end

INPUT_SHAPES     = {'input': [1, 3, 224, 224]}
CALIB_STEPS      = 128
DEVICE           = 'cuda'
ONNX_PATH        = 'onnx_models/simp-resnet18.onnx'

# quantize(
#     INPUT_SHAPES,
#     DEVICE,
#     ONNX_PATH,
#     mapname='resnet18',
#     calibset=calibset,
#     calib_steps=CALIB_STEPS
# )

quantize(
    {'input': [1, 3, 32, 32]},
    DEVICE,
    'onnx_models/simp-58.onnx',
    mapname='58',
    calibset=None,
    calib_steps=32
)

