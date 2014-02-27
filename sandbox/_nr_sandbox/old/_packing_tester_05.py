import decodes as dc
from decodes.core import *
from decodes.extensions import packing
import random
from time import time
import math

import os,cStringIO
path = os.path.expanduser("~") + os.sep + "_decodes_export"
f_prefix = "pack_21_"
random.seed(0)


# initialize parameters
print packing.rand_points(10,100)

sheet_size = Interval(240,240)
no_rects = 40
no_sheets = 1

# create list of random shapes
shapes = []
for i in range(no_rects):
    shapes.append(PGon(packing.rand_points(random.randint(3,10),random.randint(1,min(sheet_size.a,sheet_size.b)/3))))

# sort, bin and extract the polygons
print "sorting..."
shapes_sorted = packing.sort_polygons(shapes, 'a', reverse_list = True)

print "packing..."
sheets_filled = packing.bin_polygons(shapes_sorted, sheet_size)

print "extracting..."
shapes_packed = packing.extract_polygons(sheets_filled)

no_sheets = len(sheets_filled)

# send the geometry to an outie
outie = dc.makeOut(dc.Outies.SVG, f_prefix, canvas_dimensions=Interval(no_sheets * sheet_size.a,sheet_size.b), flip_y = True)

for x in shapes_packed:
    outie.put(x)
    
outie.draw()
    
raw_input("press enter...")