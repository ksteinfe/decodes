import fieldpack as fp
from fieldpack import *
import colorsys

class Color():
  def __init__(self, a=None, b=None, c=None):
    if a is None : self.r,self.g,self.b = 0.5,0.5,0.5
    elif b is None or c is None : self.r,self.g,self.b = a,a,a
    else :
      self.r = a
      self.g = b
      self.b = c
    
  @staticmethod
  def RGB(r,g,b):return Color(r,g,b)
  
  @staticmethod
  def HSB(h,s=1,b=1):
    clr = colorsys.hsv_to_rgb(h,s,b)
    #print clr[0],clr[1],clr[2]
    return Color(clr[0],clr[1],clr[2])
    
  @staticmethod
  def interpolate(c0,c1,t):
    r = (1-t) * c0.r + t * c1.r
    g = (1-t) * c0.g + t * c1.g
    b = (1-t) * c0.b + t * c1.b
    return Color(r,g,b)
    
  def __repr__(self):
    return "color[{0},{1},{2}]".format(self.r,self.g,self.b)