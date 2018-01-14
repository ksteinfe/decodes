from decodes.core import *
from . import dc_base, dc_vec, dc_point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print("graph.py loaded")

import math, itertools

class Graph(object):
    """
    A directed, weighted graph
    """
    def __init__(self):
        self.nodes = set() # a set is an unordered collection of unique elements
        self.edges = {}
        self.weights = {}
    
    def add_node(self, value):
        self.nodes.add(value)
    
    def add_edge(self, from_node, to_node, weight=1.0,bidirectional=True):
        # make sure these nodes are in our list of nodes
        if from_node not in self.nodes: self.add_node(from_node)
        if to_node not in self.nodes: self.add_node(to_node)
        
        # add the edge
        success = self._add_edge(from_node, to_node, weight)
        # add the reverse edge
        if bidirectional:
            if not from_node == to_node: 
                success= success and self._add_edge(to_node, from_node, weight)
        return success
 
    def _add_edge(self, from_node, to_node, weight):
        self.edges.setdefault(from_node, []) # key might exist already, but if not this instructs our dict to return an empty list for this key.
        if not to_node in self.edges[from_node]:
            self.edges[from_node].append(to_node)
            self.weights[(from_node, to_node)] = weight
            return True
        return False

    @property
    def node_list(self):
        return list(self.nodes)

    def __repr__(self): return "graph[{0} nodes ,{1} connections]".format(len(self.nodes),sum([len(edge) for edge in list(self.edges.values())]))


    @property
    def node_pairs(self):
        ret = []
        for n1, others in self.edges.items():
             for n2 in others: ret.append((n1,n2))
        return tuple(ret)
    
    """
    Source:
    http://forrst.com/posts/Dijkstras_algorithm_in_Python-B4U
    [noprint]
    """
    """
    A method that creates solves for the shortest possible path between nodes in a graph
    """
    def _calc_dijkstra(self, initial_node):
        # set the current visited nodes and the distance travelled
        visited = {initial_node: 0}
        # set the current node as the initial node
        current_node = initial_node
        # create an empty dictionary for the path
        path = {}
    
        # create a set of all the nodes in the graph
        nodes = set(self.nodes)
        # while there are still nodes in the set
        while nodes:
            # calculate the minimum node
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node
            if min_node is None:
                break
            # remove the current node from nodes
            nodes.remove(min_node)
            # get the distance to the current node
            cur_wt = visited[min_node]
            # for every edge connected to the current node:
            for edge in self.edges[min_node]:
                # record this edge to visited and path dicts
                wt = cur_wt + self.weights[(min_node, edge)]
                if edge not in visited or wt < visited[edge]:
                    visited[edge] = wt
                    path[edge] = min_node
    
        return visited, path

    """
    Given an initial node and an end node, this function returns the shortest path between them
    """
    def shortest_path(self, initial_node, goal_node):
        # set distances and paths to the result of the dijkstra function
        distances, paths = self._calc_dijkstra(initial_node)
        # set the route as the goal node
        route = [goal_node]
    
        # while the goal node is not the same as the initial node
        while goal_node != initial_node:
            # add the current goal node to the route
            route.append(paths[goal_node])
        
            goal_node = paths[goal_node]
    
        # reverse the route list to start from the initial node
        route.reverse()
        return route


class SpatialGraph(Graph):
    """
    A graph of spatial points
    A graph is indexed by object, not by position. This class ensures that duplicate point positions are not permitted.
    Collection of points given at construction are not checked for duplicates
    """
    def __init__(self,initial_pts=False):
        super(SpatialGraph,self).__init__()
        self.distances = {}
        
        #self.qtree = QuadTree(4, bnds)
        #for pt in pts: qt.append(pt)
        
        if initial_pts:
            for pt in initial_pts: self.add_node(pt)
        
    """
    if not check validity, duplicate point locations are not checked, nor is the existence of the requested node in the set of nodes
    """
    def add_edge(self, from_node, to_node, bidirectional=True, check_validity=True):
        if check_validity:
            na, nb = self.node_at(from_node), self.node_at(to_node)
            if na: from_node = na
            if nb: to_node = nb
        
            # make sure these nodes are in our list of nodes
            if from_node not in self.nodes: self.add_node(from_node)
            if to_node not in self.nodes: self.add_node(to_node)
        
        # add the edge
        dist = from_node.distance(to_node)   
        success = self._add_edge(from_node, to_node, dist)
        # add the reverse edge
        if bidirectional: success = success and self._add_edge(to_node, from_node, dist)
        return success
        
        
        
    def add_node(self, pt, check_validity=True):
        if check_validity:
            undup = self.node_at(pt)
            if undup: pt = undup
        
        self.nodes.add(pt)
        
        
        
        
    def to_segs(self):
        return [[Segment(spt,ept) for ept in epts] for spt, epts in list(self.edges.items())]
        
        
    def __contains__(self, pt):
        """| Overloads the containment **(in)** operator"""
        return node_at(pt) is not False
        
    def node_at(self,pt):
        for other in self.nodes:
            if pt == other : return other
        return False

















































