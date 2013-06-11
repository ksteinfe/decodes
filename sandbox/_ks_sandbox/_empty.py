import decodes as dc
from decodes.core import *

rect=Bounds(Point(0,0),10,10)
qt = QuadTree(4, rect)

for n in range(50):
    pt = Point.random(Interval(0,1),True)
    qt.append(pt)


raw_input("press enter...")