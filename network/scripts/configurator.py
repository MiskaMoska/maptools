import pickle
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
        self.xxx_paths : Dict[str, Dict[str, Any]]
            generated from `NocMapper` or read from mapsave files.
            xxx can be any of [cast, merge, gather].
            Stores the mapped paths and corresponding attributes for each connection type.
            `self.xxx_paths` = {'connection_name' : `path_dict`}
            where `path_dict` = {'sid' : int, 'src' : List[Tuple], 'dst' : List[Tuple], 
                                'path' : List[Tuple[Tuple]], 'load_ratio' : float, ....}}
        '''
        self.cast_paths = cast_paths
        self.merge_paths = merge_paths
        self.gather_paths = gather_paths
        self.root_dir = 'c:/git/nvcim-comm'
        self.__dict__.update(kwargs)


