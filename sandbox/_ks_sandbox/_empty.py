import decodes as dc
from decodes.core import *
outie = dc.makeOut(dc.Outies.Rhino)

vec = Vec(0,0,1)
outie.put(vec)

outie.draw()