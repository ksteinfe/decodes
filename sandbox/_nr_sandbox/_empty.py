import decodes as dc
from decodes.core import *
from decodes.extensions.cellular_automata import CA
import random

import os
path = os.path.expanduser("~") + os.sep + "_decodes_export"

def func(a,b):
    return True

for k in range(100):
    print func(1,2)

width = 2
height = 2
test = CA(Interval(width,height))
test.set_rule(func)

for n in range(10):
    print "step",n
    for m in range(1): test.step()
    test.record()

for n in range(10):
    img = test.hist_u[n].to_image()
    img.save("img_"+str(n), path, True)

'''
n = 0
for img in test.to_image_sequence():
    img.save("img_"+str(n), path, True)
    n+=1


vfield = ValueField(Interval(100,100))

for n in range(3):
    vfield.set(1,1,10.0)
    vfield.set(1,2,8.0)
    vfield.set(3,n,8.0)
    img = vfield.to_image(Color(1.0),Color(1.0,0,0))
    img.save("img_"+str(n), path)
'''

raw_input("press enter...")