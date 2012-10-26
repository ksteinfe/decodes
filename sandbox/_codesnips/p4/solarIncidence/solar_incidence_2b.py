import math
import fieldpack as fp
from fieldpack import *
import fieldpack.extensions.solarGeom as sg
import fieldpack.extensions.parseEPW as epw

def main():
  """a simple example of calculating solar incident radiation.  
  given a user-defined plane to evaluate, a hard-coded position, 
  and a EPW file that associates date/time with radiation level, 
  calculates the amount of radition striking the plane
  and produces a simple visualization.
  """
  outie = fp.makeOut(fp.outies.Rhino, "solar incidence")
  outie.set_color(Color(0.75))
  
  # getting user input
  epwdata = epwData("USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw")
  plane = Ray(Point(0,0,2), Vec(5,2,1)) #user-defined plane
  day = sg.calc_dayOfYear("01/03") #day of the year to calculate solar incidence 
  hour = (24*(day-1))+int(sg.calc_hourDecimal("14:00")) #hour of the day to calculate solar incidence
  
  #Yearly Average
  srfIrr = 0
  for h in range(hour, hour+1):
    srfIrr = (srfIrradiance(plane,h,epwdata))#/24
    print srfIrr
    #print srfIrr
    #srfIrr = 0 
    #for irrVal in srfIrr:
    #  irrVal += srfIrr
   #   print irrVal
    #for srfIrr in range(24):
    #srfIrr += (srfIrradiance(plane,h,epwdata))/8760
  print '{} total w/m2 for first 48 hours'.format(srfIrr)
  
  #visualize results
  colorA = Color.HSB(0.0) #saturation and brightness of HSB colors default to 1.0
  colorB = Color.HSB(0.75) #saturation and brightness of HSB colors default to 1.0
  color = Color.interpolate(colorA,colorB,srfIrr*.001)
  plane.set_color(color)
  plane.vec.length = srfIrr/10
  
  outie.put([plane])
  outie.draw()

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
  #print sunvec
  print day
  print hour
  #print
  print hourOfYr
  
  #find the angle between our plane and the sun direction
  incidenceAngle = abs(sunvec.angle(plane.vec))
  #print incidenceAngle
  if incidenceAngle > math.pi/2 : srfIrr = 0.0 #if the sun is behind our plane, return zero
  else : srfIrr = epwdata['radiation'][hourOfYr] * math.cos(incidenceAngle) # otherwise, calculate the amout of radition striking our surface
  #print max(x)
  #print '{} w/m2 for hour {} at angle {} in {}'.format(srfIrr,hourOfYr,incidenceAngle,epwdata['name'])
  #print max(incidenceAngle)
  #print max(epwdata['radiation'][hourOfYr])
  print srfIrr
  return srfIrr



# Here we check to see if this file is being executed as the "main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if __name__ == '__main__' : 
  main()

