import decodes as dc
from decodes.core import *




bnds=Bounds(center=Point(-2,2),dim_x=10,dim_y=10)

qt = QuadTree(4, bnds)

for n in range(50):
    pt = Point.random(Interval(0,1),True)
    qt.append(pt)


raw_input("press enter...")