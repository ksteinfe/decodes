import decodes as dc
from decodes.core import *
from decodes.extensions import packing
import random
from time import time
import math

def is_same(line1, line2):
    if line1.spt == line2.spt and line1.ept == line2.ept: return True
    if line1.spt == line2.ept and line1.ept == line2.spt: return True
    return False

a = PGon([Point(0,0),Point(100,0), Point(100,100), Point(0,100)])
b = PGon([Point(100,0),Point(200,0), Point(200,100), Point(100,100)])
c = PGon([Point(100,100),Point(200,100), Point(200,200), Point(100,200)])



e = a.edges

e.extend(b.edges)
e.extend(c.edges)

r = [Segment(e[0].spt, e[0].ept)]


for i in range(1,len(e)):
    flag = True
    for t in r:
        if is_same(e[i],t):
            r.remove(t)
            flag = False
            break
    if flag :
        r.append(Segment(e[i].spt, e[i].ept))

print


outie = dc.makeOut(dc.Outies.SVG, "svg_out", canvas_dimensions=Interval(1000,500), flip_y = True)
scale = 50

for x in r:
    x.set_color(Color(1,1,0))
    x.set_weight(1)
    outie.put(x)
               

outie.draw()





raw_input("Hit any key...")
