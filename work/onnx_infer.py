import torch
import onnxruntime as rt
import torch.onnx
import cv2
import numpy as np
import onnx
from PIL import Image
from torchvision import transforms
import torchvision as tv
# 使用onnxruntime进行推理

import torch.onnx as ox
from maptools import get_input

def onnx_infer(input: torch.Tensor):
    input = input.numpy()
    sess = rt.InferenceSession("onnx_models/my-yolo.onnx", None)
    #  sess = rt.InferenceSession(onnx_sim, providers=['CUDAExecutionProvider'])  # providers=[CPUExecutionProvider,'CUDAExecutionProvider']
    #  providers=[CPUExecutionProvider,'CUDAExecutionProvider']

    input_name = sess.get_inputs()[0].name
    out_name = sess.get_outputs()[0].name
    
    pred_onx = sess.run([out_name], {input_name: input}) 
    print('-'*50)
    print('onnx infer results')
    print(pred_onx[0])
    # print(np.argmax(pred_onx[0]))

import onnxsim
import onnxruntime
if __name__ == "__main__":
    onnx_infer(get_input('work/test2.png', resize=(768, 768)))
