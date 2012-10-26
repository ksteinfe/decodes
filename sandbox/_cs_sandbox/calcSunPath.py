#calcSunPath:  Uses the solarGeometry module to draw out sun path for a given location between a start and end time

import solarGeom as sg
import rhinoscriptsyntax as rs

#latitude = 42.5
#longitude = 143.28
#timezone = 9.0

latitude = 45.36
longitude = -79.20
timezone = -5.0

dateStart = "1/1"
dateEnd = "12/31"
dayStart = sg.calc_dayOfYear(dateStart)
dayEnd = sg.calc_dayOfYear(dateEnd)

startTime= "7:00"
endTime = "19:30"

hourStart = sg.calc_hourDecimal(startTime)
hourEnd = sg.calc_hourDecimal(endTime)
#print hourStart, hourEnd
#print sg.calc_solarAngles(latitude, longitude, timezone, dayNow, hourStart)

N = 20
R = 20

#for i in range(N+1):
#	sun = sg.calc_sunVector(latitude, longitude, timezone, dayStart, hourStart+i*(hourEnd-hourStart)/N)
#	if sun[2] > 0:
#		sun[:] = [x*R for x in sun]
#		rs.AddPoint(sun)
for dayNow in range(dayStart, dayEnd, 3):
	for i in range(N+1):
		sun = sg.calc_sunVector(latitude, longitude, timezone, dayNow, hourStart+i*(hourEnd-hourStart)/N)
		if sun[2] > 0:
			sun[:] = [x*R for x in sun]
			rs.AddPoint(sun)