import decodes as dc
from decodes.core import *


outie = dc.makeOut(dc.Outies.SVG, "svg points")
    
scale = 20
for x in range(10):
    for y in range(10):
        pt = Point(x*scale,y*scale)
        pt.set_color(Color(1,0,0))
        outie.put(pt)
        
for x in range(10):
    for y in range(10):
        pt = Point(x*scale,(y+20)*scale)
        outie.put(pt)
    
outie.draw()



outie = dc.makeOut(dc.Outies.SVG, "svg lines")
    
scale = 20
def func(t):
    return Point(t*scale,math.sin(t)*scale+scale)
crv = Curve(func,Interval(0,math.pi*2))

pl = crv.surrogate
pl.set_color(1,0,0)
pl.set_weight(5.0)
outie.put(pl)        

outie.draw()

