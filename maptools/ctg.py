'''
TODO support for STMX
'''
import os
import numpy as np
import networkx as nx
from graphviz import Digraph
from functools import cached_property
from typing import List, Dict, Tuple, Any, Generator, Optional
from maptools.operator_graph import *
from maptools.utils import *
from maptools.maptype import XbarConfig

__all__ = ['CTG']

class CTG(object):

    def __init__(
        self, 
        device_graph: OperatorGraph, 
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
        device_graph : OperatorGraph
            Device operator graph generated from `OnnxConverter`

        match_dict : Dict[str, int]
            Matches each compute node in the operator graph to each layer in self.map_list
            For example, to find the corresponding mapping information of node "n1" of the operator graph, use:
            >>> idx = self.match_dict['n1']
            >>> map_info = self.map_list[idx]

        map_list : List[np.ndarray]
            Contains each layer's mapping information
            For example, self.map_list = [
            np.array([[1, 2, 3], [1, 2, 3]]),
            np.array([[2, 2], [2, 2], [2, 2]]),
            ...]
            Where each numpy array represent one layer's mapping information.
            Each element in the numpy array represents a block in current layer mapped xbars.
            The value of each element in the numpy array is the number of xbars the block contains.

        map_dict : Dict[Tuple[int, int, int, int], Dict[str, Any]]
            A look-up-table for each mapped xbar to get the corresponding configuration information.
            The Tuple key is organized as (layer, region, block, idx_in_block).
            For example, to get the configuration information of the second xbar in region 1, block 2 of the first layer, use:
            >>> key = (0, 1, 2, 1)
            >>> config_info = self.map_dict[key]

        kwargs : Dict
            arch : str = 'resnet'
                The architecture of the model (or backbone).
                The arch must be one of OnnxConverter.valid_archs.

            root_dir : str = os.environ.get('NVCIM_HOME')
                The root directory of the project.

            mapname : str = 'newmap'
                Map name
        '''
        self.match_dict = match_dict
        self.map_list = map_list
        self.dicts = map_dict

        self.arch = 'resnet'
        self.root_dir = os.environ.get('NVCIM_HOME')
        self.mapname = 'newmap'
        self.quantize = device_graph.quantize
        self.__dict__.update(kwargs)

        self.xbar_nodes: List[Tuple[int, int, int, int]] = []
        self.cast_comms: List[str] = []
        self.merge_comms: List[str] = []
        self.gather_comms: List[str] = []

        # build ctg
        if self.arch == 'resnet':
            self._build_ctg_resnet(device_graph)

        # complete attributes
        self._complete_quant_attrs(device_graph)
        self._complete_connection_attrs()

    @cached_property
    def node_names(self) -> List[Any]:
        return list(nx.topological_sort(self.graph))
    
    @cached_property
    def xbars(self) -> List[Tuple]:
        return [n for n in self.node_names if self.is_xbar(n)]

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

    def is_xbar(self, node: Any) -> bool:
        return node in self.xbar_nodes
    
    def preds(self, node: Any) -> Generator:
        yield from self.graph.predecessors(node)

    def succs(self, node: Any) -> Generator:
        yield from self.graph.successors(node)

    def get_xbar_config(self, node: Any) -> XbarConfig:
        assert self.is_xbar(node), "not a xbar node, cannot get config"
        return self.dicts[node]

    def is_head_xbar(self, node: Any) -> bool:
        return self.graph.in_degree(node) == 0
    
    def is_tail_xbar(self, node: Any) -> bool:
        return self.graph.out_degree(node) == 0
    
    def get_attr(self, node: Any, attr: str) -> Any:
        if node in self.dicts:
            if attr in self.dicts[node]:
                return self.dicts[node][attr]
        return None

    @cached_property
    def xbar_num(self) -> int:
        return len(self.xbar_nodes)

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
    def regions(self) -> Generator:
        '''
        Returns all regions in turn
        A region is a set of xbars that execute the same range of output channels in Conv layer
        '''
        idx = 0
        base_idx = 0
        for i, mtx in enumerate(self.map_list):
            for j in range(mtx.shape[0]):
                base_idx += idx
                idx = 0
                region = []
                for k in range(mtx.shape[1]):
                    for t in range(mtx[j, k]):
                        region.append((i, j, k, t))
                        idx += 1
                yield base_idx, region

    def _build_ctg_resnet(self, device_graph: OperatorGraph) -> None:
        self.graph = nx.MultiDiGraph()
        self.xbar_nodes = list(self.dicts.keys())
        self.graph.add_nodes_from(self.xbar_nodes)
        self._add_comms_resnet(device_graph)

    def _add_comms_resnet(self, device_graph: OperatorGraph) -> None: 
        # add cast and gather comms
        # for ResNet, every edge in opgraph corresponds to a communication
        for e in device_graph.egdes: 
            p_lid = self.match_dict[e[0]]
            s_lid = self.match_dict[e[1]]
            p_mtx = self.map_list[p_lid] # source node map info matrix
            s_mtx = self.map_list[s_lid] # dst node map info matrix

            if device_graph.in_degree(e[1]) > 1 \
                and not is_subseq([e[0], e[1]], device_graph.trunk): # gather
                assert p_mtx.shape[0] == s_mtx.shape[0],(
                    "#regions not match for gather communication")
                for i in range(p_mtx.shape[0]): # for each region in the last layer
                    src_xbar = (p_lid, i, 0, 0) # source node of the gather path
                    dst_xbar = (s_lid, i, 0, 0) # dst node of the gather path
                    comm_name = 'gather_from_'+str(src_xbar)
                    self.graph.add_node(comm_name)
                    self.gather_comms.append(comm_name)
                    self.graph.add_edge(src_xbar, comm_name)
                    self.graph.add_edge(comm_name, dst_xbar)

            else: # cast
                assert p_mtx.shape[0] == s_mtx.shape[1], (
                    "#regions in last layer does not match #blocks in this layer")
                for i in range(p_mtx.shape[0]): # for each region in the last layer
                    src_xbar = (p_lid, i, 0, 0) # root node of the cast tree
                    comm_name = 'cast_from_'+str(src_xbar)
                    if comm_name not in self.cast_comms:
                        self.graph.add_node(comm_name)
                        self.graph.add_edge(src_xbar, comm_name)
                        self.cast_comms.append(comm_name)
                    for j in range(s_mtx.shape[0]):
                        for k in range(s_mtx[j, i]):
                            self.graph.add_edge(comm_name, (s_lid, j, i, k))
        
        # add merge comms
        for lid, mtx in enumerate(self.map_list):
            for i in range(mtx.shape[0]): # for each region in the current layer
                if np.sum(mtx[i]) > 1: # there are more than 1 xbar in the current region
                    dst_xbar = (lid, i, 0, 0) # root node of the merge tree
                    comm_name = 'merge_to_'+str(dst_xbar)
                    self.graph.add_node(comm_name)
                    self.graph.add_edge(comm_name, dst_xbar)
                    self.merge_comms.append(comm_name)
                    for j in range(mtx.shape[1]):
                        for k in range(mtx[i, j]):
                            node = (lid, i, j, k)
                            if node != dst_xbar:
                                self.graph.add_edge(node, comm_name)

    def _complete_quant_attrs(self, device_graph: OperatorGraph) -> None:
        io_quant_config = device_graph.input_output_quant_config
        if self.quantize:
            self.input_quant_config = io_quant_config[0]
            self.output_quant_config = io_quant_config[1]

    def _complete_connection_attrs(self) -> None:
        '''
        Complete connection attributes
        '''
        for xbar in self.xbar_nodes:
            cast_in, merge_in, gather_in = False, False, False
            for pred in self.graph.predecessors(xbar):
                if pred in self.cast_comms:
                    cast_in = True
                if pred in self.merge_comms:
                    merge_in = True
                if pred in self.gather_comms:
                    gather_in = True
            cast_out, merge_out, gather_out = False, False, False
            for succ in self.graph.successors(xbar):
                if succ in self.cast_comms:
                    cast_out = True
                if succ in self.merge_comms:
                    merge_out = True
                if succ in self.gather_comms:
                    gather_out = True
            is_head, is_tail = False, False
            if self.is_head_xbar(xbar):
                is_head = True
                cast_in = True # head xbar receives cast in but has no cast predecessors
            if self.is_tail_xbar(xbar):
                is_tail = True
                cast_out = True # tail xbar generates cast out but has no cast successors
            self.dicts[xbar].update({
                'cast_in': cast_in, 
                'merge_in': merge_in,
                'gather_in': gather_in,
                'cast_out': cast_out,
                'merge_out': merge_out,
                'gather_out': gather_out,
                'is_head': is_head,
                'is_tail': is_tail
            })

    @property
    def cast_trees(self) -> Generator[Tuple, None, None]:
        for c in self.cast_comms:
            src = self.graph.predecessors(c)
            src = list(src)[0]
            dst = self.graph.successors(c)
            dst = list(dst)
            yield (c, src, dst)

    @property
    def merge_trees(self) -> Generator[Tuple, None, None]:
        for m in self.merge_comms:
            src = self.graph.predecessors(m)
            src = list(src)
            dst = self.graph.successors(m)
            dst = list(dst)[0]
            yield (m, src, dst)

    @property
    def gather_pairs(self) -> Generator[Tuple, None, None]:
        for g in self.gather_comms:
            src = self.graph.predecessors(g)
            src = list(src)[0]
            dst = self.graph.successors(g)
            dst = list(dst)[0]
            yield (g, src, dst)

    def comm_load_analysis(self) -> None:
        '''
        This method provides fast communication load analysis to replace the function of 
        `TokSim`, if only communication load analysis is needed and buffer size analysis
        is not needed, use this method rather than `TokSim.run()`.
        This method will update `self.dicts` by adding communication load information.
        '''
        dict1 = dict()
        max_load = 0
        for n in self.node_names:
            if self.is_comm(n):
                succs = self.succs(n)
                succ = list(succs)[0]
                ifs = self.dicts[succ]['conv_input_size']
                ni = self.dicts[succ]['xbar_num_ichan']
                load = ifs[0] * ifs[1] * ni
                if load > max_load:
                    max_load = load
                dict1[n] = load # absolute load
        for n in self.node_names:
            if self.is_comm(n):
                load = dict1[n]
                self.update_dict(n, {'load': load, 'load_ratio': load / max_load})

    def plot_ctg(self, match_dict: Optional[Dict] = None) -> None:
        save_dir = os.path.join(self.root_dir, 'mapsave', self.mapname, 'ctg')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        dot = Digraph('graph', format='svg')
        dot.attr(rankdir='LR')

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
            if self.is_xbar(n): # xbar
                shape = 'rectangle'
                shape = 'box3d'
                label = 'log: ' + str(n) 
                if match_dict is not None:
                    label += '\nphy: ' + str(match_dict[n])
                label += '\n' + self.dicts[n]['op_type']
                label += _label
                xlabel = None
            else: # comm
                shape = 'point'
                label = None
                xlabel = _label.lstrip('\n')
            dot.node(
                str(n), 
                label=label, 
                fontname='Arial',
                shape=shape, 
                xlabel=xlabel
            )

        # plot edges
        for e in self.graph.edges:
            if e[0] in self.cast_comms or e[1] in self.cast_comms:
                color = 'red'
            elif e[0] in self.merge_comms or e[1] in self.merge_comms:
                color = 'blue'
            elif e[0] in self.gather_comms or e[1] in self.gather_comms:
                color = 'purple'
            dot.edge(str(e[0]), str(e[1]), color=color)
        dot.view(cleanup=True, directory=save_dir)
        print(f"ctg save to {save_dir}")
