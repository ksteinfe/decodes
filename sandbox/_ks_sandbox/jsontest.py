import decodes
from decodes.core import *

outie = decodes.make_out(decodes.Outies.JSON, "json_out", save_file=True)
scale = 50

for x in range(2):
    for y in range(2):
        pt = Point(x*scale,y*scale)
        pt.set_color(Color(1,0,0))
        pt.set_weight(2*y+1.5)
        outie.put(pt)
        

def func(t): return Point(0,t)
crv = Curve(func,Interval(0,math.pi*2))
sur = crv.surrogate
#outie.put(crv)

pl = PLine([Point(),Point(0,1)])
#outie.put([Point(),pl,Point()])

        

cir = Circle(Plane(Point(),Vec(0,0,1)),10)
cir.set_color(1,0,0)
cir.set_weight(5.0)
cir.set_fill(Color(0,1,0))
outie.put(cir)

seg = Segment(Point(2,2),Point(4,2))
outie.put(seg)

ray = Ray(Point(6,6),Vec(1,1))
line = Line(Point(7,6),Vec(1,1))
outie.put(ray)
outie.put(line)

'''
pg = PGon([Point(),Point(0,1),Point(1,1)])
outie.put(pg)

rg = RGon(5,2.0)
outie.put(rg)
'''


outie.draw()

