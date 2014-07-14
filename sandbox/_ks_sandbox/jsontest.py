import decodes
from decodes.core import *

outie = decodes.make_out(decodes.Outies.JSON, "json_out", save_file=True)
scale = 50


for x in range(1):
    for y in range(1):
        pt = Point(x*scale,y*scale)
        pt.set_color(Color(1,0,0))
        pt.set_weight(2*y+1.5)
        outie.put(pt)
        
outie.put(Vec(2,3))

outie.put(CS.on_xz(3,3))

def func(t): return Point(0,t)
crv = Curve(func,Interval(0,math.pi*2))
outie.put(crv)

pl = PLine([Point(),Point(0,1),Point(1,4)])
outie.put(pl)


seg = Segment(Point(2,2),Point(4,2))
seg.set_color(1,0,0)
seg.set_weight(5.0)
seg.set_name("myseg")
outie.put(seg)

ray = Ray(Point(6,6),Vec(1,1))
outie.put(ray)

line = Line(Point(7,6),Vec(1,1))
outie.put(line)


pg = PGon([Point(),Point(0,1),Point(1,1)])
pg.set_color(0,1,0)
pg.set_fill(0,0,1)
outie.put(pg)


rg = RGon(5,2.0)
outie.put(rg)


cir = Circle(Plane(Point(),Vec(0,0,1)),10)
cir.set_color(1,0,0)
cir.set_weight(5.0)
cir.set_fill(Color(0,1,0))
outie.put(cir)


arc = Arc(CS.on_yz(1,2),2.5,math.pi/3)
outie.put(arc)

pln = Plane(Point(3,3),Vec(1,1))
outie.put(pln)



tet_pts = [
    Point(0.0       , 0.0	      , 0.0),
    Point(0.9510565 , 0.0	      , 0.0),
    Point(0.6881910 , 1.3763819 , 0.0),
    Point(0.5257311 , 0.6881910	, 0.5)
]
tet_faces = [[0,1,2],[0,2,3],[2,3,0],[3,0,1]]

msh = Mesh(tet_pts,tet_faces)
outie.put(msh)
    



    
outie.draw()

