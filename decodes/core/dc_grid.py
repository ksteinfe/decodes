from decodes.core import *


class Grid(object):
    """
    an abstract class for storing information in a raster grid format.
    """
    
    def __init__(self,include_corners=False,wrap=False):
        """ Grid constructor.
        
            :param include_corners: Boolean value.
            :type include_corners: bool
            :param wrap: Boolean value.
            :type wrap: bool
            :result: Grid object
            :rtype: Grid
            
        """
        self.include_corners = include_corners
        self.wrap = wrap

    @property
    def px_width(self):
        """ Returns pixel width.
            
            :result: Pixel width.
            :rtype: int
            
        """
        return int(self._res[0])

    @property
    def px_height(self):
        """ Returns pixel height.
        
            :result: pixel height
            :rtype: int
            
        """
        return int(self._res[1])

    @property
    def addresses(self):
        """ Returns a list of tuples containing x,y addresses in this Grid.
        
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
        return self._pixels[y*self._res[0]+x]

    def set(self,x,y,value):
        """ Set color value at location (x,y).
        
            :param x: x coordinate.
            :type x: float
            :param y: y coordinate.
            :type y: float
            :param value: Color value
            :type value: Color
            :result: Grid object.
            :rtype: None
            
        """
        self._pixels[y*self.px_width+x] = value

# finds neighbors, taking into account both the type of neighborhood and whether there is wrapping or not
    def neighbors_of(self,x,y):
        """ Finds neighbors of location (x,y) in Grid.
            
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

class Image(Grid):
    """
    a raster grid of Colors
    each pixel contains a Color with normalized R,G,B values
    """
    def __init__(self, pixel_res=Interval(20,20), initial_color = Color(),include_corners=False,wrap=True):
        """ Image constructor.
        
            :param pixel_res: Resolution of image.
            :type pixel_res: Interval
            :param initial_color: Start color of image.
            :type initial_color: Color
            :param include_corners: Boolean value.
            :type include_corners: bool
            :param wrap: Boolean value.
            :type wrap: bool
            :result: Image object.
            :rtype: Image
            
            
        """
        try:
            self._res = (int(pixel_res.a),int(pixel_res.b))
        except:
            self._res = pixel_res
        self._pixels = [initial_color]*(self.px_width*self.px_height)
        super(Image,self).__init__(include_corners)

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
        data = array.array("B", (255 for i in xrange(self.px_width * self.px_height * 3)))

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
