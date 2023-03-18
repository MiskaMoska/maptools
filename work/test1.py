import pickle
from typing import Generator
file = './test1.pkl'
d = dict()

d[(3, 8)] = {'xbar_icfg': [(0, 0, 256), (1, 0, 256), (2, 0, 256), (3, 0, 256), (4, 0, 256)], 'xbar_ocfg': (0, 256), 'xbar_num_ichan': 256, 'xbar_num_ochan': 256, 'name': 'Conv_43_o', 'op_type': 'Conv-Add-Act-Bias', 'conv_input_size': [7, 7], 'conv_output_size': [7, 7], 'conv_dilations': [1, 1], 'conv_group': 1, 'conv_kernel_size': [3, 3], 'conv_pads': [1, 1, 1, 1], 'conv_strides': [1, 1], 'conv_weight': 'Conv_43_conv_weight', 'conv_bias': 'Conv_43_conv_bias', 'conv_num_ichan': 512, 'conv_num_ochan': 512, 'act_mode': 'Relu'}
d[(1, 8)] = {'xbar_icfg': [(5, 0, 256), (6, 0, 256), (7, 0, 256), (8, 0, 256)], 'xbar_ocfg': (0, 256), 'xbar_num_ichan': 256, 'xbar_num_ochan': 256, 'name': 'Conv_43_o', 'op_type': 'Conv', 'conv_input_size': [7, 7], 'conv_output_size': [7, 7], 'conv_dilations': [1, 1], 'conv_group': 1, 'conv_kernel_size': [3, 3], 'conv_pads': [1, 1, 1, 1], 'conv_strides': [1, 1], 'conv_weight': 'Conv_43_conv_weight', 'conv_bias': 'Conv_43_conv_bias', 'conv_num_ichan': 512, 'conv_num_ochan': 512, 'act_mode': 'Relu'}

with open(file, 'wb') as f:
    pickle.dump(d, f)