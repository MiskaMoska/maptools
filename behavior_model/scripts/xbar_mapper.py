'''
TODO support for STMX
'''

import math
import numpy as np
import networkx as nx
from utils import *
from graphviz import Digraph
from onnx_converter import OperatorGraph
from typing import List, Dict, Tuple, Any

__all__ = ['XbarMapper']

class CTG(object):

    def __init__(self, opgraph: OperatorGraph, 
                    match_dict: Dict[str, int],
                    map_list: List[np.array],
                    map_dict: Dict[Tuple[int, int, int, int], Dict[str, Any]],
                    arch: str = 'resnet') -> None:
        '''
        Communication Trace Graph
        '''
        self.opgraph = opgraph
        self.match_dict = match_dict
        self.map_list = map_list
        self.dicts = map_dict

        self.xbar_nodes: List[str] = []
        self.cast_comms: List[str] = []
        self.merge_comms: List[str] = []
        self.collect_comms: List[str] = []

        if arch == 'resnet':
            self._build_ctg_resnet()

    def _build_ctg_resnet(self) -> None:
        self.graph = nx.MultiDiGraph()
        self.xbar_nodes = list(self.dicts.keys())
        self.graph.add_nodes_from(self.xbar_nodes)
        self._add_comms_resnet()

    def _add_comms_resnet(self) -> None: 
        # add cast and collect comms
        for e in self.opgraph.egdes: # for ResNet, every edge in opgraph corresponds to a communication
            p_lid = self.match_dict[e[0]]
            s_lid = self.match_dict[e[1]]
            p_mtx = self.map_list[p_lid] # source node map info matrix
            s_mtx = self.map_list[s_lid] # dst node map info matrix
            if self.opgraph.in_degree(e[1]) > 1 \
                and not is_subseq([e[0],e[1]],self.opgraph.trunk): # collect
                assert p_mtx.shape[0] == s_mtx.shape[0], "#regions not match for collect communication"
                for i in range(p_mtx.shape[0]): # for each region in the last layer
                    src_xbar = (p_lid, i, 0, 0) # source node of the collect path
                    dst_xbar = (s_lid, i, 0, 0) # dst node of the collect path
                    comm_name = 'colelct_from_'+str(src_xbar)
                    self.graph.add_node(comm_name)
                    self.collect_comms.append(comm_name)
                    self.graph.add_edge(src_xbar, comm_name)
                    self.graph.add_edge(comm_name, dst_xbar)
            else: # cast
                assert p_mtx.shape[0] == s_mtx.shape[1], "#regions in last later does not match #blocks in this layer"
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


    def Plot_CTG(self) -> None:
        dot = Digraph('graph')
        dot.attr(rankdir='LR')
        # for n in self.graph.nodes:
        #     print(n)
        for n in self.graph.nodes:
            if n in self.cast_comms \
                or n in self.merge_comms \
                or n in self.collect_comms:
                shape = 'point'
            else:
                shape = 'rectangle'
            dot.node(str(n),str(n), fontname='Arial',shape=shape)
        for e in self.graph.edges:
            dot.edge(str(e[0]),str(e[1]))
        dot.view()


class XbarMapper(object):

    def __init__(self, opgraph: OperatorGraph, 
                    w: int = 256, h: int = 256, arch: str = 'resnet') -> None:
        '''
        Parameters
        ----------
        opgraph : OperatorGraph
            pass

        w : int
            Xbar width
        
        h : int
            Xbar height

        arch : str = 'resnet'
            model architecture

        Key Variables:
        --------------
        self.match_dict : Dict[str, int]
            Matches each compute node in the operator graph to each layer in self.map_list
            For example, to find the corresponding mapping information of node "n1" of the operator graph, use:
            >>> idx = self.match_dict['n1']
            >>> map_info = self.map_list[idx]

        self.map_list : List[np.array[2]]
            Contains each layer's mapping information
            For example, self.map_list = [
            np.array([[1, 2, 3], [1, 2, 3]]),
            np.array([[2, 2], [2, 2], [2, 2]]),
            ...]
            Where each numpy array represent one layer's mapping information.
            Each element in the numpy array represents a block in current layer mapped xbars.
            The value of each element in the numpy array is the number of xbars the block contains.

        self.map_dict : Dict[Tuple[int, int, int, int], Dict[str, Any]]
            A look-up-table for each mapped xbar to get the corresponding configuration information.
            The Tuple key is organized as (layer, region, block, idx_in_block).
            For example, to get the configuration information of the second xbar in region 1, block 2 of the first layer, use:
            >>> key = (0, 1, 2, 1)
            >>> config_info = self.map_dict[key]

        '''
        assert w <= h, "Xbar height must be no smaller than width"
        self.opgraph = opgraph
        self.w = w
        self.h = h
        self.arch = arch
        self.match_dict: Dict[str, int] = dict() 
        self.map_list: List[np.array[2]] = []
        self.map_dict: Dict[Tuple[int, int, int, int], Dict[str, Any]] = dict() 

    def _xbar_map_resnet(self) -> None:
        '''
        In ResNet, there is no concat operation
        '''
        for l, layer in enumerate(self.opgraph.node_dicts):
            map_info = []
            self.match_dict[layer['name']] = l
            assert layer['op_type'] in ['Conv','Conv-Pool','Conv-Add','Conv-Pool-Add','Pool','Pool-Add'], \
                f"unexpected operation in resnet operation graph: {layer['op_type']}"
            if "Conv" not in layer['op_type']: # this layer contains no Conv
                n_inchan = layer['input_dims'][1]
                n_outchan = n_inchan
                k_size = (1,1)
            else: # this layer contains Conv
                n_inchan = layer['conv_num_inchan']
                n_outchan = layer['conv_num_outchan']
                k_size = layer['conv_kernel_size']

            pes_o = math.ceil(n_outchan / self.w) 
            for i in range(pes_o):
                map_info.append([]) # add a new region

                # output vector mapping
                start_co = i * self.w
                if (i + 1) * self.w > n_outchan:
                    end_co = n_outchan
                else:
                    end_co = (i + 1) * self.w
                
                # input vector mapping
                slcs = math.ceil(n_inchan / self.w) # how many slcs a channel vector is divided to
                # get slice length, each slice is shorter than Xbar width
                for j in range(slcs):
                    map_info[i].append(0) # add a new block
                    if (j + 1) * self.w > n_inchan:
                        slc_len = n_inchan % self.w
                    else:
                        slc_len = self.w
                    start_ci = j * self.w
                    end_ci = j * self.w + slc_len
                    slc_pt = (self.h // slc_len) # max slices per tile
                    pes_i = math.ceil((k_size[0]*k_size[1]) / slc_pt) 
                    for t in range(pes_i):
                        icfg = []
                        if (t + 1) * slc_pt > k_size[0]*k_size[1]:
                            it = k_size[0]*k_size[1] % slc_pt
                        else:
                            it = slc_pt
                        for k in range(it):
                            icfg.append((t*slc_pt+k,start_ci,end_ci))
                        xbar_dict = {'icfg': icfg, 'ocfg': (start_co,end_co)}
                        xbar_dict.update(layer)
                        self.map_dict[(l, i, j, t)] = xbar_dict
                        map_info[i][j] += 1
        
            self.map_list.append(np.array(map_info))

    @property
    def ctg(self) -> CTG:
        return CTG(self.opgraph,self.match_dict,self.map_list,self.map_dict,arch=self.arch)

    def xbar_map(self) -> None: 
        '''
        Map the operator graph to xbars
        Note that any xbar supports all ops
        '''
        pass

    # def 

    # def Print_Config(self):
    #     for i,layer in enumerate(self.xbar_config):
    #         for j,region in enumerate(layer):
    #             print('\n')
    #             print('-'*50)
    #             print(f'layer{i+1}_region{j+1}')
    #             print('-'*50)
    #             for k,block in enumerate(region):
    #                 print('`'*50)
    #                 print(f'block{k+1}')
    #                 for h,tile in enumerate(block):
    #                     print(f'\ntile{h}')
    #                     print('icfg:',tile['icfg'])
    #                     print('ocfg:',tile['ocfg'])

