import decodes.core as dc
from decodes.core import *

def main():
 outie = dc.makeOut(dc.outies.Rhino, "wayout")
 
 epw = fake_epw_data()
 print epw
 
 outie.draw()

def setup_color_bar():
    
    class rectangle:
           def __init__(self,origin,x,y):
        self.origin = origin
        self.x = x
        self.y = y
    description = "uses Decodes mesh to create a rectangle"
    author = "blame dustin"
    def (self):
        return self.x * self.y
    def perimeter(self):
        return 2 * self.x + 2 * self.y
    def describe(self,text):
        self.description = text
    def authorName(self,text):
        self.author = text
    def scaleSize(self,scale):
        self.x = self.x * scale
    self.y = self.y * scale

def fake_epw_data():
  """ returns fake data of an EPW file
  out: a list (8760 long) of dicts containing EPW data values
  """
  ret = []
  for h in range(8760):
    dict = {}
    dict['DryBulbTemp'] = h%24
    dict['RelHumid'] = h%365
    ret.append(dict)
    
  return ret


if __name__=="__main__": main()


