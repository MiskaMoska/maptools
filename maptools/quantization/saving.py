import torch
import pickle
from ppq import BaseGraph
from ppq import QuantableOperation, TensorQuantizationConfig
from ppq.quantization.qfunction import PPQuantFunction_toInt
from maptools.core.proto import QuantConfig

__all__ = ['save_quantization']

ACTIVE_OPTYPE = {
    'Conv',
    'Add',
    'Relu'
}

def quant_operation_assertion(op: QuantableOperation) -> bool:
    '''
    Perform this function before saving quantization information
    '''
    assert len(op.outputs) == 1, (
        f"operation must have only one output, but got {len(op.outputs)}")
    scales = set([i.scale for i in op.output_quant_config])
    assert len(scales) == 1, (
        f"the output tensors of the operation {op.name} have different quantization info")
    if op._type == "Add":
        scales = set([i.scale for i in op.input_quant_config])
        assert len(scales) == 1, (
            f"the input tensors of the Add operation {op.name} have different quantization info")
    input_config = op.input_quant_config[0]
    output_config = op.output_quant_config[0]
    assert float(input_config.offset) == 0, (
        f"the input offset must be 0, but got {float(input_config.offset)}")
    assert float(output_config.offset) == 0, (
        f"the output offset must be 0, but got {float(output_config.offset)}")


def get_quantized_conv_weight(
    tensor: torch.Tensor, 
    config: TensorQuantizationConfig
) -> torch.Tensor:
    '''
    Get quantized convolution weight tensor according to its quantization configuration
    For TRT_INT8 platform, the quantization configuration information is generated to in `config` 
    while performing quantization.
    '''
    return PPQuantFunction_toInt(tensor, config)


def get_quantized_conv_bias(
    tensor: torch.Tensor, 
    config: TensorQuantizationConfig,
    input_config: TensorQuantizationConfig,
    weight_config: TensorQuantizationConfig
) -> torch.Tensor:
    '''
    Get quantized convolution bias tensor according to its quantization configuration
    For TRT_INT8 platform, `config` is an empty object, and the quantization configuration information
    should be calculated according to `input_config` and `weight_config`.
    '''
    config.num_of_bits = 32 # preventing overflow
    config.quant_max = pow(2, 31) - 1 # preventing overflow
    config.quant_min = -pow(2, 31) # preventing overflow
    config.scale = weight_config.scale * input_config.scale
    config.offset = 0
    return PPQuantFunction_toInt(tensor, config)


def save_quantization(
    graph: BaseGraph,
    quantinfo_save_path: str,
    quantparam_save_path: str
) -> None:
    '''
    Save quantization configuration and quantized parameters

    Parameters
    ----------
    graph : BaseGraph
        graph generated from quantizer
    '''
    config_dict = {}
    params_dict = {}
    for op in graph.operations.values():
        quant_operation_assertion(op)
        if isinstance(op, QuantableOperation) and op._type in ACTIVE_OPTYPE:
            config_kwargs = {} # kwargs to initialize QuantConfig object
            config_kwargs['name'] = op.name
            input_config = op.input_quant_config[0]
            output_config = op.output_quant_config[0]

            config_kwargs['input_bits'] = int(input_config.num_of_bits)
            config_kwargs['input_scale'] = float(input_config.scale)
            config_kwargs['output_bits'] = int(output_config.num_of_bits)
            config_kwargs['output_scale'] = float(output_config.scale)

            if op._type == 'Conv':
                weight_config = op.input_quant_config[1]
                config_kwargs['weight_bits'] = int(weight_config.num_of_bits)
                config_kwargs['weight_scale'] = weight_config.scale.cpu()
                weight_tensor = get_quantized_conv_weight(
                    op.inputs[1].value,
                    weight_config
                )
                params_dict[op.name + '_conv_weight'] = weight_tensor.cpu().numpy()

                if len(op.inputs) > 2: # has bias
                    bias_tensor = get_quantized_conv_bias(
                        op.inputs[-1].value,
                        op.input_quant_config[-1],
                        input_config,
                        weight_config
                    )
                    params_dict[op.name + '_conv_bias'] = bias_tensor.cpu().numpy()

                    # print("bias tensor dtype:", bias_tensor.dtype)
                    # print("max:", torch.max(bias_tensor))
            
            elif op._type == 'Add': ...
            elif op._type == 'Relu': ...
            elif op._type in {'MaxPool', 'AveragePool'}: ...
            else:
                assert True, f"op_type {op._type} not supported yet"

            config_dict[op.name] = QuantConfig(**config_kwargs)

    with open(quantinfo_save_path, 'wb') as f:
        pickle.dump(config_dict, f)
    print(f"quantization information has been written to: {quantinfo_save_path}")

    with open(quantparam_save_path, 'wb') as f:
        pickle.dump(params_dict, f)
    print(f"quantized parameters has been written to: {quantparam_save_path}")
