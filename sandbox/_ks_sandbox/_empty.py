import decodes as dc
from decodes.core import *
import decodes.unit_tests

#outie = dc.makeOut(dc.Outies.SVG, "svg_out", canvas_dimensions=Interval(1000,500), flip_y = True)

'''
crv_a = Curve.bezier([Point(0,0),Point(0,1)])
crv_b = Curve.bezier([Point(0,0,1),Point(0,1,1)])
crv_c = Curve.bezier([Point(0,0,2),Point(0,1,2)])

def func(u,v):
    pts = [crv.eval(u) for crv in [crv_a,crv_b,crv_c]]
    return Curve.bezier(pts).eval(v)

surf = Surface(func)



u = 0.5
v = 0.5


iso_u = surf.isocurve(u_val=u)
iso_v = surf.isocurve(v_val=v)

#iso_u.tol *= 0.25
#iso_v.tol *= 0.25



curv_u = iso_u.eval_curvature(v)
curv_v = iso_v.eval_curvature(u)
'''

'''
pts = [Point(),Point(0,1),Point(2,0)]
pl  = PLine(pts)
a = 1
print pl.edges
pl.rotate(-1)
a = 1
print pl.edges




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


#raw_input("press enter...")