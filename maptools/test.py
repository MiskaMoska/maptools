'''
Test the function of mapper
'''
import onnx
from onnx_converter import *
from operator_graph import *
from xbar_mapper import *
from ctg import *
from noc_mapper import *
from inferator import *
from map_plotter import *
import torchvision as tv
import sys
import pickle
import torch
from resnet import resnet18
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

trans = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)), 
])

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

def get_input():
    '''
    获取ResNet18的输入数据，返回一个[3,224,224]的torch.Tensor
    '''
    image_file = './test.jpg'
    img = Image.open(image_file)
    img = img.resize((224,224))
    img = trans(img)
    img = torch.unsqueeze(img, 0)
    return img

if __name__ == "__main__":
    # 获得onnx原生模型
    model = onnx.load("../onnx_models/simp-resnet18.onnx")

    # 创建onnx转换器
    oc = OnnxConverter(model,arch='resnet')

    # 执行转换
    oc.run_conversion()

    # 获得转换得到的算子图
    og = oc.og
    # oc.plot_op_graph()
    # 创建xbar映射器
    xm = XbarMapper(og, 256, 256*5)

    # 执行映射
    xm.run_map()

    # 打印映射信息
    xm.print_config()

    # 获得映射得到的CTG
    ctg = xm.ctg
    for xbar, cfg in xm.xbar_config_info:
        if xbar == (0,0,0,0):
            weight = torch.tensor(cfg['conv_weight'])
            bias = torch.tensor(cfg['conv_bias'])
            print(cfg['conv_pads'])

    model = resnet18(pretrained=True)
    model.eval()
    param = model.state_dict()
    w = param['conv1.weight']
    gamma = param['bn1.weight']
    beta = param['bn1.bias']
    mu = param['bn1.running_mean']
    sigma2 = param['bn1.running_var']
    # for i in [w,gamma,beta,mu,sigma2]:
    #     print(i.shape[0])

    new_w = torch.zeros_like(w)
    new_bias = torch.zeros_like(beta)
    for i in range(w.shape[0]):
        new_w[i,:,:,:] = gamma[i]/(torch.square(sigma2[i]+1e-9))*w[i,:,:,:]
        new_bias[i] = -(gamma[i]*mu[i]/(torch.square(sigma2[i]+1e-9))) + beta[i]

    # img = get_input()
    # img = F.pad(img, [3,2,2,3])
    # output = F.conv2d(img, weight, bias, stride=2)
    # print('self conv results')
    # print(output[0][20][52:60,52:60])

    # output1 = get_res('res.pkl', 't1')
    # print('torch conv results')
    # print(output1[0][20][52:60,52:60])

    # print(new_w[0,0])


