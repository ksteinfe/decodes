import decodes as dc
from decodes.core import *
from decodes.io import *

outie = dc.makeOut(dc.Outies.ACAD, "wayout")
pt = Point(10, 0)
outie.put(pt)
outie.draw()
