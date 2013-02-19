import decodes as dc
from decodes.core import *
outie = dc.makeOut(dc.Outies.SVG)

outie.default_color = Color(0,0,1)

scale = 20
for x in range(10):
    for y in range(10):
        pt = Point(x*scale,y*scale)
        pt.set_color(Color(1,0,0))
        pt.set_weight(y/3.0)
        outie.put(pt)
        
for x in range(10):
    for y in range(10):
        pt = Point(x*scale,(y+20)*scale)
        outie.put(pt)

r = rect(Point(100,100),20,30)
r.set_color(Color(1,0,0))
outie.put(r)

outie.draw()

