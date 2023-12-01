import os
from maptools.core.proto import NNModelArch

__all__ = [
    'ROOT_DIR',
    'TRUNCATE_OPS',
    'MERGE_OPS',
    'VALID_OPS',
    'QUANT_OP_NAMES',
    'QUANT_NAME_TABLE',
    "XBAR_POWER_PER_1",
    "ADC_POWER_PER_TRANSFER"
]

# This is the root directory of MapTools
ROOT_DIR = os.environ.get('MPTLS_HOME')
if ROOT_DIR is None:
    ROOT_DIR = os.environ.get('NVCIM_HOME')
if ROOT_DIR is None:
    raise EnvironmentError("The path to maptools root directory need to be added to environment variables named MPTLS_HOME or NVCIM_HOME")

# These are the boundary operators for graph dispatching,
# where the original graph will be truncated at the boundary operators
# and then divided into host graph and device graph.
TRUNCATE_OPS = {
    NNModelArch.VGG: {
        'MaxPool'
    },

    NNModelArch.RESNET: {
        'Conv', 
        'Relu', 'PRelu', 'HardSigmoid',
        'MaxPool', 'AveragePool'
    },

    NNModelArch.YOLO_V3 : {
        'Conv', 
        'Relu', 'PRelu', 'HardSigmoid',
        'MaxPool', 'AveragePool'
    },

    NNModelArch.SQUEEZENET : {
        'Conv', 
        'Relu', 'PRelu', 'HardSigmoid',
        'MaxPool', 'AveragePool'
    }
}


# These are the operators that merges data from several branches to
# one operator, this constant helps to construct raw operator graph
MERGE_OPS = {
    'Mul','Add','Concat'
}


# Here list all valid operators that are supported by this tool,
# including valid device operators and valid host operators
VALID_OPS = {
    'Conv', 'Gemm',
    'Mul', 'Concat', 'Add',
    'Relu', 'PRelu', 'HardSigmoid', 'Softmax', 'LeakyRelu',
    'MaxPool', 'AveragePool', 'GlobalAveragePool',
    'Flatten', 'Reshape', 'Resize', 'Transpose'
}


QUANT_OP_NAMES = {
    'conv', 'sum', 'act','pool'
}


QUANT_NAME_TABLE = {
    'Conv'          : 'conv',
    'Relu'          : 'act',
    'LeakyRelu'     : 'act',
    'PRelu'         : 'act',
    'HardSigmoid'   : 'act',
    'Add'           : 'sum',
    'MaxPool'       : 'pool',
    'AveragePool'   : 'pool'
}

# for power analysis, unit: J
XBAR_POWER_PER_1 = 0.125 * 1e-15
ADC_POWER_PER_TRANSFER = 17.5 * 1e-12