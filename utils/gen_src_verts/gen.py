"""
Source vertices generator
"""

import random
from typing import List, Union

import networkx as nx


def select_number_source_verts(graph: nx.MultiDiGraph, n: int, seed: Union[int, None] = None) -> List:
    """Return a list of random source vertices in the amount of n

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    n : int
        The number of nodes.
    
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.

    Returns
    -------
    l : List
        A random list of nodes in a graph.
    """
    num_nodes = graph.number_of_nodes()
    
    if n > num_nodes:
        raise ValueError(f"{n} exceeds the number of nodes in a graph ({num_nodes})")
    
    random.seed(seed)

    return random.sample(list(graph.nodes), n)
    
def select_percent_source_verts(graph: nx.MultiDiGraph, p: int, seed: Union[int, None] = None) -> List:
    """Return a list of random source vertices in the amount of percent p

    Parameters
    ----------
    graph : MultiDiGraph
        Initial graph.

    p : int
        The percent of nodes.
    
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.

    Returns
    -------
    l : List
        A random list of nodes in a graph.
    """
    num_nodes = graph.number_of_nodes()

    return select_number_source_verts(graph, int(num_nodes * p / 100.0), seed)