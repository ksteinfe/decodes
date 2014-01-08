from decodes.core import *
from . import dc_base, dc_vec, dc_point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "plane.py loaded"
import math


class Plane(Geometry):
    """
    a simple plane class


    """
    
    def __init__(self, point=Point(), normal=Vec(0,0,1)):
        """ Plane constructor.

            :param point: Base point for a plane. 
            :type point: Point
            :param normal: Normal direction of the new Plane. Defaults to Vec(0,0,1).
            :type normal: Vec
            :result: Plane object.
            :rtype: Plane
        """
        if normal.length == 0 : raise GeometricError("Cannot construct a plane with a normal vector of length zero: %s"%(normal))
        # super(Plane,self).__init__(point) Plane class used to override Vec class
        o = Vec(point)
        self.x = o.x
        self.y = o.y
        self.z = o.z
        self._vec = normal.normalized()

    @property
    def d(self):
        """
        The distance of this plane from the origin
        """
        from .dc_line import Line
        line = Line(self.origin, self._vec)
        t = line.near(Point())[1]
        tvec = self._vec*-t
        return tvec.length

    def __eq__(self, other):
        """Overloads the equal **(==)** operator for vector identity.
        
            :param other: Vec to be compared.
            :type other: Vec
            :result: Boolean result of comparison.
            :rtype: bool

        """    
        return self.is_identical(other)

    def __repr__(self): return "pln[{0},{1},{2},{3},{4},{5}]".format(self.x,self.y,self.z,self._vec.x,self._vec.y,self._vec.z)

    '''
    DEPRECIATED
    @property
    def vec(self): 
        """ Returns the plane's vector.

            :result: Plane's vector (Point).
            :rtype: Vec
        """
        return self._vec
    @vec.setter
    def vec(self, v): 
        """ Sets the plane's vector.

            :param v: Sets the vector of the plane (Point).
            :type v: Vec, point
            :result: Plane object.
            :rtype: Plane
        """
        self._vec = v.normalized()
    '''

    @property
    def normal(self): 
        """ Returns the plane's normal.

            :result: Plane's normal.
            :rtype: Vec
        """
        return self._vec
    @normal.setter
    def normal(self, v): 
        """ Sets the plane's normal.

            :param v: Sets the normal of the plane .
            :type v: Vec
            :result: Plane object.
            :rtype: Plane
        """
        self._vec = v.normalized()

    @property
    def origin(self): 
        """ Returns the plane's origin point.

            :result: Plane's origin point.
            :rtype: Point
        """
        return Point(self.x,self.y,self.z)
    @origin.setter
    def origin(self, pt): 
        """ Sets the plane's origin point.

            :param pt: Sets the origin point of the plane.
            :type pt: Point
            :result: Plane object.
            :rtype: Plane
        """
        self.x = pt.x
        self.y = pt.y
        self.z = pt.z
        

    def is_identical(self,other): 
        """Returns True if the planes are equal.
        
            :param other: Plane to be compared.
            :type other: Plane
            :result: Boolean result of comparison.
            :rtype: bool
        """   
        return all([self.x==other.x,self.y==other.y,self.z==other.z,self._vec.x==other._vec.x,self._vec.y==other._vec.y,self._vec.z==other._vec.z])

    def is_coplanar(self,other,tolerance=0.000001): 
        """Returns True if the planes are co-planar within a given tolerance.
        
            :param other: Plane to be compared.
            :type other: Plane
            :param tolerance: Tolerance of difference between the two planes.
            :type tolerance: float
            :result: Boolean result of comparison.
            :rtype: bool
        """   
        return all([self.near(other.origin)[0].distance(other.origin)<tolerance,self._vec.is_parallel(other._vec)])

    def near(self, p):
        """Returns a tuple of the closest point to a given Plane, its t value, and the distance from the given point to the near point.
       
            :param p: Point to look for a near point on the plane.
            :type p: Point
            :result: Tuple of near point on plane, t value and distance from given point to near point.
            :rtype: (Point, float, float)
        """
        from .dc_line import Line
        line = Line(self.origin, self._vec)
        t = line.near(p)[1]
        tvec = self._vec*-t
        point = p + tvec
        return (point,t,tvec.length) 

    def near_pt(self, p):
        """Returns the closest point to the point provided on a given Plane.
       
            :param p: Point to look for a near Point on the Plane.
            :type p: Point
            :result: Near point on Plane.
            :rtype: Point
        """
        return self.near(p)[0]

    @staticmethod
    def from_pts(pt_a,pt_b,pt_c):
        """Constructs plane from points. A plane cannot be constructed from collinear points.
            
            :param pt_a: First point.
            :type pt_a: Point
            :param pt_b: Second point.
            :type pt_b: Point
            :param pt_c: Third point.
            :type pt_c: Point
            :result: Plane object.
            :rtype: Plane
        """
        pt = Point.centroid([pt_a,pt_b,pt_c])
        try:
            nml = Vec(pt_a,pt_b).cross(Vec(pt_a,pt_c))
        except:
            raise GeometricError("Cannot create a Plane from collinear Points.")
        return Plane(pt,nml)