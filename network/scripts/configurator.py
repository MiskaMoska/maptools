import os
import pickle
import networkx as nx
import numpy as np
from typing import Tuple, List, Any, Optional, Dict
from functools import cached_property

class Configurator(object):

    def __init__(self,           
                    cast_paths: Dict[str, Dict[str, Any]],
                    merge_paths: Dict[str, Dict[str, Any]],
                    gather_paths: Dict[str, Dict[str, Any]],
                    *args, **kwargs
                    ) -> None:
        '''
        Convert the paths obtained from `NocMapper` to network configuration format,
        which can be configured to the network directly, then generate the network config 
        header files and the routing table roms.

        Parameters
        ----------
        xxx_paths : Dict[str, Dict[str, Any]]
            generated from `NocMapper` or read from mapsave files.
            xxx can be any of [cast, merge, gather].
            Stores the mapped paths and corresponding attributes for each connection type.
            `self.xxx_paths` = {'connection_name' : `path_dict`}
            where `path_dict` = {'sid' : int, 'src' : List[Tuple], 'dst' : List[Tuple], 
                                'path' : List[Tuple[Tuple]], 'load_ratio' : float, ....}
        
        Key Members
        -----------
        self.cast_config : Dict[Tuple, List[Tuple]]
            var[(0, 0)] = [(      2      ,      0      ,      0      ),(...),(...),...]
                   ^              ^             ^             ^                 ^
            router position   input port   output port    stream ID        other paths
            where 0 for local, 1 for west, 2 for east, 3 for vert0, 4 for vert1

        self.gather_config : Dict[Tuple, List[Tuple]]
            same as self.cast_config, but:
            0 for local, 1 for west, 2 for east, 3 for north, 4 for south

        self.merge_config : Dict[Tuple, Dict[str, Any]]
            var[(3, 5)] = {'input_mask': [1, 0, 1, 0, 1], 'output_sel': [0, 1, 0, 0, 0] }
            where 'input_mask' and 'output_sel' are both lists, whose index follows:
            0 for local, 1 for west, 2 for east, 3 for north, 4 for south
        '''
        self.cast_paths = cast_paths
        self.merge_paths = merge_paths
        self.gather_paths = gather_paths
        self.root_dir = os.environ.get('NVCIM_HOME')
        self.__dict__.update(kwargs)

        # configuration results
        self.cast_config: Dict[Tuple, List[Tuple]] = dict()
        self.gather_config: Dict[Tuple, List[Tuple]] = dict()
        self.merge_config = Dict[Tuple, Dict[str, Any]] = dict()

        def _cast_route_channel(src: Tuple, dst: Tuple, chan: int) -> int:
            if dst[0] > src[0]: # east
                return 2
            elif dst[0] < src[0]: # west
                return 1
            else: # south
                return 3 # only use vert0 channel

        def _gather_route_channel(src: Tuple, dst: Tuple, chan: int) -> int:
            if dst[0] > src[0]: # east
                return 2
            elif dst[0] < src[0]: # west
                return 1
            if dst[1] > src[1]: # south
                return 3

        def run_cast_config(self) -> None:
            for connect in self.cast_paths.values():
                g = nx.MultiDiGraph()
                g.add_edges_from(connect['path'])
                dst_nodes = connect['dst']
                for node in g.nodes: # add intra-router paths
                    if g.in_degree(node) == 0: # root node
                        src_chan = 0 # local
                        for dst_pos in g.successors(node):
                            out_chan = self._route_channel(node, dst_pos, 'o')
                            out_chan = (node[0], node[1], out_chan)
                            self.cast_graph.add_edge(src_chan, out_chan)


