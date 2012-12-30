from decodes import core as dc
from decodes.core import *


if dc.VERBOSE_FS: print "ghIn loaded"


#TODO: figure out how to hack the code completion thingo to display decodes geometry after gh geom has been translated



class GrasshopperIn():
  """innie for pulling stuff from grasshopper"""
  primitive_types = ["bool", "int", "float", "str"]
  friendly_types = ["DHr"]
  
  def __init__(self):
    pass
    
  @staticmethod
  def get(gh_in_str, gh_in):
    # main function for processing incoming data from Grasshopper into Decodes geometry
    # incoming may be a sigleton, a list, or a datatree
    # variable in GH script component will be replaced by whatever is returned here
    if gh_in is None : return None
    if type(gh_in) is list: return [GrasshopperIn.get(gh_in_str+"["+str(i)+"]",item) for i, item in enumerate(gh_in)]
    if type(gh_in) is rg.Vector3d : return rgvec_to_vec(gh_in)
    elif type(gh_in)is rg.Point3d : return rgpt_to_pt(gh_in)
      
    elif type(gh_in) is rg.Line : 
      return dc.Segment(dc.Point(gh_in.FromX,gh_in.FromY,gh_in.FromZ),dc.Point(gh_in.ToX,gh_in.ToY,gh_in.ToZ))
    elif type(gh_in) is System.Drawing.Color : 
      return dc.Color(float(gh_in.R)/255,float(gh_in.G)/255,float(gh_in.B)/255)
    elif type(gh_in) is rg.PolylineCurve : 
      ispolyline, gh_polyline = gh_in.TryGetPolyline()
      if (ispolyline) : return rgpolyline_to_pgon(gh_polyline)
    elif type(gh_in) is rg.NurbsCurve : 
      ispolyline, gh_polyline = gh_in.TryGetPolyline()
      if (ispolyline) : return rgpolyline_to_pgon(gh_polyline)
    elif type(gh_in) is rg.Mesh : 
      verts = [dc.Point(rh_pt.X,rh_pt.Y,rh_pt.Z) for rh_pt in gh_in.Vertices]
      faces = []
      for rh_fc in gh_in.Faces :
        faces.append([rh_fc[0],rh_fc[1],rh_fc[2]]) #add the first three points of each face
        if rh_fc[2] != rh_fc[3] :  faces.append([rh_fc[0],rh_fc[2],rh_fc[3]]) #if face is a quad, add the missing triangle
      return dc.Mesh(verts,faces)
    elif any(p in str(type(gh_in)) for p in GrasshopperIn.primitive_types) : return gh_in
    elif any(p in str(type(gh_in)) for p in GrasshopperIn.friendly_types) : return gh_in
    else :
      print "UNKNOWN TYPE: "+gh_in_str+" is a "+ str(type(gh_in))
      return gh_in
      #print inspect.getmro(gh_in.__class__)
      #if issubclass(gh_in.__class__, rg.GeometryBase ) : print "this is geometry"
      #print gh_incoming.TypeHint
      #print gh_incoming.Description

      

      
def rgvec_to_vec(rg_vec):
  return dc.Vec(rg_vec.X,rg_vec.Y,rg_vec.Z)

def rgpt_to_pt(rg_pt):
  return dc.Point(rg_pt.X,rg_pt.Y,rg_pt.Z)

def rh_plane_to_cs(rh_plane):
    cpt = rgpt_to_pt(rh_plane.Origin)
    x_axis = rgvec_to_vec(rh_plane.XAxis)
    y_axis = rgvec_to_vec(rh_plane.YAxis)
    return dc.CS(cpt,x_axis,y_axis)

def rgpolyline_to_pgon(gh_polyline):
  if not gh_polyline.IsClosed : raise dc.GeometricError("Cannot import open polylines")
  gh_curve = gh_polyline.ToNurbsCurve()
  isplanar, plane = gh_curve.TryGetPlane()
  if not isplanar : raise dc.GeometricError("Cannot import non-planar polylines")
  cs = rh_plane_to_cs(plane)
  w_verts = [rgpt_to_pt(gh_polyline[i]) for i in range(len(gh_polyline))]
  verts = [ (pt*cs.ixform).set_basis(cs) for pt in w_verts ]
  if (verts[0]==verts[-1]) : del verts[-1] #remove last vert if a duplicate
  return dc.PGon(verts,cs)
  

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