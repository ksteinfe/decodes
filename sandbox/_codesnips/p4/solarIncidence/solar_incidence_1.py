import math
import fieldpack as fp
from fieldpack import *
import fieldpack.extensions.solarGeom as sg

def main():
  """a simple example of calculating solar incident radiation.  
  given a user-defined plane to evaluate, and hard-coded position, date/time and radiation level, 
  calculates the amount of radition striking the plane
  and produces a simple visualization.
  """
  outie = fp.makeOut(fp.outies.Rhino, "solar incidence")
  outie.set_color(Color(0.75))
  
  # getting user input
  lat,long,tmz = 40.75,-73.5,-5.0 #global position
  plane = Ray(Point(0,0,0), Vec(5,2,1)) #user-defined plane
  date,hour = "05/16", "12:00" #hard-coded date/time
  radiation = 1000 #user-defined solar intensity (direct normal)
  
  #calculate the solar vector
  day = sg.calc_dayOfYear(date)
  hour = sg.calc_hourDecimal(hour)
  sunvec = sg.calc_sunVector(lat, long, tmz, day, hour)
  
  #find the angle between our plane and the sun direction
  incidenceAngle = sunvec.angle(plane.vec)
  if incidenceAngle > math.pi/2 or radiation == 0:
    #if the sun is behind our plane then no radiation is possible
    print "Solar Incidence on the Surface = 0" 
    return
  else :
    #calculate the amout of radition striking our surface
    srfIrr = radiation * math.cos(incidenceAngle)
  print "srfIrr = {}".format(srfIrr)
  
  #visualize results
  colorA = Color.HSB(0.75) #saturation and brightness of HSB colors default to 1.0
  colorB = Color.HSB(0.0) #saturation and brightness of HSB colors default to 1.0
  color = Color.interpolate(colorA,colorB,srfIrr/100)
  plane.set_color(color) #assign HSB color to user-defined plane
  plane.vec.length = srfIrr/10 #scale the vector to a length proportional to the surface irradiance
  outie.put([plane,sunvec])
  outie.draw()

# Here we check to see if this file is being executed as the "main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if __name__ == '__main__' : 
  main()