# SolarGeometry module
import decodes.core as dc
from decodes.core import *
import datetime
import math

class SolarGeom():
    def __init__(self,latitude,longitude,timezone):
        self.lat = latitude
        self.lng = longitude
        self.tmz = timezone   

    #determine the sun vector for given coordinates, day of the year, local time. 
    def vec_at(self,day_of_year,hour_of_day):
        altitude, azimuth = self.altazi_at(day_of_year,hour_of_day)
        x = math.cos(altitude)*math.sin(azimuth)
        y = math.cos(altitude)*math.cos(azimuth)
        z = math.sin(altitude)
        return Vec(x, y, z)

    def altazi_at(self,day_of_year,hour_of_day):
        altitude, azimuth, d, o = self.angles_at(day_of_year,hour_of_day)
        return altitude, azimuth

    def angles_at(self,day_of_year,hour_of_day):
        """
        calculates the following solar position angles for given coordinates, integer day of the year (0->365), local time. 
        Altitude
        Azimuth
        Declination
        Hour Angle
        all output in radians
        """
        alpha = self._calc_alpha(day_of_year, hour_of_day)
        #calculate Declination Angle
        declination = 0.396372-22.91327*math.cos(alpha)+4.02543*math.sin(alpha)-0.387205*math.cos(2*alpha)+0.051967*math.sin(2*alpha)-0.154527*math.cos(3*alpha)+0.084798*math.sin(3*alpha)
        declination_rad = math.radians(declination)
        
        # time correction for solar angle 
        TC = 0.004297+0.107029*math.cos(alpha)-1.837877*math.sin(alpha)-0.837378*math.cos(2*alpha)-2.340475*math.sin(2*alpha)
        # calculate Solar Hour Angle, angle between local longitude and solar noon
        hour_angle = (hour_of_day-12-self.tmz)*(360/24) + self.lng + TC
        if hour_angle >= 180:
            hour_angle = hour_angle - 360
        if hour_angle <= -180:
            hour_angle = hour_angle + 360
        hour_angle_rad = math.radians(hour_angle)      
        
        #calc Altitude Angle
        lat_rad = math.radians(self.lat)
        cos_zenith= math.sin(lat_rad)*math.sin(declination_rad)+math.cos(lat_rad)*math.cos(declination_rad)*math.cos(hour_angle_rad)
        if cos_zenith>1:
            cos_zenith = 1
        if cos_zenith<-1:
            cos_zenith = -1

        zenith_rad = math.acos(cos_zenith)
        altitude_rad =  math.asin(cos_zenith)
        
        #calc Azimuth angle
        cos_azimuth = (math.sin(declination_rad)-math.sin(lat_rad)*math.cos(zenith_rad))/(math.cos(lat_rad)*math.sin(zenith_rad))
        azimuth = math.degrees(math.acos(cos_azimuth))
        if hour_angle_rad > 0:
            azimuth = 360-azimuth
        azimuth_rad = math.radians(azimuth)
        
        return altitude_rad, azimuth_rad, declination_rad, hour_angle_rad



    @staticmethod
    def _calc_alpha(day_in, hour_in):
        """
        calculates alpha = ecliptic longitude, varying from alpha = 0 completing 360 in 1 year.
        """
        alphaOut = (360/365.25)*(day_in + hour_in/24) 
        return math.radians(alphaOut)
    
    @staticmethod
    def str_to_day_of_year(date_in):
        """
        converts a date given as "mo/day" into a day of year
        """
        daysInMonth= [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  
        (month, day) = date_in.split('/')
        dayOut = 0;
        for m in range(1,int(month)):
            dayOut = dayOut + daysInMonth[m-1]
        dayOut = dayOut + int(day)
        return dayOut

    @staticmethod
    def str_to_decimal_hour(time_in):
        """
        converts 24h time into a decimal hour
        """
        (hour, minutes) = time_in.split(':')
        return  int(hour) + int(minutes)/60.0

