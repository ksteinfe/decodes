# SolarGeometry module
import decodes.core as dc
from decodes.core import *
import datetime
import math

#converts a date given as "mo/day" into a day of year
def calc_day_of_year(date_in):
    daysInMonth= [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]     #days in month array
    (month, day) = date_in.split('/')
    dayOut = 0;
    for m in range(1,int(month)):
        dayOut = dayOut + daysInMonth[m-1]
    dayOut = dayOut + int(day)
    return dayOut

#converts 24h time into a decimal hour
def calc_hourDecimal(time_in):
    (hour, minutes) = time_in.split(':')
    return  int(hour) + int(minutes)/60.0

#calculates alpha = ecliptic longitute, varying from alpha = 0 at the March Equinox completing 360 in 1 year.  Output in degrees.
#divides the year into intervals between solstice-equinox and treats alpha as uniformly varying throughout each interval    
def calc_alpha(day_in):
    marchEquinox = calc_day_of_year("3/20")
    juneSolstice = calc_day_of_year("6/20")
    septemberEquinox = calc_day_of_year("9/22")
    decemberSolstice = calc_day_of_year("12/21")
    if (marchEquinox<=day_in <= juneSolstice) :
        alphaOut = 90*(day_in-marchEquinox)/(juneSolstice-marchEquinox)
    elif (juneSolstice < day_in <=septemberEquinox):
        alphaOut = 90+90*(day_in-juneSolstice)/(septemberEquinox-juneSolstice)
    elif (septemberEquinox< day_in<=decemberSolstice):
        alphaOut = 180+90*(day_in-septemberEquinox)/(decemberSolstice-septemberEquinox)
    else:
        alphaOut = 270+90*(day_in + 365 - decemberSolstice)/(marchEquinox + 365-decemberSolstice)
    return alphaOut

#calculates the following solar position angles for given coordinates, day of the year, local time. 
#        declination
#        hour angle
#        altitude
#        azimuth
# All output in degrees
def calc_solarangles(latitude_in, longitude_in, timezone, day_in, hour_in):
    alpha = calc_alpha(day_in)
    alpha_rad = math.radians(alpha)
    obliquity_rad = math.radians(23.44)
    #calc delta = declination angle 
    delta_rad = math.asin(math.sin(alpha_rad)*math.sin(obliquity_rad))
    #delta = math.degrees(delta_rad)
    
    #calc omega = hour angle, angle between local longitude and solar noon
    ET = (0.0172 + 0.4281*math.cos(alpha_rad)-7.3515*math.sin(alpha_rad)-3.3495*math.cos(2*alpha_rad) - 9.3619*math.sin(2*alpha_rad))/60
    omega = 15*(hour_in + longitude_in/15 - timezone + ET - 12)
    omega_rad = math.radians(omega)
    
    #calc altitude
    phi_rad = math.radians(latitude_in)
    altitude_rad =  math.asin(math.cos(delta_rad)*math.cos(phi_rad)*math.cos(omega_rad) + math.sin(delta_rad)*math.sin(phi_rad))
    #altitude = math.degrees(altitude_rad)
    #calc azimuth 
    azimuth_rad = math.acos((math.sin(delta_rad)*math.cos(phi_rad) - math.cos(delta_rad)*math.sin(phi_rad)*math.cos(omega_rad))/    math.cos(altitude_rad))
    if omega_rad > 0:
        azimuth_rad = math.pi-azimuth_rad
        
    return [delta_rad, omega_rad, altitude_rad, azimuth_rad]

#determine the sun vector for given coordinates, day of the year, local time. 
def calc_sunvector(latitude_in, longitude_in, timezone, day_in, hour_in):
    [d, o, altitude, azimuth] = calc_solarangles(latitude_in, longitude_in, timezone, day_in, hour_in)
    x = math.cos(altitude)*math.sin(azimuth)
    y = math.cos(altitude)*math.cos(azimuth)
    z = math.sin(altitude)
    return Vec(x, y, z)


# Check to see if this file is being executed as the "Main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if __name__ == '__main__':
    print "Welcome to the solar geometry module!"
