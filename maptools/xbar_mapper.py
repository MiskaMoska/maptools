'''
TODO support for STMX
'''

import math
import numpy as np
import networkx as nx
from graphviz import Digraph
from functools import cached_property
from typing import List, Dict, Tuple, Any, Generator
from operator_graph import *
from ctg import *
from utils import *

__all__ = ['XbarMapper']

class XbarMapper(object):

    def __init__(self, opgraph: OperatorGraph, 
                    w: int, h: int, *args, **kwargs) -> None:
        '''
        Parameters
        ----------
        opgraph : OperatorGraph
            pass

        w : int
            Xbar width
        
        h : int
            Xbar height

        kwargs : Dict
            arch : str = 'resnet'
                model architecture

        Key Members:
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
        self.arch = 'resnet'
        self.__dict__.update(kwargs)
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
                        xbar_dict = {'xbar_icfg': icfg, 'xbar_ocfg': (start_co,end_co), \
                                        'xbar_num_ichan': end_ci-start_ci, 'xbar_num_ochan': end_co-start_co}
                        xbar_dict.update(layer)
                        if j != 0 or t != 0: # not merge xbar
                            # only merge xbar has pool or add
                            xbar_dict['op_type'] = xbar_dict['op_type'].rstrip('-Add').rstrip('-Pool') 
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

    def print_config(self) -> None:
        '''
        Print xbar configs
        '''
        total = 0
        for i, mtx in enumerate(self.map_list):
            sum = np.sum(mtx)
            total += sum
            print(f"layer{i}: #region-{mtx.shape[0]}, #block-{mtx.shape[1]}, #xbar-{sum}")
        print("-"*70)
        print(f"total #xbar-{total}")

