from decodes.core import *
from . import dc_interval #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order

import colorsys

class Color(object):
    """
    a simple color class
    """
    
    def __init__(self, a=None, b=None, c=None):
        """ Color constructor.
        
            :param a: First color value (between 0.0 and 1.0). Defaults to 0.5.
            :type a: float
            :param b: Second color value (between 0.0 and 1.0). Defaults to 0.5.
            :type b: float
            :param c: Third color value (between 0.0 and 1.0). Defaults to 0.5.
            :type c: float
            :result: Color object.
            :rtype: Color
        """
        if a is None : self.r,self.g,self.b = 0.5,0.5,0.5
        elif b is None or c is None : 
            try: 
                self.r,self.g,self.b = a.r,a.g,a.b
            except:
                try: 
                    self.r,self.g,self.b = a.R/255.0,a.G/255.0,a.B/255.0
                except:
                    self.r,self.g,self.b = a,a,a
        else :
            self.r = a
            self.g = b
            self.b = c
        
    @property
    def hue(self):  
        """ Returns hue value of this color.
        
            :result: Decimal value representing hue.
            :rtype: float
        """
        return colorsys.rgb_to_hsv(self.r,self.g,self.b)[0]
    @property
    def sat(self):  
        """ Returns saturation value of this color.
        
            :result: Decimal value representing saturation.
            :rtype: float
        """        
        return colorsys.rgb_to_hsv(self.r,self.g,self.b)[1]
    @property
    def val(self):  
        """ Returns the numeric value of this color.
        
            :result: Decimal value representing this color.
            :rtype: float
        """    
        return colorsys.rgb_to_hsv(self.r,self.g,self.b)[2]

    @property
    def y(self):  
        """ Returns the y-value of this color.
        
            :result: y-value of this color.
            :rtype: float
        """
        return colorsys.rgb_to_yiq(self.r,self.g,self.b)[0]
    @property
    def i(self):  
        """ Returns the i-value of this color.
        
            :result: i-value of this color.
            :rtype: float
        """        
        return colorsys.rgb_to_yiq(self.r,self.g,self.b)[1]
    @property
    def q(self):  
        """ Returns the q-value of this color.
        
            :result: q-value of this color.
            :rtype: float
        """        
        return colorsys.rgb_to_yiq(self.r,self.g,self.b)[2]

    @staticmethod
    def RGB(r,g,b):
        """ Creates a color object from RGB values.
        
            :param r: R color value (between 0.0 and 1.0). 
            :type r: float
            :param g: G color value (between 0.0 and 1.0). 
            :type g: float
            :param b: B color value (between 0.0 and 1.0). 
            :type b: float
            :result: Color object.
            :rtype: Color
        """
        return Color(r,g,b)
    
    @staticmethod
    def HSB(h,s=1,b=1):
        """ Creates a color object from HSB values.
        
            :param h: H color value (between 0.0 and 1.0). 
            :type h: float
            :param s: S color value (between 0.0 and 1.0). Defaults to 1.
            :type s: float
            :param b: B color value (between 0.0 and 1.0). Defaults to 1.
            :type b: float
            :result: Color object.
            :rtype: Color
        """
        clr = colorsys.hsv_to_rgb(h,s,b)
        #print clr[0],clr[1],clr[2]
        return Color(clr[0],clr[1],clr[2])
        
    @staticmethod
    def interpolate(c0,c1,t=0.5):
        """ Returns a new color interpolated from two Color objects.
        
            :param c0: First Color object
            :type c0: Color
            :param c1: Second Color object
            :type c1: Color
            :param t: Interpolation value (between 0.0 and 1.0). Defaults to 0.5.
            :type t: float
            :result: Interpolated Color object.
            :rtype: Color
        """
        r = (1-t) * c0.r + t * c1.r
        g = (1-t) * c0.g + t * c1.g
        b = (1-t) * c0.b + t * c1.b
        return Color(r,g,b)
        
    @staticmethod
    def interpolate2d(u0v0, u0v1, u1v0, u1v1,u=0.5,v=0.5):
        """ Returns a new color interpolated from four Color objects.
        
            :param u0v0: Color object at bottom left corner
            :type u0v0: Color
            :param u0v1: Color object at top left corner
            :type u0v1: Color
            :param u1v0: Color object at bottom right corner
            :type u1v0: Color
            :param u1v1: Color object at top right corner
            :type u1v1: Color
            :param u: Interpolation value (between 0.0 and 1.0). Defaults to 0.5.
            :type u: float
            :param v: Interpolation value (between 0.0 and 1.0). Defaults to 0.5.
            :type v: float
            :result: Interpolated Color object.
            :rtype: Color
        """
        c1 = Color().interpolate(u1v0,u1v1,v)
        c0 = Color().interpolate(u0v0,u0v1,v)
        return Color().interpolate(c0,c1,u)
        
        
    @staticmethod
    def average(colors = []):
        """ Returns a new color that is the average of a list of Color objects.
        
            :param c: Color Objects
            :type c: List
            :result: Averaged Color object.
            :rtype: Color
        """
        try:
            n = len(colors)
        except:
            n = 0
        if n== 0:
            return Color(1.0)
        r,g,b = 0,0,0
        for c in colors:
            r += c.r
            g += c.g
            b += c.b
        return Color(r/n,g/n,b/n)
        
    def __repr__(self):
        return "color[{0},{1},{2}]".format(self.r,self.g,self.b)
        
    def __eq__(self, other):
        """ Overloads the equal **(==)** operator for Color identity.
        
            :param other: Color to be compared.
            :type other: Color
            :result: Boolean result of comparison.
            :rtype: bool

        """    
        bool = True
        if abs(self.r - other.r) > 1.0/255:
            bool = False
        if abs(self.g - other.g) > 1.0/255:
            bool = False
        if abs(self.b - other.b) > 1.0/255:
            bool = False                       
        return bool
        
    def __ne__(self, other): 
        """ Overloads the not equal **(!=)** operator for Color identity.
        
            :param other: Color to be compared.
            :type other: Color
            :result: Boolean result of comparison.
            :rtype: bool

        """
        bool = False
        if abs(self.r - other.r) > 1.0/255:
            bool = True
        if abs(self.g - other.g) > 1.0/255:
            bool = True
        if abs(self.b - other.b) > 1.0/255:
            bool = True                       
        return bool        

