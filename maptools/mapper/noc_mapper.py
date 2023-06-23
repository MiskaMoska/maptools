import os
import random
import pickle
import networkx as nx
from random import shuffle
from copy import deepcopy
from typing import List, Dict, Tuple, Any, Optional, Generator
from functools import cached_property
from maptools.mapper.tile_mapper import TileMapper
from maptools.core import CTG, ACG, ROOT_DIR
from maptools.nlrt import LayoutDesigner, LayoutResult
from maptools.nlrt import RoutingDesigner, RoutingResult
from maptools.drawing import MapPlotter

__all__ = ['NocMapper']

class NocMapper(object):

    def __init__(
        self, 
        ctg: CTG, 
        acg: ACG,
        **kwargs: Any
    ) -> None:
        '''
        Map the communication trace graph (CTG) onto network-on-chip (NoC)

        Parameter
        ---------
        ctg: CTG
            Communication Trace Graph of the AI task.

        acg: ACG
            Architecture Characterization Graph of the NoC.

        Key Members
        -----------
        self.xxx_paths : Dict[str, Dict[str, Any]]
            xxx can be any of [cast, merge].
            Stores the mapped paths and corresponding attributes for each connection type.
            `self.xxx_paths` = {'connection_name' : `path_dict`}
            where `path_dict` = {'sid' : int, 'src' : List[Tuple], 'dst' : List[Tuple], 
                                'path' : List[Tuple[Tuple]], 'load_ratio' : float, ....}}
        '''
        self.ctg = ctg
        self.acg = acg
        self.w = acg.w
        self.h = acg.h
        self.configs = kwargs

        self.mapname = 'newmap'
        self.__dict__.update(kwargs)

        # network routing paths
        self.cast_paths: Dict[str, Dict[str, Any]] = dict()
        self.merge_paths: Dict[str, Dict[str, Any]] = dict()

    def run_layout(self) -> None:
        self.layout_designer = LayoutDesigner(
            self.ctg, self.acg, **self.configs
        )
        self.layout_designer.run_layout()
        self.layout = self.layout_designer.layout_result

    def run_routing(self) -> None:
        self._merge_routing()
        self.routing_designer = RoutingDesigner(
            self.ctg, self.acg, self.layout, **self.configs
        )
        self.routing_designer.run_routing()
        self.routing = self.routing_designer.routing_result

        sid = 0
        for cset in [
            self.ctg.cast_trees, 
            self.ctg.gather_pairs
        ]:
            for c, src, dst in cset:
                sid += 1
                self.cast_paths[c] = {
                    'sid': sid,
                    'src': [self.layout[src]],
                    'dst': [self.layout[d] for d in dst],
                    'path': self.routing[c]
                }

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
    def _route_dyxy(
        sx: int, 
        sy: int, 
        dx: int, 
        dy: int, 
        path: List[Tuple], 
        patch: Optional[List[Tuple]] = None
    ) -> None:
        '''
        Route from (sx, sy) to (dx, dy) following DyXY routing algorithm.

        Parameters
        ----------
        path : List[Tuple]
            Where the routing path results is located after performing this method.

        patch : Optional[List[Tuple]]
            To constraint the routing path in a patch.
            When asserted, the routing path is limited to the nodes in `patch`.
        '''
        if sx == dx and sy == dy:
            return
        nxt_sx, nxt_sy = NocMapper._dyxy_once(sx, sy, dx, dy)

        # if constrained routing patch considered
        if not patch is None:
            if (nxt_sx, nxt_sy) not in patch:
                if sy == nxt_sy:
                    nxt_sx = sx
                    nxt_sy = sy + (1 if sy < dy else -1)
                elif sx == nxt_sx:
                    nxt_sy = sy
                    nxt_sx = sx + (1 if sx < dx else -1)
            assert (nxt_sx, nxt_sy) in patch, "critical error ecountered at merge path"
        path.append(((sx, sy), (nxt_sx ,nxt_sy)))
        NocMapper._route_dyxy(nxt_sx, nxt_sy, dx, dy, path, patch=patch)

    def _merge_routing(self) -> None:
        '''
        Planning merge routing paths
        Make sure to call this method after `self.run_layout()`
        '''
        # merge tree number
        merge_num = self.ctg.merge_num  

        for sid, (name, src_nodes, root_node) in enumerate(self.ctg.merge_trees, 1):
            root_node = self.layout[root_node] # get the mapped node pos
            src_nodes = [self.layout[src] for src in src_nodes ] # get the mapped node pos
            cluster_nodes = deepcopy(src_nodes)
            cluster_nodes.append(root_node)
            # print(f"starting merge routing {sid}/{merge_num} ....")

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
                                        patch=cluster_nodes)
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
            
            self.merge_paths[name] = {
                'sid': sid,
                'src': src_nodes,
                'dst': [root_node],
                'path': paths
            }

    @cached_property
    def tile_config(self) -> Dict:
        '''
        A dictionary with physical tile as keys and configuration info as values.
        Tile configuration information for system simulation.
        Always call this method after calling `self.run_map`.
        '''
        return {self.layout[k] : self.ctg.dicts[k] for k in self.ctg.tile_nodes}

    @property 
    def p2p_casts(self) -> Generator:
        '''
        cast information for P2P simulation.
        Make sure to call this method after calling `self.run_map`.
        '''
        for _, root_node, dst_nodes in self.ctg.cast_trees:
            yield (self.layout[root_node], [self.layout[d] for d in dst_nodes])
    
    @property
    def p2p_merges(self) -> Generator:
        '''
        merge information for P2P simulation.
        Make sure to call this method after calling `self.run_map`.
        '''
        for _, src_nodes, root_node in self.ctg.merge_trees:
            yield ([self.layout[s] for s in src_nodes], self.layout[root_node])

    @property
    def p2p_gathers(self) -> Generator:
        '''
        gather information for P2P simulation.
        Make sure to call this method after calling `self.run_map`.
        '''
        for _, src_node, dst_nodes in self.ctg.gather_pairs:
            yield (self.layout[src_node], [self.layout[d] for d in dst_nodes])

    @cached_property
    def tail_tiles(self) -> List[Tuple]:
        '''
        tail tiles information for concatenating outputs
        [(x1, y1), (x2, y2), (...), (...), ...]
        following tensor slice orders
        '''
        tails = []
        for tile in self.ctg.tile_nodes:
            if self.ctg.is_tail_tile(tile):
                tails.append(tile)
        tails.sort(key=lambda tup:tup[1])
        return [self.layout[x] for x in tails]

    def save_layout(self) -> None:
        '''
        Save layout graphs
        '''
        self.layout.draw()

    def save_routing(self) -> None:
        '''
        Save routing graphs
        '''
        self.routing.draw()
        mplt = MapPlotter(
            self.w, self.h,
            self.cast_paths, 
            self.merge_paths, 
            self.cast_paths, 
            show_path=True,
            **self.configs
        )
        mplt.plot_cast_map()
        mplt.plot_merge_map()

    def save_config(self, file_name: str = 'mapinfo') -> None:
        '''
        Save NoC configuration information
        '''
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        file_dir = os.path.join(save_dir, file_name+'.pkl')
        info_dict = dict()

        # write network size info
        info_dict['network_width'] = self.w
        info_dict['network_height'] = self.h

        # write noc mapping info
        info_dict['match_dict'] = self.layout.l2p_map
        info_dict['tile_config'] = self.tile_config

        # write network config info
        info_dict['cast_paths'] = self.cast_paths
        info_dict['merge_paths'] = self.merge_paths

        # write p2p communication info
        info_dict['p2p_casts'] = list(self.p2p_casts)
        info_dict['p2p_merges'] = list(self.p2p_merges)
        info_dict['p2p_gathers'] = list(self.p2p_gathers)

        info_dict['tail_tiles'] = self.tail_tiles

        with open(file_dir, 'wb') as f:
            pickle.dump(info_dict, f)
        # print(f"noc mapping info has been written to {file_dir}")

    def plot_ctg(self) -> None:
        '''
        Added physical tile information than `CTG.plot_ctg()`
        '''
        self.ctg.plot_ctg(match_dict=self.layout.l2p_map)
