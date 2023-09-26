import os
import pickle
import networkx as nx
from copy import deepcopy
from functools import cached_property
from typing import Dict, List, Any, Tuple, Mapping, Callable, Generator
from maptools.nlrt import RoutingTrail, LayoutResult
from maptools.utils import invoke_once
from maptools.hardware.routing_configurator import RoutingConfigurator
from maptools.core import (
    MeshEdge, Connection, ROOT_DIR,
    ACG, CTG, RouterPort, PhysicalTile)

__all__ = ['HardwareDeployer']

class HardwareDeployer(object):

    def __init__(
        self,
        cast_trails: Mapping[Connection, RoutingTrail],
        merge_trails: Mapping[Connection, RoutingTrail],
        acg: ACG,
        ctg: CTG,
        layout: LayoutResult,
        **kwargs: Any
    ) -> None:
        '''
        This class generates the hardware configuration information and writes it
        to the target files.

        Parameters
        ----------
        cast_trails: Mapping[Connection, RoutingTrail]
            all cast trails with the connection name as keys and the routing trail as values.

        merge_trails: Mapping[Connection, RoutingTrail]
            all merge trails with the connection name as keys and the routing trail as values.

        acg: ACG
            architecture characterization graph.

        ctg: CTG
            communication trace graph.

        layout: LayoutResult
            layout result containing the physical-to-logical mapping information.
        '''
        self.rc = RoutingConfigurator(
            cast_trails, merge_trails,
            acg, ctg, layout
        )
        self.w = acg.w
        self.h = acg.h
        self.ctg = ctg
        self.layout = layout

        self.mapname = 'newmap'
        self.__dict__.update(kwargs)

    @cached_property
    def tile_config(self) -> Dict[str, Any]:
        '''
        A dictionary with physical tile as keys and configuration info as values.
        Tile configuration information for system simulation.
        '''
        # get the original tile configurations from CTG
        res = {self.layout[k] : self.ctg.dicts[k] for k in self.ctg.tile_nodes}

        # now merge cast and gather VC information to the dictionary
        clic, cloc = self.rc.get_clic(), self.rc.get_cloc()
        for tile, cfg in res.items():
            cfg['cast_in_vc'] = clic[tile][0]
            cfg['gather_in_vc'] = clic[tile][1]
            cfg['cast_out_vc'] = cloc[tile][0]
            cfg['gather_out_vc'] = cloc[tile][1]

        return res

    @property 
    def p2p_casts(self) -> Generator:
        '''
        cast information for P2P simulation.
        '''
        for _, root_node, dst_nodes in self.ctg.cast_trees:
            yield (self.layout[root_node], [self.layout[d] for d in dst_nodes])
    
    @property
    def p2p_merges(self) -> Generator:
        '''
        merge information for P2P simulation.
        '''
        for _, src_nodes, root_node in self.ctg.merge_trees:
            yield ([self.layout[s] for s in src_nodes], self.layout[root_node])

    @property
    def p2p_gathers(self) -> Generator:
        '''
        gather information for P2P simulation.
        '''
        for _, src_node, dst_nodes in self.ctg.gather_pairs:
            yield (self.layout[src_node], [self.layout[d] for d in dst_nodes])
    
    def save_config(self) -> None:
        save_dir = os.path.join(ROOT_DIR, 'mapsave', self.mapname, 'hwconfig')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        self.save_general_config(os.path.join(save_dir, 'general_config.pkl'))
        self.save_cast_config(os.path.join(save_dir, 'cast_config.pkl'))
        self.save_merge_config(os.path.join(save_dir, 'merge_config.pkl'))

    def save_general_config(self, file_path: str) -> None:
        cfg_dict = {}

        # write network size info
        cfg_dict['network_width'] = self.w
        cfg_dict['network_height'] = self.h

        # write noc mapping info
        cfg_dict['match_dict'] = self.layout.l2p_map
        cfg_dict['tile_config'] = self.tile_config

        # write p2p communication info
        cfg_dict['p2p_casts'] = list(self.p2p_casts)
        cfg_dict['p2p_merges'] = list(self.p2p_merges)
        cfg_dict['p2p_gathers'] = list(self.p2p_gathers)
        
        # write injection and ejection info
        cfg_dict['tail_tiles'] = [self.layout[t] for t in self.ctg.tail_tiles]
        cfg_dict['injects'] = self.rc.get_injects()
        cfg_dict['ejects'] = self.rc.get_ejects()

        with open(file_path, 'wb') as f:
            pickle.dump(cfg_dict, f)
        print(f"general configurations has been written to {file_path}") 

    def save_cast_config(self, file_path: str) -> None:
        with open(file_path, 'wb') as f:
            pickle.dump(self.rc.get_crt(), f)
        print(f"cast configurations has been written to {file_path}")

    def save_merge_config(self, file_path: str) -> None:
        with open(file_path, 'wb') as f:
            pickle.dump(self.rc.get_mrt(), f)
        print(f"merge configurations has been written to {file_path}")
