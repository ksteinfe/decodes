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
        self.weights = {}
    
    def add_node(self, value):
        self.nodes.add(value)
    
    def add_edge(self, from_node, to_node, weight=1.0):
        # make sure these nodes are in our list of nodes
        if from_node not in self.nodes: self.add_node(from_node)
        if to_node not in self.nodes: self.add_node(to_node)
        
        # add the edge
        self._add_edge(from_node, to_node, weight)
        # add the reverse edge
        if not from_node == to_node: self._add_edge(to_node, from_node, weight)
 
    def _add_edge(self, from_node, to_node, weight):
        self.edges.setdefault(from_node, []) # key might exist already, but if not this instructs our dict to return an empty list for this key.
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight

    @property
    def node_list(self):
        return list(self.nodes)

    def __repr__(self): return "graph[{0} nodes ,{1} connections]".format(len(self.nodes),sum([len(edge) for edge in self.edges.values()]))



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

'''
class SpatialGraph(Graph):
    """
    A graph of spatial points
    important to note that graph is indexed by object, not by position. it will detect duplicate objects, but not duplicate point locations
    """
    def __init__(self):
        super(SpatialGraph,self).__init__()
        self.distances = {}

    def _add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight
        self.distances[(from_node, to_node)] = from_node.distance(to_node)
'''