from decodes import core as dc
from decodes.core import *

if dc.VERBOSE_FS: print "ghOut loaded"

import clr, outie, collections
import rhinoUtil
from rhinoUtil import *

import Rhino.Geometry as rg


test_variable = 47

component_header_code = """

import decodes.core as dc
from decodes.core import *

inputs = ghenv.Component.Params.Input
outputs = ghenv.Component.Params.Output
for output in outputs :
    if output.NickName != "out":
        vars()[output.NickName] = dc.makeOut(outies.Grasshopper)

		
"""

component_footer_code = """

for output in outputs :
    if output.NickName != "out":
        o = eval(output.NickName)
        if isinstance(o, dc.outies.GrasshopperOut) : vars()[output.NickName] = o.extract_tree()

		
"""


class GrasshopperOut(outie.Outie):
  """outie for pushing stuff to grasshopper"""
  
  def __init__(self):
    super(GrasshopperOut,self).__init__()
    self._allow_foreign = True
    
  def extract_tree(self):
    #creates a grasshopper data tree
    #calls the draw function for each geometric object
    #returns a list of whatever these draw functions return
    clr.AddReference("Grasshopper")
    from Grasshopper import DataTree
    from Grasshopper.Kernel.Data import GH_Path

    tree = DataTree[object]()
    is_leaf = self._is_leaf(self.geom)
    for n,g in enumerate(self.geom): 
      if is_leaf : 
        path = GH_Path(0)
        self._add_branch(g, tree,path)
      else :
        path = GH_Path(n)
        self._add_branch(g, tree,path)
    
    
    self.clear() #empty the outie after each draw
    return tree
    
  def _is_leaf(self, items):
	return not any(self._should_iterate(item) for item in items)

  def _should_iterate(self, item):
	return isinstance(item, collections.Iterable) and not isinstance(item,basestring)
	
  def _add_branch(self, g, tree, path):
    # here we sort out what type of geometry we're dealing with, and call the proper draw functions
    # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)
    
    if self._should_iterate(g) :
      is_leaf = self._is_leaf(g)
      for n,i in enumerate(g): 
        npath = path.AppendElement(n)
        if is_leaf : self._add_branch(i,tree,path)
        else : self._add_branch(i,tree,npath)
      return True
    
    if isinstance(g, dc.Point) : 
      tree.Add(self._drawPoint(g),path)
      return True
    if isinstance(g, dc.Vec) : 
      tree.Add(self._drawVec(g),path)
      return True
    if isinstance(g, dc.Mesh) : 
      tree.Add(self._drawMesh(g),path)
      return True
    if isinstance(g, dc.LinearEntity) : 
      tree.Add(self._drawLinearEntity(g),path)
      return True
    if isinstance(g, dc.CS) : 
      tree.Add(self._drawCS(g),path)
      return True
      
    
    if isinstance(g, (dc.Geometry) ) : raise NotImplementedError("i do not have a translation for that decodes geometry type in GrasshopperOut")
    tree.Add(g,path)

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