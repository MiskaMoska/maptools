import os
import torch
from typing import Iterable, Tuple, Dict, List, Any
from ppq import BaseGraph, QuantizationSettingFactory, TargetPlatform
from ppq.api import dispatch_graph, export_ppq_graph, load_onnx_graph, quantize_onnx_model
from ppq.quantization.analyse.graphwise import graphwise_error_analyse
from ppq.executor.torch import TorchExecutor
from maptools.quantization.saving import save_quantization

__all__ = ["quantize"]

PLATFORM = TargetPlatform.TRT_INT8

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

def quantize(
    input_shapes: Dict[str, List[int]],
    device: str,
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
    graph = dispatch_graph(graph=graph, platform=PLATFORM)

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
        platform=PLATFORM,
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

    save_quantization(
        quantized,
        quantinfo_save_path,
        quantparam_save_path
    )

