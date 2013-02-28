import decodes as dc
from decodes.core import *
import decodes.unit_tests 



pts = [Point(x,0,0) for x in range(10)]
pline = PLine(pts)
#print pline[0]
#print pline[0:-1]

pline[0] = Point(-3,2)



'''
outie = dc.makeOut(dc.Outies.SVG)


def func(t):
    return Point(t,math.sin(t))*10+Vec(100,100)

crv = Curve(func,Interval(0,math.pi*2))
outie.put(crv)


cir = circular_curve(Point(100,100),50)
outie.put(cir)

outie.draw()
'''

raw_input("press enter...")