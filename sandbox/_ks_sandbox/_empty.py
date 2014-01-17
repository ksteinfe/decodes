import decodes as dc
from decodes.core import *
#import decodes.unit_tests


pln_a = Plane(Point(0,0,2),Vec(1,0))
pln_b = Plane(Point(),Vec(0,0,1))
cs = CS(Point(0,0,2),Vec(0,0,-1),Vec(0,1))

#circ = Circle(pln_a,1.0)
arc = Arc(cs,3.0,math.pi)

xsec = Intersector()
if xsec.of(pln_b,arc):
    print "xsec found!"

print xsec.log
print xsec.log


#raw_input("press enter...")