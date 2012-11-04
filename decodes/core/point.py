import decodes.core as dc
from decodes.core import *

import math, random
if dc.VERBOSE_FS: print "point.py loaded"


# points may define a "basis"
# interpreted as any object that may be "evaluated" (passed three coords) and return a position in R3
# if no basis is defined for a point, R3 is assumed
# the _x,_y, and _z properties of a point return values in "basis space" (unevaluated by basis)
# the x,y,and z properties of a point return values in "world space" (evaluated by basis)
# if no basis has been defined, these values are the same

class Point(Vec,HasBasis):
  
  def __init__(self, a=0, b=0, c=0, basis=None):
    super(Point,self).__init__(a,b,c)
    self.basis = basis
  
  @property
  def x(self): return self.basis.eval(self.basis_stripped()).x if not self.is_baseless else self._x
  @property
  def y(self): return self.basis.eval(self.basis_stripped()).y if not self.is_baseless else self._y
  @property
  def z(self): return self.basis.eval(self.basis_stripped()).z if not self.is_baseless else self._z

  '''
  returns a new point with basis applied. 
  coords will be interpreted in world space
  points will appear in the same position when drawn
  '''
  def basis_applied(self, copy_children=True): 
    pt = Point(self.x,self.y,self.z)
    if hasattr(self, 'props') : pt.props = self.props
    return pt
  
  '''
  returns a new point stripped of any bases.  
  coords will be interpreted in world space
  points will appear in their "local" position when drawn
  '''
  def basis_stripped(self, copy_children=True): 
    pt = Point(self._x,self._y,self._z)
    if hasattr(self, 'props') : pt.props = self.props
    return pt
  
  '''
  returns a new point with a new basis defined
  '''
  def set_basis(self,basis): return Point(self._x,self._y,self._z,basis=basis)

  def __add__(self, vec): return Point(self.x+vec.x , self.y+vec.y, self.z+vec.z)
  def __sub__(self, vec): return Point(self.x-vec.x , self.y-vec.y, self.z-vec.z)
  def __div__(self, other): return Point(self.x/float(other), self.y/float(other), self.z/float(other))
  def __mul__(self, other):
    if isinstance(other, dc.Xform) :
      return other*self
    else : 
      return dc.Xform.scale(other) * self

  def __repr__(self):
    if not self.is_baseless : return "pt[{0},{1},{2}] basis: {3}".format(self._x,self._y,self._z,self.basis)
    return "pt[{0},{1},{2}]".format(self.x,self.y,self.z)

  '''comparisons are always done in world space'''
  def __lt__(self, other): 
    if self.z < other.z : return True
    if self.z == other.z and self.y < other.y : return True
    if self.z == other.z and self.y == other.y and self.x < other.x : return True
    return False
  def __gt__(self, other): 
    if self.z > other.z : return True
    if self.z == other.z and self.y > other.y : return True
    if self.z == other.z and self.y == other.y and self.x > other.x : return True
    return False
      
  def __le__(self, other): return True if (self < other or self == other) else False 
  def __eq__(self, other): return all([self.x==other.x,self.y==other.y,self.z==other.z])
  def __ne__(self, other): return not all([self.x==other.x,self.y==other.y,self.z==other.z])
  def __ge__(self, other): return True if (self > other or self == other) else False 

  '''distance squared. Cheaper to calculate.'''
  def _distance2(self, other):
    if self.basis is not other.basis : raise BasisError("Cannot measure '_distance2' between points with different bases.  Use 'distance2' instead")
    return Vec(self,other).length2
  def _distance(self, other): 
    if self.basis is not other.basis : raise BasisError("Cannot measure '_distance' between points with different bases.  Use 'distance' instead")
    return Vec(self,other).length
  def distance2(self,other): return Vec(self.basis_applied(),other.basis_applied()).length2
  def distance(self,other): return Vec(self.basis_applied(),other.basis_applied()).length
  
  @staticmethod
  def interpolate(p0,p1,t=0.5): 
    if p0.basis is p1.basis : 
      v = Vec.interpolate(p0,p1,t)
      return Point(v.x,v.y,v.z,p0.basis)
    else : 
      v = Vec.interpolate(p0.basis_applied(),p1.basis_applied(),t)
      return Point(v.x,v.y,v.z)

  @staticmethod
  def _centroid(points): 
    if all( points[0].basis is p.basis for p in points ) : 
      cent = Vec.average([p.basis_stripped() for p in points])
      return Point(cent).set_basis(points[0].basis)
    raise BasisError("Cannot calculate '_centroid' for points of mixed bases.  Use 'centroid' instead")
    
  @staticmethod
  def centroid(points): 
    return Point( Vec.average([p.basis_applied() for p in points]) )
    
  '''Returns a new point projected onto a destination vector'''
  def projected(self, other): return Point( Vec(self.x,self.y,self.z).projected(other) )
  #TODO: think about what this function will mean for new "basis" construct
  #probably eliminate, in favor of projecting onto lines and such in world space
  
  @staticmethod
  def random(rnge=[-1.0,1.0],constrain2d=False):
    x = random.uniform(rnge[0],rnge[1])
    y = random.uniform(rnge[0],rnge[1])
    z = random.uniform(rnge[0],rnge[1])
    p = Point(x,y) if constrain2d else Point(x,y,z)
    return p
    
