import decodes.core as dc
from decodes.core import *

import math, copy


outie = dc.makeOut(dc.outies.Rhino, "basistest")
outie_red = dc.makeOut(dc.outies.Rhino, "redstuff")
outie_red.set_color(1.0,0,0)

#print "CS basis"
#cs = CS(Point(5,5),Vec(1,-1))
#pts = [Point(t,math.sin(t),0,basis=cs) for t in drange(0,math.pi*2,5)]
#outie.put([cs,pts])
#print "here are the points defined relative to their base:"
#for p in pts : print p
#print "here they are in world coords:"
#for p in pts : print p.basis_applied()
#print "you can also access point coords as you would expect, using the _x,_y, and _z attributes"
#print "%s,%s,%s" %(pts[2]._x,pts[2]._y,pts[2]._z)
#print "using the x,y and z attributes returns world coords"
#print "%s,%s,%s" %(pts[2].x,pts[2].y,pts[2].z)
#
#print "if we strip the basis off, points will default to the basis of R3:"
#pts = [p.basis_stripped() for p in pts]
#outie.put(pts)


print "CylCS basis"
print "let's plot the same points in two different bases..."
cylindrical_cs = CylCS(Point(-4,0))
orthogonal_cs = CS(Point(4,0))

pts = [dc.Point(math.cos(t),t,math.sin(t)) for t in drange(0,math.pi*2,20)]
print pts
pts_cyld = [p.set_basis(cylindrical_cs) for p in pts]
pts_orth = [p.set_basis(orthogonal_cs) for p in pts]
pts_none = [p.basis_stripped() for p in pts]

outie.put([pts_cyld,cylindrical_cs])
outie.put([pts_orth,orthogonal_cs])
outie.put(pts_none)

print "this demonstrates the difference between measuring distance in 'basis space' vs 'world space'"
print "_distance() returns basis space distance, so long as both points share the same basis"
print "distance() always returns world space"
print "_distance cyld = %s" %pts_cyld[0]._distance(pts_cyld[10])
print "_distance orth = %s" %pts_orth[0]._distance(pts_orth[10])
print "distance cyld = %s" %pts_cyld[0].distance(pts_cyld[10])
print "distance orth = %s" %pts_orth[0].distance(pts_orth[10])
print "calling _distance() on points of two different bases will raise an error"
###print "_distance cyld to orth = %s" %pts_cyld[0]._distance(pts_orth[10])

print "we can manipulate the basis, and all the children follow"
orthogonal_cs.origin = Point(4,0,4)
outie.put([pts_orth,orthogonal_cs])
print "new distance diff = %s" %pts_none[0].distance(pts_orth[0])

#print "interpolating between two points that share a basis will result in a new point defined in that basis"
#pi = Point.interpolate(pts_cyld[0],pts_cyld[1],0.5)
#print "%s -> %s == %s" %(pts_cyld[0],pts_cyld[1],pi)
#print "pi.basis = %s" %pi.basis
#outie_red.put(pi)

#print "interpolating between two points with different bases will result in a point defined in R3"
#print "even if those bases happen to be very similar to one another"
#p0_clone = copy.deepcopy(pts_cyld[0])
#pi = Point.interpolate(p0_clone,pts_cyld[1],0.75)
#print "%s -> %s == %s" %(p0_clone,pts_cyld[1],pi)
#print "pi.basis = %s" %pi.basis
#outie_red.put(pi)

print "_centroid() returns a basis space centroid, so long as all points share the same basis"
print "centroid() always returns a world space centroid"
cpt_b = Point._centroid(pts_cyld)
print "cpt_b = %s" %cpt_b
cpt_w = Point.centroid(pts_cyld)
print "cpt_w = %s" %cpt_w
outie_red.put([cpt_b,cpt_w])

print "calling _centroid() on points of differing bases will raise an error"
##print "_centroid cyld to orth = %s" %Point._centroid([pts_cyld[0],pts_orth[10]])



outie.draw()
outie_red.draw()