from ppq import TargetPlatform
from maptools.quantization import quantize

INPUT_SHAPES     = {'input': [1, 3, 224, 224]}
DEVICE           = 'cpu'
QUANT_PLATFORM   = TargetPlatform.PPL_CUDA_INT8
ONNX_PATH        = 'onnx_models/simp-resnet18.onnx'

quantize(
    INPUT_SHAPES,
    DEVICE,
    QUANT_PLATFORM,
    ONNX_PATH,
    mapname='resnet18'
)

