import numpy as np
from typing import Tuple, List, Dict, Any, Literal, TypeVar

LogicalTile = Tuple[int, int, int, int]
PhysicalTile = Tuple[int, int]

TileConfig = Dict[str, Any]
OperatorConfig = Dict[str, Any]
ModelParams = Dict[str, np.ndarray]

# for layout and routing design
CIRTile = Tuple[int, int]
CIR2PhyIdxMap = Dict[CIRTile, int]
Logical2PhysicalMap = Dict[LogicalTile, PhysicalTile]

ArbitaryEdge = Tuple[PhysicalTile, PhysicalTile]
MeshEdge = Tuple[PhysicalTile, PhysicalTile]
