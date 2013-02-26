import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_empty_constructor(self):
        self.assertEqual(Point(0,0,0),Point(),"points with empty constructors are at 0,0,0")

    def test_based_constructor(self):
        # there's a unique case where we've been passed a based point along with a defined basis here.
        # in this case, we should take the local coordinates of the given point interpreted through the given basis
        pta = Point(0,0,0,basis=CS(Point(2,2,2)))
        ptb = Point(pta,basis=CS(Point(-4,-4)))
        self.assertEqual(ptb,Point(-4,-4,0),"point b adopts local coordinates of point a")



'''
print "operators"
# operations between points and vectors are performed in basis space
p0 = Point(0,2)
v = Vec(0,0,1)
p2 = p0+v # __add__
p3 = p0-v # __sub__
p4 = p0/2 # __div__
p5 = p0*3 # __mul__
p6 = ~p0 # __inv__
#outie.put([p0,p2,p3,p4,p5,p6])


print "random points"
#TODO: random points


print "interpolate"
# two points with the same basis will interpolate according to that basis
# two points with different bases will interpolate in world space
# to force interpolation in world space, use Interpolate
p0 = Point(1,0,1)
p1 = Point(1,1,1)
p2 = Point.interpolate(p0,p1,0.3)
#outie.put([p0,p1,p2])

print "distance"
# two points with the same basis will measure distance according to that basis
# two points with different bases will measure distance in world space
# to force distance in world space, use Distance
p0 = Point(2,2,0.5)
p1 = Point(2,2,1.0)
print "%s.distance(%s) = %s" % (p0,p1, p0.distance(p1) )
print "%s.distance2(%s) = %s" % (p1,p0, p1.distance2(p0) )

print "centroid"
# two points with the same basis will calculate centroid according to that basis
# two points with different bases will calculate centroid in world space
# to force centroid in world space, use Centroid
p0 = Point(1,0,2)
p1 = Point(0,1,2)
p2 = Point(1,1,2)
cent = Point.centroid([p0,p1,p2])
#outie.put([p0,p1,p2,cent])

print "comparison and sorting"

print "points are sorted in basis space by position: z, then y, then x"
p0 = Point(0,0,0)
p1 = Point(-1,1,0)
p2 = Point(-1,0,0)
p3 = Point(1,0,0)
p4 = Point(1,-1,1)
p5 = Point(1,-1,0)
p0.name,p1.name,p2.name,p3.name,p4.name,p5.name  = "p0","p1","p2","p3","p4","p5"
pts = [p0,p1,p2,p3,p4,p5]
pts.sort()
print "sort pts:  %s!" % [p.name for p in pts]

#pts = [Point.random() for n in range(100)]
#pts.sort()
#rs.AddPolyline([p.to_tuple() for p in pts])
#redoutie = dc.makeOut(dc.outies.Rhino, "redstuff")
#redoutie.set_color(1.0,0,0)
#redoutie.put(Point(pts[0]))
#redoutie.draw()

'''