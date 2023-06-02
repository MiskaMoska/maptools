import torch
import torch.onnx as ox

model_path = "model.pth"
model = torch.load('onnx_models/2362.pth')
print(model['net'].keys())