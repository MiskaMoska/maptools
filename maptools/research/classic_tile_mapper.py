import math
import numpy as np
from typing import Any, Dict, Tuple, List
from maptools.core import DeviceGraph
from maptools.mapper import TileMapper
from maptools.research.classic_ctg import ClassicCTG

__all__ = ['ClassicTileMapper']

class ClassicTileMapper(TileMapper):

    def __init__(self, device_graph: DeviceGraph, w: int, h: int, **kwargs: Any) -> None:
        '''
        A classic tile mapper which adopts input-channel-wise-mapping rather than channel-decoupling-
        mapping as the `TileMapper` does. 

        Precisely, the weights are cut into K*K channel slices, where K is the size of the convolution
        kernel. The length of each slice is equal to the number of input channels, and the slices are 
        mapped on vertical dimension of the Xbar one by one.

        Note that the slices are mapped aligned to the output vectors of each tile in the preceding layers, 
        this may to some extent reduce the resource utilization efficiency, but provides convenience for 
        research and analysis.

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
            Matches each compute node in the operator graph to each layer in self.map_list.
            For example, to find the corresponding mapping information of node "n1" of the operator graph:
            >>> idx = self.match_dict['n1']
            >>> map_info = self.map_list[idx]

        self.map_list : List[Tuple[int, List[List[int]]]]
            Contains each layer's mapping information
            For example, self.map_list = [
            (2, [[0, 1, 2], [3, 0, 1], [2, 3]), 
            (4, [[0, 1], [2, 0, 1], [2]]]),
            ...]
            Where each tuple represents one layer's mapping information.
            The first element in the tuple is a interger representing the number of output slices.
            The second element in the tuple is a list, each sublist in the list represents a tile,
            each element in the sublist is the index of an input vector slice that is mapped to the current tile. 
            For example, if the sublist is [1, 2, 3], it means the current tile holds the input slices 
            that corresponds to the output slices indexed 1, 2, and 3, respectively.
            The output slices may come from different convolution layers when a concat operator appears.

        self.map_dict : Dict[Tuple[int, int, int, int], Dict[str, Any]]
            A look-up-table for each mapped tile to get the corresponding configuration information.
            The Tuple key is organized as (layer_idx, cluster_idx, block_idx, idx_in_block).
            For example, to get the configuration information of the second tile in cluster 1, 
            block 2 of the first layer, use:
            >>> key = (0, 1, 2, 1)
            >>> config_info = self.map_dict[key]
        '''
        super().__init__(device_graph, w, h, **kwargs)
        self.map_list: List[Tuple[int, List[List[int]]]] = []

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

            if 'block_boxes' not in layer_config:
                raise KeyError("cannot find 'block_boxes' when performing tile mapping")

            unit_slices = []
            for box_index, box in enumerate(layer_config['block_boxes']):
                box_len = box[1] - box[0] # the output channel numver of the preceding layer indexed as box_index
                box_slices = math.ceil(box_len / self.w) # the number of slices of the current box
                self.device_graph.dicts[layer_name]['block_nums'].append(box_slices)
                for slice in range(box_slices):
                    start_chan = box[0] + slice * self.w
                    if (slice + 1) * self.w > box_len:
                        end_chan = box[1]
                    else:
                        end_chan = start_chan + self.w
                    unit_slices.append((start_chan, end_chan))

            print('\nlayer: ', layer_index, layer_name)
            print('num_ichan: ', n_ichan)
            print('num_ochan: ', n_ochan)
            print('unit_slices: ', unit_slices)      

            clusters_split = math.ceil(n_ochan / self.w) 
            for cluster_index in range(clusters_split):
                input_info = []
                map_info.append([]) # add a new cluster

                # output vector mapping
                start_ochan_index = cluster_index * self.w
                if (cluster_index + 1) * self.w > n_ochan: end_ochan_index = n_ochan
                else: end_ochan_index = (cluster_index + 1) * self.w

                accum_chan = 0
                tile_index = 0
                icfg, tile_input_info = [], []
                for winpos_idx in range(kernel_size[0] * kernel_size[1]):
                    for unit_slice_idx, unit_slice in enumerate(unit_slices):
                        unit_slice_len = unit_slice[1] - unit_slice[0]

                        if unit_slice_len >= self.h: # error
                            raise AssertionError(f"unit_slice too long: {unit_slice_len}")
                        
                        if accum_chan + unit_slice_len > self.h: # overflow, accomplish one tile

                            tile_dict = {
                                'xbar_icfg': icfg, 
                                'xbar_ocfg': (start_ochan_index, end_ochan_index),
                                'xbar_num_ichan': None, # mixed mapping, cannot determine num_ichan 
                                'xbar_num_ochan': end_ochan_index - start_ochan_index,
                                'box_idx': None
                            }
                            tile_dict.update(layer_config)

                            is_merge_tile = (tile_index == 0)
                            self._regularize_op_type(tile_dict, is_merge_tile)

                            self.map_dict[(layer_index, cluster_index, 0, tile_index)] = tile_dict
                            input_info.append(tile_input_info)
                            tile_index += 1

                            # resetting accumulation
                            accum_chan = 0
                            icfg, tile_input_info = [], []

                        icfg.append((winpos_idx, *unit_slice))
                        tile_input_info.append(unit_slice_idx)
                        accum_chan += unit_slice_len
                
                # over, record the last tile
                tile_dict = {
                    'xbar_icfg': icfg, 
                    'xbar_ocfg': (start_ochan_index, end_ochan_index),
                    'xbar_num_ichan': None, # mixed mapping, cannot determine num_ichan 
                    'xbar_num_ochan': end_ochan_index - start_ochan_index,
                    'box_idx': None
                }
                tile_dict.update(layer_config)

                is_merge_tile = (tile_index == 0)
                self._regularize_op_type(tile_dict, is_merge_tile)

                self.map_dict[(layer_index, cluster_index, 0, tile_index)] = tile_dict
                input_info.append(tile_input_info)

            self.map_list.append((clusters_split, input_info))

    def run_map(self) -> None: 
        self._map_for_all()
        # This class is not supporting quntization
        # if self.quantize:
        #     self._build_tile_quant_config()

    @property
    def ctg(self) -> ClassicCTG:
        return ClassicCTG(
            self.device_graph,
            self.match_dict,
            self.map_list,
            self.map_dict,
            mapname = self.mapname
        )

    def print_config(self) -> None:
        '''
        Print tile configs
        '''
        print('\n'+'-'*70)
        print('\t\tLogical Mapping Results')
        print('-'*70)
        total = 0
        _match_dict = dict(zip(self.match_dict.values(), self.match_dict.keys()))
        for i, info in enumerate(self.map_list):
            sum = len(info[1]) * info[0]
            total += sum
            print('%-30s%-10s\n%-30s%-10s\n%-30s\n%-10s\n%-30s%-10s\n\n' % (
                f'Layer{i}({_match_dict[i]}):'     , i,
                '#Cluster:'                        , info[0],
                'Input_Slice:'                     , info[1],
                '#Total_Tile:'                     , sum
            ))
        print(f"\nTotal Utilization: {total} Tiles")
        self.total_tile = total