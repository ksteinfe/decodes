from decodes.core import *
from . import dc_base, dc_vec, dc_point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "cs.py loaded"
import math, copy, collections

class CS(Geometry, IsBasis):
    """a ortho coordinate system class"""
    """a simple orthonormal cs floating around in R3"""
    """can describe any translation and rigid-body manipulation of the R3"""
    
    def __init__(self,a=None,b=None,c=None):
        """
        CS Constructor.

        .. todo:: write docstring detailing the different ways of constructing a CS
        """
        #TODO: make axes priviate and provide getters and setters that maintain orthagonality and right-handedness
        pt,vec_x,vec_y = Point(), Vec(1,0), Vec(0,1)
        if all( hasattr(a,i) for i in ['x','y','z'] ) :
            # a is something that acts like a point
            pt=a
            if b is not None : vec_x = b
            if c is not None : vec_y = c
            #TODO: handle situation when we've been passed three points
        else :
            # a cannont act like a point, let's try to make a point out of a,b,c
            pt = Point(a,b,c)

        try: self.origin = pt.basis_applied()
        except : self.origin = pt

        if vec_x.length == 0 : raise GeometricError("vec_x is a Vec of length 0")
        if vec_y.length == 0 : raise GeometricError("vec_y is a Vec of length 0")

        self.x_axis = vec_x.normalized()
        self.z_axis = self.x_axis.cross(vec_y).normalized()
        self.y_axis = self.z_axis.cross(self.x_axis).normalized()

    def __repr__(self):
        return "cs o[{0},{1},{2}] n[{3},{4},{5}]".format(self.origin.x,self.origin.y,self.origin.z,self.z_axis.x,self.z_axis.y,self.z_axis.z)

    """a CS can act as a basis for a point"""
    def eval(self,a=0,b=0,c=0):
        try:
            # try using a as a point
            x = a.x
            y = a.y
            z = a.z
        except:
            x = a
            y = b
            z = c
        return self.origin + ((self.x_axis*x)+(self.y_axis*y)+(self.z_axis*z))

    @property
    def xform(self):
        from .dc_xform import Xform
        return Xform.change_basis(CS(), self)
        
    @property
    def ixform(self): 
        from .dc_xform import Xform
        return Xform.change_basis(self, CS())

    @property
    def xy_plane(self):
        return Plane(self.origin,self.z_axis)

    @property
    def xz_plane(self):
        return Plane(self.origin,self.y_axis)

    @property
    def yz_plane(self):
        return Plane(self.origin,self.x_axis)


    @property
    def xAxis(self): 
        """
        depreciated
        """
        print "please use CS.x_axis instead"
        return self.x_axis

    @property
    def yAxis(self): 
        """
        depreciated
        """
        print "please use CS.y_axis instead"
        return self.y_axis

    @property
    def zAxis(self): 
        """
        depreciated
        """
        print "please use CS.z_axis instead"
        return self.z_axis


    @staticmethod
    def on_xy(x=0,y=0,rotation=0):
        """
        returns a coordinate system on the xy plane at a given rotation about the z-axis
        """
        x_vec = Vec(math.cos(rotation),math.sin(rotation))
        return CS(Point(x,y),x_vec,x_vec.cross(Vec(0,0,-1)))
    

class CylCS(Geometry, IsBasis):
    """a cylindrical coordinate system"""
    def __init__(self,pt=Point(0,0)):
        self.origin = pt

        def __repr__(self):
            return "cylcs o[{0},{1},{2}]".format(self.origin.x,self.origin.y,self.origin.z)

    """a CylCS can act as a basis for a point"""
    def eval(self,a,b=None,c=0):
        try:
            radius = a.x
            radians = a.y
            z = a.z
            pt = Point( radius * math.cos(radians), radius * math.sin(radians), z) + self.origin
        except:
            try:
                radius = a
                radians = b
                z = c
                pt = Point( radius * math.cos(radians), radius * math.sin(radians), z) + self.origin
            except:
                raise AttributeError("either pass me a point or three numbers please")
                
        return pt
        
        
