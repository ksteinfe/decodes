import decodes as dc
from decodes.core import *
from decodes.extensions.reaction_diffusion import GrayScott
import random

import os
path = os.path.expanduser("~") + os.sep + "_decodes_export"

width = 20
height = 20
diffusion = GrayScott(Interval(width,height))

'''
for x in range(width):
    for y in range(height):
        if random.uniform(0,1) > 0.75:
            diffusion.set_u(x,y,0.5)
            diffusion.set_v(x,y,0.25)
'''
'''
for r in range(4):
    diffusion.set_rect(random.uniform(10,width-10),random.uniform(10,height-10),random.uniform(2,8),random.uniform(2,8))
'''

diffusion.set_rect(3,10,2,8)
diffusion.set_rect(width-3,height-10,2,8)
diffusion.set_rect(width/2,2,4,4)

from time import time
for n in range(20):
    print "step",n
    t0 = time()
    for m in range(10): diffusion.step()
    diffusion.record()
    print 'step took: %f' %(time()-t0)

n = 0
for img in diffusion.to_image_sequence():
    img.save("img_"+str(n), path, True)
    n+=1

'''
vfield = ValueField(Interval(100,100))

for n in range(3):
    vfield.set(1,1,10.0)
    vfield.set(1,2,8.0)
    vfield.set(3,n,8.0)
    img = vfield.to_image(Color(1.0),Color(1.0,0,0))
    img.save("img_"+str(n), path)
'''

#raw_input("press enter...")