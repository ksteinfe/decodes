import decodes as dc
from decodes.core import *
#import decodes.unit_tests

cs = CS()
size = 1.2


argon = RGon(4,size)

for x in range(4):
    argon = argon.inflate()
    

argon = RGon.from_edge(Segment(Point(0,0),Point(0,1)),3)


pass

#raw_input("press enter...")