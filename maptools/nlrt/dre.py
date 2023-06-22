import random
import networkx as nx
from typing import Callable, List
from maptools.core import (
    CTG, ACG, DREMethod, 
    PhysicalTile, MeshEdge
)
from abc import ABCMeta, abstractmethod
from random import shuffle
from maptools.nlrt.encoding import RoutingPatternCode

class BaseDRE(Callable, metaclass=ABCMeta):
    '''
    Base Class for Deterministic Routing Engine
    '''
    def __init__(self, rpc: RoutingPatternCode, *args, **kwargs) -> None:
        super().__init__()
        self.rpc = rpc

    def __call__(self) -> RoutingPatternCode:
        self._construct_all_trees()
        return self.rpc

    @abstractmethod
    def construct_one_tree(
        self, 
        src: PhysicalTile, 
        term_nodes: List[PhysicalTile]
    ) -> List[MeshEdge]: ...

    def _construct_all_trees(self) -> None:
        for comm in self.rpc.comms:
            term_nodes = self.rpc.term_dict[comm]
            src = self.rpc.src_dict[comm]
            edges = self.construct_one_tree(src, term_nodes)
            self.rpc.path_dict[comm] = edges

        # empty decode queue to avoid mis-decoding after constructing trees
        self.rpc.empty_decode_queue()
    
    def reset(self) -> None: ...


class DyxyDLE(BaseDRE):

    def construct_one_tree(
        self, 
        src: PhysicalTile, 
        term_nodes: List[PhysicalTile]
    ) -> List[MeshEdge]:
        dst_nodes = term_nodes.copy()
        dst_nodes.remove(src)
        graph = self._build_cast_tree(src, dst_nodes)
        return list(graph.edges)
    
    @staticmethod
    def _cast_route_dyxy(
        sx: int, sy: int, 
        dx: int, dy: int, 
        graph: nx.Graph
    ) -> None:
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
        nxt_sx, nxt_sy = DyxyDLE._dyxy_once(sx, sy, dx, dy)
        if (nxt_sx, nxt_sy) in graph.nodes:
            graph.add_edge((sx, sy), (nxt_sx, nxt_sy))
            return
        graph.add_edge((sx, sy), (nxt_sx, nxt_sy))
        DyxyDLE._cast_route_dyxy(nxt_sx, nxt_sy, dx, dy, graph)

    @staticmethod
    def _dyxy_once(
        sx: int, sy: int, 
        dx: int, dy: int
    ) -> PhysicalTile:
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
    def _build_cast_tree(
        root_node: PhysicalTile, 
        dst_nodes: List[PhysicalTile]
    ) -> nx.DiGraph:
        '''
        Build cast tree according to given root node and destination nodes.
        Applying DyXY method.
        '''
        g = nx.Graph()
        # if more randomization is need, deepcopy and shuffle the dst_nodes here
        for d in dst_nodes:
            if d not in g.nodes:
                DyxyDLE._cast_route_dyxy(d[0], d[1], root_node[0], root_node[1], g)
        assert nx.is_tree(g), f"failed to build cast tree, not a tree: {g.edges}"
        g = nx.dfs_tree(g, source=root_node)
        return g
    

__DRE_ACCESS_TABLE__ = {
    DREMethod.DYXY         :DyxyDLE
}