import random
import queue
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
from typing import List, Tuple, Literal, Any, Dict
from functools import cached_property
from maptools.core import CTG, ACG
from maptools.core.typing import *
from abc import ABCMeta, abstractmethod
from copy import deepcopy

def random_steiner_tree_code(
    term_nodes: List[PhysicalTile],
    all_nodes: List[PhysicalTile]
) -> 'SteinerTreeCode':
    visited_nodes = []
    edge_list, spis = [], []

    remain_nodes = term_nodes.copy()
    init_node = random.choice(term_nodes)
    visited_nodes.append(init_node)
    remain_nodes.remove(init_node)

    for _ in range(len(term_nodes) - 1):
        select_node = random.choice(visited_nodes)
        target_node = random.choice(remain_nodes)
        edge_list.append((select_node, target_node))
        spis.append(random.choice([True, False]))

        remain_nodes.remove(target_node)
        visited_nodes.append(target_node)

    return SteinerTreeCode(
        edge_list, spis,
        random.choice(term_nodes),
        term_nodes, all_nodes
    )


class BaseCode(metaclass=ABCMeta):
    '''
    Base Class for Encoded Data Structures 
    '''
    @abstractmethod
    def mutation(self) -> None: ...

    @abstractmethod
    def undo_mutation(self) -> None: ...

    @abstractmethod
    def decode(self) -> Any: ...

    @abstractmethod
    def reset(self) -> None: ...


class LayoutPatternCode(BaseCode):

    def __init__(
        self,
        ctg: CTG,
        acg: ACG,
    ) -> None:
        '''
        Encoded Data Structure for Layout Pattern.

        Parameter
        ---------
        ctg: CTG
            Communication Trace Graph of the AI task.

        acg: ACG
            Architecture Characterization Graph of the NoC.
        '''
        # A list of the number of tiles in each cluster
        self.cluster_list: List[int] = []

        # A list of cluster-index-represented (CIR) tiles
        self.cir_tiles: List[CIRTile] = []

        # A list of indices of all physical tiles
        self.phy_indices: List[int] = []

        # A dictionary with CIR tiles as keys and logical tile as values
        self.log_dict: Dict[CIRTile, LogicalTile] = {}

        # A dictionary with physical tiles indices as keys and physical tiles as values
        self.phy_dict: Dict[int, PhysicalTile] = {}

        # A dictionary with physical tile as keys and physical tile indices as values
        # This is the inverted-mapped version of `self.phy_dict`
        self.inv_phy_dict: Dict[PhysicalTile, int] = {}

        # The core data structure of LPC
        # A dictionary with CIR tiles as keys and physical tile indices as values
        self.map: CIR2PhyIdxMap = {}

        self.noc_w, self.noc_h = acg.w, acg.h
        self.phy_indices = list(range(len(acg.nodes)))
        self.phy_dict = {i: n for i, n in enumerate(acg.nodes)}
        self.inv_phy_dict = {n: i for i, n in enumerate(acg.nodes)}

        for i, (_, tiles) in enumerate(ctg.clusters):
            self.cluster_list.append(len(tiles))
            for k, tile in enumerate(tiles):
                cir_tile = (i, k)
                self.cir_tiles.append(cir_tile)
                self.log_dict[cir_tile] = tile

        self.reset()

    def mutation(self) -> None:
        k1, k2 = random.sample(list(self.map.keys()), 2)
        self.last_swap = (k1, k2)
        self.map[k1], self.map[k2] = self.map[k2], self.map[k1]

    def undo_mutation(self) -> None:
        k1, k2 = self.last_swap
        self.map[k1], self.map[k2] = self.map[k2], self.map[k1]

    def decode(self) -> None:
        '''
        The LPC is actually a simple dictionary and does not need decoding,
        so this function is not used 
        '''
        return
    
    def reset(self) -> None:
        random.shuffle(self.phy_indices)
        for i, cir in enumerate(self.cir_tiles):
            self.map[cir] = self.phy_indices[i]

    def _search_cluster(
        self,
        x: CIR2PhyIdxMap, 
        inv_x: Dict[int, CIRTile], 
        cluster_id: int,
        tile: PhysicalTile, 
        marked: List[int]
    ) -> None:
        '''
        This method searched through a cluster and marks physical tiles 
        as many as possible following a patch-manner, if the number of 
        marked tiles equals the number of tiles in the current cluster, 
        it means the current cluster is mapped to a patch, otherwise, 
        it is not mapped to a patch.

        Parameters
        ----------
        x: CIR2PhyIdxMap
            the layout pattern

        inv_x: Dict[int, CIRTile]
            the inverted-mapped version of `x`

        cluster_id: int
            the cluster ID of the current cluster being searched
        
        tile: PhysicalTile
            the current physical tile being searched

        marked: List[int]
            a list of the physical tile indices that have been marked
        '''
        pidx = self.inv_phy_dict[tile]
        if pidx in inv_x: 
            logic = inv_x[pidx]
            if logic[0] != cluster_id: # belongs to other cluster
                return
        else: # an idle tile that is not mapped
            return
        
        if pidx in marked: # already marked
            return
        
        # If a physical tile meets three requirements:
        # 1. A tile that has been mapped
        # 2. A tile belonging to the current cluster
        # 3. A tile that is not marked yet
        # then current physical tile should be marked
        marked.append(pidx)

        if tile[0] != 0:
            self._search_cluster(x, inv_x, cluster_id, (tile[0]-1, tile[1]), marked)

        if tile[0] != self.noc_w-1:
            self._search_cluster(x, inv_x, cluster_id, (tile[0]+1, tile[1]), marked)

        if tile[1] != 0:
            self._search_cluster(x, inv_x, cluster_id, (tile[0], tile[1]-1), marked)

        if tile[1] != self.noc_h-1:
            self._search_cluster(x, inv_x, cluster_id, (tile[0], tile[1]+1), marked)
    
    def _all_clusters_in_a_patch(self) -> bool:
        '''
        This method checks the valadity of the given layout pattern,
        that is, whether all clusters are mapped to a patch region.
        '''
        inv_x = {v: k for k, v in self.map.items()}

        for cluster_id, num in enumerate(self.cluster_list):
            start_cir = (cluster_id, 0)
            start_phy_tile = self.phy_dict[self.map[start_cir]]

            marked = []
            self._search_cluster(self.map, inv_x, cluster_id, start_phy_tile, marked)
            if len(marked) != num:
                print(f'non-patch detected at cluster {cluster_id}')
                return False
            
        return True
    
    @property
    def is_valid(self) -> bool:
        return self._all_clusters_in_a_patch()


class SteinerTreeCode(BaseCode, nx.Graph):

    def __init__(
        self, 
        edges: List[ArbitaryEdge], 
        spis: List[bool], 
        root: PhysicalTile,
        term_nodes: List[PhysicalTile],
        all_nodes: List[PhysicalTile]
    ) -> None:
        '''
        Encoded Data Structure for Steiner Tree.
        
        Parameters
        ----------
        edges: List[ArbitaryEdge]
            edge list of the spanning tree. 
            spanning tree is the base structure for steiner tree, the steiner tree
            is built according to the spanning tree edges, the steiner point 
            indicators, and the given root node. 
            the `SteinerTreeCode` itself is actually a graph of the spanning tree.
            running the `SteinerTreeCode.decode` method results in the automatical 
            construction of the corresponding steiner tree.

        spis: List[bool]
            steiner point indicators.
            determines whether to use XY routing or YX routing when building raw
            steiner trees based on the spanning tree edges. 

        root: PhysicalTile
            root node of the tree, for DFS and BFS.
            under different root node placements, it can generate different steiner 
            tree structures for DFS and BFS.

        term_nodes: List[PhysicalTile]
            terminal nodes, including source node (sender) and sink nodes (receivers).
            note that source node is not equivalent to root node, if the source node
            is not the root, it can also successfully send messages to the sink nodes
            following the edges of the steiner tree.
            the root node is nothing but a concept for DFS or BFS searching.

        all_nodes: List[PhysicalTile]
            all nodes in network on chip, it must cover the hanan plane for the given
            terminal nodes, it describes the constrained space that the multicast can 
            be routed to, any node in `all_nodes` can be a routing node for multicast.
        '''
        if len(edges) == 0:
            raise ValueError("got empty edge list")
        
        if len(edges) != len(spis):
            raise ValueError("got edge list length not match spi list")

        if root not in term_nodes:
            raise RuntimeError(
                f"root {root} not in terminal nodes: {term_nodes}")

        super().__init__()
        super(BaseCode, self).__init__()

        self.root = root
        self.all_nodes = all_nodes
        self.term_nodes = term_nodes
        self.add_nodes_from(all_nodes)

        for (edge, spi) in zip(edges, spis):
            self.add_edge(*edge, spi=spi)

        self.node_pos = {n: (n[0], -n[1]) for n in self.all_nodes}
        self.node_color = {n: 'red' if n in self.term_nodes 
                            else 'black' for n in self.all_nodes}
        self.node_color[self.root] = 'green'

    def mutation(self) -> None:
        a = random.random()
        method = True if random.random() < 0.7 else False
        
        if method: # replace edge
            edge = random.choice(list(self.edges))
            self.remove_edge(*edge) # remove an edge randomly

            part1 = nx.node_connected_component(self, self.root)
            part2 = set(self.term_nodes) - part1
            node1 = random.choice(list(part1))
            node2 = random.choice(list(part2))

            spi = random.choice([True, False])
            self.add_edge(node1, node2, spi=spi)
        
        else: # relocate root
            while True:
                r = random.choice(self.term_nodes)
                if r != self.root: break

            # self.node_color[self.root] = 'red'
            # self.node_color[r] = 'green'
            self.root = r

    def undo_mutation(self) -> None:
        '''
        The mutation operation of STC not inversable,
        so this function is not used.
        '''
        return

    def decode(self) -> nx.Graph:
        self._decode_to_raw_steiner()
        # self._decode_to_true_steiner(method='dfs')
        self._decode_to_true_steiner(method='bfs')
        return self.tstg_b
    
    def reset(self) -> None:
        '''
        The STC does not support resetting, the resetting is achieved 
        by RPC by calling the function `random_steiner_tree_code`.
        '''
        return

    def _decode_to_raw_steiner(self) -> None:
        self.rstg = nx.Graph() # raw steiner tree graph
        self.rstg.add_nodes_from(self.all_nodes)
        for edge in self.edges:
            edge_data = self.get_edge_data(*edge)
            spi = edge_data['spi']
            self._add_steiner_route(self.rstg, edge, spi)

    @staticmethod
    def _add_steiner_route(
        rstg: nx.Graph,
        spanning_edge: ArbitaryEdge,
        spi: bool
    ) -> None:
        src, dst = spanning_edge
        cur = src

        while True:
            if cur == dst:
                return
            st = [0, 0]
            i = 1 if spi else 0

            if cur[i] == dst[i]:
                st[1-i] = 1 if dst[1-i] > cur[1-i] else -1
            else:
                st[i] = 1 if dst[i] > cur[i] else -1
            nxt = (cur[0] + st[0], cur[1] + st[1])

            rstg.add_edge(cur, nxt)
            cur = nxt

    def _decode_to_true_steiner(
        self, 
        method: Literal['dfs', 'bfs'] = 'dfs'
    ) -> None:
        if method == 'dfs':
            self.tstg_d = nx.Graph() # true steiner tree graph by dfs
            self.tstg_d.add_nodes_from(self.all_nodes)
            visited_nodes, remain_edges = [], []
            self._dfs(self.rstg, self.root, visited_nodes, remain_edges)
            self.tstg_d.add_edges_from(remain_edges)

        elif method == 'bfs':
            self.tstg_b = nx.Graph() # true steiner tree graph by bfs
            self.tstg_b.add_nodes_from(self.all_nodes)
            visited_nodes = []
            self._bfs(self.rstg, self.tstg_b, self.root, visited_nodes)
    
    def _dfs(
        self,
        g: nx.Graph, 
        cur: Tuple, 
        visited: List[Tuple], 
        remain: List[Tuple]
    ) -> bool:
        visited.append(cur)
        flag, leaf = False, True
        for nxt in g.neighbors(cur):
            if nxt not in visited:
                remain.append((cur, nxt))
                if self._dfs(g, nxt, visited, remain): # (cur, nxt) is not a leaf branch
                    flag = True
                else: # (cur, nxt) is a leaf branch
                    remain.remove((cur, nxt))
            else:
                leaf = False

        if cur in self.term_nodes:
            return True
        else: 
            return leaf or flag

    def _bfs(
        self,
        g: nx.Graph,
        tg: nx.Graph,
        start: Tuple, 
        visited: List[Tuple]
    ) -> None:          
        fifo = queue.Queue()  
        rethink_fifo = queue.Queue()           
        fifo.put(start)           
        visited.append(start)

        while True:
            if fifo.empty() and rethink_fifo.empty():
                break

            if not fifo.empty():
                node = fifo.get()
                endnode = True
                for nxt in g.neighbors(node):
                    if nxt not in visited:
                        fifo.put(nxt)
                        visited.append(nxt)
                        tg.add_edge(node, nxt)
                        endnode = False
                    
                if endnode and (node not in self.term_nodes):
                    pred = list(tg.neighbors(node))[0]
                    tg.remove_edge(pred, node)
                    rethink_fifo.put(pred)
            
            if not rethink_fifo.empty():
                renode = rethink_fifo.get()
                if tg.degree(renode) == 1 and renode not in self.term_nodes:
                    repred = list(tg.neighbors(renode))[0]
                    tg.remove_edge(repred, renode)
                    rethink_fifo.put(repred)

    def draw_graph(self, graph: nx.Graph, ax: plt.Axes) -> None:
        nx.draw(
            graph,
            self.node_pos, 
            node_size=40, 
            width=1, 
            node_color=list(self.node_color.values()),
            ax=ax
        )

    @cached_property
    def reroot_possibility(self) -> float:
        pass

    def draw4(self, ax1, ax2, ax3, ax4) -> None:
        self.draw_graph(self, ax1)
        self.draw_graph(self.rstg, ax2)
        self.draw_graph(self.tstg_b, ax3)
        self.draw_graph(self.tstg_d, ax4)

        ax1.set_title('spanning tree', y=-0.1)
        ax2.set_title('raw steiner', y=-0.1)
        ax3.set_title('steiner bfs', y=-0.1)
        ax4.set_title('steiner dfs', y=-0.1)


class RoutingPatternCode(BaseCode):

    def __init__(self, ctg: CTG, acg: ACG, layout: Any) -> None:
        '''
        Encoded Data Structure for Routing Pattern.
        Assembling multiple STCs (Steiner Tree Code), each for a communication
        obtained from `ctg`, the node matching is obtained from `layout`.
        
        Parameters
        ----------
        ctg: CTG
            Communication Trace Graph of the AI Task.

        acg: ACG
            Architecture Characterization Graph of the NoC.

        layout: LayoutResult
            Layout result from obtained from `LayoutDesigner`.
        '''
        self.noc_w = acg.w
        self.noc_h = acg.h
        self.all_nodes = acg.nodes

        self.comms: List[str] = [] # stores all comms
        self.decode_queue: List[str] = [] # stores all comms to be decoded

        self.stc_dict: Dict[str, SteinerTreeCode] = {} # steiner tree code dict
        self.src_dict: Dict[str, PhysicalTile] = {} # src node dict
        self.term_dict: Dict[str, List[PhysicalTile]] = {} # terminal nodes dict
        self.path_dict: Dict[str, List[MeshEdge]] = {} # communication path dict
        self.is_gather_dict: Dict[str, bool] = {} # indicates whether each communication is gather or not

        # initialize dictionaries for cast/gather connections
        connect_classes = [ctg.cast_trees, ctg.gather_pairs]
        for i, connects in enumerate(connect_classes):
            for c, src, dst in connects:
                physrc = layout[src]
                phydst = [layout[d] for d in dst]
                term_nodes = phydst + [physrc]
                self.term_dict[c] = term_nodes

                self.comms.append(c)
                self.src_dict[c] = physrc
                self.is_gather_dict[c] = bool(i)

        self.choice_probs = self.gen_choice_probs()
        self.reset()

    def gen_choice_probs(self) -> List[float]:
        '''
        Through experiments we found that linear probability distribution 
        performs better than exponential probability distribution.
        '''
        node_nums = [len(self.term_dict[k]) for k in self.comms]
        # exp_list = np.exp(np.array(node_nums))
        # exp_sum = np.sum(exp_list)
        exp_list = node_nums
        exp_sum = sum(node_nums)
        return [exp / exp_sum for exp in exp_list]

    def mutation(self) -> None:
        comm, *_ = random.choices(self.comms, weights=self.choice_probs)
        target_stc = self.stc_dict[comm]
        self.bak_comm = comm
        self.bak_stc = deepcopy(target_stc)
        target_stc.mutation()
        self.decode_queue.append(comm)

    def undo_mutation(self) -> None:
        self.stc_dict[self.bak_comm] = self.bak_stc
        self.decode_queue.append(self.bak_comm)

    def decode(self) -> None:
        while len(self.decode_queue) > 0:
            comm = self.decode_queue[-1]
            self.decode_queue.pop(-1)
            stc = self.stc_dict[comm]
            tstg: nx.Graph = stc.decode()
            tree: nx.DiGraph = nx.bfs_tree(tstg, self.src_dict[comm])
            self.path_dict[comm] = list(tree.edges)

    def reset(self) -> None:
        for comm in self.comms:
            term_nodes = self.term_dict[comm]
            self.stc_dict[comm] = random_steiner_tree_code(
                term_nodes, self.all_nodes
            )
        self.fill_decode_queue()
    
    def empty_decode_queue(self) -> None:
        self.decode_queue = []

    def fill_decode_queue(self) -> None:
        for comm in self.comms:
            self.decode_queue.append(comm)
            