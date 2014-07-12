import decodes
from decodes.core import *
from decodes.extensions.graph import SpatialGraph



edges = [
                [Point(),Point(0,1)],
                [Point(0,1),Point(1,1)],
                [Point(1,1),Point()]
            ]
                


gph = SpatialGraph([Point()])

for spt,ept in edges:
    gph.add_edge(spt,ept)



print gph