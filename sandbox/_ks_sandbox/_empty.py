import decodes as dc
from decodes.core import *


vf = VecField(Interval(4,4),Point(2,2))

add = vf.address_near(Point(2,2))
vec = vf.vec_near(Point(2,2))

print vf




#raw_input("press enter...")