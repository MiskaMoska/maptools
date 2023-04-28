import onnx
import os
from maptools.core import MERGE_OPS

def format_data_dims(name: str, graph: onnx.GraphProto) -> None:
    for tensor in graph.value_info:
        if tensor.name == name:
            tensor.type.tensor_type.shape.dim[0].dim_value = 1
            # return [d.dim_value for d in dim]
            return
    graph.input[0].type.tensor_type.shape.dim[0].dim_value = 1 # not found in value_info, then it must be input
    # return [d.dim_value for d in dim]

model = onnx.load_model('onnx_models/simp-yolo.onnx')

to_format = []

for node in model.graph.node:
    if node.op_type in MERGE_OPS:
        for input in node.input:
            to_format.append(input)
    else:
        to_format.append(node.input[0])

for name in to_format:
    format_data_dims(name, model.graph)

save_path = os.path.join(os.environ.get('NVCIM_HOME'), 'onnx_models', 'my-yolo.onnx')
with open(save_path, 'wb') as f:
    onnx.save_model(model, f)