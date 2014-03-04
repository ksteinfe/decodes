from .. import *
from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_pline, dc_mesh, dc_pgon
#from .rhino_out import *
from . import outie
if VERBOSE_FS: print "dynamo_out loaded"

import clr, collections

clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry as ds

#TODO: check at end of script if the user overwrote the established 'outie' with either a singleton, a list of sc.Geoms, or something else, and act accordingly (raising the appropriate warnings) 

class DynamoOut(outie.Outie):
    """outie for pushing stuff to grasshopper"""
    raw_types = ["Curve","Surface"]

    def __init__(self, name):
        super(DynamoOut,self).__init__()
        self._allow_foreign = True
        self.name = name
        
    def extract_tree(self):
        #creates a grasshopper data tree
        #calls the draw function for each geometric object
        #returns a list of whatever these draw functions return
        clr.AddReference("Grasshopper")
        from Grasshopper import DataTree
        from Grasshopper.Kernel.Data import GH_Path
        clr.AddReference("DcPython")
        from DcPython import Decodes as dcp
        
        tree = DataTree[object]()
        tree_p = DataTree[object]()
        is_leaf = self._is_leaf(self.geom)
        for n,g in enumerate(self.geom): 
            if is_leaf : 
                path = GH_Path(0)
                self._add_branch(g, tree,tree_p,path)
            else :
                path = GH_Path(n)
                self._add_branch(g, tree,tree_p,path)
        
        
        self.clear() #empty the outie after each draw
        return tree, tree_p
        
    def _is_leaf(self, items): return not any(self._should_iterate(item) for item in items)

    def _should_iterate(self, item): return isinstance(item, collections.Iterable) and not isinstance(item,basestring)
    
    def _add_branch(self, g, tree, tree_p, path):
        # here we sort out what type of geometry we're dealing with, and call the proper draw functions
        # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)
        
        if isinstance(g, Geometry) and not g.do_translate:
            tree.Add(g,path)
            return True

        def extract_props(g):
            from DcPython import Decodes as dcp
            att = dcp.Decodes_Attributes()
            att.layer = self.name
            if not hasattr(g, 'props') : return att
            #return "::".join(["{0}={1}".format(k,v) for (k, v) in g.props.items()])
            if "name" in g.props : att.name = g.props["name"]
            if "weight" in g.props : att.weight = g.props["weight"]
            if "color" in g.props : att.setColor( g.props["color"].r, g.props["color"].g, g.props["color"].b )
            return att
        
        if self._should_iterate(g) :
            is_leaf = self._is_leaf(g)
            for n,i in enumerate(g): 
                npath = path.AppendElement(n)
                if is_leaf : self._add_branch(i,tree,tree_p, path)
                else : self._add_branch(i,tree,tree_p, npath)
            return True
        
        # ADD ANY RAW TYPES DIRECTLY
        if any(p in str(type(g)) for p in GrasshopperOut.raw_types) : 
            tree.Add(g,path)
            tree_p.Add(extract_props(g), path)
            return True

        if isinstance(g, Point) : 
            tree.Add(self._drawPoint(g),path)
            tree_p.Add(extract_props(g), path)
            return True
        if isinstance(g, Vec) : 
            tree.Add(self._drawVec(g),path)
            tree_p.Add(extract_props(g), path)
            return True
        if isinstance(g, Mesh) : 
            tree.Add(self._drawMesh(g),path)
            tree_p.Add(extract_props(g), path)
            return True
        if isinstance(g, LinearEntity) : 
            dyn_geom = self._drawLinearEntity(g)
            props = extract_props(g)
            if type(dyn_geom) is list: 
                tree.AddRange(dyn_geom,path)
                for item in dyn_geom: tree_p.Add(props, path)
            else: 
                tree.Add(dyn_geom,path)
                tree_p.Add(props, path)
            return True
        
        if isinstance(g, PLine) : 
            tree.Add(self._drawPLine(g),path)
            tree_p.Add(extract_props(g), path)
            return True

        if isinstance(g, Circle) : 
            tree.Add(self._drawCircle(g),path)
            tree_p.Add(extract_props(g), path)
            return True
            
        if isinstance(g, Arc) : 
            tree.Add(self._drawArc(g),path)
            tree_p.Add(extract_props(g), path)
            return True

        if isinstance(g, Plane) : 
            tree.Add(self._drawPlane(g),path)
            tree_p.Add(extract_props(g), path)
            return True

        if isinstance(g, PGon) : 
            tree.Add(self._drawPGon(g),path)
            tree_p.Add(extract_props(g), path)
            return True

        if isinstance(g,Curve): 
            tree.Add(self._drawCurve(g),path)
            tree_p.Add(extract_props(g), path)
            return True

        if isinstance(g, CS) : 
            tree.Add(self._drawCS(g),path)
            tree_p.Add(extract_props(g), path)
            return True
        if isinstance(g, Color) : 
            tree.Add(self._drawColor(g),path)
            tree_p.Add(extract_props(g), path)
            return True
        
        if isinstance(g, (Geometry) ) : raise NotImplementedError("i do not have a translation for that decodes geometry type in GrasshopperOut")
        tree.Add(g,path)
        tree_p.Add(None, path)        

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
        if isinstance(ln, Segment) : return ds.Line.ByStartPointEndPoint(to_dyn_pt(spt),to_dyn_pt(ept))
        if isinstance(ln, Line) :    return ds.Line.ByStartPointEndPoint(to_dyn_pt(spt),to_dyn_pt(ept))
        if isinstance(ln, Ray) : 
            dyn_spt = to_dyn_pt(spt)
            dyn_ept = to_dyn_pt(ept)
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

    def _drawColor(self, c): 
        return gh_gutil.ColourARGB(c.r,c.g,c.b)



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
    return ds.Circle.ByCenterPointRadiusNormal(to_dyn_pt(circ.plane.orign), circ.rad, norm)
    
def to_dyn_arc(arc):
    ang = arc.angle * 57.2957795
    return ds.Arc.ByCenterPointStartPointSweepAngle(to_dyn_pt(arc.origin), to_dyn_pt(arc.spt), ang, to_dyn_vec(arc.cs.z_axis))

def to_dyn_plane(other):
    if isinstance(other, CS) : 
        return ds.CoordinateSystem.ByOriginVectors(to_dyn_pt(other.origin),to_dyn_vec(other.x_axis),to_dyn_vec(other.y_axis))
    if isinstance(other, Plane) : 
        return ds.Plane.ByOriginNormal(to_dyn_pt(other.origin),to_dyn_vec(other.normal))

def dyn_interpolated_curve(points):
    dyn_points = [to_dyn_pt(pt) for pt in points]
    return ds.NurbsCurve.ByPoints(dyn_points)



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


component_header_code = """
outputs = ghenv.Component.Params.Output
gh_outies = []
for output in outputs :
        if output.Name != "console":
                if not "_prop" in output.NickName :
                    vars()[output.NickName] = make_out(Outies.Grasshopper,output.NickName)
                    gh_outies.append(vars()[output.NickName])
		
"""

#TODO, check if an output variable is fieldpack geometry or a list of fieldpack geometry
# if so, translate apprpiately

component_footer_code = """
for gh_outie in gh_outies :
                if not isinstance(vars()[gh_outie.name], io.gh_out.GrasshopperOut) : 
                                print "Bad User!    It looks like you assigned to the output '{0}' using the equals operator like so: {0}=something.\\nYou should have used the 'put' method instead, like so: {0}.put(something)\\nYou may also use the '+=' operator, like so: {0} += something".format(gh_outie.name)
                vars()[gh_outie.name], vars()[gh_outie.name+"_props"] = gh_outie.extract_tree()
"""

