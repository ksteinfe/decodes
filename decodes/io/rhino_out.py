from .. import *
from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_pline, dc_mesh, dc_pgon
from . import outie
if VERBOSE_FS: print("rhino_out loaded")

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
        layerindex = makelayer(layername)
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
        
        if isinstance(g, Mesh) : 
            return self._drawMesh(g,obj_attr)
        if isinstance(g, CS) : 
            return self._drawCS(g,obj_attr)
        if isinstance(g, CylCS) :
            return self._drawCylCS(g,obj_attr)
        if isinstance(g, LinearEntity) : 
            return self._drawLinearEntity(g,obj_attr)
        if isinstance(g, Point) : 
            return self._drawPoint(g,obj_attr)
        if isinstance(g, Vec) : 
            return self._drawVec(g,obj_attr)
        if isinstance(g, PLine) : 
            return self._drawPline(g,obj_attr)
        if isinstance(g, PGon) : 
            return self._drawPGon(g,obj_attr)
		
        return False

    def _drawVec(self, vec, obj_attr):
        origin = Vec(0,0,0)
        guid = scriptcontext.doc.Objects.AddLine(to_rgpt(origin),to_rgpt(origin+vec),obj_attr)
        return guid!=System.Guid.Empty

    def _drawPoint(self, pt, obj_attr):
        #pt = rg.Point3d(pt.X,pt.Y,pt.Z)
        guid = scriptcontext.doc.Objects.AddPoint(to_rgpt(pt),obj_attr)
        return guid!=System.Guid.Empty

    def _drawMesh(self, mesh, obj_attr):
        rh_mesh = Rhino.Geometry.Mesh()
        for v in mesh.pts: rh_mesh.Vertices.Add(v.x,v.y,v.z)
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
        if isinstance(ln, Segment) : 
            guid = sDocObj.AddLine(to_rgpt(ln.spt),to_rgpt(ln.ept),obj_attr)
            return guid!=System.Guid.Empty
        if isinstance(ln, Ray) : 
            p = sDocObj.AddPoint(to_rgpt(ln.spt),obj_attr)
            l = sDocObj.AddLine(to_rgpt(ln.spt),to_rgpt(ln.ept),obj_attr)
            scriptcontext.doc.Groups.Add([p,l])
        if isinstance(ln, Line) : 
            p = sDocObj.AddPoint(to_rgpt(ln.spt),obj_attr)
            l = sDocObj.AddLine(to_rgpt(ln.spt-ln.vec/2),to_rgpt(ln.spt+ln.vec/2),obj_attr)
            scriptcontext.doc.Groups.Add([p,l])

    def _drawPline(self, other, obj_attr):
        verts = [Rhino.Geometry.Point3d(pt.x,pt.y,pt.z) for pt in other.pts]
        new_pline = Rhino.Geometry.Polyline(verts)
        guid = scriptcontext.doc.Objects.AddPolyline(new_pline,obj_attr)
        return guid!=System.Guid.Empty
             
    def _drawPGon(self, other, obj_attr):
        verts = [Rhino.Geometry.Point3d(pt.x,pt.y,pt.z) for pt in other.pts]
        verts.append(verts[0])
        new_pgon = Rhino.Geometry.Polyline(verts)
        guid = scriptcontext.doc.Objects.AddPolyline(new_pgon,obj_attr)
        return guid!=System.Guid.Empty
             
    def _drawCS(self, cs, obj_attr):
        sDocObj = scriptcontext.doc.Objects
        
        obj_attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,255,255)    
        
        rh_circ = Rhino.Geometry.Circle(Rhino.Geometry.Plane(to_rgpt(cs.origin),to_rgvec(cs.zAxis)), self.iconscale*0.5)
        c = sDocObj.AddCircle(rh_circ,obj_attr)
        
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,0,0)    
        x = sDocObj.AddLine(to_rgpt(cs.origin), to_rgpt(cs.origin+(cs.x_axis*self.iconscale)),obj_attr)
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(0,255,0)
        y = sDocObj.AddLine(to_rgpt(cs.origin), to_rgpt(cs.origin+(cs.y_axis*self.iconscale)),obj_attr)
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(0,0,255)
        z = sDocObj.AddLine(to_rgpt(cs.origin), to_rgpt(cs.origin+(cs.z_axis*0.5*self.iconscale)),obj_attr)
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,255,255)
        o = sDocObj.AddPoint(to_rgpt(cs.origin),obj_attr)
        scriptcontext.doc.Groups.Add([c,o,x,y,z])
        
    def _drawCylCS(self, cs, obj_attr):
        sDocObj = scriptcontext.doc.Objects

        obj_attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,255,255)    

        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,0,0)    
        x = sDocObj.AddLine(to_rgpt(cs.origin), to_rgpt(cs.origin+(Vec(1,0,0)*self.iconscale)),obj_attr)
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(0,255,0)
        rh_circ = Rhino.Geometry.Circle(Rhino.Geometry.Plane(to_rgpt(cs.origin),to_rgvec(Vec(0,0,1))), self.iconscale*0.5)
        y = sDocObj.AddCircle(rh_circ,obj_attr)
        rh_circ = Rhino.Geometry.Circle(Rhino.Geometry.Plane(to_rgpt(cs.origin+Vec(0,0,self.iconscale*0.5)),to_rgvec(Vec(0,0,1))), self.iconscale*0.5)
        yy = sDocObj.AddCircle(rh_circ,obj_attr)
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(0,0,255)
        z = sDocObj.AddLine(to_rgpt(cs.origin), to_rgpt(cs.origin+(Vec(0,0,1)*0.5*self.iconscale)),obj_attr)
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,255,255)
        o = sDocObj.AddPoint(to_rgpt(cs.origin),obj_attr)
        scriptcontext.doc.Groups.Add([o,x,y,yy,z])
        
        return True


def to_rgvec(vec):
    return Rhino.Geometry.Vector3d(vec.x,vec.y,vec.z)
    
def to_rgpt(pt):
    return Rhino.Geometry.Point3d(pt.x,pt.y,pt.z)
    
def to_rgpolyline(other):
    verts = [to_rgpt(pt) for pt in other.pts]
    if isinstance(other, PGon) : verts.append(verts[0])
    return Rhino.Geometry.Polyline(verts)

def to_rgcircle(circ):
    rh_plane = to_rgplane(circ.plane)
    return Rhino.Geometry.Circle(rh_plane,circ.rad)
    
def to_rgarc(arc):
    rh_plane = to_rgplane(arc.basis)
    return Rhino.Geometry.Arc(rh_plane,arc.rad,arc.angle)

def to_rgplane(other):
    if isinstance(other, CS) : 
        return Rhino.Geometry.Plane(to_rgpt(other.origin),to_rgvec(other.x_axis),to_rgvec(other.y_axis))
    if isinstance(other, Plane) : 
        return Rhino.Geometry.Plane(to_rgpt(other.origin),to_rgvec(other.normal))

def to_rh_transform(xf):
    rh_xf = rh_xform = Rhino.Geometry.Transform(1.0)
    rh_xf.M00, rh_xf.M01, rh_xf.M02, rh_xf.M03 = xf.m00, xf.m01, xf.m02, xf.m03
    rh_xf.M10, rh_xf.M11, rh_xf.M12, rh_xf.M13 = xf.m10, xf.m11, xf.m12, xf.m13
    rh_xf.M20, rh_xf.M21, rh_xf.M22, rh_xf.M23 = xf.m20, xf.m21, xf.m22, xf.m23
    rh_xf.M30, rh_xf.M31, rh_xf.M32, rh_xf.M33 = xf.m30, xf.m31, xf.m32, xf.m33
    return rh_xf


def makelayer(layer_name):
    import scriptcontext
    import Rhino
    import System
    layer_index = scriptcontext.doc.Layers.Find(layer_name, True)
    if layer_index>=0:
        if VERBOSE_FS: print("already have a layer called ", layer_name)
        return layer_index
        
    layer_index = scriptcontext.doc.Layers.Add(layer_name, System.Drawing.Color.FromArgb(0,0,0))
    return layer_index

def interpolated_curve(points):
    import Rhino
    import System
    rh_points = [to_rgpt(pt) for pt in points]
    degree = 3
    start_tangent = Rhino.Geometry.Vector3d(0,0,0)
    end_tangent = Rhino.Geometry.Vector3d(0,0,0)
    knotstyle = System.Enum.ToObject(Rhino.Geometry.CurveKnotStyle, 0)
    curve = Rhino.Geometry.Curve.CreateInterpolatedCurve(rh_points, degree, knotstyle, start_tangent, end_tangent)
    if not curve: raise Exception("unable to CreateInterpolatedCurve")
    return curve