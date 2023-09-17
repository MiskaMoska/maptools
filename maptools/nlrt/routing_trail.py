import networkx as nx
from typing import List, Tuple, Literal, Optional
from maptools.core import (
    PhysicalTile, MeshEdge, ACG, TrailType,
    RouterPort
)

__all__ = [
    'RoutingTrail'
]

class RoutingTrail(object):

    def __init__(
        self, 
        sid: int,
        src: List[PhysicalTile], 
        dst: List[PhysicalTile],
        trail: List[MeshEdge],
        acg: ACG,
        trail_type: TrailType = TrailType.CAST
    ) -> None:
        '''
        This class stores the routing trail information of the connection,
        providing APIs for path drawing and VC configuration.
        
        Parameters
        ----------
        sid: int
            stream ID of the connection.

        src: List[PhysicalTile]
            source node(s), only one source node for cast and gather connections.

        dst: List[PhysicalTile]
            destination node(s), only one destination node for merge and gather connections.

        path: List[MeshEdge]
            the routing trail of the connection on the Mesh NoC.

        acg: ACG
            architecture characterization graph.

        trail_type: TrailType = TrailType.CAST
            type of the routing trail
        '''
        self._sid = sid
        self._src = src
        self._dst = dst
        self._trail = trail
        self._type = trail_type

        self.w = acg.w
        self.h = acg.h

        if self.is_cast():
            assert len(self._src) == 1, (
                "number of source node must be 1 for cast connection")
            
        elif self.is_merge():
            assert len(self._dst) == 1, (
                "number of destination node must be 1 for merge connection")

    @staticmethod
    def _route_calcu(
        now_node: Tuple, 
        desire_node: Tuple, 
        mode: Literal['i', 'o']
    ) -> RouterPort:
        if desire_node[0] < now_node[0]: # go west
            return (RouterPort.WEST_O if mode == 'o' 
                else RouterPort.EAST_I)
        
        if desire_node[0] > now_node[0]: # go east
            return (RouterPort.EAST_O if mode == 'o' 
                else RouterPort.WEST_I)
        
        if desire_node[1] > now_node[1]: # go south
            return (RouterPort.SOUTH_O if mode == 'o' 
                else RouterPort.NORTH_I)
        
        else: # go north
            return (RouterPort.NORTH_O if mode == 'o' 
                else RouterPort.SOUTH_I)
    
    @staticmethod
    def _get_link(edge: Tuple) -> Optional[Tuple]:
        sn, dn = edge[0], edge[1]

        if dn[0] > sn[0]:
            return ((sn[0], sn[1], RouterPort.EAST_O), 
                    (dn[0], dn[1], RouterPort.WEST_I))
        
        if dn[0] < sn[0]:
            return ((sn[0], sn[1], RouterPort.WEST_O), 
                    (dn[0], dn[1], RouterPort.EAST_I))
        
        if dn[1] > sn[1]:
            return ((sn[0], sn[1], RouterPort.SOUTH_O), 
                    (dn[0], dn[1], RouterPort.NORTH_I))
        
        if dn[1] < sn[1]:
            return ((sn[0], sn[1], RouterPort.NORTH_O), 
                    (dn[0], dn[1], RouterPort.SOUTH_I))
        
    def is_cast(self) -> bool:
        return self._type == TrailType.CAST

    def is_merge(self) -> bool:
        return self._type == TrailType.MERGE

    @property
    def cast_transitions(self) -> List[Tuple]:
        '''
        get cast intra-router transitions
        '''
        if not self.is_cast():
            raise AssertionError("invalid operation, this is not a cast connection")
        
        g = nx.DiGraph()
        g.add_edges_from(self._trail)
        transitions = []

        dst_nodes = self._dst
        for node in g.nodes:
            if g.in_degree(node) == 0: # root node
                src_port = (node[0], node[1], RouterPort.LOCAL_I)
                for dst_pos in g.successors(node):
                    out_port = (
                        node[0], node[1],
                        self._route_calcu(node, dst_pos, 'o')
                    )
                    transitions.append((src_port, out_port))

            else: # non-root node
                if g.out_degree(node) > 0: # routing node
                    src_pos = list(g.predecessors(node))[0]
                    src_port = (
                        node[0], node[1],
                        self._route_calcu(src_pos, node, 'i')
                    )
                    for dst_pos in g.successors(node):
                        dst_port = (
                            node[0], node[1],
                            self._route_calcu(node, dst_pos, 'o')
                        )
                        transitions.append((src_port, dst_port))

                if node in dst_nodes: # target node
                    src_pos = list(g.predecessors(node))[0]
                    src_port = self._route_calcu(src_pos, node, 'i')
                    src_port = (node[0], node[1], src_port)
                    dst_port = (node[0], node[1], RouterPort.LOCAL_O)
                    transitions.append((src_port, dst_port))

        return transitions
    
    @property
    def merge_transitions(self) -> List[Tuple]:
        '''
        get merge intra-router transitions
        '''
        if not self.is_merge():
            raise AssertionError("invalid operation, this is not a merge connection")
        
        g = nx.DiGraph()
        g.add_edges_from(self._trail)
        transitions = []

        for node in g.nodes:
            if g.out_degree(node) == 0: # root node
                dst_port = (node[0], node[1], RouterPort.LOCAL_O)
                for src_pos in g.predecessors(node):
                    src_port = (
                        node[0], node[1],
                        self._route_calcu(src_pos, node, 'i')
                    )
                    transitions.append((src_port, dst_port))

            else: # not root node, must be source node
                src_port = (node[0], node[1], RouterPort.LOCAL_I)
                dst_pos = list(g.successors(node))[0]
                dst_port = (
                    node[0], node[1],
                    self._route_calcu(node, dst_pos, 'o')
                )
                transitions.append((src_port, dst_port))

                for src_pos in g.predecessors(node):
                    src_port = (
                        node[0], node[1],
                        self._route_calcu(src_pos, node, 'i')
                    )
                    transitions.append((src_port, dst_port))

        return transitions

    @property           
    def links(self) -> List[Tuple]:
        '''
        get cast or merge inter-router links
        ''' 
        g = nx.DiGraph()
        g.add_edges_from(self._trail)
        return [self._get_link(edge) for edge in g.edges]
        
