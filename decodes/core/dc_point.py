from decodes.core import *
from . import dc_base, dc_vec #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
import math, random, warnings, copy
if VERBOSE_FS: print "point.py loaded"


# points may define a "basis"
# interpreted as any object that may be "evaluated" (passed three coords) and return a position in R3
# if no basis is defined for a point, R3 is assumed
# the _x,_y, and _z properties of a point return values in "basis space" (unevaluated by basis)
# the x,y,and z properties of a point return values in "world space" (evaluated by basis)
# if no basis has been defined, these values are the same

class Point(Vec):
    """
    a simple point class
    """
    
    def __init__(self, a=0, b=0, c=0):
        """ Point Constructor.

            :param a: a value
            :type a: float
            :param b: b value
            :type b: float
            :param c: c value
            :type c: float
            :result: Point object
            :rtype: Point
        """
        super(Point,self).__init__(a,b,c)
    
    def __mul__(self, other):
        """| Overloads the multiplication **(*)** operator.
           | If a transformation is provided, applies the transformation to this point in a way equivalent to the expression ``other * self``.
           | Otherwise, returns a new point that results from multiplying each of the point's coordinates by the value provided.
        
           :param other: Point or Vec to be multiplied
           :type other: Point or Vec
           :result: New point
           :rtype: Point
        """
        from .dc_xform import Xform
        if isinstance(other, Xform) : return other*self
        else : 
            return Point(self.x * other, self.y * other, self.z * other)

    def __add__(self, other): 
        """| Overloads the addition **(+)** operator. 
           | Returns a new point that results from adding this point's world coordinates to the other point's (or vector's) world coordinates.
           | No matter the basis of the inputs, the resulting point will have no basis.
        
           :param other: Point or Vec to be added
           :type other: Point or Vec
           :result: New point.
           :rtype: Point
        """
        return Point(self.x+other.x , self.y+other.y, self.z+other.z)
    
    def __sub__(self, other): 
        """| Overloads the subtraction **(-)** operator
           | Returns a new point that results from subtracting the other point's (or vector's) world coordinates from this point's world coordinates.
           | No matter the basis of the inputs, the resulting point will have no basis.

           :param other: Point or Vec to be subtracted
           :type other: Point or Vec
           :result: New point.
           :rtype: Point
        """
        return Point(self.x-other.x , self.y-other.y, self.z-other.z)

    def __truediv__(self,other): return self.__div__(other)
    def __div__(self, other): 
        """| Overloads the division **(/)** operator
           | Returns a new point that results from dividing each of this point's world coordinates by the value provided.
           | No matter the basis of the inputs, the resulting point will have no basis.
        
           :param other: Point or Vec to be divided
           :type other: Point or Vec
           :result: New point
           :rtype: Point
        """
        return Point(self.x/float(other), self.y/float(other), self.z/float(other))

    def __repr__(self):
        return "pt[{0},{1},{2}]".format(self.x,self.y,self.z)

    def __lt__(self, other):
        """ Overloads the less than **(<)** operator.
        
            :param other: Point to be compared
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        try:
            if self.z < other.z : return True
            if self.z == other.z and self.y < other.y : return True
            if self.z == other.z and self.y == other.y and self.x < other.x : return True
            return False
        except:
            return False
        
    def __gt__(self, other): 
        """ Overloads the greater than **(>)** operator.
        
            :param other: Point to be compared
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        try:
            if self.z > other.z : return True
            if self.z == other.z and self.y > other.y : return True
            if self.z == other.z and self.y == other.y and self.x > other.x : return True
            return False
        except:
            return False

    def __le__(self, other): 
        """ Overloads the less than or equal to **(<=)** operator.
        
            :param other: Point to be compared
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        return True if (self < other or self == other) else False
        
    def __eq__(self, other): 
        """ Overloads the equal **(==)** operator.
        
            :param other: Point to be compared
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        try:
            return all([self.x==other.x,self.y==other.y,self.z==other.z])
        except:
            return False

    def __ne__(self, other): 
        """ Overloads the not equal **(!=)** operator.
        
            :param other: Point to be compared
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        try:
            return not all([self.x==other.x,self.y==other.y,self.z==other.z])
        except:
            return False

    def __ge__(self, other): 
        """ Overloads the greater than or equal to **(>=)** operator.
        
            :param other: Point to be compared
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        return True if (self > other or self == other) else False 
    
    def distance2(self,other): 
        """ Returns the distance squared between this point and the other point in local space. Both points must use the same basis.
        
            :param other: Point to calculate the distance from
            :type other: Point
            :result: Distance squared between points
            :rtype: float
        """
        return Vec(self,other).length2

    def distance(self,other): 
        """ Returns the distance between this point and the other point in local space. Both points must use the same basis.
        
            :param other: Point to calculate the distance from
            :type other: Point
            :result: Distance between points
            :rtype: float
        """
        return Vec(self,other).length
    
    def projected(self, other): 
        """ Returns a new point projected onto a destination vector
        
            :param other: Destination vector
            :type other: Vec
            :result: A point projected onto a Vector
            :rtype: Point
        """
        return Point( Vec(self.x,self.y,self.z).projected(other) )

    @staticmethod
    def near(pt, pts):
        """ Returns a point from the given list of points which is nearest to the source point.

            :param pt: Source point
            :type pt: Point
            :param pts: A list of points through which to search
            :type pts: Point
            :result: A point from the list which is nearest to the source point
            :rtype: Point
        """
        return pts[Point.near_index(pt,pts)]

    @staticmethod
    def near_index(pt, pts):
        """ Returns the index of the point within the given list of points which is nearest to the source point.

            :param pt: Source point
            :type pt: Point
            :param pts: A list of points through which to search
            :type pts: Point
            :result: The index of the nearest point
            :rtype: int
        """
        dists = [pt.distance2(p) for p in pts]
        return dists.index(min(dists))

    @staticmethod
    def far(pt, pts):
        """ Returns a point from the given list of points which is furthest from the source point.

            :param pt: Source point
            :type pt: Point
            :param pts: A list of points through which to search
            :type pts: Point
            :result: A point from the list which is furthest from the source point
            :rtype: Point
        """
        return pts[Point.far_index(pt,pts)]

    @staticmethod
    def far_index(pt, pts):
        """ Returns the index of the point within the given list of points which is furthest from the source point.

            :param pt: Source point
            :type pt: Point
            :param pts: A list of points through which to search
            :type pts: Point
            :result: The index of the furthest point
            :rtype: int
        """
        dists = [pt.distance2(p) for p in pts]
        return dists.index(max(dists))

    @staticmethod
    def interpolate(p0,p1,t=0.5): 
        """ Returns a new point which is the result of an interpolation between the two given points at the given t-value.
        
            :param p0: First point to interpolate
            :type p0: Point
            :param p1: Second point to interpolate
            :type p1: Point
            :param t: t-value of interpolation
            :type t: float
            :result: Interpolated point
            :rtype: Point
        """
        v = Vec.interpolate(p0,p1,t)
        return Point(v.x,v.y,v.z)
        
    @staticmethod
    def centroid(points): 
        """ Returns the centroid of a point cloud.
        
            :param points: Point cloud
            :type points: [Point]
            :result: Centroid of point cloud.
            :rtype: Point
        """
        return Point( Vec.average(points) )
    
    @staticmethod
    def random(interval=None,constrain2d=False):
        """ Returns a random point within the given (optional) range.
        
            :param interval: Range to get the random value from.
            :type interval: Interval
            :param constrain2d: Constrain the point to 2d space.
            :type constrain2d: bool
            :result: Random point
            :rtype: Point
        """
        if interval is None:
            interval = Interval(-1.0,1.0)
        x = random.uniform(interval.a,interval.b)
        y = random.uniform(interval.a,interval.b)
        z = random.uniform(interval.a,interval.b)
        p = Point(x,y) if constrain2d else Point(x,y,z)
        return p
        
    @staticmethod
    def cull_duplicates(pts, threshold = None):
        """ Discards duplicate points from a list of points.
        
            :param pts: A list of points
            :type pts: list
            :param threshold: Tolerance of difference between points
            :type threshold: float
            :result: List of points without duplicates
            :rtype: List
        """
        if threshold == None:
            culled_pts = []
            for pt in pts: 
                if not (pt in culled_pts) : culled_pts.append(pt)
            return culled_pts
        else:
            culled_pts = [pts[0]]
            for pt in pts:
                is_good = True
                for cpt in culled_pts:
                    if pt.distance2(cpt) < threshold**2 : 
                        is_good = False
                        break
                if is_good: culled_pts.append(pt)
            return culled_pts


class BPoint(Point,HasBasis):
    """
    A based point class
    """
    
    def __init__(self, a=0, b=0, c=0, basis=None):
        """ BPoint Constructor.

            :param a: a value
            :type a: float
            :param b: b value
            :type b: float
            :param c: c value
            :type c: float
            :result: Point object
            :rtype: Point
        """
        super(BPoint,self).__init__(a,b,c)
        self.basis = basis

        # there's a unique case where we've been passed a based point along with a defined basis here.
        # in this case, we should take the local coordinates of the given point interpreted through the given basis
        if isinstance(a, Point) and b==0 and c == 0 and basis !=None :  self._x , self._y, self._z = a._x , a._y, a._z

    @property
    def x(self): 
        """ The x-coordinate of this point. Setting the x-value of a point with a basis requires stripping the basis of the point. Set pt._x to alter the local coordinate instead.

            :result: x value
            :rtype: float
        """
        return self.basis.eval(self.basis_stripped()).x if not self.is_baseless else self._x
    @x.setter
    def x(self,value): 
        if self.is_baseless :
            self._x = value
        else: 
            npt = self.basis_applied()
            self.basis = None
            self.x,self.y,self.z =    npt._x, value, npt._z
    
    @property
    def y(self): 
        """ The y-coordinate of this point. Setting the y-value of a point with a basis requires stripping the basis of the point. Set pt._y to alter the local coordinate instead.
        
            :result: y value
            :rtype: float
        """    
        return self.basis.eval(self.basis_stripped()).y if not self.is_baseless else self._y
    @y.setter
    def y(self,value): 
        if self.is_baseless :
            self._y = value
        else: 
            npt = self.basis_applied()
            self.basis = None
            self.x,self.y,self.z = value, npt._y, npt._z
    
    @property
    def z(self): 
        """ The z-coordinate of this point. Setting the z-value of a point with a basis requires stripping the basis of the point. Set pt._z to alter the local coordinate instead.
        
            :result: z value
            :rtype: float
        """
        return self.basis.eval(self.basis_stripped()).z if not self.is_baseless else self._z
    @z.setter
    def z(self,value): 
        if self.is_baseless :
            self._z = value
        else: 
            npt = self.basis_applied()
            self.basis = None
            self.x,self.y,self.z = npt._x, npt._y, value


    

    def basis_applied(self, copy_children=True): 
        """ Returns a new point with basis applied. Coordinates will be interpreted in world space. Points will appear in the same position when drawn.
        
            :param copy_children: If True, creates a new point object with 'world' coordinates
            :type copy_children: bool
            :result: Point object with basis applied
            :rtype: Point
        """
        pt = Point(self.x,self.y,self.z)
        if hasattr(self, 'props') : pt.props = self.props
        return pt
    
    def basis_stripped(self, copy_children=True): 
        """ Returns a new point stripped of any bases. Coordinates will be interpreted in world space, and points will appear in their 'local' position when drawn.
        
            :param copy_children: If True, creates a new point object with 'local' coordinates
            :type copy_children: bool
            :result: Point object with basis stripped
            :rtype: Point
        """
        pt = Point(self._x,self._y,self._z)
        if hasattr(self, 'props') : pt.props = self.props
        return pt
    
    def set_basis(self,basis): 
        """ Returns a new point whose local coordinates are the same as this point, but whose basis is set by the basis provided.
        
            :param basis: New basis for the point
            :type basis: Basis
            :result: Point object with new basis
            :rtype: Point
        """
        return Point(self._x,self._y,self._z,basis=basis)

    def __repr__(self):
        #TODO: provide mechanism to print basis info if desired
        #if not self.is_baseless : return "pt[{0},{1},{2}] basis: {3}".format(self._x,self._y,self._z,self.basis)
        if not self.is_baseless : return "wpt[{0},{1},{2}]".format(self.x,self.y,self.z)
        return "pt[{0},{1},{2}]".format(self.x,self.y,self.z)

    def _distance2(self, other):
        """ Distance squared in local space. Cheaper to calculate than distance. Both points must use the same basis.
        
            :param other: Point to calculate the distance from
            :type other: Point
            :result: Distance squared between points
            :rtype: float
        """
        
        if self.basis is not other.basis : raise BasisError("Cannot measure '_distance2' between points with different bases.    Use 'distance2' instead")
        return Vec(self,other).length2

    def _distance(self, other): 
        """ Returns the distance between this point and the other point in local space. Both points must use the same basis.
        
            :param other: Point to calculate the distance from
            :type other: Point
            :result: Distance between points
            :rtype: float
        """
        if self.basis is not other.basis : raise BasisError("Cannot measure '_distance' between points with different bases.    Use 'distance' instead")
        return Vec(self,other).length
    
    def distance2(self,other): 
        """ Returns the distance between this point and the other point in local space.
        
            :param other: Point to calculate the distance from
            :type other: Point
            :result: Distance squared between points
            :rtype: float
        """
        return Vec(self.basis_applied(),other.basis_applied()).length2

    def distance(self,other): 
        """ Returns the distance between this point and the other point in local space.
        
            :param other: Point to calculate the distance from
            :type other: Point
            :result: Distance between points
            :rtype: float
        """
        return Vec(self.basis_applied(),other.basis_applied()).length


    @staticmethod
    def interpolate(p0,p1,t=0.5): 
        """ Returns a new point which is the result of an interpolation between the two given points at the given t-value
        
            :param p0: First point to interpolate
            :type p0: Point
            :param p1: Second point to interpolate
            :type p1: Point
            :param t: t-value of interpolation
            :type t: float
            :result: Interpolated point
            :rtype: Point
        """
        #TODO this method used to maintain basis for same-based points, but this seemed to fuck things up in the rgon.inflate method.
        #if p0.basis is p1.basis : 
        if False : 
            v = Vec.interpolate(p0,p1,t)
            return Point(v.x,v.y,v.z,p0.basis)
        else : 
            v = Vec.interpolate(p0.basis_applied(),p1.basis_applied(),t)
            return Point(v.x,v.y,v.z)

    @staticmethod
    def _centroid(points): 
        """ Returns the centroid of a point cloud in local coordinates. All given points will be evaluated with their bases stripped, and the basis of the returned point will adopt the basis of the given points. Mixed bases among the given points will throw an error.

            :param points: Point cloud
            :type points: list
            :result: Centroid of point cloud
            :rtype: Point
        """
        if all( points[0].basis is p.basis for p in points ) : 
            cent = Vec.average([p.basis_stripped() for p in points])
            return Point(cent).set_basis(points[0].basis)
        raise BasisError("Cannot calculate '_centroid' for points of mixed bases.    Use 'centroid' instead")







