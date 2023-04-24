import pickle
from maptools.core import OperatorGraph, OperatorQuantConfig, QUANT_NAME_TABLE

__all__ = ['load_quant_to_graph']

def load_quant_to_graph(quantinfo_path: str, graph: OperatorGraph) -> None:
    with open(quantinfo_path, 'rb') as f:
        quantinfo = pickle.load(f)
    for node, config in quantinfo.items():
        assert isinstance(config, OperatorQuantConfig), (
            f"the items in quantinfo file should be instances of {OperatorQuantConfig}, but got {type(config)}")
        if node in graph.dicts:
            op_type = graph.op_type(node)
            if op_type in QUANT_NAME_TABLE:
                name = QUANT_NAME_TABLE[graph.op_type(node)]
                graph.add_attr_to_node(node, name + '_quant_config', config)