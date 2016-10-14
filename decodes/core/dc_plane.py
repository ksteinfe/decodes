from decodes.core import *
from . import dc_base, dc_vec, dc_point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print("plane.py loaded")
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
            
            ::
            
                pln_1=Plane(Point(0,0,0), Vec(1,1,1))
                
                pln_2=Plane(Point(0,0,0), Point(0,1,1), Point(1,0,1))
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
        """ The distance of this plane from the origin.
            
            :result: Distance from origin.
            :rtype: float
            
            ::
                
                pln_1.d
        
        
        """
        from .dc_line import Line
        line = Line(self.origin, self._vec)
        t = line.near(Point())[1]
        tvec = self._vec*-t
        return tvec.length

    def __eq__(self, other):
        """ Overloads the equal **(==)** operator for Plane identity.
        
            :param other: Plane to be compared.
            :type other: Plane
            :result: Boolean result of comparison.
            :rtype: bool

        """    
        return self.is_equal(other)

    def __repr__(self): return "pln[{0},{1},{2},{3},{4},{5}]".format(self.x,self.y,self.z,self._vec.x,self._vec.y,self._vec.z)

    @property
    def normal(self): 
        """ Returns the plane's normal.

            :result: Plane's normal.
            :rtype: Vec
            
            ::
            
                pln_1.normal
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
            
            ::
            
                pln_1.origin
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
        self.x, self.y, self.z = point.tup
        
    @property
    def pt(self): 
        """ Returns the plane's origin point.

            :result: Plane's origin point.
            :rtype: Point
            
            ::
            
                pln_1.origin
        """
        return Point(self.x,self.y,self.z)
    @pt.setter
    def pt(self, point): 
        """ Sets the plane's origin point.

            :param pt: Sets the origin point of the plane.
            :type pt: Point
            :result: Plane object.
            :rtype: Plane
        """
        self.x, self.y, self.z = point.tup

    def is_equal(self,other,pt_tol=None, vec_tol=None):
        """ Returns True if the given Plane shares a reference Point and normal direction with this Plane
        
            :param other: Plane to be compared.
            :type other: Plane
            :param pos_tol: Tolerance of point projection distance.
            :type pos_tol: float               
            :param vec_tol: Tolerance of vector direction difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.
            :type vec_tol: float
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_pln.is_equal(other_pln)
        """
        return self.origin.is_equal(other.origin,pt_tol) and self.normal.is_coincident(other.normal,vec_tol)

    def is_coincident(self,other,pt_tol=None, vec_tol=None):
        """ Returns True if the given Plane shares any contained Point, and if the two normal directions are coincident
        
            :param other: Plane to be compared.
            :type other: Plane
            :param pos_tol: Tolerance of point projection distance.
            :type pos_tol: float               
            :param vec_tol: Tolerance of vector direction difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.
            :type vec_tol: float          
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_pln.is_coincident(other_pln)
        """   
        if self.normal.is_coincident(other.normal,vec_tol): 
            if pt_tol is None: pt_tol = EPSILON
            if self.near(other.origin)[2] <= pt_tol and other.near(self.origin)[2] <= pt_tol: return True
        return False
        
    def is_coplanar(self,other,pt_tol=None, vec_tol=None):
        """ Returns True if the given Plane shares any contained Point, and if the two normal directions are parallel
        
            :param other: Plane to be compared.
            :type other: Plane
            :param pos_tol: Tolerance of point projection distance.
            :type pos_tol: float               
            :param vec_tol: Tolerance of vector direction difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.
            :type vec_tol: float          
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_pln.is_coplanar(other_pln)
        """   
        if self.normal.is_parallel(other.normal,vec_tol): 
            if pt_tol is None: pt_tol = EPSILON
            if self.near(other.origin)[2] <= pt_tol and other.near(self.origin)[2] <= pt_tol: return True
        return False        

    def is_parallel(self,other, vec_tol=None):
        """ Returns True if the normal directions of this Plane and the given Plane are parallel

            :param other: Plane to be compared.
            :type other: Plane
            :param vec_tol: Tolerance of vector direction difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.
            :type vec_tol: float          
            :result: Boolean result of comparison.
            :rtype: bool
        
            
        """
        return self.normal.is_parallel(other.normal,vec_tol)
    
    def is_perpendicular(self,other, vec_tol=None):
        """ Returns True if the normal directions of this Plane and the given Plane are perpendicular
           
            :param other: Plane to be compared.
            :type other: Plane
            :param vec_tol: Tolerance of vector direction difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.
            :type vec_tol: float          
            :result: Boolean result of comparison.
            :rtype: bool
                     
        """
        return self.normal.is_perpendicular(other.normal,vec_tol)
        
        
    def near(self, p):
        """ Returns a tuple of the closest point to a given Plane, its t value, and the distance from the given point to the near point.
       
            :param p: Point to look for a near point on the plane.
            :type p: Point
            :result: Tuple of near point on plane, t value and distance from given point to near point.
            :rtype: (Point, float, float)
            
            ::
                
                pln_1.near(Point(1,1,1))
        """
        from .dc_line import Line
        line = Line(self.origin, self._vec)
        t = line.near(p)[1]
        tvec = self._vec*-t
        point = p + tvec
        return (point,t,tvec.length)

    def near_pt(self, p):
        """ Returns the closest point to the point provided on a given Plane.
       
            :param p: Point to look for a near Point on the Plane.
            :type p: Point
            :result: Near point on Plane.
            :rtype: Point
        """
        return self.near(p)[0]
        
    def contains(self,pt,tol=None):
        """ Returns True if the given Point lines in the Plane within a given tolerance

            :param other: Point to be appraised.
            :type other: Point             
            :param tol: Tolerance of point projection.
            :type tol: float
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_plane.contains(pt)
        """
        if tol is None: tol = EPSILON
        if self.near(pt)[2] < tol: return True
        return False    
 

    def to_cs(self, guide_vec):
        """ Returns a CS aligned with this Plane, with the x-axis oriented toward the given guide Vec.
       
            :param guide_vec: Vec that guides the orientation of the x-axis of the resulting CS.
            :type p: Vec
        """
        from .dc_cs import CS
        y_vec = self.normal.cross(guide_vec)
        x_vec = self.normal.cross(y_vec).inverted()
        return CS(self.origin, x_vec, y_vec)
        
        
    @staticmethod
    def from_pts(a,b=None,c=None):
        """ Constructs plane from points. A plane cannot be constructed from collinear points.
            
            :param pt_a: First point.
            :type pt_a: Point
            :param pt_b: Second point.
            :type pt_b: Point
            :param pt_c: Third point.
            :type pt_c: Point
            :result: Plane object.
            :rtype: Plane
            
            ::
            
                pln_2=Plane(Point(0,0,0), Point(0,1,1), Point(1,0,1))
        """
        pt_a, pt_b, pt_c = a,b,c
        if b is None and c is None:
            pt_a, pt_b, pt_c = a[0],a[1],a[2]
        
        pt = Point.centroid([pt_a,pt_b,pt_c])
        try:
            nml = Vec(pt_a,pt_b).cross(Vec(pt_a,pt_c))
        except:
            raise GeometricError("Cannot create a Plane from collinear Points.")
        return Plane(pt,nml)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        