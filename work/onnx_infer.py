import torch
import onnxruntime as rt
import torch.onnx
import cv2
import numpy as np
import onnx
from PIL import Image
from torchvision import transforms
import torchvision as tv
import torch.onnx as ox
from maptools.calcusim import get_input

def onnx_infer(input):
    input = input.numpy()
    sess = rt.InferenceSession("onnx_models/simp-resnet18.onnx", None)
    #  sess = rt.InferenceSession(onnx_sim, providers=['CUDAExecutionProvider'])  # providers=[CPUExecutionProvider,'CUDAExecutionProvider']
    #  providers=[CPUExecutionProvider,'CUDAExecutionProvider']

    input_name = sess.get_inputs()[0].name
    out_name = sess.get_outputs()[0].name
    
    pred_onx = sess.run([out_name], {input_name: input}) 
    print('-'*50)
    print('onnx infer results')
    print(np.argmax(pred_onx[0]))

if __name__ == "__main__":
    onnx_infer(get_input('work/test2.png'))
