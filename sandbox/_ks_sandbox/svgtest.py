import decodes as dc
from decodes.core import *


outie = dc.makeOut(dc.Outies.SVG, "svg_out", canvas_dimensions=Interval(1000,500), flip_y = True)
scale = 50

for x in range(10):
    for y in range(10):
        pt = Point(x*scale,y*scale)
        pt.set_color(Color(1,0,0))
        pt.set_weight(2*y+1.5)
        outie.put(pt)
        
    
def func(t):
    return Point(t*scale,math.sin(t)*scale)
crv = Curve(func,Interval(0,math.pi*2))

pl = crv.surrogate
pl.set_color(1,0,0)
pl.set_weight(5.0)
outie.put(pl)        

outie.draw()

