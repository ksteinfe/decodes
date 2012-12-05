from decodes import core as dc
from decodes.core import *


if dc.VERBOSE_FS: print "ghIn loaded"


#TODO: figure out how to hack the code completion thingo to display decodes geometry after gh geom has been translated

class GrasshopperIn():
  """innie for pulling stuff from grasshopper"""
  
  def __init__(self):
    pass
    
  def get(self, gh_incoming):
    # main function for processing incoming data from Grasshopper into Decodes geometry
    # incoming may be a sigleton, a list, or a datatree
    # variable in GH script component will be replaced by whatever is returned here
    
    return False



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
primitive_types = ["bool", "int", "float", "str"]
for input in inputs :
    gh_in_str = input.NickName
    gh_in = eval(gh_in_str)
    if gh_in is not None : 
        if type(gh_in) is rg.Vector3d : 
            vars()[gh_in_str] = dc.Vec(gh_in.X,gh_in.Y,gh_in.Z)
        elif type(gh_in)is rg.Point3d : 
            vars()[gh_in_str] = dc.Point(gh_in.X,gh_in.Y,gh_in.Z)
        elif type(gh_in) is rg.Line : 
            vars()[gh_in_str] = dc.Segment(Point(0,1),Vec(0,0,1))
        elif type(gh_in) is System.Drawing.Color : 
            vars()[gh_in_str] = dc.Color(float(gh_in.R)/255,float(gh_in.G)/255,float(gh_in.B)/255)
            
        elif type(gh_in) is rg.Mesh : 
            verts = [dc.Point(rh_pt.X,rh_pt.Y,rh_pt.Z) for rh_pt in gh_in.Vertices]
            faces = []
            for rh_fc in gh_in.Faces :
                faces.append([rh_fc[0],rh_fc[1],rh_fc[2]]) #add the first three points of each face
                if rh_fc[2] != rh_fc[3] : 
                  faces.append([rh_fc[0],rh_fc[2],rh_fc[3]]) #if face is a quad, add the missing triangle
            vars()[gh_in_str] = dc.Mesh(verts,faces)
        elif any(p in str(type(gh_in)) for p in primitive_types) :
            pass
            #print "primitive: "+ str(type(gh_in))
        else :
            print "UNKNOWN TYPE: "+gh_in_str+" is a "+ str(type(gh_in))
            #print inspect.getmro(gh_in.__class__)
            #if issubclass(gh_in.__class__, rg.GeometryBase ) : print "this is geometry"
            #print input.TypeHint
            #print input.Description
"""

component_footer_code = ""