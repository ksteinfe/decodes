import math
import fieldpack as fp
from fieldpack import *
import fieldpack.extensions.solarGeom as sg
import fieldpack.extensions.parseEPW as epw

def main():
  """a simple example of a "component" tiling of a mesh surface.  
  given a mesh with only quad faces, we will generate a simple pyramid-like 
  component to take the place of each mesh face.
  """
  outie = fp.makeOut(fp.outies.Rhino, "component")
  outie.set_color(Color.RGB(0.75,0.5,1.0))
  
  # get user input
  innie = fp.makeIn(fp.innies.Rhino)
  mymesh = innie.get_mesh()
  
  # go through each mesh face, and construct a component for each face
  for i in range(len(mymesh.faces)):
    outie.put(pyramidComponent(mymesh,i,2))
  
  outie.draw()


def pyramidComponent(parentMesh,faceIndex,h):
  """makes a simple pyramid-shaped component
  given a mesh and the index of a quad-face we want to build on,
  returns a pyramid-shaped mesh of height h
  """
  mVerts = parentMesh.face_verts(faceIndex)
  mCent = parentMesh.face_centroid(faceIndex)
  mNormal = parentMesh.face_normal(faceIndex)
  mNormal.length = h
  # insert the top point of the pyramid at the start of mVerts
  mVerts.insert(0,mCent + mNormal) 
  
  faces = [(0,1,2),(0,2,3),(0,3,4),(0,4,1)]
  return Mesh(mVerts,faces)



# Here we check to see if this file is being executed as the "main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if __name__ == '__main__' : 
  main()

