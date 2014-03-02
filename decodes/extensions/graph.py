import decodes.core as dc
from decodes.core import *
import math

class Graph(object):
    """
    A simple undirected, weighted graph
    """
    def __init__(self):
        self.nodes = set() # a set is an unordered collection of unique elements
        self.edges = {}
        # could do this: self.edges = defaultdict(list)
        self.distances = {}
    
    def add_node(self, value):
        self.nodes.add(value)
    
    def add_edge(self, from_node, to_node, distance):
        self._add_edge(from_node, to_node, distance)
        self._add_edge(to_node, from_node, distance)
 
    def _add_edge(self, from_node, to_node, distance):
        self.edges.setdefault(from_node, []) # key might exist already, but if not, return an empty list for this key. could erase this line with default dict
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance