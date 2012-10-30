from decodes import core as dc
if dc.VERBOSE_FS: print "rhinoOut loaded"

import outie
import rhinoUtil
from rhinoUtil import VecToPoint3d

import scriptcontext
import Rhino
import System.Guid


class RhinoOut(outie.Outie):
  """outie for pushing stuff to rhino"""
  
  def __init__(self, layername):
    super(RhinoOut,self).__init__()
    
    # create a copy of this document's default object atts and modify
    self.attr = scriptcontext.doc.CreateDefaultAttributes()
    #attr.ObjectDecoration = Rhino.DocObjects.ObjectDecoration.BothArrowhead
    layerindex = rhinoUtil.makelayer(layername)
    self.attr.LayerIndex = layerindex
    
  def _startDraw(self):
    if hasattr(self, 'color'):
      self.attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
      self.attr.ObjectColor = System.Drawing.Color.FromArgb(self.color.r*255,self.color.g*255,self.color.b*255)
  
  def _endDraw(self):
    scriptcontext.doc.Views.Redraw();
    
  def _drawGeom(self, g):
    # here we sort out what type of geometry we're dealing with, and call the proper draw functions
    # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)
    obj_attr = self.attr.Duplicate()
    if hasattr(g, 'name'): obj_attr.Name = g.name
    if hasattr(g, 'props') and 'color' in g.props:
      obj_attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
      obj_attr.ObjectColor = System.Drawing.Color.FromArgb(g.props['color'].r*255,g.props['color'].g*255,g.props['color'].b*255)
    
    if isinstance(g, dc.Mesh) : 
      return self._drawMesh(g,obj_attr)
    if isinstance(g, dc.CS) : 
      return self._drawCS(g,obj_attr)
    if isinstance(g, dc.CylCS) :
      return self._drawCylCS(g,obj_attr)
    if isinstance(g, dc.LinearEntity) : 
      return self._drawLinearEntity(g,obj_attr)
    if isinstance(g, dc.Point) : 
      return self._drawPoint(g,obj_attr)
    if isinstance(g, dc.Vec) : 
      return self._drawVec(g,obj_attr)
    
    return False

  def _drawVec(self, vec, obj_attr):
    origin = Vec(0,0,0)
    guid = scriptcontext.doc.Objects.AddLine(VecToPoint3d(origin),VecToPoint3d(origin+vec),obj_attr)
    return guid!=System.Guid.Empty

  def _drawPoint(self, pt, obj_attr):
    pt = pt.basis_applied()
    guid = scriptcontext.doc.Objects.AddPoint(VecToPoint3d(pt),obj_attr)
    return guid!=System.Guid.Empty

  def _drawMesh(self, mesh, obj_attr):
    rh_mesh = Rhino.Geometry.Mesh()
    for v in mesh.verts: rh_mesh.Vertices.Add(v.x,v.y,v.z)
    for f in mesh.faces: 
      if len(f)==3 : rh_mesh.Faces.AddFace(f[0], f[1], f[2])
      if len(f)==4 : rh_mesh.Faces.AddFace(f[0], f[1], f[2], f[3])
    rh_mesh.Normals.ComputeNormals()
    rh_mesh.Compact()
    guid = scriptcontext.doc.Objects.AddMesh(rh_mesh, obj_attr)
    return guid!=System.Guid.Empty
    
  def _drawLinearEntity(self, ln, obj_attr):
    if ln._vec.length == 0 : return False
    sDocObj = scriptcontext.doc.Objects
    if isinstance(ln, dc.Segment) : 
      guid = sDocObj.AddLine(VecToPoint3d(ln.spt),VecToPoint3d(ln.ept),obj_attr)
      return guid!=System.Guid.Empty
    if isinstance(ln, dc.Ray) : 
      p = sDocObj.AddPoint(VecToPoint3d(ln.spt),obj_attr)
      l = sDocObj.AddLine(VecToPoint3d(ln.spt),VecToPoint3d(ln.ept),obj_attr)
      scriptcontext.doc.Groups.Add([p,l])
    if isinstance(ln, dc.Line) : 
      p = sDocObj.AddPoint(VecToPoint3d(ln.spt),obj_attr)
      l = sDocObj.AddLine(VecToPoint3d(ln.spt-ln.vec/2),VecToPoint3d(ln.spt+ln.vec/2),obj_attr)
      scriptcontext.doc.Groups.Add([p,l])
        
  def _drawCS(self, cs, obj_attr):
    sDocObj = scriptcontext.doc.Objects
    
    obj_attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
    obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,255,255)  
    
    rh_circ = Rhino.Geometry.Circle(Rhino.Geometry.Plane(VecToPoint3d(cs.origin),VecToVec3d(cs.zAxis)), self.iconscale*0.5)
    c = sDocObj.AddCircle(rh_circ,obj_attr)
    
    obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,0,0)  
    x = sDocObj.AddLine(VecToPoint3d(cs.origin), VecToPoint3d(cs.origin+(cs.xAxis*self.iconscale)),obj_attr)
    obj_attr.ObjectColor = System.Drawing.Color.FromArgb(0,255,0)
    y = sDocObj.AddLine(VecToPoint3d(cs.origin), VecToPoint3d(cs.origin+(cs.yAxis*self.iconscale)),obj_attr)
    obj_attr.ObjectColor = System.Drawing.Color.FromArgb(0,0,255)
    z = sDocObj.AddLine(VecToPoint3d(cs.origin), VecToPoint3d(cs.origin+(cs.zAxis*0.5*self.iconscale)),obj_attr)
    obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,255,255)
    o = sDocObj.AddPoint(VecToPoint3d(cs.origin),obj_attr)
    scriptcontext.doc.Groups.Add([c,o,x,y,z])
    
  def _drawCylCS(self, cs, obj_attr):
    sDocObj = scriptcontext.doc.Objects

    obj_attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
    obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,255,255)  

    obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,0,0)  
    x = sDocObj.AddLine(VecToPoint3d(cs.origin), VecToPoint3d(cs.origin+(Vec(1,0,0)*self.iconscale)),obj_attr)
    obj_attr.ObjectColor = System.Drawing.Color.FromArgb(0,255,0)
    rh_circ = Rhino.Geometry.Circle(Rhino.Geometry.Plane(VecToPoint3d(cs.origin),VecToVec3d(Vec(0,0,1))), self.iconscale*0.5)
    y = sDocObj.AddCircle(rh_circ,obj_attr)
    rh_circ = Rhino.Geometry.Circle(Rhino.Geometry.Plane(VecToPoint3d(cs.origin+Vec(0,0,self.iconscale*0.5)),VecToVec3d(Vec(0,0,1))), self.iconscale*0.5)
    yy = sDocObj.AddCircle(rh_circ,obj_attr)
    obj_attr.ObjectColor = System.Drawing.Color.FromArgb(0,0,255)
    z = sDocObj.AddLine(VecToPoint3d(cs.origin), VecToPoint3d(cs.origin+(Vec(0,0,1)*0.5*self.iconscale)),obj_attr)
    obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,255,255)
    o = sDocObj.AddPoint(VecToPoint3d(cs.origin),obj_attr)
    scriptcontext.doc.Groups.Add([o,x,y,yy,z])
    
    return True
    