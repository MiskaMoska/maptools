import pickle
import numpy as np
from typing import Tuple, List, Any, Optional, Dict
from functools import cached_property

class Configurator(object):

    def __init__(self,           
                    cast_paths: Dict[str, Dict[str, Any]],
                    merge_paths: Dict[str, Dict[str, Any]],
                    gather_paths: Dict[str, Dict[str, Any]],
                    network_dir: str = '/mnt/c/git/'
                    ) -> None:
        '''
        Convert the paths obtained from `NocMapper` to network configuration format,
        which can be configured to the network directly, then generate the `network_conifg.svh`
        file and the routing table roms.

        Parameters
        ----------
        cast_paths
        '''
