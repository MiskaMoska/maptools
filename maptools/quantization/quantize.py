import os
import torch
from typing import Iterable, Tuple, Dict, List, Any, Optional

from .ppq_lowbit import *
from ppq import BaseGraph, QuantizationSettingFactory, TargetPlatform
from ppq.api import dispatch_graph, export_ppq_graph, load_onnx_graph, quantize_onnx_model
from ppq.quantization.analyse.graphwise import graphwise_error_analyse
from ppq.executor.torch import TorchExecutor

from maptools.quantization.saving import save_quantization
from maptools.core import ROOT_DIR

__all__ = ["quantize"]

PLATFORM = TargetPlatform.TRT_INT8

def generate_calibration_dataset(
    input_shapes: Dict[str, List[int]],
    graph: BaseGraph, 
    num_of_batches: int = 32
) -> Iterable[Dict[str, torch.Tensor]]:
    dataset = []
    for i in range(num_of_batches):
        sample = {name: torch.rand(input_shapes[name]) for name in graph.inputs}
        dataset.append(sample)
    return dataset

def quantize(
    input_shapes: Dict[str, List[int]],
    device: str,
    onnx_path: str,
    bit_width: int = 8,
    per_channel: bool = True,
    mapname = 'newmap',
    calibset: Optional[Iterable[Dict[str, torch.Tensor]]] = None,
    calib_steps: int = 32
) -> None:
    def collate_fn(batch: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        return {k: v.to(device) for k, v in batch.items()}
    
    # use default quantization settings
    QSetting = QuantizationSettingFactory.trt_setting() 
    QSetting.lsq_optimization = False

    # load and dispatch
    graph = load_onnx_graph(onnx_import_file=onnx_path)

    for name in graph.inputs:
        if name not in input_shapes:
            raise KeyError(f'Graph input {name} needs a valid shape.')
    
    if len(graph.inputs) != 1:
        raise ValueError('This program requires graph to have only 1 input.')

    if len(graph.outputs) != 1:
        raise ValueError('This program requires graph to have only 1 output.')

    # get calibration dataset
    if calibset is None:
        print("Calibration dataset not specified, using random calibration dataset")
        calibset = generate_calibration_dataset(input_shapes, graph)
    else:
        print("Using user defined calibration dataset")

    # get input data, must be a dictionary
    inputs = {name: torch.rand(input_shapes[name]) for name in graph.inputs}

    # perform quantization
    quantized: BaseGraph = quantize_onnx_model_lowbit(
        onnx_import_file=onnx_path,
        bit_width=bit_width,
        symmetrical=True,
        per_channel=per_channel,
        calib_dataloader=calibset,
        calib_steps=calib_steps, 
        input_shape=None, 
        inputs=collate_fn(inputs),
        setting=QSetting, 
        collate_fn=collate_fn, 
        platform=PLATFORM,
        device=device,
        verbose=0
    )

    graphwise_error_analyse(
        graph=quantized, 
        running_device=device, 
        collate_fn=collate_fn, 
        dataloader=calibset
    )

    # save quantized onnx model and quantization information
    quant_save_dir = os.path.join(ROOT_DIR, 'mapsave', mapname)

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

    save_quantization(
        quantized,
        quantinfo_save_path,
        quantparam_save_path
    )

