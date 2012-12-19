from decodes import core as dc
if dc.VERBOSE_FS: print "rhinoUtil loaded"

import scriptcontext
import System
import Rhino


def makelayer(layer_name):
  global scriptcontext
  global System
  layer_index = scriptcontext.doc.Layers.Find(layer_name, True)
  if layer_index>=0:
    if dc.VERBOSE_FS: print "already have a layer called ", layer_name
    return layer_index
    
  layer_index = scriptcontext.doc.Layers.Add(layer_name, System.Drawing.Color.Black)
  return layer_index
  
   
def VecToPoint3d(vec):
  return Rhino.Geometry.Point3d(vec.x,vec.y,vec.z)

def VecToVec3d(vec):
  return Rhino.Geometry.Vector3d(vec.x,vec.y,vec.z)
