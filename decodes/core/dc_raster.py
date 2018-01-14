from decodes.core import *


class Raster(object):
    """
    an abstract class for storing information in a raster grid format.
    """
    
    def __init__(self,pixel_dim=None,**kwargs):
        """ Raster constructor.
        
            :param pixel_dim: Pixel dimension of this Raster.
            :type pixel_dim: Interval or Tuple        
            :param include_corners: Boolean value.
            :type include_corners: bool
            :param wrap: Boolean value.
            :type wrap: bool
            :result: Raster object
            :rtype: Raster
            
        """
        if pixel_dim is None: pixel_dim = Interval(20,20)
        try:
            self._dim = (int(pixel_dim.a),int(pixel_dim.b))
        except:
            try:
                a,b = pixel_dim
                a,b = int(a), int(b)
                self._dim = a,b
            except:
                raise Exception("The first given argument should be either an Interval or a Tuple of two Integers")            
        
        self.include_corners = False
        self.wrap = False
        if "include_corners" in kwargs: self.include_corners = kwargs["include_corners"]
        if "wrap" in kwargs: self.wrap = kwargs["wrap"]
        
        # the _pixels collection is initialized but not populated
        self._pixels = []

        
    @property
    def px_dim(self):
        """ Returns pixel dimension.
            
            :result: Pixel Dimension.
            :rtype: (int,int)
            
        """
        return self._dim
        
    @property
    def px_width(self):
        """ Returns pixel width.
            
            :result: Pixel width.
            :rtype: int
            
        """
        return int(self._dim[0])

    @property
    def px_height(self):
        """ Returns pixel height.
        
            :result: pixel height
            :rtype: int
            
        """
        return int(self._dim[1])
        
    @property
    def px_count(self):
        """ Returns the total number of pixels.
        
            :result: pixel count
            :rtype: int
            
        """
        return self.px_width*self.px_height

    @property
    def addresses(self):
        """ Returns a list of tuples containing x,y addresses in this Raster.
        
            :result: a list of tuples
            :rtype: [(int,int)]
            
        """
        return [(x,y) for x in range(self.px_width) for y in range(self.px_height)]
        
    def get(self,x,y):
        """ Returns value at location (x,y).
        
            :param x: x coordinate.
            :type x: float
            :param y: y coordinate.
            :type y: float
            :result: Color value.
            :rtype: Color
            
        """
        return self._pixels[y*self._dim[0]+x]

    def set(self,x,y,value):
        """ Set color value at location (x,y).
        
            :param x: x coordinate.
            :type x: float
            :param y: y coordinate.
            :type y: float
            :param value: Color value
            :type value: Color
            :result: Raster object.
            :rtype: None
            
        """
        self._pixels[y*self.px_width+x] = value
    
    def populate(self,val,do_copy=False):
        """ Populates every pixel with the given value, or a copy of the value
        
            :param val: The value to populate this Raster.
            :type val: object
            :param do_copy: Switch to create copies of the given value
            :type value: Boolean
            :result: Raster object.
            :rtype: None
            
        """
        if not do_copy: self._pixels = [val]*self.px_count
        else: 
            self._pixels = []
            for n in range(self.px_count): self._pixels.append(copy.copy(val))

# finds neighbors, taking into account both the type of neighborhood and whether there is wrapping or not
    def neighbors_of(self,x,y):
        """ Finds neighbors of location (x,y) in Raster.
            
            :param x: x coordinate.
            :type x: float
            :param y: y coordinate.
            :type y: float
            :result: List of neighbors.
            :rtype: list
            
        """
        m = self.px_width
        n = self.px_height
        ret=[]
        for di in [-1,0,1]:
            for dj in [-1,0,1]:
                if (abs(di)+abs(dj)) > 0:
                    if self.wrap :          # wrap is true
                        new_index = ((y+dj)%n)*m+((x+di)%m)
                        if (di == 0) or (dj == 0) : ret.append(self._pixels[new_index])
                        elif self.include_corners : ret.append(self._pixels[new_index])
                    else:           # wrap is false
                        if ((x+di) in range(m)) and ((y+dj) in range(n)):
                            new_index = ((y+dj)%n)*m+((x+di)%m)
                            if (di == 0) or (dj == 0) : ret.append(self._pixels[new_index])
                            elif self.include_corners : ret.append(self._pixels[new_index])
        return ret

class Image(Raster):
    """
    a raster grid of Colors
    each pixel contains a Color with normalized R,G,B values
    """
    def __init__(self,pixel_dim,initial_color = Color(),**kwargs):
        """ Image constructor.
        
            :param pixel_dim: Resolution of image.
            :type pixel_dim: Interval or Tuple of two Integers
            :param initial_color: Start color of image.
            :type initial_color: Color
            :param include_corners: Boolean value.
            :type include_corners: bool
            :param wrap: Boolean value.
            :type wrap: bool
            :result: Image object.
            :rtype: Image
            
            
        """
        super(Image,self).__init__(pixel_dim,**kwargs)
        self.populate(initial_color)
        

    def save(self, filename, path=False, verbose=False):
        """ Saves image file.
            
            :param filename: Name of the image.
            :type filename: str
            :param path: File path to save image to.
            :type path: bool
            :param verbose: Boolean value
            :type verbose: bool
            :result: Saved image file.
            :rtype: None
        
        """
        import os, struct, array
        if path==False : path = os.path.expanduser("~")
        filename = filename + ".tga"

        if verbose:
            print("saving image to ",os.path.join(path, filename))
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
        Width = int(self.px_width)
        Height = int(self.px_height)
        BPP = 24
        Orientation = 0

        # (c 'short' stays for 16 bit data)
        StructFmt = "<BBBHHBHHhhBB"

        header = struct.pack(StructFmt, Offset, ColorType, ImageType,
                                        PaletteStart, PaletteLen, PalBits,
                                        XOrigin, YOrigin, Width, Height,
                                        BPP, Orientation)

        # Array mdule and format documentation at:  http://docs.python.org/library/array.html
        data = array.array("B", (255 for i in range(self.px_width * self.px_height * 3)))

        for n,clr in enumerate(self._pixels):
            data[n * 3] = int(clr.b*255)
            data[n * 3 + 1] = int(clr.g*255)
            data[n * 3 + 2] = int(clr.r*255)

        if verbose: 
            t1 = time()
            print('packing data took: %f' %(t1-t0))

        if not os.path.exists(path):
            if verbose : print("creating folder",path)
            os.makedirs(path)
        
        datafile = open(os.path.join(path, filename), "wb")
        datafile.write(header)
        data.write(datafile)
        datafile.close()

        if verbose: 
            t2 = time()
            print('writing file took: %f' %(t2-t1))



class ValueField(Raster):
    """
    a raster grid of floating point values
    each pixel contains a floating point number
    """
    def __init__(self, pixel_dim=None, initial_value=0.0, **kwargs):
        """ ValueField constructor.
        
            :param pixel_dim: Resolution of ValueField.
            :type pixel_dim: Interval
            :param initial_value: Start value of ValueField.
            :type initial_value: float
            :param include_corners: Boolean Value.
            :type include_corners: bool
            :param wrap: Boolean Value.
            :type wrap: bool
            :result: ValueField Object
            :rtype: ValueField
            
        """
        if "wrap" not in kwargs: kwargs["wrap"] = True
        super(ValueField,self).__init__(pixel_dim,**kwargs)
        self.populate(initial_value)
        

    @property
    def max_value(self):
        """ Returns max value of ValueField.
        
            :result: Maximum value.
            :rtype: float
        """
    
        return max(self._pixels)

    @property
    def min_value(self):
        """ Returns min value of ValueField.
        
            :result: Minimum value.
            :rtype: float
        """
        return min(self._pixels)

    def to_image(self,min_color,max_color,value_range=None):
        """ Constructs image from ValueField.
        
            :param min_color: Minimum color in image.
            :type min_color: Color
            :param max_color: Maximum color in image.
            :type max_color: Color
            :param value_range: Range of values.
            :type value_range: Interval
            :result: Image.
            :rtype: Image.
            
        """
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

class BoolField(Raster):
    """
    a raster grid of boolean values
    each pixel contains a True or a False
    """
    
    def __init__(self, pixel_dim=None, initial_value=False, **kwargs):
        """ BoolField constructor.
        
            :param pixel_dim: Resolution of BoolField.
            :type pixel_dim: Interval
            :param initial_value: Start value of BoolField
            :type initial_value: bool
            :param include_corners: Boolean value.
            :type include_corners: bool
            :param wrap: Boolean value.
            :type wrap: bool
            :result: BoolField object.
            :rtype: BoolField
            
        """
        if "wrap" not in kwargs: kwargs["wrap"] = True
        super(BoolField,self).__init__(pixel_dim,**kwargs)
        self.populate(initial_value)
        

    def to_image(self,false_color=Color(1.0),true_color=Color(0.0)):
        """ Constructs and image from the BoolField.
            
            :param false_color: Color for False values.
            :type false_color: Color
            :param true_color: Color for True values.
            :type true_color: Color
            :result: Image
            :rtype: Image
            
        """
        img = Image(self._dim,false_color)
        for n, bool in enumerate(self._pixels):
            if bool : img._pixels[n] = true_color

        return img

        
