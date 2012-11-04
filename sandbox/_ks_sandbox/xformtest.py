import decodes.core as dc
from decodes.core import *
outie = dc.makeOut(dc.outies.Rhino, "wayout")

import scriptcontext
import System
import Rhino
from decodes.core.outies.rhinoUtil import *
import math


'''
print "from rhino transform"
rh_xform = Rhino.Geometry.Transform.Translation(VecToVec3d(Vec(10,20,30)))
xf = Xform.from_rh_transform(rh_xform)
print rh_xform
print xf
'''

'''
print "to rhino transform"
xf = Xform(99)
rh_xform = Xform.to_rh_transform(xf)
print rh_xform
print xf
'''

'''
print "matrix multiplication"
vec = Vec(1,1,1)
rotPt = Point(1,1)
ang = math.pi/2
rh_xformA = Rhino.Geometry.Transform.Rotation(ang,VecToVec3d(vec),VecToPoint3d(rotPt))
xfA = Xform.rotation(center=rotPt, angle=ang, axis=vec)
print rh_xformA
print xfA

rh_xformB = Rhino.Geometry.Transform.Scale(VecToPoint3d(Point(0,0)),2.0)
xfB = Xform.scale(2.0)
print rh_xformB
print xfB

rh_xformC1 = rh_xformA * rh_xformB
rh_xformC2 = rh_xformB * rh_xformA
xfC1 = xfA * xfB
xfC2 = xfB * xfA
print rh_xformC1
print xfC1

outie = dc.makeOut(dc.outies.Rhino, "matrix multiplication")
out.iconscale = 0.5
out.set_color(1.0,1.0,0)
cs = CS(Point(0,1))
csXA = cs * xfA
csXB = cs * xfB
csXC1 = cs * xfC1
csXC2 = cs * xfC2

for g in [cs,csXA, csXB, csXC1, csXC2] : outie.put(g)
vec.set_origin(rotPt) #TODO: replace this with ray object
outie.put(vec)
outie.draw()
'''


'''
print "translation"
outie = dc.makeOut(dc.outies.Rhino, "translation")
out.set_color(1.0,1.0,0)
pt0 = Point(1,1)
vec = Vec(1,2,3)
vec.set_origin(pt0)  #TODO: replace this with ray object
xf = Xform.translation(vec)
print xf
pt1 = pt0 * xf
for p in [pt0,pt1,vec]: outie.put(p)
outie.draw()
print "with translation stripped out..."
xf2 = xf.strip_translation()
print xf2
'''

'''
print "scale"
outie = dc.makeOut(dc.outies.Rhino, "scale")
out.set_color(1.0,1.0,0)
pt0 = Point(1,1)
xf = Xform.scale(0.5)
print xf
'''


print "mirror"
outie = dc.makeOut(dc.outies.Rhino, "mirror")
outie.set_color(1.0,0.0,1.0)
pt = Point(1,1,1)
xf = Xform.mirror("worldYZ")
ptX = pt * xf
for p in [pt,ptX]: outie.put(p)
print xf

cs = CS(Point(),Vec(1.0,0.5),Vec(0,0,1))
xf = Xform.mirror(cs)
print xf
ptXX = pt * xf
for p in [cs,ptXX]: outie.put(p)
outie.draw()

'''
print "rotation"
basePt = Point(1,1)
outie.put(basePt)

outie = dc.makeOut(dc.outies.Rhino, "rotation")
out.set_color(1.0,0.0,1.0)
rotPt = Point(0,1)
xf = Xform.rotation(center=Point(0,1), angle=math.pi/2)
pt1 = basePt * xf
for p in [rotPt,pt1] : outie.put(p)
outie.draw()

out.set_color(0.0,0.0,1.0)
vec = Vec(1,0)
rotPt = Point(1,2)
vec.set_origin(rotPt) #TODO: replace this with ray object
xf = Xform.rotation(center=rotPt, angle=math.pi/2, axis=vec)
pt1 = basePt * xf
for p in [rotPt,pt1,vec] : outie.put(p)
outie.draw()
'''

'''
print "change basis"
outie = dc.makeOut(dc.outies.Rhino, "change basis")
out.set_color((1.0,0.0,0.5))
pa,pb,pc = Point(2,1,4),Point(2,1,5),Point(2,1,6)
sourceCS = CS(Point(2,2,4),Vec(0,0,1))
targetCS = CS(Point(2,-2),Vec(1,-1))
xf = Xform.change_basis(sourceCS,targetCS)
pax,pbx,pcx = map(lambda pt:pt*xf,[pa,pb,pc])
for g in [pa,pb,pc,pax,pbx,pcx,sourceCS,targetCS] : outie.put(g)
outie.draw()

cs = CS(Point(3,0,4))
csx = cs * xf
for g in [cs,csx] : outie.put(g)
'''


outie.draw()