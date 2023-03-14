'''
TODO need to provide support for random region division
'''
import random
from random import shuffle
import networkx as nx
from matplotlib import pyplot as plt
from typing import List, Dict, Tuple, Any, Optional, Generator
from functools import cached_property
from xbar_mapper import *
from copy import deepcopy
from ctg import *
from utils import *

__all__ = ['NocMapper']

class NocMapper(object):

    def __init__(self, ctg: CTG, w: int, h: int, *args, **kwargs) -> None:
        '''
            Parameters
            ----------
            ctg : CTG
                communication trace graph

            w : int
                xbar array width

            h : int
                xbar array height

            kwargs : Dict
                dir_name : str = './'
                    root path to save the map figure.
            
                cast_method : bool = 'steiner'
                    'dyxy'      : DyXY-routing-based algorithm to run cast routing path plan, random.
                    'steiner'   : minimum steiner-tree-based algorithm to run cast routing path plan, deterministic.
        
            Key Members:
            ------------
            self.map_dict : Dict[Tuple[int, int, int, int], Tuple[int, int]]
                Map the logical xbar (4-element tuple) to the physical xbar (2-element tuple).

            self.xxx_paths : Dict[str, Dict[str, Any]]
                xxx can be any of [cast, merge, gather].
                Stores the mapped paths and corresponding attributes for each connection type.
                {'connection_name' : {'sid' : int, 'path' : List[Tuple], 'load_ratio' : float, ....}}
        '''
        self.ctg = ctg
        self.w = w
        self.h = h
        self.dir_name = './'
        self.cast_method = 'steiner'
        self.__dict__.update(kwargs)

        # mapping from logical xbars to physical xbars
        self.map_dict: Dict[Tuple[int, int, int, int], Tuple[int, int]] = dict()

        # intermediate representations
        self.projected_model = []
        self.model_regions = []
        self.merge_nodes = []
        self.cast_targets = []

        # network routing paths
        self.cast_paths: Dict[str, Dict[str, Any]] = dict()
        self.merge_paths: Dict[str, Dict[str, Any]] = dict()
        self.gather_paths: Dict[str, Dict[str, Any]] = dict()

    @staticmethod
    def _gen_reverse_s(w: int, h: int) -> List[Tuple[int, int]]:
        '''
        generate reverse-s path
        '''
        rs_path = []
        for i in range(h):
            for j in range(w):
                idx = (i+1)*w-j-1 if i % 2 else i*w+j
                rs_path.append((idx % w, idx // w))
        return rs_path
    
    def _map_xbars(self) -> None:
        '''
        Map the xbars to the xbar array following reverse-s path
        '''
        rs_path = self._gen_reverse_s(self.w, self.h)
        for idx, region in self.ctg.regions:
            merge_xbar = region[0]
            while True:
                valid = True
                shuffle(region) # random mapping
                merge_idx = region.index(merge_xbar) # find the merge xbar
                y_pos_merge = rs_path[idx+merge_idx]
                for i in range(merge_idx, len(region)):
                    if rs_path[idx+i] > y_pos_merge: # larger y_pos than merge xbar
                        valid = False
                        break
                if not valid: # begin next loop
                    continue

                for i, xbar in enumerate(region):
                    self.map_dict[xbar] = rs_path[idx+i] # record map
                break

    @staticmethod
    def _route_dyxy(w: int, h: int, sx: int, sy: int, 
                        dx: int, dy: int, path: List[Tuple], 
                        region: Optional[List[Tuple]] = None) -> None:
        '''
        Route from (sx, sy) to (dx, dy) following DyXY routing algorithm.

        Parameters
        -------------------
        path : List[Tuple]
            Where the routing path results is located after performing this method.

        region : Optional[List[Tuple]]
            To constraint the routing path in a region.
            When asserted, the routing path is limited to the nodes in `region`.
        '''
        if sx == dx and sy == dy:
            return
        if sx != dx and sy != dy:
            # prechoose horizontal
            nxt_sy = sy
            nxt_sx = sx + (1 if sx < dx else -1)
            go_vertical = True if random.random() > 0.5 else False
            if go_vertical:
                nxt_sx = sx
                nxt_sy = sy + (1 if sy < dy else -1)
        else:
            if sx == dx:
                nxt_sx = sx
                nxt_sy = sy + (1 if sy < dy else -1)
            elif sy == dy:
                nxt_sy = sy
                nxt_sx = sx + (1 if sx < dx else -1)

        # if constrained routing region considered
        if not region is None:
            if (nxt_sx, nxt_sy) not in region:
                if sy == nxt_sy:
                    nxt_sx = sx
                    nxt_sy = sy + (1 if sy < dy else -1)
                elif sx == nxt_sx:
                    nxt_sy = sy
                    nxt_sx = sx + (1 if sx < dx else -1)
            assert (nxt_sx, nxt_sy) in region, "critical error ecountered at merge path"
        path.append(((sx, sy), (nxt_sx ,nxt_sy)))
        NocMapper._route_dyxy(w,h,nxt_sx,nxt_sy,dx,dy,path,region=region)

    @staticmethod
    def _get_channel(bias_pos: Tuple, now_pos: Tuple, root_pos: Tuple) -> int:
        if bias_pos[0] < now_pos[0]: # west
            return 1
        if bias_pos[0] > now_pos[0]: # east
            return 2
        if now_pos[0] < root_pos[0]: # vert0
            return 3
        return 4 # vert1

    def _cast_plan(self) -> None:
        '''
        Planning cast routing paths
        Make sure to call this method after `self._map_xbars()`
        '''
        # cast tree number
        cast_num = self.ctg.cast_num

        for sid, (name, root_node, dst_nodes) in enumerate(self.ctg.cast_trees,1):
            root_node = self.map_dict[root_node] # get the mapped node pos
            print(f"starting cast plan {sid}/{cast_num} ....")
            # keep generating the multicast tree until it is valid
            # valid means every node in the multicast tree has no more than 1 in_edge
            if self.cast_method == 'steiner':
                dst_nodes = [self.map_dict[n] for n in dst_nodes]
                base_g = build_mesh(dst_nodes + [root_node])
                g = nx.algorithms.approximation.steiner_tree(base_g, dst_nodes + [root_node])
                g = nx.dfs_tree(g, source=root_node)
            elif self.cast_method == 'dyxy':
                while True:
                    # for each multicast tree
                    # create the simple cast graph where each node represents a cast router
                    g = nx.MultiDiGraph()

                    # complete the simple cast graph by the generated multicast tree
                    paths = []
                    for dst_node in dst_nodes:
                        path = []
                        self._route_dyxy(self.w, self.h,
                                            root_node[0], root_node[1], 
                                            dst_node[0], dst_node[1], path)
                        paths.extend(path)
                    paths = list(set(paths))
                    g.add_edges_from(paths)

                    # verify the validity of the generated multicast tree
                    flag = True
                    for node in g.nodes():
                        if g.in_degree(node) > 1:
                            flag = False
                            break
                    if flag:
                        break
            self.cast_paths[name] = dict()
            self.cast_paths[name]['sid'] = sid
            self.cast_paths[name]['root_node'] = root_node
            self.cast_paths[name]['dst_nodes'] = dst_nodes
            self.cast_paths[name]['path'] = list(g.edges) # add to cast_paths
            self.cast_paths[name]['load_ratio'] = self.ctg.get_attr(name, 'load_ratio')

    def _merge_plan(self) -> None:
        '''
        Planning merge routing paths
        Make sure to call this method after `self._map_xbars()`
        '''
        # merge tree number
        merge_num = self.ctg.merge_num  

        for sid, (name, src_nodes, root_node) in enumerate(self.ctg.merge_trees, 1):
            root_node = self.map_dict[root_node] # get the mapped node pos
            src_nodes = [self.map_dict[src] for src in src_nodes ] # get the mapped node pos
            region_nodes = deepcopy(src_nodes)
            region_nodes.append(root_node)
            print(f"starting merge plan {sid}/{merge_num} ....")
            # keep generating the merge tree until it is valid
            # valid means every node in the merge tree has no more than 1 in_edge
            while True:
                # for each merge tree
                # create the simple merge graph where each node represents a merge router
                g = nx.MultiDiGraph()

                # complete the simple merge graph by the generated merge tree
                paths = []
                for src_node in src_nodes:
                    path = []
                    self._route_dyxy(self.w, self.h,
                                        src_node[0], src_node[1], 
                                        root_node[0], root_node[1], path, 
                                        region=region_nodes)
                    paths.extend(path)
                paths = list(set(paths))
                g.add_edges_from(paths)
            
                # verify the validity of the generated merge tree
                flag = True
                for node in g.nodes():
                    if g.out_degree(node) > 1:
                        flag = False
                        break
                if flag:
                    break
            self.merge_paths[name] = dict()
            self.merge_paths[name]['sid'] = sid
            self.merge_paths[name]['path'] = paths # add to merge_paths
            self.merge_paths[name]['load_ratio'] = self.ctg.get_attr(name, 'load_ratio')

    def _gather_plan(self) -> None:
        '''
        Planning gather routing paths
        Make sure to call this method after calling `self._map_xbars`
        '''
        # gather pair  number
        gather_num = self.ctg.gather_num
        
        for sid, (name, src_node, dst_node) in enumerate(self.ctg.gather_pairs,1):
            src_node = self.map_dict[src_node]
            dst_node = self.map_dict[dst_node]
            print(f"starting gather plan {sid}/{gather_num} ....")
            # keep generating the gather path until it is valid
            # valid means it has no conflit with existing paths
            path = []
            self._route_dyxy(self.w, self.h, 
                                src_node[0], src_node[1],
                                dst_node[0], dst_node[1], path)
            self.gather_paths[name] = dict()
            self.gather_paths[name]['sid'] = sid
            self.gather_paths[name]['path'] = path
            self.gather_paths[name]['load_ratio'] = self.ctg.get_attr(name, 'load_ratio')

    def run_map(self) -> None:
        self._map_xbars()
        self._cast_plan()
        self._merge_plan()
        self._gather_plan()

    @property
    def xbar_config_info(self) -> Generator:
        '''
        Xbar configuration information for system simulation.
        Always call this method after calling `self.run_map`.
        '''
        for k, v in self.ctg.dicts.items():
            yield (self.map_dict[k], v)

    @property
    def p2p_casts(self) -> Generator:
        '''
        cast information for P2P simulation.
        Make sure to call this method after calling `self.run_map`.
        '''
        for _, root_node, dst_nodes in self.ctg.cast_trees:
            yield (self.map_dict[root_node], [self.map_dict[d] for d in dst_nodes])
    
    @property
    def p2p_merges(self) -> Generator:
        '''
        merge information for P2P simulation.
        Make sure to call this method after calling `self.run_map`.
        '''
        for _, src_nodes, root_node in self.ctg.merge_trees:
            yield ([self.map_dict[s] for s in src_nodes], self.map_dict[root_node])

    @property
    def p2p_gathers(self) -> Generator:
        '''
        gather information for P2P simulation.
        Make sure to call this method after calling `self.run_map`.
        '''
        for _, src_node, dst_node in self.ctg.gather_pairs:
            yield (self.map_dict[src_node], self.map_dict[dst_node])
