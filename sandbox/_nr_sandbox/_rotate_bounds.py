import decodes as dc
from decodes.core import *
from decodes.extensions import packing
import random
from time import time
import math

import os,cStringIO
path = os.path.expanduser("~") + os.sep + "_decodes_export"
f_prefix = "pack_19_"
random.seed(0)


shape = PGon(packing.rand_points(random.randint(3,10),random.randint(1, 100)))

min_area = shape.bounds.dim_x * shape.bounds.dim_y
print "Initial shape bounding area: ", min_area


n = 6
m = 10
min_a = 0
max_a = .5 * math.pi


for j in range(m):
    
    delta_a = (max_a - min_a) / n

    t_list = []

    # make a copy and rotate into initial position
    t = copy.deepcopy(shape)
    xf = Xform.rotation(angle = (min_a - delta_a))
    t._verts = [v * xf for v in t._verts]


    # make transform for incremental rotations
    xf = Xform.rotation(angle = delta_a)

    for i in range(n+1):
        t._verts = [v * xf for v in t._verts]
        b_area = t.bounds.dim_x * t.bounds.dim_y
        t_list.append([min_a + i*delta_a,b_area])

    min_vals = min(t_list, key=lambda s: (s[1]))
    print "Iteration :",j
    print t_list
    print "Minimum values : ",min_vals

    min_a = min_vals[0] - delta_a
    max_a = min_vals[0] + delta_a
    delta_a = 2 * delta_a / n


print

raw_input("press enter...")