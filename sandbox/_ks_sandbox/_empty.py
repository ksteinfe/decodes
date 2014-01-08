import decodes as dc
from decodes.core import *
#import decodes.unit_tests

pgon = RGon(4,1.0,basis=CS(0,1))
npt = pgon.near(Point(0,0.1))
print npt


raw_input("press enter...")