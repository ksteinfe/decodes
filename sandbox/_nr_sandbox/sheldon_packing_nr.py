import decodes as dc
from decodes.core import *
from decodes.extensions import packing
import random
from time import time
import math

import os,cStringIO
path = os.path.expanduser("~") + os.sep + "_decodes_export"
f_prefix = "s_pack_01_"
random.seed(0)

size = 100

i_size = Interval(500,500)


def sheldon_packing(width, shape):
    result = []
    cut = sheldon_cut(w,shape)
    if cut:                 # returns True if cuttable
        result.append(cut[0])
        result.append(sheldon_packing(width, cut[1]))
    else:
        result.append(shape)
    return result


pts = packing.rand_points(4,size)

for i in range(4):
    pts[i] = pts[i] + Vec(i_size.a/2.0,i_size.b/2.0)

shape = PGon(pts)

shape.set_color(Color(0.0))

# send the geometry to an outie
outie = dc.makeOut(dc.Outies.SVG, f_prefix, canvas_dimensions=i_size, flip_y = True)
'''
for x in strips_packed:
    outie.put(x)
'''
outie.put(shape)
    
outie.draw()
    
raw_input("press enter...")