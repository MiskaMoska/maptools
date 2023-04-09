'''
Types for mapping
TODO specify the relationship xbar type and tile type
'''
from typing import Tuple, List

LogXbar = Tuple[int, int, int, int]
PhyXbar = Tuple[int, int]

Path = Tuple[PhyXbar, PhyXbar]
Paths = List[Path]
