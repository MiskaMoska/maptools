import random
from maptools.core.typing import *
from typing import List, Tuple, Literal
from maptools.nlrt.encoding import SteinerTreeCode

def random_steiner_tree_code(
    term_nodes: List[PhysicalTile],
    all_nodes: List[PhysicalTile]
) -> SteinerTreeCode:
    visited_nodes = []
    edge_list, spis = [], []

    remain_nodes = term_nodes.copy()
    init_node = random.choice(term_nodes)
    visited_nodes.append(init_node)
    remain_nodes.remove(init_node)

    for _ in range(len(term_nodes) - 1):
        select_node = random.choice(visited_nodes)
        target_node = random.choice(remain_nodes)
        edge_list.append((select_node, target_node))
        spis = random.choice([True, False])

        remain_nodes.remove(target_node)
        visited_nodes.append(target_node)

    return SteinerTreeCode(
        edge_list, spis,
        random.choice(term_nodes),
        term_nodes, all_nodes
    )

