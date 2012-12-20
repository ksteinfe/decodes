from decodes import core as dc
from decodes.core import *

if dc.VERBOSE_FS: print "ghOut loaded"

import clr, outie, collections
import rhinoUtil
from rhinoUtil import *

import Rhino.Geometry as rg

#TODO: check at end of script if the user overwrote the established 'outie' with either a singleton, a list of sc.Geoms, or something else, and act accordingly (raising the appropriate warnings) 

class GrasshopperOut(outie.Outie):
  """outie for pushing stuff to grasshopper"""
  
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
    
  def _is_leaf(self, items):
	return not any(self._should_iterate(item) for item in items)

  def _should_iterate(self, item):
	return isinstance(item, collections.Iterable) and not isinstance(item,basestring)
	
  def _add_branch(self, g, tree, tree_p, path):
    # here we sort out what type of geometry we're dealing with, and call the proper draw functions
    # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)
    
    def extract_props(g):
      if not hasattr(g, 'props') : g.props = {}
      g.props['layer'] = self.name
      return "::".join(["{0}={1}".format(k,v) for (k, v) in g.props.items()])
    
    if self._should_iterate(g) :
      is_leaf = self._is_leaf(g)
      for n,i in enumerate(g): 
        npath = path.AppendElement(n)
        if is_leaf : self._add_branch(i,tree,tree_p, path)
        else : self._add_branch(i,tree,tree_p, npath)
      return True
    
    if isinstance(g, dc.Point) : 
      tree.Add(self._drawPoint(g),path)
      tree_p.Add(extract_props(g), path)
      return True
    if isinstance(g, dc.Vec) : 
      tree.Add(self._drawVec(g),path)
      tree_p.Add(extract_props(g), path)
      return True
    if isinstance(g, dc.Mesh) : 
      tree.Add(self._drawMesh(g),path)
      tree_p.Add(extract_props(g), path)
      return True
    if isinstance(g, dc.LinearEntity) : 
      rh_geom = self._drawLinearEntity(g)
      props = extract_props(g)
      if type(rh_geom) is list: 
        tree.AddRange(rh_geom,path)
        for item in rh_geom: tree_p.Add(props, path)
      else: 
        tree.Add(rh_geom,path)
        tree_p.Add(props, path)
      return True
    if isinstance(g, dc.CS) : 
      tree.Add(self._drawCS(g),path)
      tree_p.Add(extract_props(g), path)
      return True
    if isinstance(g, dc.Color) : 
      tree.Add(self._drawColor(g),path)
      tree_p.Add(extract_props(g), path)
      return True
    
    if isinstance(g, (dc.Geometry) ) : raise NotImplementedError("i do not have a translation for that decodes geometry type in GrasshopperOut")
    tree.Add(g,path)
    tree_p.Add(extract_props(g), path)    

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
    if isinstance(ln, dc.Line) :  return rg.Line(rg.Point3d(ln.spt.x,ln.spt.y,ln.spt.z),rg.Point3d(ln.ept.x,ln.ept.y,ln.ept.z))
    if isinstance(ln, dc.Ray) : 
      rh_spt = rg.Point3d(ln.spt.x,ln.spt.y,ln.spt.z)
      rh_ept = rg.Point3d(ln.ept.x,ln.ept.y,ln.ept.z)
      return [rh_spt,rg.Line(rh_spt,rh_ept)]
    
  def _drawCS(self, cs):
    o = rg.Point3d(cs.origin.x,cs.origin.y,cs.origin.z)
    x = rg.Vector3d(cs.xAxis.x,cs.xAxis.y,cs.xAxis.z) 
    y = rg.Vector3d(cs.yAxis.x,cs.yAxis.y,cs.yAxis.z) 
    return rg.Plane(o,x,y)
	
  def _drawColor(self, c): 
	import Grasshopper.GUI.GH_GraphicsUtil as gh_gutil
	return gh_gutil.ColourARGB(c.r,c.g,c.b)
	
'''
for reference: the following code is injected before and after a user's script in grasshopper components
## -- BEGIN DECODES HEADER -- ##
import decodes.core as dc
from decodes.core import *
exec(dc.innies.ghIn.component_header_code)
exec(dc.outies.ghOut.component_header_code)
## -- END DECODES HEADER -- ##

## -- BEGIN DECODES FOOTER -- ##
exec(dc.innies.ghIn.component_footer_code)
exec(dc.outies.ghOut.component_footer_code)
## -- END DECODES FOOTER -- ##
'''


component_header_code = """
outputs = ghenv.Component.Params.Output
gh_outies = []
for output in outputs :
    if output.Name != "console":
        if not "_prop" in output.NickName :
          vars()[output.NickName] = dc.makeOut(outies.Grasshopper,output.NickName)
          gh_outies.append(vars()[output.NickName])
		
"""

#TODO, check if an output variable is fieldpack geometry or a list of fieldpack geometry
# if so, translate apprpiately
component_footer_code = """

for gh_outie in gh_outies :
        if not isinstance(vars()[gh_outie.name], dc.outies.GrasshopperOut) : 
                print "Bad User!  It looks like you assigned to the output '{0}' using the equals operator like so: {0}=something.  You should have used the 'put' method instead, like so: {0}.put(something)".format(gh_outie.name)
        vars()[gh_outie.name], vars()[gh_outie.name+"_props"] = gh_outie.extract_tree()

		
"""

