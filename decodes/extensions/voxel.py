import decodes.core as dc
from decodes.core import *
import math

class VoxelField(Geometry):
    """
    Currently rounds down to nearest whole Voxel
    
    """
    def __init__(self, boundary, res_x, res_y, res_z, initial_value = 0.0):
        self.bnds = boundary
        self._res_x = res_x 
        self._res_y = res_y 
        self._res_z = res_z
        self._stack = tuple(ValueField(Interval(res_x,res_y),initial_value) for z in range(self._res_z))
        
    @property
    def res_x(self):
        return self._res_x

    @property
    def res_y(self):
        return self._res_y

    @property
    def res_z(self):
        return self._res_z

    @property
    def bnds(self):
        return self._bnds

    @bnds.setter
    def bnds(self,value): 
        self._dim_pixel = None
        self._dim_pixel2 = None
        self._bnds = value

    @property
    def dim_pixel(self):
        """
        returns the spatial dimensions of a single pixel of this voxel grid as a vector
        """
        if self._dim_pixel is None : self._dim_pixel = Vec(self.bnds.dim_x / self._res_x , self.bnds.dim_y / self._res_y, self.bnds.dim_z / self._res_z)
        return self._dim_pixel

    @property
    def dim_pixel2(self):
        """
        returns the spatial dimensions of HALF OF a single pixel of this voxel grid as a tuple
        """
        if self._dim_pixel2 is None : self._dim_pixel2 = self._dim_pixel = Vec(self.bnds.dim_x / self._res_x , self.bnds.dim_y / self._res_y, self.bnds.dim_z / self._res_z) / 2.0
        return self._dim_pixel2

    @property
    def max_value(self):
        return max([tray.max_value for tray in stack])

    @property
    def min_value(self):
        return min([tray.max_value for tray in stack])

    def set(self,x,y,z,value) :
        if x<0 or x>self._res_x-1 : raise IndexError("x out of bounds. this voxel field has %s pixels in the x direction and you asked to set %s"%(self._res_x,x))
        if y<0 or y>self._res_y-1 : raise IndexError("y out of bounds. this voxel field has %s pixels in the y direction and you asked to set %s"%(self._res_y,y))
        if z<0 or z>self._res_z-1 : raise IndexError("z out of bounds. this voxel field has %s pixels in the z direction and you asked to set %s"%(self._res_z,z))
        self._stack[z]._pixels[int(self.res_y*y+x)] = value
    
    def get(self,x,y,z) :
        if x<0 or x>self._res_x-1 : raise IndexError("x out of bounds. this voxel field has %s pixels in the x direction and you asked for %s"%(self._res_x,x))
        if y<0 or y>self._res_y-1 : raise IndexError("y out of bounds. this voxel field has %s pixels in the y direction and you asked for %s"%(self._res_y,y))
        if z<0 or z>self._res_z-1 : raise IndexError("z out of bounds. this voxel field has %s pixels in the z direction and you asked for %s"%(self._res_z,z))
        return self._stack[z]._pixels[int(self.res_y*y+x)]
    
    def cpt_at(self,x,y,z):
        """
        returns the centerpoint of the pixel referenced by the given address
        """
        if x<0 or x>self._res_x-1 : raise IndexError("x out of bounds. this voxel field has %s pixels in the x direction and you asked for %s"%(self._res_x,x))
        if y<0 or y>self._res_y-1 : raise IndexError("y out of bounds. this voxel field has %s pixels in the y direction and you asked for %s"%(self._res_y,y))
        if z<0 or z>self._res_z-1 : raise IndexError("z out of bounds. this voxel field has %s pixels in the z direction and you asked for %s"%(self._res_z,z))
        pt = self.bnds.eval(float(x)/float(self._res_x),float(y)/float(self._res_y),float(z)/float(self._res_z))
        pt = pt + self.dim_pixel2
        pt.val = self._stack[z]._pixels[int(self.res_y*y+x)]
        return pt
    
    def to_pts(self) :
        pts = []
        for z in range(self.res_z): 
            for y in range(self.res_y): 
                for x in range(self.res_x):
                    pts.append(self.cpt_at(x,y,z))
        return pts