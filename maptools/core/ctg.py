import os
import numpy as np
import networkx as nx
from graphviz import Digraph
from functools import cached_property
from typing import (
    List, Dict, Tuple, Any, 
    Generator, Optional, Literal
)
from maptools.core.graph import DeviceGraph
from maptools.core.utils import is_subseq
from maptools.core.typing import TileConfig, LogicalTile, Connection
from maptools.core.common import ROOT_DIR

__all__ = ['CTG']

class CTG(object):

    def __init__(
        self, 
        device_graph: DeviceGraph, 
        match_dict: Dict[str, int],
        map_list: List[np.ndarray],
        map_dict: Dict[Tuple[int, int, int, int], Dict[str, Any]],
        **kwargs: Any
    ) -> None:
        '''
        Communication Trace Graph
        TODO support first layer cast comm

        Parameters
        ----------
        device_graph : DeviceGraph
            Device operator graph generated from `OnnxConverter`

        match_dict : Dict[str, int]
            Matches each compute node in the operator graph to each layer in self.map_list
            For example, to find the corresponding mapping information of node "n1" of the 
            operator graph, use:
            >>> idx = self.match_dict['n1']
            >>> map_info = self.map_list[idx]

        map_list : List[np.ndarray]
            Contains each layer's mapping information
            For example, self.map_list = [
            np.array([[1, 2, 3], [1, 2, 3]]),
            np.array([[2, 2], [2, 2], [2, 2]]),
            ...]
            Where each numpy array represent one layer's mapping information.
            Each element in the numpy array represents a block in current layer mapped tiles.
            The value of each element in the numpy array is the number of tiles the block contains.

        map_dict : Dict[Tuple[int, int, int, int], Dict[str, Any]]
            A look-up-table for each mapped tile to get the corresponding configuration information.
            The Tuple key is organized as (layer_idx, cluster_idx, block_idx, idx_in_block).
            For example, to get the configuration information of the second tile in cluster 1, 
            block 2 of the first layer, use:
            >>> key = (0, 1, 2, 1)
            >>> config_info = self.map_dict[key]

        kwargs : Dict
            mapname : str = 'newmap'
                Map name
        '''
        self.match_dict = match_dict
        self.map_list = map_list
        self.dicts = map_dict

        self.mapname = 'newmap'
        self.quantize = device_graph.quantize
        self.__dict__.update(kwargs)

        # number of output layers
        self.output_num = device_graph.output_num 

        # graph nodes
        self.tile_nodes: List[Tuple[int, int, int, int]] = []
        self.cast_comms: List[str] = []
        self.merge_comms: List[str] = []
        self.gather_comms: List[str] = []

        # build ctg
        self._build_ctg(device_graph)
        self._complete_connection_attrs()
        self._channel_match_check()

    @cached_property
    def node_names(self) -> List[Any]:
        return list(nx.topological_sort(self.graph))
    
    @cached_property
    def tiles(self) -> List[Tuple]:
        return [n for n in self.node_names if self.is_tile(n)]
    
    @cached_property
    def head_tile(self) -> LogicalTile:
        for tile in self.tile_nodes:
            if self.is_head_tile(tile):
                return tile
        raise RuntimeError("cannot find head tile in CTG")

    @cached_property
    def tail_tiles(self) -> List[LogicalTile]:
        tails = [] 
        for tile in self.tile_nodes:
            if self.is_tail_tile(tile):
                tails.append(tile)
        tails.sort(key=lambda tup:tup[1])
        return tails

    @property
    def comms(self) -> List[str]:
        return self.cast_comms + self.merge_comms + self.gather_comms

    def is_cast_comm(self, node: Any) -> bool:
        return node in self.cast_comms

    def is_merge_comm(self, node: Any) -> bool:
        return node in self.merge_comms
    
    def is_gather_comm(self, node: Any) -> bool:
        return node in self.gather_comms
    
    def is_comm(self, node: Any) -> bool:
        return node in self.comms

    def is_tile(self, node: Any) -> bool:
        return node in self.tile_nodes
    
    def preds(self, node: Any) -> Generator:
        yield from self.graph.predecessors(node)

    def succs(self, node: Any) -> Generator:
        yield from self.graph.successors(node)

    def get_tile_config(self, node: Any) -> TileConfig:
        assert self.is_tile(node), "not a tile node, cannot get config"
        return self.dicts[node]

    def is_head_tile(self, node: Any) -> bool:
        return self.graph.in_degree(node) == 0
    
    def is_tail_tile(self, node: Any) -> bool:
        return self.graph.out_degree(node) == 0
    
    def has_cast_in(self, node: Tuple) -> bool:
        return self.dicts[node]['cast_in']
    
    def has_merge_in(self, node: Tuple) -> bool:
        return self.dicts[node]['merge_in']
    
    def has_gather_in(self, node: Tuple) -> bool:
        return self.dicts[node]['gather_in']
    
    def has_cast_out(self, node: Tuple) -> bool:
        return self.dicts[node]['cast_out']
    
    def has_merge_out(self, node: Tuple) -> bool:
        return self.dicts[node]['merge_out']
    
    def has_gather_out(self, node: Tuple) -> bool:
        return self.dicts[node]['gather_out']
    
    def cast_pred_comm(self, node: Tuple) -> str:
        return self.dicts[node]['cast_pred_comm']

    def merge_pred_comm(self, node: Tuple) -> str:
        return self.dicts[node]['merge_pred_comm']

    def gather_pred_comm(self, node: Tuple) -> str:
        return self.dicts[node]['gather_pred_comm']

    def cast_succ_comm(self, node: Tuple) -> str:
        return self.dicts[node]['cast_succ_comm']

    def merge_succ_comm(self, node: Tuple) -> str:
        return self.dicts[node]['merge_succ_comm']

    def gather_succ_comm(self, node: Tuple) -> str:
        return self.dicts[node]['gather_succ_comm']
    
    def get_attr(self, node: Any, attr: str) -> Any:
        if node in self.dicts:
            if attr in self.dicts[node]:
                return self.dicts[node][attr]
        return None

    @cached_property
    def tile_num(self) -> int:
        return len(self.tile_nodes)

    @cached_property
    def cast_num(self) -> int:
        return len(self.cast_comms)

    @cached_property
    def merge_num(self) -> int:
        return len(self.merge_comms)

    @cached_property
    def gather_num(self) -> int:
        return len(self.gather_comms)

    def update_dict(self, key: Any, value: Dict) -> None:
        '''
        This method updates {key : value} to `self.dicts`,
        if key in `self.dicts`, merge value to `self.dicts[key]`,
        if key not in `self.dicts`, create the key and set `self.dicts[key] = value`
        '''
        if key in self.dicts:
            self.dicts[key].update(value)
        else:
            self.dicts[key] = value

    @property
    def clusters(self) -> Generator:
        '''
        Returns all clusters in turn
        A cluster is a set of tiles that execute the same range of output channels in Conv layer
        '''
        idx = 0
        base_idx = 0
        for i, mtx in enumerate(self.map_list):
            for j in range(mtx.shape[0]):
                base_idx += idx
                idx = 0
                cluster = []
                for k in range(mtx.shape[1]):
                    for t in range(mtx[j, k]):
                        cluster.append((i, j, k, t))
                        idx += 1
                yield base_idx, cluster

    def _build_ctg(self, device_graph: DeviceGraph) -> None:
        self.graph = nx.MultiDiGraph()
        self.tile_nodes = list(self.dicts.keys())
        self.graph.add_nodes_from(self.tile_nodes)
        self._construct_connections(device_graph)

    def _construct_connections(self, device_graph: DeviceGraph) -> None: 
        for e in device_graph.egdes: 
            p_lid = self.match_dict[e[0]] # source node layer id
            s_lid = self.match_dict[e[1]] # dest node layer id
            p_mtx = self.map_list[p_lid] # source node map info matrix
            s_mtx = self.map_list[s_lid] # dest node map info matrix

            # add gather comms
            if device_graph.in_degree(e[1]) > 1 and device_graph.is_add_edge(e):
                assert p_mtx.shape[0] == s_mtx.shape[0], (
                    "#clusters not match for gather communication")
                    
                for i in range(p_mtx.shape[0]): # for each cluster in the last layer
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

                else: # is not a concat connection
                    assert p_mtx.shape[0] == s_mtx.shape[1], (
                        "#clusters in last layer does not match #blocks in this layer")
                    base_block_idx = 0

                for i in range(p_mtx.shape[0]):
                    src_tile = (p_lid, i, 0, 0)
                    comm_name = 'cast_from_' + str(src_tile)

                    if comm_name not in self.cast_comms:
                        self.graph.add_node(comm_name)
                        self.graph.add_edge(src_tile, comm_name)
                        self.cast_comms.append(comm_name)

                    for j in range(s_mtx.shape[0]):
                        for k in range(s_mtx[j, i]):
                            self.graph.add_edge(comm_name, (s_lid, j, base_block_idx+i, k))
        
        # add merge comms
        for lid, mtx in enumerate(self.map_list):
            for i in range(mtx.shape[0]): # for each cluster in the current layer
                if np.sum(mtx[i]) > 1: # there are more than 1 tile in the current cluster
                    dst_tile = (lid, i, 0, 0) # root node of the merge tree
                    comm_name = 'merge_to_'+str(dst_tile)
                    
                    self.graph.add_node(comm_name)
                    self.graph.add_edge(comm_name, dst_tile)
                    self.merge_comms.append(comm_name)
                    
                    for j in range(mtx.shape[1]):
                        for k in range(mtx[i, j]):
                            node = (lid, i, j, k)
                            if node != dst_tile:
                                self.graph.add_edge(node, comm_name)

    def _complete_connection_attrs(self) -> None:
        '''
        This method completes connection attributes.
        This step is performed after building CTG rather than in-time with 
        building CTG to achieve procedure decoupling and safety.
        '''
        for tile in self.tile_nodes:
            is_head, is_tail = False, False

            cast_in, merge_in, gather_in = False, False, False
            cast_pred_comm, merge_pred_comm, gather_pred_comm = None, None, None

            cast_out, merge_out, gather_out = False, False, False
            cast_succ_comm, merge_succ_comm, gather_succ_comm = None, None, None

            for pred in self.graph.predecessors(tile):
                if pred in self.cast_comms:
                    cast_in, cast_pred_comm = True, pred
                if pred in self.merge_comms:
                    merge_in, merge_pred_comm = True, pred
                if pred in self.gather_comms:
                    gather_in, gather_pred_comm = True, pred

            for succ in self.graph.successors(tile):
                if succ in self.cast_comms:
                    cast_out, cast_succ_comm = True, succ
                if succ in self.merge_comms:
                    merge_out, merge_succ_comm = True, succ
                if succ in self.gather_comms:
                    gather_out, gather_succ_comm = True, succ

            if self.is_head_tile(tile):
                is_head = True
                cast_in = True # head tile receives cast in but has no cast predecessors

            if self.is_tail_tile(tile):
                is_tail = True
                cast_out = True # tail tile generates cast out but has no cast successors

            self.dicts[tile].update({
                'is_head': is_head,
                'is_tail': is_tail,

                'cast_in': cast_in, 
                'merge_in': merge_in,
                'gather_in': gather_in,

                'cast_out': cast_out,
                'merge_out': merge_out,
                'gather_out': gather_out,

                'cast_pred_comm': cast_pred_comm,
                'merge_pred_comm': merge_pred_comm,
                'gather_pred_comm': gather_pred_comm,

                'cast_succ_comm': cast_succ_comm,
                'merge_succ_comm': merge_succ_comm,
                'gather_succ_comm': gather_succ_comm
            })

    def _channel_match_check(self) -> None:
        for tile in self.tile_nodes:
            if self.is_head_tile(tile):
                continue

            cast_conn = self.cast_pred_comm(tile)
            tx_tile = list(self.preds(cast_conn))[0]
            tx_config = self.get_tile_config(tx_tile)
            tx_ocfg = tx_config['xbar_ocfg']
            tx_start_chan = tx_ocfg[0]
            tx_end_chan = tx_ocfg[1]

            rx_config = self.get_tile_config(tile)
            rx_icfg = rx_config['xbar_icfg']
            rx_start_chan = min([box[1] for box in rx_icfg])
            rx_end_chan = max([box[2] for box in rx_icfg])
            rx_num_ichan = rx_config['xbar_num_ichan']

            if (tx_start_chan != rx_start_chan) or (
                tx_end_chan != rx_end_chan) or (
                tx_end_chan - tx_start_chan != rx_num_ichan):
                raise AssertionError(
                    f'''channel not match at tile pair: {tx_tile} and {tile},
                        tx_chan_range: {tx_start_chan, tx_end_chan},
                        rx_chan_range: {rx_start_chan, rx_end_chan},
                        rx_icfg: {rx_icfg}''')

    @property
    def cast_trees(self) -> Generator[Tuple, None, None]:
        for c in self.cast_comms:
            src = list(self.graph.predecessors(c))[0]
            dst = list(self.graph.successors(c))
            yield (c, src, dst)

    @property
    def merge_trees(self) -> Generator[Tuple, None, None]:
        for m in self.merge_comms:
            src = list(self.graph.predecessors(m))
            dst = list(self.graph.successors(m))[0]
            yield (m, src, dst)

    @property
    def gather_pairs(self) -> Generator[Tuple, None, None]:
        for g in self.gather_comms:
            src = list(self.graph.predecessors(g))[0]
            dst = list(self.graph.successors(g))
            yield (g, src, dst)

    def get_comm_load(self, conn: Connection) -> int:
        '''
        This method returns the communication load of a given connection.
        unit: Tokens/Input Frame
        '''
        succ = list(self.succs(conn))[0]
        ifs = self.dicts[succ]['conv_input_size']
        pred = list(self.preds(conn))[0]
        nchan = self.dicts[pred]['xbar_num_ochan']
        
        return ifs[0] * ifs[1] * nchan

    def get_comm_lifetime(self, conn: Connection) -> float:
        '''
        This method returns the lifetime of a given connection.
        '''
        for dst_tile in self.graph.successors(conn):
            config = self.get_tile_config(dst_tile)
            return 1 - config['arrival_time']
        
        raise AssertionError(f"connection {conn} has no destination tiles")
    
    def report_communication(self) -> None:
        print('\n'+'-'*70)
        print('\t\tCommunication Report')
        print('-'*70)
        for comm in self.comms:
            load = self.get_comm_load(comm)
            lifetime = self.get_comm_lifetime(comm)
            print(f"comm: {comm}, load: {load}, lifetime: {lifetime}")

    def report_local_port_buffer_number(self) -> None:
        print('\n'+'-'*70)
        print('\t\tLocal Port Buffer Number Report')
        print('-'*70)
        nums = []
        for tile in self.tile_nodes:
            if not self.is_head_tile(tile):
                cast_in = [
                    node for node in self.preds(tile)
                    if self.is_cast_comm(node)
                ]
                num = len(cast_in)
                nums.append(num)
                print(f"tile {tile} local port buffer num: {num}")

        print(f"maximum local port buffer number: {max(nums)}")
        print(f"average local port buffer number: {sum(nums)/len(nums)}")

    def plot_ctg(
        self, 
        match_dict: Optional[Dict] = None, 
        direction: Literal['LR', 'UD'] = 'LR',
        abstract: bool = False
    ) -> None:
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'ctg')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        dot = Digraph('graph', format='svg')
        dot.attr(rankdir=direction)

        # plot nodes
        for n in self.graph.nodes:
            local = self.dicts[n] if n in self.dicts else dict()
            _label = ''
            for key in [
                'conv_buf', 
                'pool_buf', 
                'gather_buf', 
                'load', 
                'load_ratio'
            ]:
                if key in local:
                    _label += f'\n{key} : {local[key]}'
            if self.is_tile(n): # tile
                if abstract:
                    shape = 'box3d'
                    label = 'Tile'
                    xlabel = None
                    fixedsize = 'true'
                    height = 0.6
                    width = 0.6
                    penwidth = 2
                else:
                    config = self.dicts[n]
                    ichan_range = (
                        min([box[1] for box in config['xbar_icfg']]),
                        max([box[2] for box in config['xbar_icfg']])
                    )
                    ochan_range = config['xbar_ocfg']
                    box_idx = config['box_idx']
                    shape = 'rectangle'
                    shape = 'box3d'
                    label = 'log: ' + str(n) 
                    if match_dict is not None:
                        label += '\nphy: ' + str(match_dict[n])
                    label += f'\nop_type: {config["op_type"]}'
                    label += f'\nichan: {ichan_range}'
                    label += f'\nochan: {ochan_range}'
                    label += f'\nbox_idx: {box_idx}'
                    label += _label
                    xlabel = None
                    fixedsize = 'false'
                    height = None
                    width = None
                    penwidth = 2
            else: # comm
                shape = 'point'
                label = None
                xlabel = _label.lstrip('\n')
                fixedsize = 'false'
                height = None
                width = None
                penwidth = 2
            dot.node(
                str(n), 
                label=label, 
                fontname='Arial',
                shape=shape, 
                xlabel=xlabel,
                fixedsize=fixedsize,
                height=str(height),
                width=str(width),
                penwidth=str(penwidth)
            )

        # plot edges
        for e in self.graph.edges:
            if e[0] in self.cast_comms or e[1] in self.cast_comms:
                color = 'red'
            elif e[0] in self.merge_comms or e[1] in self.merge_comms:
                color = 'blue'
            elif e[0] in self.gather_comms or e[1] in self.gather_comms:
                color = 'purple'
            dot.edge(str(e[0]), str(e[1]), color=color, penwidth='2')
            
        dot.render(cleanup=True, directory=save_dir, view=False)
        print(f"ctg saved to {save_dir}")