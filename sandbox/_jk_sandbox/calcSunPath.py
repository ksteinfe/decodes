#calcSunPath:  Uses the solarGeometry module to draw out sun pat

import solarGeom as sg
import rhinoscriptsyntax as rs
import math

#NYC
#latitude = 40.75
#longitude = -73.5
#timezone = -5.0

#Santiago, Chile
latitude = -33.45
longitude = -70.6667
timezone = -3.0


#'fake' direct beam intensity function
def directNormalIrad(day, hour):
	return 1000*max(0, -math.cos(hour*math.pi/12) + 1/8.0 - (day-171)**2/115600)

# this module can be used to compute all the solar angles as well as the sun vector for
# any day and time (given in local time)
day = sg.calc_dayOfYear("3/21")
hour = sg.calc_hourDecimal("11:00")

solarAngles = sg.calc_solarAngles(latitude, longitude, timezone, day, hour)
print "Altitude = ", solarAngles[2]
print "Azimuth = ", solarAngles[3]

sun = sg.calc_sunVector(latitude, longitude, timezone, day, hour)
R = 20 #scaling for the sun vector so that it is more visible on canvas
sun[:] = [x*R for x in sun]
rs.AddPoints(sun)


# or to show the sun path throughout the a range of times in the day
startTime= "7:00"
endTime = "19:30"
hourStart = sg.calc_hourDecimal(startTime)
hourEnd = sg.calc_hourDecimal(endTime)
R = 20
N = 20 #number of sample points between starting time and end time
for i in range(N+1):
	sun = sg.calc_sunVector(latitude, longitude, timezone, day, hourStart+i*(hourEnd-hourStart)/N)
	if sun[2] > 0:
		sun[:] = [x*R for x in sun]
		rs.AddPoint(sun)

for h in range(24):
	print ("for hour "+str(h)
		+", directbeamintensity = "+str(directNormalIrad(day, h))
	      )
		
 
# or to show the sun path throughout a range of dates in the year, and for each date, a range of
# times in the day
dateStart = "1/1"
dateEnd = "12/31"
dayStart = sg.calc_dayOfYear(dateStart)
dayEnd = sg.calc_dayOfYear(dateEnd)
startTime= "7:00"
endTime = "19:30"
hourStart = sg.calc_hourDecimal(startTime)
hourEnd = sg.calc_hourDecimal(endTime)
R = 20
N = 20 #number of sample points between starting time and end time
for dayNow in range(dayStart, dayEnd, 3):
	for i in range(N+1):
		sun = sg.calc_sunVector(latitude, longitude, timezone, dayNow, hourStart+i*(hourEnd-hourStart)/N)
		if sun[2] > 0:
			sun[:] = [x*R for x in sun]
			rs.AddPoint(sun)