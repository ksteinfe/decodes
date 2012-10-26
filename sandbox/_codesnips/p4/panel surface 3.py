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
  pathPrefix = "solarIncidence/"
  path = pathPrefix + "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
  epwdata = epwData(path)
  
  # go through each mesh face, and calcuate the average surface irradiance
  # and store value in irrArr
  irrArr = []
  for i in range(len(mymesh.faces)):
    facePlane = Ray(mymesh.face_centroid(i),mymesh.face_normal(i))
    irrArr.append(avgIrradinaceForYear(facePlane,epwdata))
  
  # go through each mesh face, and construct a component for each face
  for i in range(len(mymesh.faces)):
    height = irrArr[i] / 30
    if height < 1.0 : height = 1.0
    outie.put(pyramidComponent(mymesh,i,height))
  
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


def epwData(filepath):
  """given a path to an EPW file, 
  extracts the direct normal irradiance, lat, long, tmz
  out: a dictionary with the above information
  """
  radValues = epw.parse_epw_file(filepath, "DirNormIrad")
  metadata = epw.epw_metadata(filepath)
  dict = {}
  dict['lat'] = metadata['lat']
  dict['long'] = metadata['long']
  dict['timezone'] = metadata['timezone']
  dict['name'] = metadata['name']
  dict['radiation'] = radValues
  return dict

def avgIrradinaceForYear(plane,epwdata):
  """calculates the average irradiance striking a given plane across the year
  plane (fp.Ray) the plane in question
  epwdata (dict) a dictionary of epw data
  out: the average amount of radition striking the plane
  """
  irrArr = []
  for h in range(8760): irrArr.append(srfIrradiance(plane,h,epwdata))
  avgIrr = (sum(irrArr))/(len(irrArr)) #Calculates Yearly Average Radiation
  return avgIrr

def srfIrradiance(plane,hourOfYr,epwdata):
  """calculates irradiance striking a given plane at a given hour for a given location
  plane (fp.Ray) the plane in question
  hour (int) the hour of the year to test, 0-8760
  epwdata (dict) a dictionary of epw data
  out: the amount of radition striking the plane
  """
  #calculate the solar vector
  day = int(hourOfYr/24)
  hour = hourOfYr%24
  sunvec = sg.calc_sunVector(epwdata['lat'], epwdata['long'], epwdata['timezone'], day, hour)
  
  #find the angle between our plane and the sun direction
  incidenceAngle = abs(sunvec.angle(plane.vec))
  if incidenceAngle > math.pi/2 : srfIrr = 0.0 #if the sun is behind our plane, return zero
  else : srfIrr = epwdata['radiation'][hourOfYr] * math.cos(incidenceAngle) # otherwise, calculate the amout of radition striking our surface
  #print srfIrr
  return srfIrr

# Here we check to see if this file is being executed as the "main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if __name__ == '__main__' : 
  main()

