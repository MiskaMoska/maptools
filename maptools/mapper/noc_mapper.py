import os
import random
import pickle
import networkx as nx
from random import shuffle
from copy import deepcopy
from typing import List, Dict, Tuple, Any, Optional, Generator
from functools import cached_property
from maptools.mapper.tile_mapper import TileMapper
from maptools.core import CTG, ACG, ROOT_DIR, Connection, TrailType, MeshEdge
from maptools.nlrt import LayoutDesigner, LayoutResult
from maptools.nlrt import RoutingDesigner, RoutingResult, RoutingTrail
from maptools.drawing import draw_cast_trails, draw_merge_trails

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
        '''
        self.ctg = ctg
        self.acg = acg
        self.w = acg.w
        self.h = acg.h
        self.configs = kwargs

        self.mapname = 'newmap'
        self.__dict__.update(kwargs)

        self._merge_path: Dict[str, List[MeshEdge]] = dict()

    def run_layout(self) -> None:
        self.layout_designer = LayoutDesigner(
            self.ctg, self.acg, **self.configs
        )
        self.layout_designer.run_layout()
        self.layout = self.layout_designer.layout_result

    def run_routing(self) -> None:
        self.run_merge_routing()
        self.run_cast_routing()

    def run_map(self) -> None:
        self.run_layout()
        self.run_routing()

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

    def run_merge_routing(self) -> None:
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

            self._merge_path[name] = paths

    def run_cast_routing(self) -> None:
        '''
        Planning merge routing paths
        Make sure to call this method after `self.run_layout()`
        '''
        self.routing_designer = RoutingDesigner(
            self.ctg, self.acg, self.layout, **self.configs
        )
        self.routing_designer.run_routing()
        self.routing = self.routing_designer.routing_result

    @cached_property
    def cast_trails(self) -> Dict[Connection, RoutingTrail]:
        '''
        Constructing cast routing trail,
        Make sure to call this method after `self.run_routing()`
        '''
        sid = 0
        cast_trails = {}
        for cset in [
            self.ctg.cast_trees, 
            self.ctg.gather_pairs
        ]:
            for conn, src, dst in cset:
                sid += 1
                cast_trails[conn] = RoutingTrail(
                    sid, [self.layout[src]], 
                    [self.layout[d] for d in dst],
                    self.routing.get_path(conn),
                    acg=self.acg, 
                    is_gather=self.routing.is_gather(conn)   
                )

        return cast_trails
    
    @cached_property
    def merge_trails(self) -> Dict[Connection, RoutingTrail]:
        '''
        Constructing merge routing trail,
        Make sure to call this method after `self.run_routing()`
        '''
        merge_trails = {}
        for sid, (conn, src, dst) in enumerate(self.ctg.merge_trees, 1):
            merge_trails[conn] = RoutingTrail(
                sid, [self.layout[s] for s in src],
                [self.layout[dst]],
                self._merge_path[conn],
                acg=self.acg, 
                trail_type=TrailType.MERGE
            )

        return merge_trails

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
        draw_cast_trails(
            list(self.cast_trails.values()), 
            mapname=self.mapname
        )
        draw_merge_trails(
            list(self.merge_trails.values()), 
            mapname=self.mapname           
        )

    def plot_ctg(self) -> None:
        '''
        Added physical tile information than `CTG.plot_ctg()`
        '''
        self.ctg.plot_ctg(match_dict=self.layout.l2p_map)
