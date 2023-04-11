import torch
import pickle
import os
import sys
from typing import Iterable, Tuple, Dict, List, Any
from ppq import BaseGraph, QuantizationSettingFactory, TargetPlatform
from ppq import OperationQuantizationConfig
from ppq.api import dispatch_graph, export_ppq_graph, load_onnx_graph, quantize_onnx_model
from ppq.quantization.analyse.graphwise import graphwise_error_analyse
from ppq.executor.torch import TorchExecutor
from ppq import QuantableOperation
from ppq.quantization.qfunction import PPQuantFunction_toInt
from maptools.core.proto import QuantConfig

__all__ = ["quantize"]

def generate_calibration_dataset(
    input_shapes: Dict[str, List[int]],
    graph: BaseGraph, 
    num_of_batches: int = 32
) -> Tuple[Iterable[dict], torch.Tensor]:
    dataset = []
    for i in range(num_of_batches):
        sample = {name: torch.rand(input_shapes[name]) for name in graph.inputs}
        dataset.append(sample)
    return dataset, sample # last sample


def check_quant_outputs(op: QuantableOperation) -> bool:
    '''
    Check whether all output tensor have the same quantization config info
    '''
    output_config = op.output_quant_config
    scales = set([i.scale for i in output_config])
    return True if len(scales) == 1 else False


def save_quant(
    graph: BaseGraph,
    quantinfo_save_path: str,
    quantparam_save_path: str
) -> None:
    '''
    Save quantization information including:
    1. input and output quantization information of each convolution operation
    2. quantized weights and biased of each convolution operation
    '''
    info_dict = {}
    params_dict = {}
    for op in graph.operations.values():
        if isinstance(op, QuantableOperation) and op._type == "Conv":
            assert len(op.outputs) == 1, (
                f"operation must have only one output, but got {len(op.outputs)}")
            assert check_quant_outputs(op), (
                f"the output tensors of the operation {op.name} have different quantization info")
            input_config = op.input_quant_config[0]
            weight_config = op.input_quant_config[1]
            output_config = op.output_quant_config[0]
            assert float(input_config.offset) == 0, (
                f"the input offset must be 0, but got {float(input_config.offset)}")
            assert float(output_config.offset) == 0, (
                f"the output offset must be 0, but got {float(output_config.offset)}")

            # input and output quantization information of the current operation
            info_dict[op.name] = QuantConfig(
                name = op.name,
                input_bits = int(input_config.num_of_bits),
                input_scale = float(input_config.scale),
                output_bits = int(output_config.num_of_bits),
                output_scale = float(output_config.scale),
                weight_bits = int(weight_config.num_of_bits),
                weight_scale = weight_config.scale
            )

            arg_list = [(cv[1].value, cv[0]) for cv in op.config_with_variable[1:-1]] # strip input and output data
            assert len(arg_list) <= 2, (
                f"conv operation must have no more than 2 parameters (weight and bias), but got {len(arg_list)}")
            maps = {0: '_conv_weight', 1: '_conv_bias'}

            for i, arg in enumerate(arg_list):
                tensor_int = PPQuantFunction_toInt(*arg)
                name = op.name + maps[i]
                params_dict[name] = tensor_int.cpu().numpy()

    with open(quantinfo_save_path, 'wb') as f:
        pickle.dump(info_dict, f)
    print(f"quantization information has been written to: {quantinfo_save_path}")

    with open(quantparam_save_path, 'wb') as f:
        pickle.dump(params_dict, f)
    print(f"quantized parameters has been written to: {quantparam_save_path}")


def quantize(
    input_shapes: Dict[str, List[int]],
    device: str,
    quant_platform: TargetPlatform,
    onnx_path: str,
    mapname = 'newmap'
) -> None:
    def collate_fn(batch: dict) -> torch.Tensor:
        return {k: v.to(device) for k, v in batch.items()}
    
    # use default quantization settings
    QSetting = QuantizationSettingFactory.default_setting() 
    QSetting.lsq_optimization = False

    # load and dispatch
    graph = load_onnx_graph(onnx_import_file=onnx_path)
    graph = dispatch_graph(graph=graph, platform=quant_platform)
    for name in graph.inputs:
        if name not in input_shapes:
            raise KeyError(f'Graph input {name} needs a valid shape.')

    if len(graph.outputs) != 1:
        raise ValueError('This program requires graph to have only 1 output.')

    # generate calibration dataset
    calibration_dataset, sample = generate_calibration_dataset(input_shapes, graph)
    quantized: BaseGraph = quantize_onnx_model(
        onnx_import_file=onnx_path, 
        calib_dataloader=calibration_dataset,
        calib_steps=32, 
        input_shape=None, 
        inputs=collate_fn(sample),
        setting=QSetting, 
        collate_fn=collate_fn, 
        platform=quant_platform,
        device=device, 
        verbose=0
    )

    executor, reference_outputs = TorchExecutor(quantized), []
    for sample in calibration_dataset:
        reference_outputs.append(executor.forward(collate_fn(sample)))

    graphwise_error_analyse(
        graph=quantized, 
        running_device=device, 
        collate_fn=collate_fn, 
        dataloader=calibration_dataset
    )

    # save quantized onnx model and quantization information
    root_dir  = os.environ.get('NVCIM_HOME')
    quant_save_dir = os.path.join(root_dir, 'mapsave', mapname)

    if not os.path.exists(quant_save_dir):
        os.makedirs(quant_save_dir)
    onnx_output_path = os.path.join(quant_save_dir, 'quant_model.onnx')

    export_ppq_graph(
        graph=quantized, 
        platform=TargetPlatform.ONNXRUNTIME,
        graph_save_to=onnx_output_path
    )
    quantinfo_save_path = os.path.join(quant_save_dir, 'quantinfo.pkl')
    quantparam_save_path = os.path.join(quant_save_dir, 'quantparams.pkl')

    save_quant(
        quantized, 
        quantinfo_save_path,
        quantparam_save_path
    )

