import decodes as dc
from decodes.core import *
#import decodes.unit_tests


basis=CS(0,1)
verts = ([Point(0,0,1),Point(0,1,1),Point(1,1,1),Point(1,0,1)])

pgon = PGon(verts)
#npt = pgon.near(Point(0,0.1))
print pgon


raw_input("press enter...")