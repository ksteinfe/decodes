import decodes as dc
from decodes.core import *
#import decodes.unit_tests

from decodes.extensions.graph import *


gph = Graph()
gph.add_edge('a','b')
gph.add_edge('b','c')
gph.add_edge('c','d')
gph.add_edge('a','d',2)

print gph
print gph.weights

print gph._calc_dijkstra('a')
print gph.shortest_path('a','d')
print gph.node_list


raw_input("press enter...")