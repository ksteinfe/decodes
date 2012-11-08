import decodes.core as dc
from decodes.core import *


def main():
  outie = makeOut(outies.SVG, "svgtest", path="svgtest_out.svg")
  
  r = rect(Point(100,100),20,30)
  r.set_color(Color(1,0,0))
  outie.put(r)
  
  outie.draw()


if __name__ == "__main__" : 
    main()
