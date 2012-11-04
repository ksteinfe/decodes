from decodes import core as dc
from decodes.core import *

if dc.VERBOSE_FS: print "ghOut loaded"

import outie, collections
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
    self._allow_foreign = True
    
  def _startDraw(self):
    pass
  
  def _endDraw(self):
    pass
    
  def _drawGeom(self, g):
    # here we sort out what type of geometry we're dealing with, and call the proper draw functions
    # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)
    
    if isinstance(g, collections.Iterable) : 
      for n,i in enumerate(g): g[n] = self._drawGeom(i)
      return g
    
    if isinstance(g, dc.Point) : 
        return self._drawPoint(g)
    if isinstance(g, dc.Vec) : 
        return self._drawVec(g)
    if isinstance(g, dc.Mesh) : 
        return self._drawMesh(g)
    if isinstance(g, dc.LinearEntity) : 
      return self._drawLinearEntity(g)
    if isinstance(g, dc.CS) : 
      return self._drawCS(g)
      
    raise NotImplementedError("i do not have a translation for that object type in GrasshopperOut")
    return False

  def _drawVec(self, vec): 
    return rg.Vector3d(vec.x,vec.y,vec.z)

  def _drawPoint(self, pt):
    pt = pt.basis_applied()
    return rg.Point3d(pt.x,pt.y,pt.z)
    
  def _drawMesh(self, mesh):
    rh_mesh = rg.Mesh()
    for v in mesh.verts: rh_mesh.Vertices.Add(v.x,v.y,v.z)
    for f in mesh.faces: 
      if len(f)==3 : rh_mesh.Faces.AddFace(f[0], f[1], f[2])
      if len(f)==4 : rh_mesh.Faces.AddFace(f[0], f[1], f[2], f[3])
    rh_mesh.Normals.ComputeNormals()
    rh_mesh.Compact()
    return rh_mesh
  
  def _drawLinearEntity(self, ln):
    if isinstance(ln, dc.Segment) : return rg.Line(rg.Point3d(ln.spt.x,ln.spt.y,ln.spt.z),rg.Point3d(ln.ept.x,ln.ept.y,ln.ept.z))
    if isinstance(ln, dc.Ray) : return [rg.Point3d(ln.spt.x,ln.spt.y,ln.spt.z),rg.Vector3d(ln.vec.x,ln.vec.y,ln.vec.z)]
    if isinstance(ln, dc.Line) :  return rg.Line(rg.Point3d(ln.spt.x,ln.spt.y,ln.spt.z),rg.Point3d(ln.ept.x,ln.ept.y,ln.ept.z))
    
  def _drawCS(self, cs):
    o = rg.Point3d(cs.origin.x,cs.origin.y,cs.origin.z)
    x = rg.Vector3d(cs.xAxis.x,cs.xAxis.y,cs.xAxis.z) 
    y = rg.Vector3d(cs.yAxis.x,cs.yAxis.y,cs.yAxis.z) 
    return rg.Plane(o,x,y)