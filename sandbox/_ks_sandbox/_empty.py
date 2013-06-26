import decodes as dc
from decodes.core import *
#import decodes.unit_tests

#outie = dc.makeOut(dc.Outies.SVG, "svg_out", canvas_dimensions=Interval(1000,500), flip_y = True)





'''

pts = [Point(),Point(1,1),Point(2,2)]
cs = CS(Point(0,0,-2))
pl  = PLine(pts)
pl.basis = cs

vec = Vec(0,0,1)
xf = Xform.translation(vec)

pl *= xf

pts = [
       Point(0,0),
       Point(1,0),
       Point(1,2),
       Point(0,2)
       ]

pg = PGon(pts)
print pg.area

pg.reverse().rotate(-1)
'''
raw_input("press enter...")