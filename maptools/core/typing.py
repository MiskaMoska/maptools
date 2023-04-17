import numpy as np
from typing import Tuple, List, Dict, Any, Literal

__all__ = [
    'LogicalTile',
    'PhysicalTile',
    'Path',
    'Paths',
    'TileConfig',
    'OperatorConfig',
    'DeviceParams'
]

LogicalTile = Tuple[int, int, int, int]
PhysicalTile = Tuple[int, int]

Path = Tuple[PhysicalTile, PhysicalTile]
Paths = List[Path]

TileConfig = Dict[str, Any]
OperatorConfig = Dict[str, Any]
DeviceParams = Dict[str, np.ndarray]
