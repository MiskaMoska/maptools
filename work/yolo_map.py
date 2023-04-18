import os
import onnx
from maptools import OnnxConverter, XbarMapper
from maptools.core import ROOT_DIR
from maptools import NNModelArch

ONNXDIR = os.path.join(ROOT_DIR, 'onnx_models', 'simp-yolo.onnx')
MAPNAME = 'yolo'

model = onnx.load(ONNXDIR)
oc = OnnxConverter(model, mapname=MAPNAME, quantize=False, arch=NNModelArch.YOLO_V3)
oc.run_conversion()
oc.plot_device_graph()

xm = XbarMapper(oc.device_graph, 128, 256, arch=NNModelArch.YOLO_V3)
xm.run_map()
xm.print_config()
ctg = xm.ctg
ctg.plot_ctg()

