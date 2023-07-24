from typing import Any, Callable, Iterable, List, Union
import torch
from torch.utils.data import DataLoader

import ppq.lib as PFL
from ppq.api.setting import QuantizationSetting, QuantizationSettingFactory
from ppq.core import TargetPlatform, TensorQuantizationConfig, QuantizationProperty
from ppq.executor import TorchExecutor
from ppq.IR import BaseGraph
from ppq.api import load_onnx_graph, dispatch_graph
from ppq.utils.round import ppq_tensor_round
from .trt_lowbit_quantizer import TrtLowBitQuantizer


def quantize_onnx_model_lowbit(
        onnx_import_file: str,
        calib_dataloader: DataLoader,
        calib_steps: int,
        input_shape: List[int],
        platform: TargetPlatform,
        bit_width: int = 8,  # 量化位宽，不建议小于4bit
        symmetrical: bool = True,  # 对称/非对称
        per_channel: bool = True,  # per_channel/per_tensor
        input_dtype: torch.dtype = torch.float,
        inputs: List[Any] = None,
        setting: QuantizationSetting = None,
        collate_fn: Callable = None,
        device: str = 'cuda',
        verbose: int = 0,
        do_quantize: bool = True,
) -> BaseGraph:
    """量化一个 onnx 原生的模型 api, 使用定制的低比特量化器
    """
    if do_quantize:
        if calib_dataloader is None or calib_steps is None:
            raise TypeError(
                'Quantization needs a valid calib_dataloader and calib_steps setting.')

    if setting is None:
        setting = QuantizationSettingFactory.default_setting()

    ppq_ir = load_onnx_graph(onnx_import_file=onnx_import_file)
    ppq_ir = dispatch_graph(graph=ppq_ir, platform=platform,
                            dispatcher=setting.dispatcher,
                            dispatching_table=setting.dispatching_table)

    if inputs is None:
        dummy_input = torch.zeros(size=input_shape, device=device,
                                  dtype=input_dtype)
    else:
        dummy_input = inputs

    quantizer = TrtLowBitQuantizer(graph=ppq_ir, per_channel=per_channel,
                                   symmetrical=symmetrical,
                                   num_of_bits=bit_width)
    executor = TorchExecutor(graph=quantizer._graph, device=device)
    if do_quantize:
        quantizer.quantize(
            inputs=dummy_input,
            calib_dataloader=calib_dataloader,
            executor=executor,
            setting=setting,
            calib_steps=calib_steps,
            collate_fn=collate_fn
        )
        if verbose: quantizer.report()
        return quantizer._graph
    else:
        executor = TorchExecutor(graph=ppq_ir, device=device)
        executor.tracing_operation_meta(inputs=dummy_input)
        return quantizer._graph


def quantize_native_model_lowbit(
        model: BaseGraph,
        calib_dataloader: DataLoader,
        calib_steps: int,
        input_shape: List[int],
        platform: TargetPlatform,
        bit_width: int = 8,  # 量化位宽，不建议小于4bit
        symmetrical: bool = True,  # 对称/非对称
        per_channel: bool = True,  # per_channel/per_tensor
        input_dtype: torch.dtype = torch.float,
        inputs: List[Any] = None,
        setting: QuantizationSetting = None,
        collate_fn: Callable = None,
        device: str = 'cuda',
        verbose: int = 0,
        do_quantize: bool = True,
) -> BaseGraph:
    """
    量化一个 已经加载的Graph模型 , 使用定制的低比特量化器
    """
    if do_quantize:
        if calib_dataloader is None or calib_steps is None:
            raise TypeError(
                'Quantization needs a valid calib_dataloader and calib_steps setting.')

    if setting is None:
        setting = QuantizationSettingFactory.default_setting()
    ppq_ir = dispatch_graph(graph=model, platform=platform,
                            dispatcher=setting.dispatcher,
                            dispatching_table=setting.dispatching_table)

    if inputs is None:
        dummy_input = torch.zeros(size=input_shape, device=device,
                                  dtype=input_dtype)
    else:
        dummy_input = inputs

    quantizer = TrtLowBitQuantizer(graph=ppq_ir, per_channel=per_channel,
                                   symmetrical=symmetrical,
                                   num_of_bits=bit_width)
    executor = TorchExecutor(graph=quantizer._graph, device=device)

    if do_quantize:
        quantizer.quantize(
            inputs=dummy_input,
            calib_dataloader=calib_dataloader,
            executor=executor,
            setting=setting,
            calib_steps=calib_steps,
            collate_fn=collate_fn
        )
        if verbose: quantizer.report()
        return quantizer._graph
    else:
        executor = TorchExecutor(graph=ppq_ir, device=device)
        executor.tracing_operation_meta(inputs=dummy_input)
        return quantizer._graph


def PPQLinearQuant_toInt_My(tensor: torch.Tensor, config: TensorQuantizationConfig) -> torch.Tensor:
    '''
    For quantization calculation, supporting all num_of_bits
    '''
    if not config.policy.has_property(QuantizationProperty.LINEAR):
        raise ValueError('Critical Quantization Error! Non-linear config detected.')
    
    if config.policy.has_property(QuantizationProperty.PER_CHANNEL):
        shape = [1 if axis != config.channel_axis else -1 for axis in range(tensor.ndim)]
        scale, offset = config.scale.view(shape), config.offset.view(shape)
        tensor = ppq_tensor_round((tensor / scale), config.rounding) + offset
        tensor = torch.clamp(tensor, config.quant_min, config.quant_max)

    elif config.policy.has_property(QuantizationProperty.PER_TENSOR):
        tensor = ppq_tensor_round((tensor / config.scale), config.rounding) + config.offset
        tensor = torch.clamp(tensor, config.quant_min, config.quant_max)

    if config.num_of_bits <= 8:  # 源码里写死的8,就提出来自己改一下
        if config.policy.has_property(QuantizationProperty.SYMMETRICAL):
            return tensor.type(dtype=torch.int8)
        
        if config.policy.has_property(QuantizationProperty.ASYMMETRICAL):
            return tensor.type(dtype=torch.uint8)
        
    elif config.num_of_bits > 8:
        return tensor.type(dtype=torch.int32)
    
    else: raise Exception('Do not konw how to convert value into int. num of bits is unexpected.')