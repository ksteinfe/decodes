# SolarGeometry module

import datetime
import math

#converts a date given as "mo/day" into a day of year
def calc_dayOfYear(dateIn):
	daysInMonth= [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] 	#days in month array
	(month, day) = dateIn.split('/')
	dayOut = 0;
	for m in range(1,int(month)):
		dayOut = dayOut + daysInMonth[m-1]
	dayOut = dayOut + int(day)
	return dayOut


#calculates the following solar position angles for given coordinates, day of the year, local time. 
#		declination
#		hour angle
#		altitude
#		azimuth
# All output in degrees
def calc_solarAngles(latitudeIn, longitudeIn, timezone, dateIn, timeIn):
	(hour, minutes) = timeIn.split(':')
	localTime = int(hour) + int(minutes)/60.0
	(m, d) = dateIn.split('/')
	month = int(m)
	day = int(d)
	#calculates delta = declination angle 
	n = calc_dayOfYear(dateIn)
	print "day of year = ", n
	alpha = (n-1)*360/365.0
	t = math.radians(alpha)
	delta_rad = 0.006918 - 0.399912*math.cos(t)+0.070257*math.sin(t)-0.006758*math.cos(2*t)+0.000907*math.sin(2*t)-0.002697*math.cos(3*t)+0.001480*math.sin(3*t)
	delta = math.degrees(delta_rad)
	print "Declination angle = ", delta

	obliquity_rad = math.radians(23.44)
	rightAsc_rad = math.atan2(math.cos(obliquity_rad)*math.sin(t),math.cos(t))
	if rightAsc_rad < 0.0:
		rightAsc_rad = rightAsc_rad + 2*math.pi
	rightAsc = math.degrees(rightAsc_rad)
	print "Right Ascension angle = ", rightAsc
	
	#calculates Equation of Time (h)
	ET = math.radians(4*(alpha - (rightAsc+180))/60.0)
	ET_Yu = (0.0172 + 0.4281*math.cos(t)-7.3515*math.sin(t)-3.3495*math.cos(2*t) - 9.3619*math.sin(2*t))/60
	print "alpha_rad, ET = ", t, ET, ET_Yu
	
	longitude_rad = math.radians(longitudeIn)
	diff = longitude/15- timezone
	solarTime = localTime + ET + diff
	
	#calc hour-angle
	omega = 15*(solarTime - 12)
	omega_rad = math.radians(omega)
	print "omega = ", omega
	
	#calculate altitude
	phi_rad = math.radians(latitudeIn)
	altitude_rad =  math.asin(math.cos(delta_rad)*math.cos(phi_rad)*math.cos(omega_rad) + math.sin(delta_rad)*math.sin(phi_rad))
	altitude = math.degrees(altitude_rad)
	print "Altitude = ", altitude
	#calc azimuth 
	#azimuth_rad = math.acos((math.sin(delta_rad)*math.cos(phi_rad) - math.cos(delta_rad)*math.sin(phi_rad)*math.cos(omega_rad))/	math.cos(altitude_rad))
	#if math.degrees(omega_rad) < 0:
	#	azimuth = math.degrees(azimuth_rad)
	#else:
	#	azimuth = 360-math.degrees(azimuth_rad)
	#print "Azimuth = ", azimuth	
	#return [delta, omega, altitude, azimuth]

#determine the sun vector for given coordinates, day of the year, local time. 
def calc_sunVector(latitudeIn, longitudeIn, dayIn, hourIn):
	[d, o, altitude, azimuth] = calc_solarAngles(latitudeIn, longitudeIn, dayIn, hourIn)
	altitude_rad= math.radians(altitude)
	azimuth_rad = math.radians(azimuth)
	x = math.cos(altitude_rad)*math.sin(azimuth_rad)
	y = math.cos(altitude_rad)*math.cos(azimuth_rad)
	z = math.sin(altitude_rad)
	return [x, y, z]


# Check to see if this file is being executed as the "Main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if __name__ == '__main__':
	print "Welcome to the solar geometry module!"
	latitude = 42.5
	longitude = 143.28
	timeZone = 9.0  # = GMT+9:00 
	dateNow = "2/11"
	startTime= "11:05"
	
	calc_solarAngles(latitude, longitude, timeZone, dateNow, startTime)
	
	#print calc_solarAngles(latitude, longitude, dayNow, hourStart)
