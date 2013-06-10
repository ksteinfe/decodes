from decodes.core import *
from . import dc_interval #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order

import colorsys

class Color():
    """
    a simple color class
    """
    
    def __init__(self, a=None, b=None, c=None):
        """Color constructor
        
            :param a: First color value (between 0.0 and 1.0). Defaults to 0.5
            :type a: float
            :param b: Second color value (between 0.0 and 1.0). Defaults to 0.5
            :type b: float
            :param c: Third color value (between 0.0 and 1.0). Defaults to 0.5
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
    def hue(self):  return colorsys.rgb_to_hsv(self.r,self.g,self.b)[0]
    @property
    def sat(self):  return colorsys.rgb_to_hsv(self.r,self.g,self.b)[1]
    @property
    def val(self):  return colorsys.rgb_to_hsv(self.r,self.g,self.b)[2]

    @property
    def y(self):  return colorsys.rgb_to_yiq(self.r,self.g,self.b)[0]
    @property
    def i(self):  return colorsys.rgb_to_yiq(self.r,self.g,self.b)[1]
    @property
    def q(self):  return colorsys.rgb_to_yiq(self.r,self.g,self.b)[2]

    @staticmethod
    def RGB(r,g,b):
        """Creates a color object from RGB values.
        
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
        """Creates a color object from HSB values.
        
            :param h: H color value (between 0.0 and 1.0). 
            :type h: float
            :param s: S color value (between 0.0 and 1.0). Defaults to 1
            :type s: float
            :param b: B color value (between 0.0 and 1.0). Defaults to 1
            :type b: float
            :result: Color object.
            :rtype: Color
        """
        clr = colorsys.hsv_to_rgb(h,s,b)
        #print clr[0],clr[1],clr[2]
        return Color(clr[0],clr[1],clr[2])
        
    @staticmethod
    def interpolate(c0,c1,t=0.5):
        """Returns a new color interpolated from two Color objects.
        
            :param c0: First Color object
            :type c0: Color
            :param c1: Second Color object
            :type c1: Color
            :param t: Interpolation value (between 0.0 and 1.0). Defaults to 0.5
            :type t: float
            :result: Interpolated Color object.
            :rtype: Color
        """
        r = (1-t) * c0.r + t * c1.r
        g = (1-t) * c0.g + t * c1.g
        b = (1-t) * c0.b + t * c1.b
        return Color(r,g,b)
        
    def __repr__(self):
        return "color[{0},{1},{2}]".format(self.r,self.g,self.b)

class PixelGrid(object):
    """
    an abstract class for storing information in a raster grid format.
    """
    
    @property
    def width(self):
        return int(self._size.a)

    @property
    def height(self):
        return int(self._size.b)

    @property
    def dimensions(self):
        return self._size

    def get(self,x,y):
        return self._pixels[y*self._size.a+x]

    def set(self,x,y,value):
        self._pixels[y*self.width+x] = value

    def neighbors_of(self,x,y,include_corners=False,wrap=True):
        ret = []
        #left
        if x > 0 : ret.append(self.get(x-1,y))
        if wrap and x == 0 : ret.append(self.get(self.width-1,y))
        
        #up
        if y < self.height-1 : ret.append(self.get(x,y+1))
        if wrap and y == self.height-1 : ret.append(self.get(x,0))

        #right
        if x < self.width-1 : ret.append(self.get(x+1,y))
        if wrap and x == self.width-1 : ret.append(self.get(0,y))

        #down
        if y > 0 : ret.append(self.get(x,y-1))
        if wrap and y == 0 : ret.append(self.get(x,self.height-1))

        if include_corners:
            raise NotImplementedError("no corners yet")

        return ret

class ValueField(PixelGrid):
    """
    a raster grid of floating point values
    each pixel contains a floating point number
    """
    def __init__(self, dimensions=Interval(20,20), initial_value = 0.0):
        self._size = Interval(int(dimensions.a),int(dimensions.b))
        self._pixels = [initial_value]*(self.width*self.height)

    @property
    def max_value(self):
        return max(self._pixels)

    @property
    def min_value(self):
        return min(self._pixels)

    def to_image(self,min_color,max_color,value_range=None):
        from .dc_interval import Interval
        if value_range is None : value_range = Interval(self.min_value,self.max_value)
        img = Image(self.dimensions)
        for n, val in enumerate(self._pixels):
            try: 
                t = value_range.deval(val)
            except :
                t = 0.0
            img._pixels[n] = Color.interpolate(min_color,max_color,t)
        return img

class BoolField(PixelGrid):
    """
    a raster grid of boolean values
    each pixel contains a True or a False
    """
    def __init__(self, dimensions=Interval(20,20), initial_value = False):
        self._size = Interval(int(dimensions.a),int(dimensions.b))
        self._pixels = [initial_value]*(self.width*self.height)





class Image(PixelGrid):
    """
    a raster grid of Colors
    each pixel contains a Color with normalized R,G,B values
    """
    def __init__(self, dimensions=Interval(20,20), initial_color = Color()):
        self._size = Interval(int(dimensions.a),int(dimensions.b))
        self._pixels = [initial_color]*(self.width*self.height)

    def save(self, filename, path=False, verbose=False):
        import os, struct, array
        if path==False : path = os.path.expanduser("~")
        filename = filename + ".tga"

        if verbose:
            print "saving image to ",os.path.join(path, filename)
            from time import time
            t0 = time()

        ## begin tga header fields:
        ## structure seen at 
        ## http://gpwiki.org/index.php/TGA, 2009-09-20
        Offset = 0
        ColorType = 0
        ImageType = 2
        PaletteStart = 0
        PaletteLen = 0
        PalBits = 8
        XOrigin = 0
        YOrigin = 0
        Width = int(self.width)
        Height = int(self.height)
        BPP = 24
        Orientation = 0

        # (c 'short' stays for 16 bit data)
        StructFmt = "<BBBHHBHHhhBB"

        header = struct.pack(StructFmt, Offset, ColorType, ImageType,
                                        PaletteStart, PaletteLen, PalBits,
                                        XOrigin, YOrigin, Width, Height,
                                        BPP, Orientation)

        # Array mdule and format documentation at:  http://docs.python.org/library/array.html
        data = array.array("B", (255 for i in xrange(self.width * self.height * 3)))

        for n,clr in enumerate(self._pixels):
            data[n * 3] = int(clr.b*255)
            data[n * 3 + 1] = int(clr.g*255)
            data[n * 3 + 2] = int(clr.r*255)

        if verbose: 
            t1 = time()
            print 'packing data took: %f' %(t1-t0)

        if not os.path.exists(path):
            if verbose : print "creating folder",path
            os.makedirs(path)
        
        datafile = open(os.path.join(path, filename), "wb")
        datafile.write(header)
        data.write(datafile)
        datafile.close()

        if verbose: 
            t2 = time()
            print 'writing file took: %f' %(t2-t1)
