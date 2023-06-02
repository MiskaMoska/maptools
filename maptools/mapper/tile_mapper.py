import math
import numpy as np
from typing import List, Dict, Tuple, Any
from maptools.core import (
    DeviceGraph, CTG, TileQuantConfig, OperatorQuantConfig,
    QUANT_OP_NAMES
)
from maptools.utils import destruct_scale

__all__ = ['TileMapper']

class TileMapper(object):

    def __init__(
        self, 
        device_graph: DeviceGraph, 
        w: int, 
        h: int, 
        **kwargs: Any
    ) -> None:
        '''
        Parameters
        ----------
        device_graph : DeviceGraph
            `OnnxConverter.device_graph`

        w : int
            Xbar width
        
        h : int
            Xbar height

        Key Members
        -----------
        self.match_dict : Dict[str, int]
            Matches each compute node in the operator graph to each layer in self.map_list
            For example, to find the corresponding mapping information of node "n1" of the 
            operator graph, use:
            >>> idx = self.match_dict['n1']
            >>> map_info = self.map_list[idx]

        self.map_list : List[np.ndarray]
            Contains each layer's mapping information
            For example, self.map_list = [
            np.array([[1, 2, 3], [1, 2, 3]]),
            np.array([[2, 2], [2, 2], [2, 2]]),
            ...]
            Where each numpy array represent one layer's mapping information.
            Each element in the numpy array represents a block in current layer mapped tiles.
            The value of each element in the numpy array is the number of tiles the block contains.

        self.map_dict : Dict[Tuple[int, int, int, int], Dict[str, Any]]
            A look-up-table for each mapped tile to get the corresponding configuration information.
            The Tuple key is organized as (layer_idx, cluster_idx, block_idx, idx_in_block).
            For example, to get the configuration information of the second tile in cluster 1, 
            block 2 of the first layer, use:
            >>> key = (0, 1, 2, 1)
            >>> config_info = self.map_dict[key]
        '''
        assert w <= h, "Xbar height must be no smaller than width"
        self.device_graph = device_graph
        self.w = w
        self.h = h
        self.mapname = 'newmap'
        self.quantize = False
        self.__dict__.update(kwargs)
        self.match_dict: Dict[str, int] = dict() 
        self.map_list: List[np.ndarray] = []
        self.map_dict: Dict[Tuple[int, int, int, int], Dict[str, Any]] = dict() 

    def _assert_first_layer(self, in_len: int, out_len: int) -> None:
        '''
        The first layer of the device graph must hold the weights whose size
        is no larger than the volume of one xbar, so assertion is needed
        '''
        if in_len > self.h:
            raise ValueError(
                f"first layer input vector overflow, xbar height {self.h} but got vector length {in_len}")
        if out_len > self.w:
            raise ValueError(
                f"first layer output vector overflow, xbar width {self.w} but got vector length {out_len}")

    def _map_for_all(self) -> None:
        for layer_index, layer_config in enumerate(self.device_graph.node_configs):
            map_info = []
            layer_name = layer_config['name']
            self.match_dict[layer_name] = layer_index
            
            if 'Conv' not in layer_config['op_type']:
                raise AssertionError(f"all operator in device graph must have 'Conv', but got {layer_config['op_type']}")
            
            n_ichan = layer_config['conv_num_ichan']
            n_ochan = layer_config['conv_num_ochan']
            kernel_size = layer_config['conv_kernel_size']

            if layer_index == 0:
                self._assert_first_layer(n_ichan * kernel_size[0] * kernel_size[1], n_ochan)

            clusters_split = math.ceil(n_ochan / self.w) 
            for cluster_index in range(clusters_split):
                map_info.append([]) # add a new cluster

                # output vector mapping
                start_ochan_index = cluster_index * self.w
                if (cluster_index + 1) * self.w > n_ochan: end_ochan_index = n_ochan
                else: end_ochan_index = (cluster_index + 1) * self.w
                
                if 'block_boxes' not in layer_config:
                    raise KeyError("cannot find 'block_boxes' when tile mapping")
                
                # `block base index` is the base block index for each box
                block_base_index = 0

                for box_index, box in enumerate(layer_config['block_boxes']):
                    # `box_vector_len` is the number of input channels within the current box
                    box_vector_len = box[1] - box[0]

                    # input vector mapping
                    box_blocks_split = math.ceil(box_vector_len / self.w) # how many slices a box vector is divided to
                    self.device_graph.dicts[layer_name]['block_nums'].append(box_blocks_split)

                    # get slice length, each slice is shorter than Xbar width
                    # `box_lock_index` is the block index within the current box
                    for box_block_index in range(box_blocks_split):
                        map_info[cluster_index].append(0) # add a new block

                        # `block_index` is the real index of blocks, spanning multiple boxes
                        block_index = block_base_index + box_block_index

                        # slice_len is the length of the slice in currernt block with index `box_block_index`
                        if (box_block_index + 1) * self.w > box_vector_len:
                            slice_len = box_vector_len % self.w
                        else: slice_len = self.w

                        start_ichan_index = box[0] + box_block_index * self.w # box[0] is the base # ichannel
                        end_ichan_index = start_ichan_index + slice_len

                        slices_per_tile = self.h // slice_len # max slices per tile
                        tiles_per_block = math.ceil((kernel_size[0] * kernel_size[1]) / slices_per_tile)
                    
                        for tile_index in range(tiles_per_block):
                            icfg = []
                            if (tile_index + 1) * slices_per_tile > kernel_size[0] * kernel_size[1]:
                                slices_now_tile = kernel_size[0] * kernel_size[1] % slices_per_tile
                            else: slices_now_tile = slices_per_tile
                            
                            for k in range(slices_now_tile):
                                winpos_idx = tile_index * slices_per_tile + k
                                icfg.append((winpos_idx, start_ichan_index, end_ichan_index))
                                
                            tile_dict = {
                                'xbar_icfg': icfg, 
                                'xbar_ocfg': (start_ochan_index, end_ochan_index),
                                'xbar_num_ichan': end_ichan_index - start_ichan_index, 
                                'xbar_num_ochan': end_ochan_index - start_ochan_index,
                                'box_idx': box_index
                            }
                            tile_dict.update(layer_config)

                            is_merge_tile = (block_index == 0 and tile_index == 0)
                            self._regularize_op_type(tile_dict, is_merge_tile)

                            self.map_dict[(layer_index, cluster_index, block_index, tile_index)] = tile_dict
                            map_info[cluster_index][block_index] += 1

                    # for each box, the `block_base_index` accumulate
                    block_base_index += box_blocks_split

            self.map_list.append(np.array(map_info))

    def _regularize_op_type(self, tile_dict: Dict, is_merge_tile: bool) -> None:
        '''
        This method regularizes tile op_type
        cause only merge tile can have [add, act, pool, bias, resize]
        '''
        if is_merge_tile:
            tile_dict['op_type'] += '-Bias'
            return
        for ops in {'Pool', 'Act', 'Add', 'Rsz'}:
            tile_dict['op_type'] = tile_dict['op_type'].replace('-'+ops, '')

    def _build_tile_quant_config(self) -> None:
        '''
        This method builds tile quant config (TQC) objects for all tiles
        according to the operator quant config (OQC) objects in the tile config,
        and the removes all OQCs from all tiles.
        Always call this method after calling `self._map_for_all`
        '''
        for config in self.map_dict.values():
            tqc_kwargs = {}
            tqc_kwargs['op_type'] = config['op_type']
            conv_qc: OperatorQuantConfig = config['conv_quant_config']
            tqc_kwargs['ci_scale'] = conv_qc.input_scale
            tqc_kwargs['co_scale'] = conv_qc.output_scale
            tqc_kwargs['i_scale'] = conv_qc.input_scale
            tqc_kwargs['o_scale'] = conv_qc.output_scale

            ocfg = config['xbar_ocfg']
            weight_scale = conv_qc.weight_scale[ocfg[0]:ocfg[1]]
            tqc_kwargs['ctrans'] = weight_scale * conv_qc.input_scale / conv_qc.output_scale
            tqc_kwargs['ctrans_i'], tqc_kwargs['ctrans_s'] = destruct_scale(tqc_kwargs['ctrans'])

            if 'Add' in config['op_type']:
                sum_qc: OperatorQuantConfig = config['sum_quant_config']
                tqc_kwargs['si_scale'] = sum_qc.input_scale
                tqc_kwargs['so_scale'] = sum_qc.output_scale
                tqc_kwargs['o_scale'] = sum_qc.output_scale

                tqc_kwargs['strans'] = sum_qc.input_scale / sum_qc.output_scale
                tqc_kwargs['strans_i'], tqc_kwargs['strans_s'] = destruct_scale(tqc_kwargs['strans'])

            if 'Act' in config['op_type']:
                act_qc: OperatorQuantConfig = config['act_quant_config']
                tqc_kwargs['ai_scale'] = act_qc.input_scale
                tqc_kwargs['ao_scale'] = act_qc.output_scale
                tqc_kwargs['o_scale'] = act_qc.output_scale

                tqc_kwargs['atrans'] = act_qc.input_scale / act_qc.output_scale
                tqc_kwargs['atrans_i'], tqc_kwargs['atrans_s'] = destruct_scale(tqc_kwargs['atrans'])
            
            config['tqc'] = TileQuantConfig(**tqc_kwargs)
            
            for name in QUANT_OP_NAMES:
                key = name + '_quant_config'
                if key in config: config.pop(key)

    def run_map(self) -> None: 
        self._map_for_all()
        if self.quantize:
            self._build_tile_quant_config()

    @property
    def ctg(self) -> CTG:
        return CTG(
            self.device_graph,
            self.match_dict,
            self.map_list,
            self.map_dict,
            mapname = self.mapname
        )

    @property
    def tile_config(self) -> Dict:
        '''
        A dictionary with logical tile as keys and configuration info as values.
        '''
        return self.map_dict

    def print_config(self) -> None:
        '''
        Print tile configs
        '''
        print('\n'+'-'*70)
        print('\t\tTile Mapping Results')
        print('-'*70)
        total = 0
        _match_dict = dict(zip(self.match_dict.values(), self.match_dict.keys()))
        for i, mtx in enumerate(self.map_list):
            sum = np.sum(mtx)
            total += sum
            print(f"layer{i}({_match_dict[i]}): #cluster-{mtx.shape[0]}, #block-{mtx.shape[1]}, #tile-{sum}")
        print(f"\ntotal #tile-{total}")
        self.total_tile = total

