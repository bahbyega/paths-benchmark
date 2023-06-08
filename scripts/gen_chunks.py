"""
Source vertices generator
"""

import random
from typing import List, Union

import networkx as nx


def select_number_source_verts(num_nodes, n: int, seed: Union[int, None] = None) -> List:
    """Return a list of random source vertices in the amount of n

    Parameters
    ----------
    graph :
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
    if n > num_nodes:
        n = num_nodes
        # raise ValueError(f"{n} exceeds the number of nodes in a graph ({num_nodes})")
    
    random.seed(seed)

    return random.sample([x for x in range(num_nodes)], n)
    
def select_percent_source_verts(num_nodes, p: int, seed: Union[int, None] = None) -> List:
    """Return a list of random source vertices in the amount of percent p

    Parameters
    ----------
    graph :
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
    return select_number_source_verts(num_nodes, int(num_nodes * p / 100.0), seed)

def generate_single_source(
    graph
    ) -> List[int]:
    """Returns a set of vertices for single-source evaluation for the given graph.
    The size of generated set is dependant on the number of nodes in the graph.
    For 
    Parameters
    ----------
    graph :
        Graph for which the sample is generated.
    Returns
    -------
    nodes: List[int]
        The list of sampled node indices for which to evaluate single-source CFPQ.
    """
    nodes = graph.num_nodes
    sources = []
    noderange = int(0)
    if nodes < 10000:
        noderange = nodes
    elif nodes < 100000:
        noderange = nodes // 10
    else:
        noderange = nodes // 100

    for i in range(noderange):
        sources.append(random.randrange(0, nodes))

    return sources