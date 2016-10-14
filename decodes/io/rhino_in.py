from .. import *
from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_xform
import rhinoscriptsyntax as rs
if VERBOSE_FS: print("rhino_in loaded")


class RhinoIn():
    """innie for pulling stuff from rhino"""
    """based on Rhinoscript package"""
    
    def __init__(self):
        pass
        
    def get_point(self, prompt="select a point"):
        rh_point = rs.GetPoint(prompt)
        return Point(rh_point[0],rh_point[1],rh_point[2])
        
    def get_mesh(self, prompt="select a mesh", triangulate=False):
        mesh_id = rs.GetObject(prompt, 32, True)
        rh_mesh = rs.coercemesh(mesh_id)
        
        verts = [Point(rh_pt.X,rh_pt.Y,rh_pt.Z) for rh_pt in rh_mesh.Vertices]
        faces = []
        for rh_fc in rh_mesh.Faces :
            if triangulate:
                faces.append([rh_fc[0],rh_fc[1],rh_fc[2]]) #add the first three points of each face
                if rh_fc[2] != rh_fc[3] : 
                    faces.append([rh_fc[0],rh_fc[2],rh_fc[3]]) #if face is a quad, add the missing triangle
            else :
                if rh_fc[2] == rh_fc[3] : faces.append([rh_fc[0],rh_fc[1],rh_fc[2]])
                else : faces.append([rh_fc[0],rh_fc[1],rh_fc[2],rh_fc[3]])
            
        return Mesh(verts,faces)


def from_rgvec(rg_vec):
    return Vec(rg_vec.X,rg_vec.Y,rg_vec.Z)

def from_rgpt(rg_pt):
    return Point(rg_pt.X,rg_pt.Y,rg_pt.Z)

def from_rgplane(rh_plane):
        cpt = from_rgpt(rh_plane.Origin)
        x_axis = from_rgvec(rh_plane.XAxis)
        y_axis = from_rgvec(rh_plane.YAxis)
        return CS(cpt,x_axis,y_axis)

def from_rgpolyline(gh_polyline):
    if gh_polyline.IsClosed : 
        gh_curve = gh_polyline.ToNurbsCurve()
        isplanar, plane = gh_curve.TryGetPlane()
        if isplanar : 
            cs = from_rgplane(plane)
            w_verts = [from_rgpt(gh_polyline[i]) for i in range(len(gh_polyline))]
            verts = [ Vec(pt*cs.ixform) for pt in w_verts ]
            if (verts[0]==verts[-1]) : del verts[-1] #remove last vert if a duplicate
            return PGon(verts,cs)
        else:
            warnings.warn("Cannot import non-planar closed polyline as PGon, attempting to import as a PLine")
        
    # if we've gotten this far, then the pline isn't closed, or is closed and non-planar
    gh_curve = gh_polyline.ToNurbsCurve()
    w_verts = [from_rgpt(gh_polyline[i]) for i in range(len(gh_polyline))]
    return PLine(w_verts)
    

def from_rgtransform(rh_xf):
    xf = Xform()
    xf.m00, xf.m01, xf.m02, xf.m03 = rh_xf.M00, rh_xf.M01, rh_xf.M02, rh_xf.M03
    xf.m10, xf.m11, xf.m12, xf.m13 = rh_xf.M10, rh_xf.M11, rh_xf.M12, rh_xf.M13
    xf.m20, xf.m21, xf.m22, xf.m23 = rh_xf.M20, rh_xf.M21, rh_xf.M22, rh_xf.M23
    xf.m30, xf.m31, xf.m32, xf.m33 = rh_xf.M30, rh_xf.M31, rh_xf.M32, rh_xf.M33
    return xf

