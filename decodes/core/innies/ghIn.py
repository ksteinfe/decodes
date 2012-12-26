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
    #gh_in_str = gh_incoming.NickName
    #gh_in = eval(gh_in_str)
    if gh_in is None : return None
    if type(gh_in) is list: return [GrasshopperIn.get(gh_in_str+"["+str(i)+"]",item) for i, item in enumerate(gh_in)]
    if type(gh_in) is rg.Vector3d : 
      return dc.Vec(gh_in.X,gh_in.Y,gh_in.Z)
    elif type(gh_in)is rg.Point3d : 
      return dc.Point(gh_in.X,gh_in.Y,gh_in.Z)
    elif type(gh_in) is rg.Line : 
      return dc.Segment(Point(gh_in.FromX,gh_in.FromY,gh_in.FromZ),Point(gh_in.ToX,gh_in.ToY,gh_in.ToZ))
    elif type(gh_in) is System.Drawing.Color : 
      return dc.Color(float(gh_in.R)/255,float(gh_in.G)/255,float(gh_in.B)/255)
        
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