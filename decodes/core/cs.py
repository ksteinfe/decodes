import decodes.core as dc
from decodes.core import *
if VERBOSE_FS: print "cs.py loaded"

import Rhino
import math

from decodes.core.outies.rhinoUtil import *
import copy, collections

class CS(Geometry, Basis):
  """a ortho coordinate system class"""
  """a simple orthonormal cs floating around in R3"""
  """can describe any translation and rigid-body manipulation of the R3"""
  
  def __init__(self,pt=Point(0,0),vecX=Vec(1,0),vecY=Vec(0,1)):
    #TODO: make axes priviate and provide getters and setters that maintain orthagonality and right-handedness
    try: self.origin = pt.basis_applied()
    except : self.origin = pt
    self.xAxis = vecX.normalized()
    self.zAxis = self.xAxis.cross(vecY).normalized()
    self.yAxis = self.zAxis.cross(self.xAxis).normalized()

  def __repr__(self):
    return "cs o[{0},{1},{2}] n[{3},{4},{5}]".format(self.origin.x,self.origin.y,self.origin.z,self.zAxis.x,self.zAxis.y,self.zAxis.z)

  """a CS can act as a basis for a point"""
  def eval(self,other):
    try:
        x = other.x
        y = other.y
        z = other.z
    except TypeError:
        print("mallard can't quack()")
    return self.origin + ((self.xAxis*x)+(self.yAxis*y)+(self.zAxis*z))

  @property
  def xform(self): 
    return Xform.change_basis(CS(), self)
    
  @property
  def ixform(self): 
    return Xform.change_basis(self, CS())
  
  def toRhPlane(self):
    return Rhino.Geometry.Plane(VecToPoint3d(self.origin),VecToVec3d(self.xAxis),VecToVec3d(self.yAxis))


class CylCS(Geometry, Basis):
  """a cylindrical coordinate system"""
  def __init__(self,pt=Point(0,0)):
    self.origin = pt

    def __repr__(self):
      return "cylcs o[{0},{1},{2}]".format(self.origin.x,self.origin.y,self.origin.z)

  """a CylCS can act as a basis for a point"""
  def eval(self,other):
    try:
        radius = other.x
        radians = other.y
        z = other.z
    except TypeError:
        print("mallard can't quack()")
        
    return Point( radius * math.cos(radians), radius * math.sin(radians), z) + self.origin
    
    
