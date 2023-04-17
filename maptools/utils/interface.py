import pickle
from maptools.core import OperatorGraph, QuantConfig

__all__ = ['load_quant_to_graph']

def load_quant_to_graph(quantinfo_path: str, graph: OperatorGraph) -> None:

    QUANT_NAME_TABLE = {
        'Conv'          :'conv',
        'Relu'          :'relu',
        'Add'           :'add',
        'MaxPool'       :'pool',
        'AveragePool'   :'pool'
    }

    with open(quantinfo_path, 'rb') as f:
        quantinfo = pickle.load(f)
    for node, config in quantinfo.items():
        assert isinstance(config, QuantConfig), (
            f"the items in quantinfo file should be instances of {QuantConfig}, but got {type(config)}")
        if node in graph.dicts:
            name = QUANT_NAME_TABLE[graph.op_type(node)]
            graph.add_attr_to_node(node, name + '_quant_config', config)