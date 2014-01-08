import decodes as dc
from decodes.core import *
#import decodes.unit_tests

lent = Ray(Point(0,0.1),Vec(0.1,1))
pgon = RGon(4,1.0,basis=CS(0,1))


xsec = Intersector()
print xsec.log

if xsec.of(lent,pgon):
    print "found {0} intersections".format(len(xsec))
    print xsec.results
else:
    print "no intersection"
    print lent.vec

raw_input("press enter...")