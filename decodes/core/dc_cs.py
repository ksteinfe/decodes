from decodes.core import *
from . import dc_base, dc_vec, dc_point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "cs.py loaded"
import math, copy, collections

class CS(Geometry, Basis):
    """a ortho coordinate system class"""
    """a simple orthonormal cs floating around in R3"""
    """can describe any translation and rigid-body manipulation of the R3"""
    
    def __init__(self,a=None,b=None,c=None):
        """ CS Constructor.
           
            :param a: Point or decimal number.
            :type a: Point or float
            :param b: None or decimal number.
            :type b: None or float
            :param c: None or decimal number.
            :type c: None or float
            :result: Coordinate system.
            :rtype: Coordinate system
        """
        #TODO: write docstring detailing the different ways of constructing a CS
        #TODO: make axes private and provide getters and setters that maintain orthogonality and right-handedness
        pt,vec_x,vec_y = Point(), Vec(1,0), Vec(0,1)
        if all( hasattr(a,i) for i in ['x','y','z'] ) :
            # a is something that acts like a point
            pt=a
            if b is not None : vec_x = b
            if c is not None : vec_y = c
            #TODO: handle situation when we've been passed three points
        else :
            # a cannot act like a point, let's try to make a point out of a,b,c
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

    def eval(self,a,b=0,c=0):
        """ Evaluates the given coordinates (or coordinates contained within a given Point) relative to this CS and returns a Point.
            
            :param a: Point or decimal number.
            :type a: Point or float
            :param b: None or decimal number.
            :type b: None or float
            :param c: None or decimal number.
            :type c: None or float
            :result: Point in world coordinates.
            :rtype: Point
            
        """
        try:
            x,y,z = a.x,a.y,a.z
        except:
            x,y,z = a,b,c
        return Point(self.origin + ((self.x_axis*x)+(self.y_axis*y)+(self.z_axis*z)))

    def deval(self,a,b=0,c=0):
        """ Evaluates the given coordinates (or coordinates contained within a given Point) and returns a Vector between the origin of this CS and the point.
            
            :param a: Point or decimal number.
            :type a: Point or float
            :param b: None or decimal number.
            :type b: None or float
            :param c: None or decimal number.
            :type c: None or float
            :result: Vector in this CS.
            :rtype: Vec
            
        """
        from .dc_line import Line  
        try:
            x,y,z = a.x,a.y,a.z
        except:
            x,y,z = a,b,c
        
        pt = Point(x,y,z)
        xx = Line(self.origin,self.x_axis).near(pt)[1]
        yy = Line(self.origin,self.y_axis).near(pt)[1]
        zz = Line(self.origin,self.z_axis).near(pt)[1]
        return Vec(xx,yy,zz)

    @property
    def xform(self):
        """ Returns the Xform that corresponds to the transformation from world space to CS space.
        
        """
        from .dc_xform import Xform
        return Xform.change_basis(CS(), self)
        
    @property
    def ixform(self): 
        """ Returns the Xform that corresponds to the transformation from CS space to world space.
        
        """
        from .dc_xform import Xform
        return Xform.change_basis(self, CS())

    @property
    def xy_plane(self):
        """ Returns the xy plane.
        
        """
        return Plane(self.origin,self.z_axis)

    @property
    def xz_plane(self):
        """ Returns the xz plane.
        
        """
        return Plane(self.origin,self.y_axis)

    @property
    def yz_plane(self):
        """ Returns the yz plane.
        
        """
        return Plane(self.origin,self.x_axis)

    @property
    def x_ray(self):
        """ Returns a ray along the x-axis.
        """
        from .dc_line import Ray
        return Ray(self.origin,self.x_axis)

    @property
    def y_ray(self):
        """ Returns a ray along the y-axis.
        """
        from .dc_line import Ray
        return Ray(self.origin,self.y_axis)

    @property
    def z_ray(self):
        """ Returns a ray along the z-axis.
        """
        from .dc_line import Ray
        return Ray(self.origin,self.z_axis)

    @property
    def xAxis(self): 
        """ depreciated
        """
        warnings.warn("cs.xAxis depreciated. please use CS.x_axis instead")
        return self.x_axis

    @property
    def yAxis(self): 
        """ depreciated
        """
        warnings.warn("cs.yAxis depreciated. please use CS.y_axis instead")
        return self.y_axis

    @property
    def zAxis(self): 
        """ depreciated
        """
        warnings.warn("cs.zAxis depreciated. please use CS.z_axis instead")
        return self.z_axis


    @staticmethod
    def on_xy(x=0,y=0,x_vec=None,rot=None):
        """ Returns a coordinate system on the world xy plane. Optionally, one may define the origin_x and origin_y of the resulting CS. One may also define ONE (but not both) of the following: 
            
            * a vector that controls the rotation of the resulting CS on the xy_plane. The z coordinate of this vector will be ignored.
            * a rotation value (0->2PI) that does the same thing
        
            :param x: x coordinate of CS origin.
            :type x: float
            :param y: y coordinate of CS origin.
            :type y: float
            :param x_vec: A vector that controls the rotation of the CS.
            :type x_vec: Vec
            :param rot: A rotation value between 0 and 2PI.
            :type rot: float
            :result: Coordinate system on the world xy plane.
            :rtype: Coordinate system.
            
        """

        if x_vec is not None and rot is not None : raise GeometricError("You may specify *only* one of the following: x_vec, rotation")
        if rot is not None:
            x_vec = Vec(math.cos(rot),math.sin(rot))
        if x_vec is None:
            x_vec = Vec(1,0)
        x_vec.z = 0
        return CS(Point(x,y,0),x_vec,x_vec.cross(Vec(0,0,-1)))
    
    @staticmethod
    def on_xz(x=0,z=0,x_vec=None,rot=None):
        """ Returns a coordinate system on the world xz plane. Optionally, one may define the origin_x and origin_z of the resulting CS. One may also define ONE (but not both) of the following: 
        
            * a vector that controls the rotation of the resulting CS on the xz_plane. The y coordinate of this vector will be ignored.
            * a rotation value (0->2PI) that does the same thing
            
            :param x: x coordinate of CS origin.
            :type x: float
            :param z: z coordinate of CS origin.
            :type z: float
            :param x_vec: A vector that controls the rotation of the CS.
            :type x_vec: Vec
            :param rot: A rotation value between 0 and 2PI.
            :type rot: float
            :result: Coordinate system on the world xz plane.
            :rtype: Coordinate system.         
        """

        if x_vec is not None and rot is not None : raise GeometricError("You may specify *only* one of the following: x_vec, rotation")
        if rot is not None:
            x_vec = Vec(math.cos(rot),0,math.sin(rot))
        if x_vec is None:
            x_vec = Vec(1,0)
        x_vec.y = 0
        return CS(Point(x,0,z),x_vec,x_vec.cross(Vec(0,1,0)))

    @staticmethod
    def on_yz(y=0,z=0,x_vec=None,rot=None):
        """ Returns a coordinate system on the world yz plane. Optionally, one may define the origin_y and origin_z of the resulting CS. One may also define ONE (but not both) of the following: 
        
            * a vector that controls the rotation of the resulting CS on the yz_plane. The x coordinate of this vector will be ignored.
            * a rotation value (0->2PI) that does the same thing
            
            :param y: y coordinate of CS origin.
            :type y: float
            :param z: z coordinate of CS origin.
            :type z: float
            :param x_vec: A vector that controls the rotation of the CS.
            :type x_vec: Vec
            :param rot: a rotation value between 0 and 2PI
            :type rot: float
            :result: Coordinate system on the world yz plane.
            :rtype: Coordinate system        
        """

        if x_vec is not None and rot is not None : raise GeometricError("You may specify *only* one of the following: x_vec, rotation")
        if rot is not None:
            x_vec = Vec(0,math.cos(rot),math.sin(rot))
        if x_vec is None:
            x_vec = Vec(1,0)
        x_vec.x = 0
        return CS(Point(0,y,z),x_vec,x_vec.cross(Vec(-1,0,0)))


class ShearedCS(Geometry, Basis):
    def __init__(self,pt=Point(0,0),x_axis=Vec(1,0),y_axis=Vec(1,0),z_axis=None):
        self.origin = pt



class CylCS(Geometry, Basis):
    """a cylindrical coordinate system"""
    def __init__(self,pt=Point(0,0)):
        self.origin = pt

        def __repr__(self):
            return "cylcs o[{0},{1},{2}]".format(self.origin.x,self.origin.y,self.origin.z)

    """a CylCS can act as a basis for a point"""
    def eval(self,a,b=None,c=0):
        """ Returns a Point from this CS to a Cylindrical CS.
        
            :param a: Point or decimal number.
            :type a: Point or float
            :param b: None or decimal number.
            :type b: None or float
            :param c: None or decimal number.
            :type c: None or float
            :result: A Point in a Cylindrical CS.
            :rtype: Point
            
        """
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
        
        
