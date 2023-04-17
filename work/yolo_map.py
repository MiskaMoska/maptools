import os
import onnx
from maptools import OnnxConverter
from maptools.core import ROOT_DIR
from maptools import NNModelArch

ONNXDIR = os.path.join(ROOT_DIR, 'onnx_models', 'simp-yolo.onnx')
MAPNAME = 'yolo'

model = onnx.load(ONNXDIR)
oc = OnnxConverter(model, mapname=MAPNAME, quantize=False, arch=NNModelArch.YOLO_V3)
oc.run_conversion()
oc.plot_device_graph()
