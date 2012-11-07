import decodes.core as dc
from decodes.core import *


def main():
    outie = makeOut(outies.SVG, "svgtest", path="svgtest_out.svg")
    
    scale = 20
    for x in range(10):
      for y in range(10):
        pt = Point(x*scale,y*scale)
        pt.set_color(Color(1,0,0))
        outie.put(pt)
        
    for x in range(10):
      for y in range(10):
        pt = Point(x*scale,(y+20)*scale)
        outie.put(pt)
    
    outie.draw()

if __name__ == "__main__" : 
    main()
