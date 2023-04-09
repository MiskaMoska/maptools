'''
TODO need to provide support for random region division
'''
import os
import random
from random import shuffle
import pickle
import networkx as nx
from typing import List, Dict, Tuple, Any, Optional, Generator
from functools import cached_property
from maptools.xbar_mapper import *
from maptools.ctg import *
from maptools.utils import *
from copy import deepcopy

__all__ = ['NocMapper']

class NocMapper(object):

    def __init__(self, ctg: CTG, w: int, h: int, **kwargs: Any) -> None:
        '''
        Map the communication trace graph (CTG) onto network-on-chip (NoC)

        Parameters
        ----------
        ctg : CTG
            communication trace graph

        w : int
            xbar array width

        h : int
            xbar array height

        kwargs : Dict
            root_dir : str = os.environ.get('NVCIM_HOME')
                The root directory of the project.
        
            cast_method : bool = 'dyxy'
                'dyxy'      : DyXY-routing-based algorithm to run cast routing path plan, random.
                'steiner'   : minimum steiner-tree-based algorithm to run cast routing path plan, deterministic.

            mapname : str = 'newmap'
                Map name

        Key Members
        -----------
        self.match_dict : Dict[Tuple[int, int, int, int], Tuple[int, int]]
            A dictionary with logical xbar as keys and physical xbar as values
            Map the logical xbar (4-element tuple) to the physical xbar (2-element tuple).

        self.xxx_paths : Dict[str, Dict[str, Any]]
            xxx can be any of [cast, merge, gather].
            Stores the mapped paths and corresponding attributes for each connection type.
            `self.xxx_paths` = {'connection_name' : `path_dict`}
            where `path_dict` = {'sid' : int, 'src' : List[Tuple], 'dst' : List[Tuple], 
                                'path' : List[Tuple[Tuple]], 'load_ratio' : float, ....}}
        '''
        self.ctg = ctg
        self.w = w
        self.h = h
        self.root_dir = os.environ.get('NVCIM_HOME')
        self.cast_method = 'dyxy' # steiner tree is harmful
        self.mapname = 'newmap'
        self.__dict__.update(kwargs)

        # mapping from logical xbars to physical xbars
        self.match_dict: Dict[Tuple[int, int, int, int], Tuple[int, int]] = dict()

        # # intermediate representations
        # self.projected_model = []
        # self.model_regions = []
        # self.merge_nodes = []
        # self.cast_targets = []

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
                    self.match_dict[xbar] = rs_path[idx+i] # record map
                break

    @staticmethod
    def _dyxy_once(sx: int, sy: int, dx: int, dy: int) -> Tuple:
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
        return nxt_sx, nxt_sy

    @staticmethod
    def _cast_route_dyxy(sx: int, sy: int,dx: int, dy: int,graph: nx.Graph) -> None:
        '''
        Only for cast tree planning.
        Route from (sx, sy) to (dx, dy) following DyXY routing algorithm.

        Parameters
        ----------
        graph : Graph
            The udirected-tree-graph of the current cast communication.
        '''
        if sx == dx and sy == dy:
            return
        nxt_sx, nxt_sy = NocMapper._dyxy_once(sx, sy, dx, dy)
        if (nxt_sx, nxt_sy) in graph.nodes:
            graph.add_edge((sx, sy), (nxt_sx, nxt_sy))
            return
        graph.add_edge((sx, sy), (nxt_sx, nxt_sy))
        NocMapper._cast_route_dyxy(nxt_sx, nxt_sy, dx, dy, graph)
    
    @staticmethod
    def _build_cast_tree(root_node: Tuple, dst_nodes: List[Tuple]) -> nx.DiGraph:
        '''
        Build cast tree according to given root node and destination nodes.
        Applying DyXY method.
        '''
        g = nx.Graph()
        # if more randomization is need, deepcopy and shuffle the dst_nodes here
        for d in dst_nodes:
            if d not in g.nodes:
                NocMapper._cast_route_dyxy(d[0], d[1], root_node[0], root_node[1], g)
        assert nx.is_tree(g), f"failed to build cast tree, not a tree: {g.edges}"
        g = nx.dfs_tree(g, source=root_node)
        return g

    @staticmethod
    def _route_dyxy(
        sx: int, 
        sy: int, 
        dx: int, 
        dy: int, 
        path: List[Tuple], 
        region: Optional[List[Tuple]] = None
    ) -> None:
        '''
        Route from (sx, sy) to (dx, dy) following DyXY routing algorithm.

        Parameters
        ----------
        path : List[Tuple]
            Where the routing path results is located after performing this method.

        region : Optional[List[Tuple]]
            To constraint the routing path in a region.
            When asserted, the routing path is limited to the nodes in `region`.
        '''
        if sx == dx and sy == dy:
            return
        nxt_sx, nxt_sy = NocMapper._dyxy_once(sx, sy, dx, dy)

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
        NocMapper._route_dyxy(nxt_sx, nxt_sy, dx, dy, path, region=region)

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
            root_node = self.match_dict[root_node] # get the mapped node pos
            dst_nodes = [self.match_dict[n] for n in dst_nodes] # get the mapped node pos
            print(f"starting cast plan {sid}/{cast_num} ....")

            if self.cast_method == 'steiner':
                base_g = build_mesh(dst_nodes + [root_node])
                g = nx.algorithms.approximation.steiner_tree(base_g, dst_nodes + [root_node])
                g = nx.dfs_tree(g, source=root_node)
            elif self.cast_method == 'dyxy':
                g = self._build_cast_tree(root_node, dst_nodes)

            self.cast_paths[name] = dict()
            self.cast_paths[name]['sid'] = sid
            self.cast_paths[name]['src'] = [root_node]
            self.cast_paths[name]['dst'] = dst_nodes
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
            root_node = self.match_dict[root_node] # get the mapped node pos
            src_nodes = [self.match_dict[src] for src in src_nodes ] # get the mapped node pos
            region_nodes = deepcopy(src_nodes)
            region_nodes.append(root_node)
            print(f"starting merge plan {sid}/{merge_num} ....")

            # needed to be optimized by modified dyxy routing
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
                    self._route_dyxy(src_node[0], src_node[1], 
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
            self.merge_paths[name]['src'] = src_nodes
            self.merge_paths[name]['dst'] = [root_node]
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
            src_node = self.match_dict[src_node] # get the mapped node pos
            dst_node = self.match_dict[dst_node] # get the mapped node pos
            print(f"starting gather plan {sid}/{gather_num} ....")
            # keep generating the gather path until it is valid
            # valid means it has no conflit with existing paths
            path = []
            self._route_dyxy(src_node[0], src_node[1],
                                dst_node[0], dst_node[1], path)
            self.gather_paths[name] = dict()
            self.gather_paths[name]['sid'] = sid
            self.gather_paths[name]['src'] = [src_node]
            self.gather_paths[name]['dst'] = [dst_node]
            self.gather_paths[name]['path'] = path
            self.gather_paths[name]['load_ratio'] = self.ctg.get_attr(name, 'load_ratio')

    def run_map(self) -> None:
        self._map_xbars()
        self._cast_plan()
        self._merge_plan()
        self._gather_plan()

    @cached_property
    def xbar_config(self) -> Dict:
        '''
        A dictionary with physical xbar as keys and configuration info as values.
        Xbar configuration information for system simulation.
        Always call this method after calling `self.run_map`.
        '''
        return {self.match_dict[k] : self.ctg.dicts[k] for k in self.ctg.xbar_nodes}

    @property 
    def p2p_casts(self) -> Generator:
        '''
        cast information for P2P simulation.
        Make sure to call this method after calling `self.run_map`.
        '''
        for _, root_node, dst_nodes in self.ctg.cast_trees:
            yield (self.match_dict[root_node], [self.match_dict[d] for d in dst_nodes])
    
    @property
    def p2p_merges(self) -> Generator:
        '''
        merge information for P2P simulation.
        Make sure to call this method after calling `self.run_map`.
        '''
        for _, src_nodes, root_node in self.ctg.merge_trees:
            yield ([self.match_dict[s] for s in src_nodes], self.match_dict[root_node])

    @property
    def p2p_gathers(self) -> Generator:
        '''
        gather information for P2P simulation.
        Make sure to call this method after calling `self.run_map`.
        '''
        for _, src_node, dst_node in self.ctg.gather_pairs:
            yield (self.match_dict[src_node], self.match_dict[dst_node])

    @cached_property
    def tail_xbars(self) -> List[Tuple]:
        '''
        tail xbars information for concatenating outputs
        [(x1, y1), (x2, y2), (...), (...), ...]
        following tensor slice orders
        '''
        tails = []
        for xbar in self.ctg.xbar_nodes:
            if self.ctg.is_tail_xbar(xbar):
                tails.append(xbar)
        tails.sort(key=lambda tup:tup[1])
        return [self.match_dict[x] for x in tails]

    def save_map(self, file_name: str = 'mapinfo') -> None:
        '''
        save the mapping results as pkl sequence
        '''
        save_dir = os.path.join(self.root_dir, 'mapsave', self.mapname)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        file_dir = os.path.join(save_dir, file_name+'.pkl')
        info_dict = dict()

        # write network size info
        info_dict['network_width'] = self.w
        info_dict['network_height'] = self.h

        # write noc mapping info
        info_dict['match_dict'] = self.match_dict
        info_dict['xbar_config'] = self.xbar_config

        # write network config info
        info_dict['cast_paths'] = self.cast_paths
        info_dict['merge_paths'] = self.merge_paths
        info_dict['gather_paths'] = self.gather_paths

        # write p2p communication info
        info_dict['p2p_casts'] = list(self.p2p_casts)
        info_dict['p2p_merges'] = list(self.p2p_merges)
        info_dict['p2p_gathers'] = list(self.p2p_gathers)

        info_dict['tail_xbars'] = self.tail_xbars

        with open(file_dir, 'wb') as f:
            pickle.dump(info_dict, f)
        print(f"noc mapping info has been written to {file_dir}")

    def plot_ctg(self) -> None:
        '''
        Added physical xbar information than `CTG.plot_ctg()`
        '''
        self.ctg.plot_ctg(match_dict=self.match_dict)
