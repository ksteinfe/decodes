import decodes as dc
from decodes.core import *
import decodes.extensions.reaction_diffusion
#import decodes.unit_tests 

img = ValueField(Interval(200,200))
img.set(1,1,10.0)
img.set(1,2,8.0)
img.set(3,1,8.0)

img = img.to_image(Color(1.0),Color(1.0,0,0))
img.save("ksteinfe")


#raw_input("press enter...")