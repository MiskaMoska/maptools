import random
import networkx as nx
from typing import Callable, List, Literal
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
    def __init__(self, rpc: RoutingPatternCode) -> None:
        super().__init__()
        self.rpc = rpc
        self.noc_w = rpc.noc_w
        self.noc_h = rpc.noc_h

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
        # if more randomization is needed, deepcopy and shuffle the dst_nodes here
        for d in dst_nodes:
            if d not in g.nodes:
                DyxyDLE._cast_route_dyxy(d[0], d[1], root_node[0], root_node[1], g)
        assert nx.is_tree(g), f"failed to build cast tree, not a tree: {g.edges}"
        g = nx.dfs_tree(g, source=root_node)
        return g


class SP_ReverseS_DRE(BaseDRE):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rpath = self._generate_path()

    def _get_path_idx(self, node: PhysicalTile) -> int:
        y = node[1]
        x = self.noc_w - node[0] - 1 if y % 2 else node[0]
        return y * self.noc_w + x

    def _generate_path(self) -> List[PhysicalTile]:
        path = []
        for y in range(self.noc_h):
            for x in range(self.noc_w):
                real_x = self.noc_w-x-1 if y % 2 else x
                path.append((real_x, y))
        return path

    def construct_one_tree(
        self, 
        src: PhysicalTile, 
        term_nodes: List[PhysicalTile]
    ) -> List[MeshEdge]:
        src_idx = self._get_path_idx(src)
        lower_idx = self._get_lower_idx(term_nodes)
        upper_idx = self._get_upper_idx(term_nodes)

        # print("src_idx: ", src_idx)
        # print("upper_idx: ", upper_idx)
        # print("lower_idx: ", lower_idx)

        path = []
        for dir in {'up', 'down'}:
            self._generate_edges(
                src_idx, upper_idx, lower_idx, path, dir)

        return path

    def _get_upper_idx(self, term_nodes: List[PhysicalTile]) -> int:
        indices = map(self._get_path_idx, term_nodes)
        return max(indices)
    
    def _get_lower_idx(self, term_nodes: List[PhysicalTile]) -> int:
        indices = map(self._get_path_idx, term_nodes)
        return min(indices)
    
    def _generate_edges(
        self, 
        now_idx: int, 
        upper_idx: int,
        lower_idx: int,
        path: List[MeshEdge], 
        search_dir: Literal['up', 'down']
    ) -> None:
        if (search_dir == 'down' and now_idx == lower_idx) or (
            search_dir == 'up' and now_idx == upper_idx):
            return
        
        nxt_idx = now_idx + (1 if search_dir == 'up' else -1)
        path.append((self.rpath[now_idx], self.rpath[nxt_idx]))
        self._generate_edges(
            nxt_idx, upper_idx, lower_idx, 
            path, search_dir
        )
    

__DRE_ACCESS_TABLE__ = {
    DREMethod.DYXY              :DyxyDLE,
    DREMethod.SP_REVERSE_S      :SP_ReverseS_DRE
}