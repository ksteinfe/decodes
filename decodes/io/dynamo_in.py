from .. import *
from ..core import *
from ..core import dc_color, dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_xform, dc_intersection
from .rhino_in import *
if VERBOSE_FS: print "dynamo_in loaded"

#import Rhino.Geometry as rg
#import System.Drawing.Color

import clr, collections

clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry as ds

#TODO: figure out how to hack the code completion thingo to display decodes geometry after gh geom has been translated



class DynamoIn():
    """innie for pulling stuff from dynamo"""
    primitive_types = ["bool", "int", "float", "str"]
    structure_types = ["classobj", "instance", "function", "class"]
    friendly_types = ["DHr"]
    
    def __init__(self):
        pass
        
    @staticmethod
    def get(gh_in_str, gh_in):
        # main function for processing incoming data from Grasshopper into Decodes geometry
        # incoming may be a sigleton, a list, or a datatree
        # variable in GH script component will be replaced by whatever is returned here

        if gh_in is None : return None
        if type(gh_in) is list: return [DynamoIn.get(gh_in_str+"["+str(i)+"]",item) for i, item in enumerate(gh_in)]
        
        #if type(gh_in) is rg.Interval: return Interval(gh_in.T0,gh_in.T1)

        if type(gh_in) is ds.Rectangle3d :  gh_in = gh_in.ToPolyline()

        if type(gh_in) is rg.Vector3d : return from_dynvec(gh_in)
        elif type(gh_in)is rg.Point3d : return from_dynpt(gh_in)
        elif type(gh_in)is rg.Plane : 
            return CS(from_dynpt(gh_in.Origin), from_dynvec(gh_in.XAxis), from_dynvec(gh_in.YAxis))
        elif type(gh_in) is rg.Line : 
            return Segment(Point(gh_in.FromX,gh_in.FromY,gh_in.FromZ),Point(gh_in.ToX,gh_in.ToY,gh_in.ToZ))
        elif type(gh_in) is rg.LineCurve : 
            return Segment(Point(gh_in.PointAtStart.X,gh_in.PointAtStart.Y,gh_in.PointAtStart.Z),Point(gh_in.PointAtEnd.X,gh_in.PointAtEnd.Y,gh_in.PointAtEnd.Z))
        elif type(gh_in) is System.Drawing.Color : 
            return Color(float(gh_in.R)/255,float(gh_in.G)/255,float(gh_in.B)/255)

        elif type(gh_in)is rg.Circle :
            pln = Plane( from_dynpt(gh_in.Center), from_dynvec(gh_in.Plane.Normal))
            return Circle(pln,gh_in.Radius)
            
        elif type(gh_in)is rg.Arc :
            x_axis = Vec(from_dynpt(gh_in.Center),from_dynpt(gh_in.StartPoint))
            y_axis = from_dynvec(gh_in.Plane.Normal).cross(x_axis)
            cs = CS( from_dynpt(gh_in.Center), x_axis, y_axis )
            swp_ang = abs(gh_in.EndAngle - gh_in.StartAngle)
            return Arc(cs,gh_in.Radius,swp_ang)

        elif type(gh_in) is rg.PolylineCurve: 
            ispolyline, dyn_polyline = gh_in.TryGetPolyline()
            if (ispolyline) : return from_rgpolyline(dyn_polyline)
        elif type(gh_in) is rg.Polyline:
            return from_rgpolyline(gh_in)
        elif type(gh_in) is rg.NurbsCurve : 
            #TODO: check if gh_in can be described as a line first...
            ispolyline, dyn_polyline = gh_in.TryGetPolyline()
            if (ispolyline) : return from_rgpolyline(dyn_polyline)
        elif type(gh_in) is rg.Mesh : 
            verts = [Point(rh_pt.X,rh_pt.Y,rh_pt.Z) for rh_pt in gh_in.Vertices]
            faces = []
            for rh_fc in gh_in.Faces :
                if rh_fc[2] == rh_fc[3] : faces.append([rh_fc[0],rh_fc[1],rh_fc[2]]) #add this triangle
                else : faces.append([rh_fc[0],rh_fc[1],rh_fc[2],rh_fc[3]]) #add this quad
            return Mesh(verts,faces)

        elif any(p in str(type(gh_in)) for p in GrasshopperIn.primitive_types) : return gh_in
        elif any(p in str(type(gh_in)) for p in GrasshopperIn.friendly_types) : return gh_in
        elif any(p in str(type(gh_in)) for p in GrasshopperIn.structure_types) : return gh_in
        else :
            print "UNKNOWN TYPE: "+gh_in_str+" is an "+ str(type(gh_in))
            return gh_in
            #print inspect.getmro(gh_in.__class__)
            #if issubclass(gh_in.__class__, rg.GeometryBase ) : print "this is geometry"
            #print gh_incoming.TypeHint
            #print gh_incoming.Description


def from_dynvec(dyn_vec):
    return Vec(dyn_vec.X,dyn_vec.Y,dyn_vec.Z)

def from_dynpt(dyn_pt):
    return Point(dyn_pt.X,dyn_pt.Y,dyn_pt.Z)

def from_dynplane(dyn_plane):
        cpt = from_dynpt(dyn_plane.Origin)
        x_axis = from_dynvec(dyn_plane.XAxis)
        y_axis = from_dynvec(dyn_plane.YAxis)
        return CS(cpt,x_axis,y_axis)

def from_rgpolyline(dyn_polyline):
    if not dyn_polyline.IsClosed : 
        gh_curve = dyn_polyline.ToNurbsCurve()
        w_verts = [from_dynpt(dyn_polyline[i]) for i in range(len(dyn_polyline))]
        return PLine(w_verts)
    else:
        gh_curve = dyn_polyline.ToNurbsCurve()
        isplanar, plane = gh_curve.TryGetPlane()
        if not isplanar : raise GeometricError("Cannot import non-planar polylines as polygons.  Did you give me degenerate geometry?")
        cs = from_dynplane(plane)
        w_verts = [from_dynpt(dyn_polyline[i]) for i in range(len(dyn_polyline))]
        verts = [ Vec(pt*cs.ixform) for pt in w_verts ]
        if (verts[0]==verts[-1]) : del verts[-1] #remove last vert if a duplicate
        return PGon(verts,cs)
    

def from_rgtransform(rh_xf):
    xf = Xform()
    xf.m00, xf.m01, xf.m02, xf.m03 = rh_xf.M00, rh_xf.M01, rh_xf.M02, rh_xf.M03
    xf.m10, xf.m11, xf.m12, xf.m13 = rh_xf.M10, rh_xf.M11, rh_xf.M12, rh_xf.M13
    xf.m20, xf.m21, xf.m22, xf.m23 = rh_xf.M20, rh_xf.M21, rh_xf.M22, rh_xf.M23
    xf.m30, xf.m31, xf.m32, xf.m33 = rh_xf.M30, rh_xf.M31, rh_xf.M32, rh_xf.M33
    return xf

'''
for reference: the following code is injected before and after a user's script in grasshopper components
## -- BEGIN DECODES HEADER -- ##
import decodes as dc
from decodes.core import *
from decodes.io.gh_in import *
from decodes.io.gh_out import *
exec(io.gh_in.component_header_code)
exec(io.gh_out.component_header_code)
## -- END DECODES HEADER -- ##

## -- BEGIN DECODES FOOTER -- ##
exec(io.gh_in.component_footer_code)
exec(io.gh_out.component_footer_code)
## -- END DECODES FOOTER -- ##
'''
        
#TODO: make this into a proper innie instead
component_header_code = """
inputs = ghenv.Component.Params.Input
import Rhino.Geometry as rg
import System.Drawing.Color
for input in inputs : 
        gh_in_str = input.Name
        vars()[gh_in_str] = GrasshopperIn.get(gh_in_str, eval(gh_in_str))
"""

component_footer_code = ""