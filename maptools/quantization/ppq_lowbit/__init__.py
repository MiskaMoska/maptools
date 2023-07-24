from .trt_lowbit_quantizer import *
from .onnxruntime_lowbit_exporter import *
from ppq.lib.extension import *
from ppq.core import TargetPlatform
from .api import *

register_network_quantizer(TrtLowBitQuantizer, TargetPlatform.TRT_INT8)
register_network_exporter(ONNXRUNTIMLowBitExporter, TargetPlatform.ONNXRUNTIME)