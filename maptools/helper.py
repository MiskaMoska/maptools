import torch
import torch.nn as nn
import torch.onnx as ox
import torchvision as tv
import torch.nn.functional as F
import numpy as np
from PIL import Image
from torchvision import transforms
from resnet import resnet18
import pickle

class Rest(nn.Module):
    def __init__(self, fc_w, fc_b) -> None:
        super().__init__()
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc_w = fc_w
        self.fc_b = fc_b

    def forward(self, x):
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = x.transpose(1,0)
        x = F.linear(x, self.fc_w, self.fc_b)
        return x

trans = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)), 
])

model = resnet18(pretrained=True, save_dir='./')
model.eval()

def get_input():
    '''
    获取ResNet18的输入数据，返回一个[3,224,224]的torch.Tensor
    '''
    image_file = './test.jpg'
    img = Image.open(image_file)
    img = img.resize((224,224))
    img = trans(img)
    return img

def torch_infer():
    '''
    Pytorch推理
    返回分类索引（int），狗狗对应的是463
    '''
    image_file = 'test.jpg'
    img = Image.open(image_file)
    img = img.resize((224,224))
    img = trans(img)
    img = torch.unsqueeze(img, 0)
    output = model(img)
    return int(torch.argmax(output))

def cim_infer(x: torch.Tensor = torch.tensor(np.zeros([512,7,7], dtype=np.float32))):
    '''
    对CIM的剩余部分进行推理
    输入是从CIM仿真器上获得的结果，是一个[512,7,7]的torch.Tensor
    返回分类索引（int），狗狗对应的是463
    '''
    state_dict = model.state_dict()
    fc_w = state_dict['fc.weight']
    fc_b = state_dict['fc.bias']
    r = Rest(fc_w, fc_b)
    output = r(x)
    return int(torch.argmax(output))

def get_res(pkl_path, test_point):
    '''
    获取中间结果
    pkl_path: 中间结果文件的保存路径， 如"./res.pkl"
    test_point: 测试点，只能选['t1', 't2','t3','t4','t5','t6','t7']
    返回的是一个torch.Tensor
    '''
    with open(pkl_path, 'rb') as f_read:
        res_dict = pickle.load(f_read)
    assert test_point in ['t1', 't2','t3','t4','t5','t6','t7'], "test_point给的不对"
    return res_dict[test_point]

if __name__ == "__main__":
    torch_infer()
