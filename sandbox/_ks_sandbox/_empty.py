import decodes as dc
from decodes.core import *
#import decodes.unit_tests

#outie = dc.makeOut(dc.Outies.SVG, "svg_out", canvas_dimensions=Interval(1000,500), flip_y = True)


pts = [
       Point(0,0),
       Point(1,0),
       Point(1,2),
       Point(0,2)
       ]

pg = PGon(pts)
print pg.area

pg = pg.inflate()




raw_input("press enter...")