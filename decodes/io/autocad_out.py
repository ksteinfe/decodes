from .. import *
from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_pline, dc_mesh, dc_pgon
from . import outie
if VERBOSE_FS: print("autocad-out loaded")

from decodes.io.pyautocad import *



class AutocadOut(outie.Outie):
    """outie for pushing stuff to autocad"""
    
    def __init__(self, layername):
        super(AutocadOut,self).__init__()
        
    def _startDraw(self):
    
        # Get the current document, if it doesn't exist, create it.
        self.acad = Autocad(create_if_not_exists=True)
        # Add some code to make layers...
        '''
        layerindex = makelayer(layername)
        self.attr.LayerIndex = layerindex'''
        '''
        if hasattr(self, 'color'):
            self.attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
            self.attr.ObjectColor = System.Drawing.Color.FromArgb(self.color.r*255,self.color.g*255,self.color.b*255)'''
    
    def _drawGeom(self, g):
        # here we sort out what type of geometry we're dealing with, and call the proper draw functions
        # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)

        obj_attr = {}
        if hasattr(g, 'name'): obj_attr['name'] = g.name
        if hasattr(g, 'props') and 'color' in g.props:
            obj_attr['color'] = g.props['color']
        if hasattr(g, 'props') and 'weight' in g.props:
            obj_attr['weight'] = g.props['weight']
        else:
            obj_attr = None
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
            return self._drawPLine(g,obj_attr)
        if isinstance(g, PGon) : 
            return self._drawPGon(g,obj_attr)
        if isinstance(g, Curve) : 
            return self._drawCurve(g,obj_attr)
        if isinstance(g, Plane) : 
            return self._drawPlane(g,obj_attr)
        
        return False
    
    def _drawVec(self, vec, obj_attr):
        origin = Vec(0,0,0)
        new_geom = self.acad.model.AddLine(to_acadpt(origin),to_acadpt(vec))
        if new_geom: return True

    def _drawPoint(self, pt, obj_attr):
        pt = pt.basis_applied()
        new_geom = self.acad.model.AddPoint(to_acadpt(pt))
        if new_geom: return True
    
    def _drawMesh(self, mesh, obj_attr):
        meshes = Mesh.explode(mesh)
        for mesh in meshes:
            if len(mesh.pts) == 3:
                pt1 = aDouble([mesh.pts[0].x,mesh.pts[0].y,mesh.pts[0].z])
                pt2 = aDouble([mesh.pts[1].x,mesh.pts[1].y,mesh.pts[1].z])
                pt3 = aDouble([mesh.pts[2].x,mesh.pts[2].y,mesh.pts[2].z])
                new_geom = self.acad.model.Add3DFace(pt1,pt2,pt3,pt3)
                #testing to add colors
                #new_geom.Color = 15
            else:
                pt1 = aDouble([mesh.pts[0].x,mesh.pts[0].y,mesh.pts[0].z])
                pt2 = aDouble([mesh.pts[1].x,mesh.pts[1].y,mesh.pts[1].z])
                pt3 = aDouble([mesh.pts[2].x,mesh.pts[2].y,mesh.pts[2].z])
                pt4 = aDouble([mesh.pts[3].x,mesh.pts[3].y,mesh.pts[3].z])
                new_geom = self.acad.model.Add3DFace(pt1,pt2,pt4,pt3)
        if new_geom: return True
        
    def _drawPlane(self, plane, obj_attr):
        origin = plane.origin
        tvec = plane.vec
        '''
        pt1 = aDouble([plane.pts[0].x,plane.pts[0].y,plane.pts[0].z])
        pt2 = aDouble([plane.pts[1].x,plane.pts[1].y,plane.pts[1].z])
        pt3 = aDouble([plane.pts[2].x,plane.pts[2].y,plane.pts[2].z])
        pt4 = aDouble([plane.pts[3].x,plane.pts[3].y,plane.pts[3].z])
        new_geom = self.acad.model.Add3DFace(pt1,pt2,pt4,pt3)
        '''
        if new_geom: return True
    
    def _drawLinearEntity(self, ln, obj_attr):
        if ln._vec.length == 0 : return False
        if isinstance(ln, Segment) : 
            new_geom = self.acad.model.AddLine(to_acadpt(ln.spt),to_acadpt(ln.ept))
            if new_geom: return True
        if isinstance(ln, Ray) : 
            new_geom = self.acad.model.AddRay(to_acadpt(ln.spt),to_acadpt(ln.ept))
            if new_geom: return True
        if isinstance(ln, Line) : 
            new_geom = self.acad.model.AddXLine(to_acadpt(ln.spt),to_acadpt(ln.ept))
            if new_geom: return True
            
    def _drawPLine(self, pl, obj_attr):
        if pl.length == 0 : return False
        new_geom = self.acad.model.Add3Dpoly(to_acadverts(pl))
        if new_geom: return True
        
    def _drawPGon(self, pg, obj_attr):
        if len(pg.edges) == 0 : return False
        new_geom = self.acad.model.Add3Dpoly(to_acadverts(pg,True))
        if new_geom: return True

    def _drawCurve(self, crv, obj_attr):
        crv = crv.surrogate
        if crv.length == 0 : return False
        new_geom = self.acad.model.Add3Dpoly(to_acadverts(crv))
        new_lay = self.acad.Layers.Add("ABC")
        new_geom.Layer = new_lay
        if new_geom: return True
        
    '''
    def _drawCS(self, cs, obj_attr):
        sDocObj = scriptcontext.doc.Objects
        
        obj_attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,255,255)    
        
        rh_circ = Rhino.Geometry.Circle(Rhino.Geometry.Plane(to_rgpt(cs.origin),to_rgvec(cs.zAxis)), self.iconscale*0.5)
        c = sDocObj.AddCircle(rh_circ,obj_attr)
        
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(255,0,0)    
        x = sDocObj.AddLine(to_rgpt(cs.origin), to_rgpt(cs.origin+(cs.xAxis*self.iconscale)),obj_attr)
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(0,255,0)
        y = sDocObj.AddLine(to_rgpt(cs.origin), to_rgpt(cs.origin+(cs.yAxis*self.iconscale)),obj_attr)
        obj_attr.ObjectColor = System.Drawing.Color.FromArgb(0,0,255)
        z = sDocObj.AddLine(to_rgpt(cs.origin), to_rgpt(cs.origin+(cs.zAxis*0.5*self.iconscale)),obj_attr)
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
    
'''
def to_acadpt(point):
    return APoint(point.x, point.y, point.z) 
    
def to_acadverts(pl, closed=False):
    pline_pts = []
    for vert in pl.pts:
        pline_pts.append(vert.x)
        pline_pts.append(vert.y)
        pline_pts.append(vert.z)
    if closed: 
        pline_pts.append(pline_pts[0])
        pline_pts.append(pline_pts[1])
        pline_pts.append(pline_pts[2])
    return aDouble(pline_pts)

'''
def to_rgplane(other):
    if isinstance(other, CS) : 
        return Rhino.Geometry.Plane(to_rgpt(other.origin),to_rgvec(other.xAxis),to_rgvec(other.yAxis))
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
        if VERBOSE_FS: print "already have a layer called ", layer_name
        return layer_index
        
    layer_index = scriptcontext.doc.Layers.Add(layer_name, System.Drawing.Color.Black)
    return layer_index
'''