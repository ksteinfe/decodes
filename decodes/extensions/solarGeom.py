# SolarGeometry module
import decodes.core as dc
from decodes.core import *
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

#converts 24h time into a decimal hour
def calc_hourDecimal(timeIn):
	(hour, minutes) = timeIn.split(':')
	return  int(hour) + int(minutes)/60.0

#calculates alpha = ecliptic longitute, varying from alpha = 0 at the March Equinox completing 360 in 1 year.  Output in degrees.
#divides the year into intervals between solstice-equinox and treats alpha as uniformly varying throughout each interval	
def calc_alpha(dayIn):
	marchEquinox = calc_dayOfYear("3/20")
	juneSolstice = calc_dayOfYear("6/20")
	septemberEquinox = calc_dayOfYear("9/22")
	decemberSolstice = calc_dayOfYear("12/21")
	if (marchEquinox<=dayIn <= juneSolstice) :
		alphaOut = 90*(dayIn-marchEquinox)/(juneSolstice-marchEquinox)
	elif (juneSolstice < dayIn <=septemberEquinox):
		alphaOut = 90+90*(dayIn-juneSolstice)/(septemberEquinox-juneSolstice)
	elif (septemberEquinox< dayIn<=decemberSolstice):
		alphaOut = 180+90*(dayIn-septemberEquinox)/(decemberSolstice-septemberEquinox)
	else:
		alphaOut = 270+90*(dayIn + 365 - decemberSolstice)/(marchEquinox + 365-decemberSolstice)
	return alphaOut

#calculates the following solar position angles for given coordinates, day of the year, local time. 
#		declination
#		hour angle
#		altitude
#		azimuth
# All output in degrees
def calc_solarAngles(latitudeIn, longitudeIn, timezone, dayIn, hourIn):
	alpha = calc_alpha(dayIn)
	alpha_rad = math.radians(alpha)
	obliquity_rad = math.radians(23.44)
	#calc delta = declination angle 
	delta_rad = math.asin(math.sin(alpha_rad)*math.sin(obliquity_rad))
	delta = math.degrees(delta_rad)
	
	#calc omega = hour angle, angle between local longitude and solar noon
	ET = (0.0172 + 0.4281*math.cos(alpha_rad)-7.3515*math.sin(alpha_rad)-3.3495*math.cos(2*alpha_rad) - 9.3619*math.sin(2*alpha_rad))/60
	omega = 15*(hourIn + longitudeIn/15 - timezone + ET - 12)
	omega_rad = math.radians(omega)
	
	#calc altitude
	phi_rad = math.radians(latitudeIn)
	altitude_rad =  math.asin(math.cos(delta_rad)*math.cos(phi_rad)*math.cos(omega_rad) + math.sin(delta_rad)*math.sin(phi_rad))
	altitude = math.degrees(altitude_rad)
	#calc azimuth 
	azimuth_rad = math.acos((math.sin(delta_rad)*math.cos(phi_rad) - math.cos(delta_rad)*math.sin(phi_rad)*math.cos(omega_rad))/	math.cos(altitude_rad))
	if math.degrees(omega_rad) < 0:
		azimuth = math.degrees(azimuth_rad)
	else:
		azimuth = 360-math.degrees(azimuth_rad)
		
	return [delta, omega, altitude, azimuth]

#determine the sun vector for given coordinates, day of the year, local time. 
def calc_sunVector(latitudeIn, longitudeIn, timezone, dayIn, hourIn):
	[d, o, altitude, azimuth] = calc_solarAngles(latitudeIn, longitudeIn, timezone, dayIn, hourIn)
	altitude_rad= math.radians(altitude)
	azimuth_rad = math.radians(azimuth)
	x = math.cos(altitude_rad)*math.sin(azimuth_rad)
	y = math.cos(altitude_rad)*math.cos(azimuth_rad)
	z = math.sin(altitude_rad)
	return Vec(x, y, z)


# Check to see if this file is being executed as the "Main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if __name__ == '__main__':
	print "Welcome to the solar geometry module!"
