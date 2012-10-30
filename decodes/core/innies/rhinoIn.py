import fieldpack as fp
from fieldpack import *
from fieldpack.outies.rhinoUtil import *
if fp.VERBOSE_FS: print "rhinoIn loaded"

import rhinoscriptsyntax as rs


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
      
    return fp.Mesh(verts,faces)
    