import decodes as dc
from decodes.core import *
from decodes.io import *
from decodes.io.pyautocad import *

acad = Autocad(False,  True)


outie = dc.makeOut(dc.Outies.ACAD, "wayout")

pt = Point(0,10)
# Testing points
pts = [Point(i, i) for i in range(10)]
# Testing Segments
segs = [Segment(pt, Point(5,0)) for pt in pts]
# Testing Rays
rays = [Ray(pt, Point(i+1,0)) for i,pt in enumerate(pts)]
# Testing Line
line = Line(pt, Point())
# Testing Vecs
vecs = [Vec(i,5,0) for i in range(10)]
# Testing PLine
plines = [PLine([pt,Point(15,1,0),Point(20,1,0)]) for pt in pts]
# Testing PGon
pgon = PGon([pt,Point(0,5,0),Point(-3,15,0)])
# Testing Meshes 
mesh4 = Mesh([Point(),Point(-5,0,0),Point(0,-5,0),Point(-5,-5,0)], [[0,1,2,3]])
mesh3 = Mesh([Point(),Point(-5,0,0),Point(0,-5,0)], [[0,1,2]])
mesh3.set_color(1,0.5,0.5)
mesh3.set_weight(3)
# Testing Curves
crv_pts = [Point(-5), Point(-10,-10), Point(-12)]
curve = Curve.bezier(crv_pts)

outie.put([pts, 
            segs, 
            rays, 
            line, 
            vecs, 
            plines, 
            pgon, 
            mesh4, 
            mesh3,
            curve
            ])
            
outie.draw()

