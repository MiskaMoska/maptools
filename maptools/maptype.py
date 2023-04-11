'''
Types for mapping
TODO specify the relationship xbar type and tile type
'''
import numpy as np
from typing import Tuple, List, Dict, Any, Literal

LogXbar = Tuple[int, int, int, int]
PhyXbar = Tuple[int, int]

Path = Tuple[PhyXbar, PhyXbar]
Paths = List[Path]

XbarConfig = Dict[str, Any]
OperatorConfig = Dict[str, Any]
DeviceParams = Dict[str, np.ndarray]
