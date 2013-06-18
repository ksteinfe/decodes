import decodes as dc
from decodes.core import *
#import decodes.unit_tests

cs = CS()
size = 1.0


argon = RGon(4,size)
print argon

'''
import time
t0 = time.time()
for n in range(100): a = sin_pi
print time.time()-t0

t0 = time.time()
for n in range(100): a = math.sin(math.pi)
print time.time()-t0
'''

argon = RGon.from_edge(Segment(Point(0,0),Point(0,1)),3)


pass

#raw_input("press enter...")