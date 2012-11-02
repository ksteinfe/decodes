import decodes.core as dc
from decodes.core import *

outie = dc.makeOut(dc.outies.Rhino, "wayout")

o = Point(0,0,10)
vx = Vec(0,0,10)
vy = Vec(0,10,0)
cs1 = CS(o,vx,vy)
cs2 = CS(Point(),Vec(1,0),Vec(0,1))
for g in [cs1,cs2] : outie.put(g)


pa = Point(2,1,10)
pb = Point(2,1,11)
pc = Point(2,1,12)
cs3 = CS(pc+Vec(0,0,1))
for g in [pa,pb,pc,cs3] : outie.put(g)


xf = Xform.change_basis(cs1,cs2)
csx = cs3*xf
pax,pbx,pcx = map(lambda pt:pt*xf,[pa,pb,pc])
for g in [pax,pbx,pcx,csx] : outie.put(g)
# for g in parr : outie.put(g)

outie.draw()