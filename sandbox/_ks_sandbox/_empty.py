import decodes as dc
from decodes.core import *
import math


print Interval.remap(5,Interval(0,10),Interval(20,30))


outie = dc.makeOut(dc.Outies.SVG)


scale = 20
for x in range(10):
    for y in range(10):
        pt = Point(x*scale,y*scale)
        pt.set_color(Color(1,0,0))
        pt.set_weight(y/3.0)
        outie.put(pt)
        
pl = PGon()
for t in frange(0,math.pi*2,math.pi*2/30) :
    pt = Point(math.sin(t+5)-math.sin(t)**2,math.cos(t+10)-math.cos(t)**2)
    pl.append(pt*40+Vec(200,400))

#outie.put(pl)

r = PGon.rectangle(Point(100,100),20,30)
r.set_color(Color(1,0,0))
#outie.put(r)


dough = PGon.doughnut(Point(200,500),10,100)
outie.put(dough)


ln = Segment(Point(100,300),Vec(0,50))
#outie.put(ln)


outie.draw()

