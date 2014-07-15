from decodes.extensions.graph import Graph

'''
4.02.L02a
Creates a class that maps Point proximity from a point cloud to a Graph

members:
graph (Graph) The Graph object that is wrapped by this ProximityGraph

methods:
rebuild_edges(None) Rebuilds a Graph such that each contained Point forms connections with a given number of Points nearest to it.
nearest_to(Point, Integer) Searches for the closest points in the Point cloud to a given point.
divide_edges(Integer) Interpolates between Point-Point connections on the Graph
'''

"""
Inflatable Graph Class
Creates a class that maps Point proximity from a point cloud to a Graph
"""
class InflatableGraph(Graph):
    
    def __init__(self, pts=False):
        super(InflatableGraph, self).__init__()
        if pts:
            for pt in pts: self.add_node(pt)
            self.rebuild_edges()
    
    """
    Rebuild Edges
    Rebuilds a Graph such that each Point forms connections with a given number of Points nearest to it.
    """
    def rebuild_edges(self):
        # create a new empty graph and copy over existing nodes
        ngraph = Graph()
        # for every point in the old graph:
        for p1 in self.nodes:
            # for each of the other points nearest to this one:
            for p2 in self.nearest_to(p1):
                ngraph.add_edge(p1,p2,bidirectional=False)
                        
        # update the nodes and edges of this proximity graph
        self.nodes = ngraph.nodes
        self.edges = ngraph.edges
    
    """
    Nearest Points Method
    Returns the closest points to a given point in the list of points stored in this InflatableGraph's graph 
    """
    def nearest_to(self, pt, count=5):
        # make a list of all points in the graph without pt
        others = [p for p in self.nodes if p != pt]
        # sort them by distance to pt
        others.sort(key = lambda p: p.distance2(pt))
        # return the closest ones
        return others[0:count]
    
    """
    Divide Edges Method
    Rebuilds the stored graph with additional points by subdividing existing graph edges
    """
    def inflate(self, divs=2):
        print len(self.nodes)
        # copy existing nodes into a new set
        nodes = set()
        # for each Point in the nodes:
        for key_pt in self.nodes:
            if not pt_in_set(key_pt,nodes): 
                nodes.add(key_pt)
                # for each connection Point to that node:
                for edge_pt in self.edges[key_pt]:
                    # interpolate between the two Points
                    pt = Point.interpolate(key_pt,edge_pt,0.5)
                    if not pt_in_set(pt,nodes): nodes.add(pt)
        # redefine the nodes in our graph and rebuild
        self.nodes = nodes
        
        print len(self.nodes)
        self.rebuild_edges()


def pt_in_set(pt,set):
    return any([pt==other for other in set])