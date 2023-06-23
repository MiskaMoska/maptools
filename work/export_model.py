# 将pytorch的模型导出onnx

import torch 
import torchvision as tv
import torch.nn as nn
import torch.onnx as ox
import onnx

# vgg16 = tv.models.vgg16()
# print(vgg16.get_num_params())
# ox.export(vgg16,torch.randn(1,3,224,224),"vgg16.onnx")


# ssd = tv.models.detection.ssd300_vgg16()
# print(ssd.get_num_params())
# ox.export(ssd,torch.randn(1,3,300,300),"ssd300_vgg16.onnx",opset_version=13)

# model = tv.models.resnet18()
model = tv.models.vgg16()
# print(model.get_num_params())
ox.export(
    model,
    torch.randn([1,3,224,224]),
    "onnx_models/vgg16.onnx",
    opset_version=11,
    input_names=["input"],
    output_names=["output"]
)
print("done")
# model = onnx.load("vgg16.onnx")
# print(model.graph)