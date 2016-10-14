from .. import *
from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_pline, dc_mesh, dc_pgon
from .rhino_out import *
from . import outie
if VERBOSE_FS: print("gh_out loaded")

import clr, collections
import Rhino.Geometry as rg

#TODO: check at end of script if the user overwrote the established 'outie' with either a singleton, a list of sc.Geoms, or something else, and act accordingly (raising the appropriate warnings) 

class GrasshopperOut(outie.Outie):
    """outie for pushing stuff to grasshopper"""
    raw_types = ["Curve","Surface"]

    def __init__(self, name):
        super(GrasshopperOut,self).__init__()
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

    def _should_iterate(self, item): return isinstance(item, collections.Iterable) and not isinstance(item,str)
    
    def _add_branch(self, g, tree, tree_p, path):
        # here we sort out what type of geometry we're dealing with, and call the proper draw functions
        # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)
        
        if isinstance(g, Geometry) and not g.do_translate:
            tree.Add(g,path)
            return True

        # treat Tris as PGons
        if isinstance(g, Tri):  g = PGon([g.pa,g.pb,g.pc])
            
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
            rh_geom = self._drawLinearEntity(g)
            props = extract_props(g)
            if type(rh_geom) is list: 
                tree.AddRange(rh_geom,path)
                for item in rh_geom: tree_p.Add(props, path)
            else: 
                tree.Add(rh_geom,path)
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

        if isinstance(g, PGon): 
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
        return rg.Vector3d(vec.x,vec.y,vec.z)

    def _drawPoint(self, pt):
        return rg.Point3d(pt.x,pt.y,pt.z)
        
    def _drawPlane(self, pln):
        o = rg.Point3d(pln.origin.x,pln.origin.y,pln.origin.z)
        n = rg.Vector3d(pln.normal.x,pln.normal.y,pln.normal.z) 
        return rg.Plane(o,n)

    def _drawMesh(self, mesh):
        rh_mesh = rg.Mesh()
        for v in mesh.pts: rh_mesh.Vertices.Add(v.x,v.y,v.z)
        for f in mesh.faces: 
            if len(f)==3 : rh_mesh.Faces.AddFace(f[0], f[1], f[2])
            if len(f)==4 : rh_mesh.Faces.AddFace(f[0], f[1], f[2], f[3])
        rh_mesh.Normals.ComputeNormals()
        rh_mesh.Compact()
        return rh_mesh
    
    def _drawLinearEntity(self, ln):
        if isinstance(ln, Segment) : return rg.Line(rg.Point3d(ln.spt.x,ln.spt.y,ln.spt.z),rg.Point3d(ln.ept.x,ln.ept.y,ln.ept.z))
        if isinstance(ln, Line) :
            ept = ln.spt + ln.vec
            return rg.Line(rg.Point3d(ln.spt.x,ln.spt.y,ln.spt.z),rg.Point3d(ept.x,ept.y,ept.z))
        if isinstance(ln, Ray) : 
            rh_spt = rg.Point3d(ln.spt.x,ln.spt.y,ln.spt.z)
            ept = ln.spt + ln.vec
            rh_ept = rg.Point3d(ept.x,ept.y,ept.z)
            return [rh_spt,rg.Line(rh_spt,rh_ept)]
    
    def _drawPLine(self, pline):
        return to_rgpolyline(pline)

    def _drawCircle(self, circ):
        return to_rgcircle(circ)
        
    def _drawArc(self, circ):
        return to_rgarc(circ)
            
    def _drawPGon(self, pgon):
        return to_rgpolyline(pgon)

    def _drawCurve(self, curve):
        return interpolated_curve(curve.surrogate.pts)

    def _drawCS(self, cs):
        o = rg.Point3d(cs.origin.x,cs.origin.y,cs.origin.z)
        x = rg.Vector3d(cs.x_axis.x,cs.x_axis.y,cs.x_axis.z) 
        y = rg.Vector3d(cs.y_axis.x,cs.y_axis.y,cs.y_axis.z) 
        return rg.Plane(o,x,y)

    def _drawColor(self, c): 
        import Grasshopper.GUI.GH_GraphicsUtil as gh_gutil
        return gh_gutil.ColourARGB(c.r,c.g,c.b)







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

