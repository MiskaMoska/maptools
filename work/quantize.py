from ppq import TargetPlatform
from maptools.quantization import quantize

INPUT_SHAPES     = {'input': [1, 3, 224, 224]}
DEVICE           = 'cuda'
ONNX_PATH        = 'onnx_models/simp-resnet18.onnx'

quantize(
    INPUT_SHAPES,
    DEVICE,
    ONNX_PATH,
    mapname='resnet18'
)

