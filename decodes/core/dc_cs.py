from decodes.core import *
from . import dc_base, dc_vec, dc_point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print("cs.py loaded")
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

        #try: self.origin = pt.basis_applied()
        #except : self.origin = pt
        self.origin = pt
        
        if vec_x.length == 0 : raise GeometricError("vec_x is a Vec of length 0")
        if vec_y.length == 0 : raise GeometricError("vec_y is a Vec of length 0")

        self.x_axis = vec_x.normalized()
        self.z_axis = self.x_axis.cross(vec_y).normalized()
        self.y_axis = self.z_axis.cross(self.x_axis).normalized()

    def __eq__(self, other):
        """ Overloads the equal **(==)**  operator for position and orientation of this CS as compared to the given CS.
        
            :param other: CS to be compared.
            :type other: CS
            :result: Boolean result of comparison.
            :rtype: bool

        """
        try:
            return self.origin == other.origin and self.x_axis == other.x_axis and  self.y_axis == other.y_axis and  self.z_axis == other.z_axis
        except:
            return False
        
    def __ne__(self, other): 
        """ Overloads the not equal **(!=)** operator for position and orientation of this CS as compared to the given CS.
        
            :param other: CS to be compared.
            :type other: CS
            :result: Boolean result of comparison.
            :rtype: bool

        """
        return not self == other
        
        
    def __add__(self, other): 
        """| Overloads the addition **(+)** operator. 
           | Translates this CS by adding the given Vec to the origin of this CS and returns this CS
        
           :param other: Vec to be added
           :type other: Vec
           :result: this CS.
           :rtype: CS
           
           ::
                
                cs + vec
        """
        self.origin += other
        return self
        
        
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
        try:
            x,y,z = a.x,a.y,a.z
        except:
            x,y,z = a,b,c
        
        v = Vec(self.origin,Point(x,y,z)) 
        xx = v.dot(self.x_axis)
        yy = v.dot(self.y_axis)
        zz = v.dot(self.z_axis)

        return Vec(xx,yy,zz)

    def eval_cyl(self,radius,radians,z=0):
        """ Returns a Point relative to this CS given three cylindrical coordinates.
        
            :param radius: number representing the distance of the resulting Point from the origin of this CS.
            :type radius: float
            :param radians: number representing the rotation angle (in radians) of the resulting Point measured from the x-axis of this CS.
            :type radians: float
            :param z: number representing the distance of the resulting Point from the xy_plane of this CS.
            :type z: float
            :result: A Point in a cylindrical space.
            :rtype: Point
            
        """
        pt = Point( radius * math.cos(radians), radius * math.sin(radians), z)
        return self.eval(pt)

    def deval_cyl(self,a,b=0,c=0):
        """ Evaluates the given coordinates (or coordinates contained within a given Point) and returns a tuple containing the cylindrical coordinate representation of this Point relative to this CS.
            
            :param a: Point or decimal number.
            :type a: Point or float
            :param b: None or decimal number.
            :type b: None or float
            :param c: None or decimal number.
            :type c: None or float
            :result: Tuple of cylindrical coordinates - radius, radians, z.
            :rtype: (float, float, float)
            
        """
        vec = self.deval(a,b,c)
        z = vec.z
        vec.z = 0
        radius = vec.length
        ang = vec.angle(self.x_axis)

        vec_lcl = self.deval(a,b,c)
        z = vec_lcl.z
        vec_lcl.z = 0
        radius = vec_lcl.length
    
        vec_gbl = Vec(self.origin,self.eval(vec_lcl.x,vec_lcl.y))
        ang = vec_gbl.angle(self.x_axis)

        if not self.x_axis.is_parallel(vec_gbl):
            crs = self.x_axis.cross(vec_gbl)
            if crs.angle(self.z_axis) > math.pi/2 : ang = math.pi*2-ang

        return(radius,ang,z)
        
    def eval_sph(self, rho, phi, theta):
        """ Returns a Point relative to this CS given three spherical coordinates.
        
            :param rho: number representing the distance of the resulting Point from the origin of this CS.
            :type rho: float
            :param phi: number representing the polar coordinate running from 0 to pi (colatitude).
            :type phi: float
            :param theta: number representing the azimuthal coordinate running from 0 to 2pi (longitude).
            :type theta: float
            :result: a Point in a spherical space.
            :rtype: point
            
        """
        x = rho*math.sin(phi)*math.cos(theta)
        y = rho*math.sin(phi)*math.sin(theta)
        z = rho*math.cos(phi)
        
        return self.eval(Point(x,y,z))
    
    def deval_sph(self,a,b=0,c=0):
        """ Evaluates the given coordinates (or coordinates contained within a given Point) and returns a tuple containing the spherical coordinate representation of this Point relative to this CS.
            
            :param a: Point or decimal number.
            :type a: Point or float.
            :param b: None or decimal number.
            :type b: None or float.
            :param c: None or decimal number.
            :type c: None or float
            :result: Tuple of spherical coordinates - radius, longitude, colatitude
            :rtype: (float, float, float)
        
        """
        
        vec = self.deval(a,b,c)
        rho = vec.length
        theta = math.radians((180/math.pi)*math.atan2(-vec.y, -vec.x)+180)
        phi = Vec.uz().angle(vec)
        
        return (rho, phi, theta)
    
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
            x_vec = Vec(0,0,1)
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
            x_vec = Vec(0,0,1)
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
        
