from .. import core as dc
if dc.VERBOSE_FS: print "cs.py loaded"

import Rhino

from core.outies.rhinoUtil import *
import copy, collections

class CS(dc.Geometry, dc.Basis):
  """a ortho coordinate system class"""
  """a simple orthonormal cs floating around in R3"""
  """can describe any translation and rigid-body manipulation of the R3"""
  
  def __init__(self,pt=dc.Point(0,0),vecX=dc.Vec(1,0),vecY=dc.Vec(0,1)):
    #TODO: make axes priviate and provide getters and setters that maintain orthagonality and right-handedness
    self.origin = pt.basis_applied()
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
    return dc.Xform.change_basis(CS(), self)
    
  @property
  def ixform(self): 
    return dc.Xform.change_basis(self, CS())
  
  def toRhPlane(self):
    return Rhino.Geometry.Plane(VecToPoint3d(self.origin),VecToVec3d(self.xAxis),VecToVec3d(self.yAxis))


class CylCS(dc.Geometry, dc.Basis):
  """a cylindrical coordinate system"""
  def __init__(self,pt=dc.Point(0,0)):
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
    
    
