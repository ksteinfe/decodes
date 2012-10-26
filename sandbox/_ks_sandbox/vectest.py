import fieldpack as fp
from fieldpack import *

import Rhino
import rhinoscriptsyntax as rs
 
    
outie = fp.makeOut(fp.outies.Rhino, "vectest")


print "constructors"
v0 = Vec(1,-2)
p0 = Point(0,2,2)
p1 = Point(1,1,1)
v1 = Vec(p0,p1)

outie.put([p1,p0,v0,v1])


print "operators"
v0 = Vec(0,0,1)
v1 = Vec(0,2)
v2 = v0+v1 # __add__
v3 = v1-v0 # __sub__
v4 = v0/2 # __div__
v5 = v0*3 # __mul__
v6 = ~v0 # __inv__
outie.put([v0,v1,v2,v3,v4,v5,v6])


print "cross product, dot product, projection angles"
v0 = Vec(2,0)
v1 = Vec(2,2)
vUp = v0.cross(v1)
vDwn = v1.cross(v0)
outie.put([v0,v1,vUp,vDwn])

print "%s.angle(%s) = %s" % (v0,v1, v0.angle_deg(v1) )
print "%s.angle(%s) = %s" % (v0,vUp, v0.angle_deg(vUp) )
print "%s.angle(%s) = %s" % (v0,vDwn, v0.angle_deg(vDwn) )
print "%s.angle(%s) = %s" % (vDwn,v0, vDwn.angle_deg(v0) )

p0 = Point(1.5,0.25,0.5)
p1 = p0.projected(v0)
p2 = p1.projected(p0)
outie.put([p0,p1,p2])

print "random vectors"
vec = Vec.random()
outie.put([vec])


print "interpolate"
v0 = Vec(1,0)
v1 = Vec(1,1)
v2 = Vec.interpolate(v0,v1,0.3)
outie.put([v0,v1,v2])


print "bisector"
v0 = Vec(3,0,1)
v1 = Vec(3,0,0)
v2 = Vec.bisector(v0,v1)
outie.put([v0,v1,v2])


print "limited"
v0 = Vec(3,3)
v1 = v0.limited(2)
outie.put([v0,v1])


print "average & centroid"
v0 = Vec(1,0)
v1 = Vec(0,1)
v2 = Vec(1,1)
vAvg = Vec.average([v0,v1,v2])
outie.put([v0,v1,v2,vAvg])


#print "comparison and sorting"
#
#print "vector comparisons only check length"
#v0 = Vec(0,2)
#v1 = Vec(0,-1)
#v2 = Vec(3,3)
#print "%s < %s?  %s!" % (v0,v1, ( v0<v1 ))
#print "%s > %s?  %s!" % (v0,v1, ( v0>v1 ))
#print "%s == %s?  %s!" % (v0,v1, ( v0==v1 ))
#print "%s == %s?  %s!" % (v0,v2, ( v0==v2 ))
#
#print "%s.is_identical(%s)?  %s!" % (v1,v2, ( v1.is_identical(v2) ))
#print "%s.is_coincident(%s)?  %s!" % (v1,v2, ( v1.is_coincident(v2) ))
#print "%s.is_2d?  %s!" % (v2, ( v2.is_2d ))
#
#outie.put(v2)
#v2.length = v0.length
#v2 = v2.inverted() # same as v2 = ~v2
#outie.put(v2)
#v2 = v2.rounded()
#outie.put(v2)
#
#
#print "vecs are sorted by length"
#redoutie = fp.makeOut(fp.outies.Rhino, "redstuff")
#redoutie.set_color(1.0,0,0)

#vecs = [Vec.random(normalize=False) for n in range(20)]
#vecs.sort()
#rs.AddPolyline([v.to_tuple() for v in vecs])
#outie.put(Point(vecs[0]))
#redoutie.put(vecs)



outie.draw()