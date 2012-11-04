from decodes import core as dc
from decodes.core import *

if dc.VERBOSE_FS: print "ghOut loaded"

import outie
import rhinoUtil
from rhinoUtil import *

#import scriptcontext
#import Rhino
#import System.Guid

import Rhino.Geometry as rg


class GrasshopperOut(outie.Outie):
  """outie for pushing stuff to grasshopper"""
  
  def __init__(self):
    super(GrasshopperOut,self).__init__()
    
  def _startDraw(self):
    print "startDraw"
  
  def _endDraw(self):
    print "endDraw"
    
  def _drawGeom(self, g):
    # here we sort out what type of geometry we're dealing with, and call the proper draw functions
    # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)

    if isinstance(g, dc.Point) : 
      return self._drawPoint(g)
    if isinstance(g, dc.Vec) : 
      return self._drawVec(g)
    
    raise NotImplementedError("i do not have a translation for that object type in GrasshopperOut")
    return False

  def _drawVec(self, vec): 
    return rg.Vector3d(vec.x,vec.y,vec.z)

  def _drawPoint(self, pt):
    pt = pt.basis_applied()
    return rg.Point3d(pt.x,pt.y,pt.z)

    