import numpy as np
from typing import Tuple, List, Dict, Any, Literal, TypeVar

__all__ = [
    'LogicalTile',
    'PhysicalTile',
    'Path',
    'Paths',
    'TileConfig',
    'OperatorConfig',
    'ModelParams'
]

LogicalTile = TypeVar('LogicalTile', bound=Tuple[int, int, int, int])
PhysicalTile = Tuple[int, int]

Path = Tuple[PhysicalTile, PhysicalTile]
Paths = List[Path]

TileConfig = Dict[str, Any]
OperatorConfig = Dict[str, Any]
ModelParams = Dict[str, np.ndarray]
