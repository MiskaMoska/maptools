import os
import pickle
import networkx as nx
from typing import Tuple, List, Any, Dict
from maptools.hardware.fc_plan import fc_plan
from maptools.core import ROOT_DIR

__all__ = ['NocConfig']

class NocConfig(object):

    def __init__(
        self, 
        w: int, 
        h: int,         
        cast_paths: Dict[str, Dict[str, Any]],
        merge_paths: Dict[str, Dict[str, Any]],
        gather_paths: Dict[str, Dict[str, Any]],
        **kwargs: Any
    ) -> None:
        '''
        Convert the paths obtained from `NocMapper` to network configuration format,
        which can be configured to the network directly, then generate the network config 
        header files and the routing table roms.

        Parameters
        ----------
        w : int
            network width
        
        h : int
            network height
        
        xxx_paths : Dict[str, Dict[str, Any]]
            generated from `NocMapper` or read from mapsave files.
            xxx can be any of [cast, merge, gather].
            Stores the mapped paths and corresponding attributes for each connection type.
            `self.xxx_paths` = {'connection_name' : `path_dict`}
            where `path_dict` = {'sid' : int, 'src' : List[Tuple], 'dst' : List[Tuple], 
                                'path' : List[Tuple[Tuple]], 'load_ratio' : float, ....}
        
        kwargs : Dict
            mapname : str = 'newmap'
                Map name

        Key Members
        -----------
        self.cast_config : Dict[Tuple, List[Tuple]]
            var[(0, 0)] = [(      2,            0,            0      ),(...),(...),...]
                   ^              ^             ^             ^                 ^
            router position   input port   output port    stream ID        other paths
            where 0 for local, 1 for west, 2 for east, 3 for vert0, 4 for vert1

        self.gather_config : Dict[Tuple, List[Tuple]]
            same as self.cast_config, but:
            0 for local, 1 for west, 2 for east, 3 for north, 4 for south

        self.merge_config : Dict[Tuple, Dict[str, Any]]
            var[(3, 5)] = {'input_mask': [1, 0, 1, 0, 1], 'output_sel': [0, 1, 0, 0, 0] }
            where 'input_mask' is list, 'output_sel' is int, whose indices follows:
            0 for local, 1 for west, 2 for east, 3 for north, 4 for south
        '''
        self.w = w
        self.h = h
        self.cast_paths = cast_paths
        self.merge_paths = merge_paths
        self.gather_paths = gather_paths
        self._assertion()
        self.mapname = 'newmap'
        self.__dict__.update(kwargs)

        # configuration results
        self.cast_config: Dict[Tuple, List[Tuple]] = dict()
        self.gather_config: Dict[Tuple, List[Tuple]] = dict()
        self.merge_config: Dict[Tuple, Dict[str, Any]] = dict()

    def _assertion(self) -> None:
        assert len(self.cast_paths) <= 1000, f"number of cast streams exceeded 1000, got {len(self.cast_paths)}"
        assert len(self.gather_paths) <= 1000, f"number of gather streams exceeded 1000, got {len(self.gather_paths)}"

    @staticmethod
    def _cast_route_channel(now: Tuple, neigh: Tuple) -> int:
        if neigh[0] > now[0]: # east
            return 2 
        elif neigh[0] < now[0]: # west
            return 1 
        else: # south
            return 3 # only use vert0 channel

    @staticmethod
    def _gather_route_channel(now: Tuple, neigh: Tuple) -> int:
        if neigh[0] > now[0]: # east
            return 2 
        elif neigh[0] < now[0]: # west
            return 1 
        if neigh[1] > now[1]: # south
            return 4 
        elif neigh[1] < now[1]: # north
            return 3 

    def run_cast_config(self) -> None:
        for connect in self.cast_paths.values():
            g = nx.MultiDiGraph()
            g.add_edges_from(connect['path'])
            sid = connect['sid']
            dst_nodes = connect['dst']
            for node in g.nodes: # add intra-router paths
                if node not in self.cast_config:
                    self.cast_config[node] = []
                
                if g.in_degree(node) == 0: # root node
                    for dst_pos in g.successors(node):
                        out_chan = self._cast_route_channel(node, dst_pos)
                        self.cast_config[node].append((0, out_chan, sid))

                else: # not root node
                    if g.out_degree(node) > 0: # routing node
                        src_pos = list(g.predecessors(node))[0]
                        in_chan = self._cast_route_channel(node, src_pos)
                        for dst_pos in g.successors(node):
                            out_chan = self._cast_route_channel(node, dst_pos)
                            self.cast_config[node].append((in_chan, out_chan, sid))

                    if node in dst_nodes: # target node
                        src_pos = list(g.predecessors(node))[0]
                        in_chan = self._cast_route_channel(node, src_pos)
                        self.cast_config[node].append((in_chan, 0, sid))

    def run_gather_config(self) -> None:
        for connect in self.gather_paths.values():
            g = nx.MultiDiGraph()
            g.add_edges_from(connect['path'])
            sid = connect['sid']
            for node in g.nodes: # add intra-router paths
                if node not in self.gather_config:
                    self.gather_config[node] = []
                
                if g.in_degree(node) == 0: # start node
                    dst_pos = list(g.successors(node))[0]
                    out_chan = self._gather_route_channel(node, dst_pos)
                    self.gather_config[node].append((0, out_chan, sid))
                
                elif g.out_degree(node) == 0: # dst node
                    src_pos = list(g.predecessors(node))[0]
                    in_chan = self._gather_route_channel(node, src_pos)
                    self.gather_config[node].append((in_chan, 0, sid))

                else: # routing node
                    src_pos = list(g.predecessors(node))[0]
                    dst_pos = list(g.successors(node))[0]
                    in_chan = self._gather_route_channel(node, src_pos)
                    out_chan = self._gather_route_channel(node, dst_pos)
                    self.gather_config[node].append((in_chan, out_chan, sid))

    def run_merge_config(self) -> None:
        g = nx.MultiDiGraph()
        g.add_nodes_from([(x, y) for x in range(self.w) for y in range(self.h)])
        merge_nodes = [connect['dst'][0] for connect in self.merge_paths.values()]

        for connect in self.merge_paths.values():
            g.add_edges_from(connect['path'])

        for node in g.nodes:
            x = node[0]
            y = node[1]
            neigh_nodes = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            input_mask = []
            output_sel = []
            if node not in merge_nodes:
                input_mask.append(1) # non-merge node has local input
                output_sel.append(0) # non-merge node has no local output
            else:
                input_mask.append(0) # merge node has no local input
                output_sel.append(1) # merge node has local output
            for neigh_node in neigh_nodes:
                if neigh_node in g.predecessors(node):
                    input_mask.append(1)
                else:
                    input_mask.append(0)
                if neigh_node in g.successors(node):
                    output_sel.append(1)
                else:
                    output_sel.append(0)
            self.merge_config[node] = {'input_mask': input_mask, 'output_sel': output_sel}

    def run_config(self) -> None:
        self.run_cast_config()
        self.run_merge_config()
        self.run_gather_config()

    def save_config(self, file_name: str = 'cfginfo') -> None:
        '''
        save the configuration results as pkl sequence
        '''
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        file_dir = os.path.join(save_dir, file_name+'.pkl')
        info_dict = dict()

        info_dict['network_width'] = self.w
        info_dict['network_height'] = self.h

        info_dict['cast_config'] = self.cast_config
        info_dict['merge_config'] = self.merge_config
        info_dict['gather_config'] = self.gather_config

        info_dict['cast_fc'] = fc_plan(self.cast_paths, self.cast_config)
        info_dict['gather_fc'] = fc_plan(self.gather_paths, self.gather_config)

        with open(file_dir, 'wb') as f:
            pickle.dump(info_dict, f)
        print(f"noc config info has been written to {file_dir}")
