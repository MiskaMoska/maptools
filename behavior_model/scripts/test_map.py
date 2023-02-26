'''
Test the function of mapper
'''
import onnx
from onnx_converter import *
from xbar_mapper import XbarMapper

if __name__ == "__main__":
    model = onnx.load("../models/simp-resnet50.onnx")
    oc = OnnxConverter(model,arch='resnet')
    oc.Run_Conversion()
    og = oc.og
    xm = XbarMapper(og, 256, 256*5)
    xm._xbar_map_resnet()
    ctg = xm.ctg
    ctg.Plot_CTG()
    # xm._xbar_map_resnet()
    # xm.Print_Config()
    
