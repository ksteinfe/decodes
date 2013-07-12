import decodes as dc
from decodes.core import *
import decodes.unit_tests

#outie = dc.makeOut(dc.Outies.SVG, "svg_out", canvas_dimensions=Interval(1000,500), flip_y = True)

def func(u,v):
    return Point(u,v,math.sin(u+v))
twopi = Interval.twopi()
surf = Surface(func,twopi,twopi)

pl = surf.isopolyline(u_val=0.5)


raw_input("press enter...")