import math
import numpy as np
from typing import Any, Dict, List, Tuple, Generator, Optional
from maptools.core import DeviceGraph, CTG, Connection, LogicalTile
from maptools.core.utils import is_subseq

__all__ = ['ClassicCTG']

class ClassicCTG(CTG):

    def __init__(
        self, 
        device_graph: DeviceGraph, 
        match_dict: Dict[Connection, int], 
        map_list: List[Tuple[int, List[List[int]]]], 
        map_dict: Dict[LogicalTile, Dict[str, Any]], 
        **kwargs: Any
    ) -> None:
        '''
        This is a CTG re-designed for the classical mapping methods.

        The classical input-channel-wise-mapping methods raised new requirements for the strategy 
        to construct communication connections. For example, multiple cast connections can share 
        the same destination tile, where the data concatenation happens, but this will never happen 
        under our novel channel-decoupling-mapping methods.

        This CTG provides a method `self.to_full_concat()` to transform itself to full-concatenation-
        form, which is the most original and most conventional communication structure.
        '''
        self.concater_layers: Dict[Connection, List[int]] = {}
        self.comm_load: Dict[Connection, int] = {}
        super().__init__(device_graph, match_dict, map_list, map_dict, **kwargs)

    def _construct_connections(self, device_graph: DeviceGraph) -> None: 
        for e in device_graph.egdes:
            p_lid = self.match_dict[e[0]] # source node layer id
            s_lid = self.match_dict[e[1]] # dest node layer id
            p_info = self.map_list[p_lid] # source node map info matrix
            s_info = self.map_list[s_lid] # dest node map info matrix

            # add gather comms
            if device_graph.in_degree(e[1]) > 1 and (
                'Add' in device_graph.dicts[e[1]]['op_type']) and (
                not is_subseq([e[0], e[1]], device_graph.trunk)): 
                assert p_info[0] == s_info[0], (
                    "# clusters not match for gather communication")
                    
                for i in range(p_info[0]): # for each cluster in the last layer
                    src_tile = (p_lid, i, 0, 0) # source node of the gather path
                    dst_tile = (s_lid, i, 0, 0) # dst node of the gather path
                    comm_name = 'gather_from_'+str(src_tile)

                    self.graph.add_node(comm_name)
                    self.gather_comms.append(comm_name)
                    self.graph.add_edge(src_tile, comm_name)
                    self.graph.add_edge(comm_name, dst_tile)

            else: # add cast comms
                if device_graph.in_degree(e[1]) > 1 and (
                    'Add' not in device_graph.dicts[e[1]]['op_type']): # is a concat connection
                    concat_slots = device_graph.dicts[e[0]]['concat_slots']
                    concat_idx = concat_slots[e[1]]
                    block_nums = device_graph.dicts[e[1]]['block_nums']
                    base_block_idx = sum(block_nums[:concat_idx])

                    # mark the concaters (concatenation partners)
                    concaters = [self.match_dict[layer] for layer in device_graph.preds(e[1])]
                    self.concater_layers[e[1]] = concaters

                else: # is not a concat connection
                    base_block_idx = 0

                for i in range(p_info[0]):
                    src_tile = (p_lid, i, 0, 0)
                    comm_name = 'cast_from_' + str(src_tile)

                    if comm_name not in self.cast_comms:
                        self.graph.add_node(comm_name)
                        self.graph.add_edge(src_tile, comm_name)
                        self.cast_comms.append(comm_name)

                    for j, slices in enumerate(s_info[1]):
                        if base_block_idx + i in slices:
                            for k in range(s_info[0]):
                                self.graph.add_edge(comm_name, (s_lid, k, 0, j))
        
        # add merge comms
        for lid, info in enumerate(self.map_list):
            if len(info[1]) > 1: # there are more than 1 tile in the current cluster
                for i in range(info[0]): # for each cluster
                    dst_tile = (lid, i, 0, 0) # root node of the merge tree
                    comm_name = 'merge_to_'+str(dst_tile)
                    
                    self.graph.add_node(comm_name)
                    self.graph.add_edge(comm_name, dst_tile)
                    self.merge_comms.append(comm_name)
                    
                    for j in range(1, len(info[1])):
                        node = (lid, i, 0, j)
                        self.graph.add_edge(node, comm_name)

    @property
    def clusters(self) -> Generator:
        '''
        Returns all clusters in turn
        A cluster is a set of tiles that execute the same range of output channels in Conv layer
        '''
        idx = 0
        base_idx = 0
        for i, info in enumerate(self.map_list):
            for j in range(info[0]):
                base_idx += idx
                idx = 0
                cluster = []
                for k in range(len(info[1])):
                    cluster.append((i, j, 0, k))
                    idx += 1
                yield base_idx, cluster

    def to_full_concat(self) -> None:
        for layer, info in enumerate(self.map_list):
            o_slices = info[0]
            flag, root = self._get_concat_root_layer(layer)

            if flag or o_slices > 1: # is concater layer or has multiple clusters
                for i in range(o_slices):
                    tile = (layer, i, 0, 0)
                    comm = self.cast_succ_comm(tile)
                    if comm is None: # current tile has no cast successor communication
                        continue
                    
                    dsts = list(self.graph.successors(comm)) # cast destination nodes
                    load = self.get_comm_load(comm) # cast communication load
                    relay = (root if flag else layer, 0, 0, 0) # relay tile

                    if tile == relay: # avoid self-connection
                        continue

                    # remove the original cast comm
                    self.graph.remove_node(comm)
                    self.cast_comms.remove(comm)

                    # add the new concat comm
                    concat_comm = f'new_concat_from_{tile}'
                    self.graph.add_node(concat_comm)
                    self.cast_comms.append(concat_comm)
                    self.graph.add_edge(tile, concat_comm)
                    self.graph.add_edge(concat_comm, relay)
                    self.comm_load[concat_comm] = load

                    # add the new cast comms
                    cast_comm = f'new_cast_from_{tile}'
                    self.graph.add_node(cast_comm)
                    self.cast_comms.append(cast_comm)
                    self.graph.add_edge(relay, cast_comm)
                    self.comm_load[cast_comm] = load

                    for dst in dsts:
                        self.graph.add_edge(cast_comm, dst)

    def _get_concat_root_layer(self, layer: int) -> Tuple[bool, Optional[int]]:
        '''
        This method judges if a layer is a concater layer,
        if so, returns (True, concat_root_layer_id),
        if not, returns (False, None)
        '''
        if len(self.concater_layers) == 0: # no concat in the CNN model
            return (False, None)
        
        for concaters in self.concater_layers.values():
            if layer in concaters:
                return (True, concaters[0])
            
        return (False, None)

    def cast_succ_comm(self, node: LogicalTile) -> Optional[Connection]:
        for succ in self.graph.successors(node):
            if self.is_cast_comm(succ):
                return succ
            
        return None
    
    def get_comm_load(self, conn: Connection) -> int:
        if conn in self.comm_load:
            return self.comm_load[conn]
        
        return super().get_comm_load(conn)
