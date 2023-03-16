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

model = tv.models.resnet18(pretrained=True)
model.eval()
trans = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)), 
])

def get_input():
    image_file = './test2.jpg'
    img = Image.open(image_file)
    img = img.resize((224,224))
    img = trans(img)
    img = torch.unsqueeze(img, 0)
    return img

def export():
    ox.export(model,
                torch.randn([1,3,224,224]),
                "resnet18.onnx",
                opset_version=11,
                input_names=["input"],
                output_names=["output"]
                )

def torch_infer(input):
    output = model(input)
    output = output.detach().numpy()
    print('-'*50)
    print('torch infer results')
    print(np.argmax(output))

def onnx_infer(input):
    input = input.numpy()
    sess = rt.InferenceSession("resnet18.onnx", None)
    #  sess = rt.InferenceSession(onnx_sim, providers=['CUDAExecutionProvider'])  # providers=[CPUExecutionProvider,'CUDAExecutionProvider']
    #  providers=[CPUExecutionProvider,'CUDAExecutionProvider']

    input_name = sess.get_inputs()[0].name
    out_name = sess.get_outputs()[0].name
    
    # X_test = cv2.imread(img_path)
    # X_test = cv2.resize(X_test, (224, 224))
    # # X_test = cv2.cvtColor(X_test, cv2.COLOR_BGR2RGB)
    # X_test = X_test / 255
    # X_test = X_test.swapaxes(0,2)
    # print(X_test.shape)
    # X_test = X_test.astype(np.float32)
    # print(X_test.shape)
    # X_test = np.expand_dims(X_test, axis=0)
    # print(X_test.shape)

    pred_onx = sess.run([out_name], {input_name: input}) # 执行推断
    print('-'*50)
    print('onnx infer results')
    print(np.argmax(pred_onx[0]))

if __name__ == "__main__":
    export()
    input = get_input()
    onnx_infer(input)
    torch_infer(input)
