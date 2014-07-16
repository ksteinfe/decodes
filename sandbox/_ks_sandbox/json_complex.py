import decodes
from decodes.core import *

outie = decodes.make_out(decodes.Outies.JSON, "json_out", save_file=True)


from decodes.extensions.graph import SpatialGraph




"""
Proximity Edges
Adds edges to a given SpatialGraph such that each Point forms connections with a given number of Points nearest to it.
"""
def add_proximity_connections(gph,val=5):
    for p1 in gph.nodes:
        # make a list of all points in the graph without pt
        others = [p for p in gph.nodes if p != p1]
        # sort them by distance to pt
        others.sort(key = lambda p: p.distance2(p1))
        # return the closest ones
        others = others[:val]
        for p2 in others:
            gph.add_edge(p1,p2,bidirectional=False,check_validity=False)
        
        
"""
Divide Edges Method
Subdivides a given graph's edges a given number of times, and returns the resulting points.
"""
def divide_edges(gph, divs=4):
    ret = []
    t_vals = (Interval()/divs)[1:]
    for spt, epts in gph.edges.items():
        for ept in epts:
            ret.extend([Point.interpolate(spt,ept,t) for t in t_vals])
    return ret

"""
SpatialGraph Inflation Routine
Constructs and successively divides a SpatialGraph, reconstructing its edges based on proximity at each step.
"""
point_cloud = [Point.random(Interval(0,10)) for n in range(4)]
graph = SpatialGraph(point_cloud)
add_proximity_connections(graph)

count = 3

for n in range(count):
    inflated_graph = SpatialGraph(graph.nodes)
    for pt in divide_edges(graph): inflated_graph.add_node(pt)
    add_proximity_connections(inflated_graph)
    graph = inflated_graph



for spt, epts in graph.edges.items(): outie.put([Segment(spt, ept) for ept in epts])
    
outie.draw()

