import os
import csv
import pickle
from maptools.toksim.c_toksim cimport C_TokSim
from typing import Tuple, Dict, List, Union, Any
from maptools.core import CTG, ROOT_DIR, LogicalTile

cdef class TokSim:

    cdef C_TokSim c_toksim
    ctg: CTG
    mapname: str
    _need_bufs: Dict[bytes, Dict[bytes, int]]

    # cpp interface variables
    # Dict[bytes, Any] is for c++ map/unordered_map
    # Dict[str, Any] is for c++ struct
    _nodes: List[bytes]
    _node_attr_dict: Dict[bytes, Dict[str, Any]]
    _tile_config_dict: Dict[bytes, Dict[str, Any]]

    _token_dict: Dict[bytes, List[int]]

    def __init__(self, ctg: CTG, mapname: str = 'newmap', **kwargs) -> None:
        self.ctg = ctg
        self.mapname = mapname
        self._cpp_get_interface_vars()
        self.c_toksim = C_TokSim(
            self._nodes, 
            self._node_attr_dict,
            self._tile_config_dict
        )

    def run(self) -> None:
        self.c_toksim.run()
        self.save_execu()

    def get_bufs(self) -> List[List[Any]]:
        log, csv_data = "", []
        self._need_bufs = self.c_toksim.need_bufs
        csv_data.append(['tile','gbuf','mbuf','pbuf','ibuf','cbuf'])

        for node in self._nodes:
            if node in self._need_bufs:
                bufs: Dict[bytes, int] = self._need_bufs[node]
                keys = ['tile'] + [str(k, 'utf-8') for k in list(bufs.keys())]
                values = [str(node, 'utf-8')] + list(bufs.values())

                csv_data.append(values)
                log += '%-5s%-20s%-11s%-18s%-10s%-18s%-9s%-18s%-10s%-18s%-9s%-10s\n' % \
                    tuple(v for pair in zip(keys, values) for v in pair)

        print("\n\n"+"-"*70)
        print("TokSim Buffer Evaluation Report")
        print("-"*70)
        print(log)
        return csv_data

    def save_execu(self, file_name: str = 'token'):
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'toksim')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # save token information
        file_dir = os.path.join(save_dir, 'tokens.pkl')
        self._token_dict = {
            t: self.c_toksim.execu_dict[self.encode(t)]
            for t in self.ctg.tiles
        }
        with open(file_dir,'wb') as f:
            pickle.dump(self._token_dict, f)
        print(f"\rtoken info written to {file_dir}")

        # save buffer log
        file_dir = os.path.join(save_dir, 'buffer.csv')
        csv_data = self.get_bufs()

        with open(file_dir, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in csv_data:
                writer.writerow(row)
        print(f"\nbuffer log written to {file_dir}")

    def _cpp_get_interface_vars(self) -> None:
        self._nodes = [
            self.encode(node) 
            for node in self.ctg.node_names
        ]

        self._node_attr_dict = {
            self.encode(node): self._cpp_get_node_attr(node)
            for node in self.ctg.node_names
        }
        self._tile_config_dict = {
            self.encode(node): self._cpp_get_tile_config(node)
            for node in self.ctg.tiles
        }

    @staticmethod
    def encode(node: Union[str, LogicalTile]) -> bytes:
        return bytes(str(node), encoding='utf-8')

    def _cpp_get_node_attr(self, node: Union[str, LogicalTile]) -> Dict[str, Any]:
        attr = {
            'is_tile': self.ctg.is_tile(node),
            'is_head_tile': self.ctg.is_head_tile(node),
            'is_tail_tile': self.ctg.is_tail_tile(node),
            'is_comm': self.ctg.is_comm(node),
            'is_cast_comm': self.ctg.is_cast_comm(node),
            'is_merge_comm': self.ctg.is_merge_comm(node),
            'is_gather_comm': self.ctg.is_gather_comm(node),
            'preds': [self.encode(n) for n in self.ctg.preds(node)],
            'succs': [self.encode(n) for n in self.ctg.succs(node)]
        }
        return attr
    
    def _cpp_get_tile_config(self, node: LogicalTile) -> Dict[str, Any]:
        config = self.ctg.dicts[node]
        tile_config = {
            'has_conv': 'Conv' in config['op_type'],
            'has_pool': 'Pool' in config['op_type'],
            'has_resize': 'Rsz' in config['op_type'],
            'is_merge': config['merge_in'],
            'is_gather': config['gather_in'],
            'xbar_num_ichan': config['xbar_num_ichan'],
            'xbar_num_ochan': config['xbar_num_ochan']
        }

        conv_names = {
            'conv_input_size',
            'conv_output_size',
            'conv_kernel_size',
            'conv_strides',
            'conv_pads'
        }

        pool_names = {
            'pool_input_size',
            'pool_output_size',
            'pool_kernel_size',
            'pool_strides',
            'pool_pads'
        }

        resize_names = {
            'resize_scales'
        }

        # conv configuration
        tile_config.update({
            name: config[name]
            for name in conv_names
        })

        # pool configuration
        if 'Pool' in config['op_type']:
            tile_config.update({
                name: config[name]
                for name in pool_names
            })
        else:
            tile_config.update({
                name: []
                for name in pool_names
            })

        # resize configuration
        if 'Rsz' in config['op_type']:
            tile_config.update({
                name: config[name]
                for name in resize_names
            })
        else:
            tile_config.update({
                name: []
                for name in resize_names
            })

        return tile_config
