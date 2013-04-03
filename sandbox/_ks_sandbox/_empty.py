import decodes as dc
from decodes.core import *
#import decodes.unit_tests 

pts = [Point(1,1),Point(2,1),Point(1,2)]
cs = CS(Point(10,10))
pgon = PGon(pts,cs)


print pgon

def flip_geom(geom):
    xf = Xform.mirror(plane="world_xz")
    ngeom = geom*xf
    xf = Xform.translation(Vec(0,10))
    ngeom = ngeom*xf
    if hasattr(geom, 'props'): ngeom.props = geom.props
    return ngeom

pgon_flipped = flip_geom(pgon)

print pgon_flipped



#raw_input("press enter...")