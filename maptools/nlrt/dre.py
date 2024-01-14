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


class DyxyDRE(BaseDRE):

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
        nxt_sx, nxt_sy = DyxyDRE._dyxy_once(sx, sy, dx, dy)
        if (nxt_sx, nxt_sy) in graph.nodes:
            graph.add_edge((sx, sy), (nxt_sx, nxt_sy))
            return
        graph.add_edge((sx, sy), (nxt_sx, nxt_sy))
        DyxyDRE._cast_route_dyxy(nxt_sx, nxt_sy, dx, dy, graph)

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
                DyxyDRE._cast_route_dyxy(d[0], d[1], root_node[0], root_node[1], g)
        assert nx.is_tree(g), f"failed to build cast tree, not a tree: {g.edges}"
        g = nx.dfs_tree(g, source=root_node)
        return g


class SP_FULL_DRE(BaseDRE):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.outer_dir = 0
        self.inner_dir = 0
        self.fcn = [min, max]

    def randomize_shape(self) -> None:
        self.outer_dir = random.choice([0, 1])
        self.inner_dir = random.choice([0, 1])

    def get_full_path(
        self,
        term_nodes: List[PhysicalTile]
    ) -> List[MeshEdge]:
        self.randomize_shape()
        edges = [] # undirectional edges
        key = lambda x : x[self.outer_dir]
        min_pos = min(self.xy[1-self.outer_dir])

        start_layer = [
            n for n in term_nodes 
            if n[1-self.outer_dir] == min_pos
        ]
        start_node = self.fcn[self.inner_dir](
            start_layer, key=key
        )
        direction = self.inner_dir
        cur_node = start_node
        remain_nodes = term_nodes.copy()

        turn_node = (
            start_node[0] if self.outer_dir 
            else (0 if self.inner_dir else self.noc_w-1),
            start_node[1] if (1-self.outer_dir) 
            else (0 if self.inner_dir else self.noc_h-1)
        )

        while True:
            if cur_node in remain_nodes:
                remain_nodes.remove(cur_node)

            if len(remain_nodes) == 0:
                break

            if cur_node == turn_node:
                nxt_node = (
                    cur_node[0] + self.outer_dir, 
                    cur_node[1] + 1-self.outer_dir
                )
                turn_node = (
                    turn_node[0]+1 if self.outer_dir 
                    else self.noc_w-1-turn_node[0], 
                    self.noc_h-1-turn_node[1] 
                    if self.outer_dir else turn_node[1]+1
                )
                direction = 1- direction
            
            else:
                nxt_node = (
                    cur_node[0] + (1-self.outer_dir) 
                    *(-1 if direction else 1),
                    cur_node[1] + self.outer_dir 
                    *(-1 if direction else 1)
                )

            edges.append((cur_node, nxt_node))
            cur_node = nxt_node
            
        return edges

    def construct_one_tree(
        self, 
        src: PhysicalTile, 
        term_nodes: List[PhysicalTile]
    ) -> List[MeshEdge]:
        self.xy = list(zip(*term_nodes))
        edges = self.get_full_path(term_nodes)
        graph: nx.Graph = nx.Graph()
        graph.add_edges_from(edges)
        digraph: nx.DiGraph = nx.bfs_tree(graph, src)
        return list(digraph.edges)
    

class SP_PART_DRE(SP_FULL_DRE):

    def simplify_path(
        self, 
        src_node: PhysicalTile, 
        term_nodes: List[PhysicalTile], 
        edges: List[MeshEdge]
    ) -> List[MeshEdge]:
        
        def tup2(a, b):
            return (a, b) if self.outer_dir else (b, a)
        
        graph = nx.Graph()
        graph.add_edges_from(edges)
        direction = self.inner_dir
        slayer_id = min(self.xy[1-self.outer_dir])
        elayer_id = max(self.xy[1-self.outer_dir])

        for i in range(slayer_id, elayer_id):
            now = (1-direction) * (
                (self.noc_h if self.outer_dir 
                else self.noc_w) - 1)
            
            while True:
                if (tup2(i+1, now) not in term_nodes) and (
                    tup2(i, now) not in term_nodes):
                    if graph.has_edge(tup2(i-1, now), tup2(i, now)) and (
                        all(n[1-self.outer_dir] != i for n in term_nodes)):
                        break
                    graph.remove_edge(tup2(i, now), tup2(i+1, now))
                    # print("layer: ", i, "now: ", now)
                    nxt = now + (1 if direction else -1)
                    graph.remove_edge(tup2(i, now), tup2(i, nxt))
                    graph.remove_edge(tup2(i+1, now), tup2(i+1, nxt))
                    graph.add_edge(tup2(i, nxt), tup2(i+1, nxt))
                    now = nxt
                else:
                    break

            direction = 1 - direction

        digraph: nx.DiGraph = nx.bfs_tree(graph, src_node)
        return list(digraph.edges)

    def construct_one_tree(
        self, 
        src: PhysicalTile, 
        term_nodes: List[PhysicalTile]
    ) -> List[MeshEdge]:
        self.randomize_shape()
        self.xy = list(zip(*term_nodes))
        edges = self.get_full_path(term_nodes)
        print("term_nodes:", term_nodes)
        print("outer_dir:", self.outer_dir)
        print("inner_dir:", self.inner_dir)
        return self.simplify_path(
            src, term_nodes, edges
        )


__DRE_ACCESS_TABLE__ = {
    DREMethod.DYXY              :DyxyDRE,
    DREMethod.SP_FULL           :SP_FULL_DRE,
    DREMethod.SP_PART           :SP_PART_DRE
}