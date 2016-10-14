from .. import *
from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_pline, dc_mesh, dc_pgon
from . import outie
if VERBOSE_FS: print("dynamo_out loaded")

import clr, collections

clr.AddReference('ProtoGeometry')
clr.AddReference('DSCoreNodes')

import Autodesk.DesignScript.Geometry as ds
import DSCore
#TODO: check at end of script if the user overwrote the established 'outie' with either a singleton, a list of sc.Geoms, or something else, and act accordingly (raising the appropriate warnings) 

class DynamoOut(outie.Outie):
    """outie for pushing stuff to grasshopper"""
    raw_types = ["Curve","Surface"]
    primitive_types = ["bool", "int", "float", "str"]
    structure_types = ["classobj", "instance", "function", "class"]
    friendly_types = ["DHr"]

    def __init__(self):
        super(DynamoOut,self).__init__()
        self._allow_foreign = True
        
    def _is_leaf(self, items): return not any(self._should_iterate(item) for item in items)

    def _should_iterate(self, item): return isinstance(item, collections.Iterable) and not isinstance(item,str)
    
    def _drawGeom(self, g):
        # here we sort out what type of geometry we're dealing with, and call the proper draw functions
        # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)
        
        if self._should_iterate(g) :
            return [self._drawGeom(gg) for gg in g]
            
        if isinstance(g, Mesh) : 
            return self._drawMesh(g)
        if isinstance(g, CS) : 
            return self._drawCS(g)
        if isinstance(g, CylCS) :
            return self._drawCylCS(g,obj_attr)
        if isinstance(g, LinearEntity) : 
            dyn_geom = self._drawLinearEntity(g)
        if isinstance(g, Point) : 
            return self._drawPoint(g)
        if isinstance(g, Vec) : 
            return self._drawVec(g)
        if isinstance(g, PLine) : 
            return self._drawPLine(g)
        if isinstance(g, Circle) : 
            return self._drawCircle(g)
        if isinstance(g, Arc) : 
            return self._drawArc(g)
        if isinstance(g, PGon) : 
            return self._drawPGon(g)
        if isinstance(g, Plane) : 
            return self._drawPlane(g)
        if isinstance(g,Curve): 
            return self._drawCurve(g)
        if isinstance(g,Color): 
            return self._drawColor(g)
        # ADD ANY RAW TYPES DIRECTLY
        if any(p in str(type(g)) for p in DynamoOut.raw_types) : return g
        if any(p in str(type(g)) for p in DynamoOut.primitive_types): 
            return g
        if any(p in str(type(g)) for p in DynamoOut.friendly_types): 
            return g
        if any(p in str(type(g)) for p in DynamoOut.structure_types): 
            return g
        
        #if isinstance(g, (Geometry) ) : raise NotImplementedError("I do not have a translation for that decodes geometry type in DynamoOut")

    def _drawVec(self, vec): 
        return ds.Vector.ByCoordinates(vec.x,vec.y,vec.z)

    def _drawPoint(self, pt):
        return ds.Point.ByCoordinates(pt.x,pt.y,pt.z)
        
    def _drawPlane(self, pln):
        return ds.Plane.ByOriginNormal(to_dyn_pt(pln.origin),to_dyn_vec(pln.normal))

    def _drawMesh(self, mesh):
        verts = tuple([to_dyn_pt(pt) for pt in mesh.pts])
        dyn_faces = []
        for face in mesh.faces:
            dyn_faces.append(ds.IndexGroup.ByIndices(tuple(face)))
        dyn_faces = tuple(dyn_faces)
        return ds.Mesh.ByPointsFaceIndices(verts, dyn_faces)
    
    def _drawLinearEntity(self, ln):
        if isinstance(ln, Segment) : return ds.Line.ByStartPointEndPoint(to_dyn_pt(ln.spt),to_dyn_pt(ln.ept))
        if isinstance(ln, Line) :    return ds.Line.ByStartPointEndPoint(to_dyn_pt(ln.spt),to_dyn_pt(ln.ept))
        if isinstance(ln, Ray) : 
            dyn_spt = to_dyn_pt(ln.spt)
            dyn_ept = to_dyn_pt(ln.ept)
            return tuple([dyn_spt,ds.Line.ByStartPointEndPoint(dyn_spt,dyn_ept)])
    
    def _drawPLine(self, pline):
        return to_dyn_polyline(pline)

    def _drawCircle(self, circ):
        return to_dyn_circle(circ)
        
    def _drawArc(self, circ):
        return to_dyn_arc(circ)
            
    def _drawPGon(self, pgon):
        return to_dyn_polyline(pgon)

    def _drawCurve(self, curve):
        return dyn_interpolated_curve(curve.surrogate.pts)

    def _drawCS(self, cs):
        return ds.CoordinateSystem.ByOriginVectors(to_dyn_pt(cs.origin),to_dyn_vec(cs.x_axis),to_dyn_vec(cs.y_axis))
        
    def _drawColor(self, color):
        return to_dyn_dscolor(color)

def to_dyn_vec(vec):
    return ds.Vector.ByCoordinates(vec.x,vec.y,vec.z)
    
def to_dyn_pt(pt):
    return ds.Point.ByCoordinates(pt.x,pt.y,pt.z)
    
def to_dyn_polyline(other):
    verts = tuple([to_dyn_pt(pt) for pt in other.pts])
    if isinstance(other, PGon) : return ds.PolyCurve.ByPoints(verts, True)
    return ds.PolyCurve.ByPoints(verts, False)

def to_dyn_circle(circ):
    norm = to_dyn_vec(circ.plane.normal)
    return ds.Circle.ByCenterPointRadiusNormal(to_dyn_pt(circ.plane.origin), circ.rad, norm)
    
def to_dyn_arc(arc):
    ang = arc.angle * 57.2957795
    return ds.Arc.ByCenterPointStartPointSweepAngle(to_dyn_pt(arc.origin), to_dyn_pt(arc.spt), ang, to_dyn_vec(arc._basis.z_axis))

def to_dyn_plane(other):
    if isinstance(other, CS) : 
        return ds.CoordinateSystem.ByOriginVectors(to_dyn_pt(other.origin),to_dyn_vec(other.x_axis),to_dyn_vec(other.y_axis))
    if isinstance(other, Plane) : 
        return ds.Plane.ByOriginNormal(to_dyn_pt(other.origin),to_dyn_vec(other.normal))

def dyn_interpolated_curve(points):
    dyn_points = [to_dyn_pt(pt) for pt in points]
    return ds.NurbsCurve.ByPoints(dyn_points)
    
def to_dyn_dscolor(color):
    ri = Interval(0,255).eval(5)#color.r)
    gi = Interval(0,255).eval(5)#color.g)
    bi = Interval(0,255).eval(5)#color.b)
    return DSCore.Color.ByARGB(255,ri,gi,bi)


'''
for reference: the following code is injected before and after a user's script in grasshopper components
## -- BEGIN DECODES HEADER -- ##
import decodes as dc
from decodes.core import *
from decodes.io.dynamo_in import *
from decodes.io.dynamo_out import *
exec(io.dynamo_in.component_header_code)
exec(io.dynamo_out.component_header_code)
## -- END DECODES HEADER -- ##

## -- BEGIN DECODES FOOTER -- ##
exec(io.dynamo_in.component_footer_code)
exec(io.dynamo_out.component_footer_code)
## -- END DECODES FOOTER -- ##
'''

component_header_code = """
out = make_out(Outies.Dynamo)		
"""


component_footer_code = """
if not isinstance(out, io.dynamo_out.DynamoOut) : print "Bad User!    It looks like you assigned to the output using the equals operator like so: out=something.\\nYou should have used the 'put' method instead, like so: out.put(something)\\nYou may also use the '+=' operator, like so: out += something"
OUT = out.draw()
"""

