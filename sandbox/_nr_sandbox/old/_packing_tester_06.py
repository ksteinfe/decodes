import decodes as dc
from decodes.core import *
from decodes.extensions import packing
import random
from time import time
import math

import os,cStringIO
path = os.path.expanduser("~") + os.sep + "_decodes_export"
f_prefix = "pack_24_"
random.seed(0)

b = packing.Strip(0,200,50)
b.put_item(200)

# initialize parameters

stock_size = Interval(0,300)
height = stock_size.b/10.0
no_lengths = 40
no_strips = 1

# create list of random shapes
strips = []
for i in range(no_lengths):
    strips.append(random.randint(height,stock_size.b/2.0))

# sort, bin and extract the polygons
print "sorting..."
strips.sort(reverse=True)

print "packing..."
stock_filled = packing.bin_strips(strips, stock_size)

print "extracting..."
strips_packed = packing.extract_strips(stock_filled, height = height)

no_stock = len(stock_filled)

# send the geometry to an outie
outie = dc.makeOut(dc.Outies.SVG, f_prefix, canvas_dimensions=Interval(stock_size.b,no_stock*height), flip_y = True)

for x in strips_packed:
    outie.put(x)
    
outie.draw()
    
raw_input("press enter...")