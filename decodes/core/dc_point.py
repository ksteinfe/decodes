from decodes.core import *
from . import dc_base, dc_vec #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
import math, random, warnings, copy
if VERBOSE_FS: print("point.py loaded")


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
            
            
            ::
            
                pt_a=Point()
                
                pt_b=Point(1,1)
                
                pt_c=Point(1,1,1)
                
                pts=[Point(i,i,i) for i in range(10)]
                
            
        """
        super(Point,self).__init__(a,b,c)
    
    def __mul__(self, other):
        """| Overloads the multiplication **(*)** operator.
           | If a transformation is provided, applies the transformation to this point in a way equivalent to the expression ``other * self``.
           | Otherwise, returns a new point that results from multiplying each of the point's coordinates by the value provided.
        
           :param other: Number to multiply Point by.
           :type other: float or Xform
           :result: New point
           :rtype: Point
           
           ::
           
                pt_a * 5
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
           
           ::
                
                pt_a + pt_b
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
           
           ::
           
                pt_a - pt_b
        """
        return Point(self.x-other.x , self.y-other.y, self.z-other.z)

    def __truediv__(self,other): return self.__div__(other)
    def __div__(self, other): 
        """| Overloads the division **(/)** operator
           | Returns a new point that results from dividing each of this point's world coordinates by the value provided.
           | No matter the basis of the inputs, the resulting point will have no basis.
        
           :param other: Number to divide Point by.
           :type other: float.
           :result: New point
           :rtype: Point
           
           ::
           
                pt_a / 5
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
            
            ::
            
                pt_a < pt_b
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
            
            ::
            
                pt_a.distance2(pt_b)
        """
        return Vec(self,other).length2

    def distance(self,other): 
        """ Returns the distance between this point and the other point in local space. Both points must use the same basis.
        
            :param other: Point to calculate the distance from
            :type other: Point
            :result: Distance between points
            :rtype: float
            
            ::
            
                pt_a.distance(pt_b)
        """
        return Vec(self,other).length
        
    def dist2(self,other): 
        """ Returns the distance squared between this point and the other point in local space. Both points must use the same basis.
        
            :param other: Point to calculate the distance from
            :type other: Point
            :result: Distance squared between points
            :rtype: float
            
            ::
            
                pt_a.distance2(pt_b)
        """
        return Vec(self,other).length2

    def dist(self,other): 
        """ Returns the distance between this point and the other point in local space. Both points must use the same basis.
        
            :param other: Point to calculate the distance from
            :type other: Point
            :result: Distance between points
            :rtype: float
            
            ::
            
                pt_a.distance(pt_b)
        """
        return Vec(self,other).length
        
        
    
    def projected(self, other): 
        """ Returns a new point projected onto a destination vector
        
            :param other: Destination vector
            :type other: Vec
            :result: A point projected onto a Vector
            :rtype: Point
            
            ::
            
                pt_a.projected(Vec(1,1,1))
        """
        return Point( Vec(self.x,self.y,self.z).projected(other) )

    @staticmethod
    def sorted_by_distance(pts,pt):
        return [tup[1] for tup in sorted( [(p.dist2(pt),p) for p in pts] )]
        
    @staticmethod
    def near(pt, pts):
        """ Returns a point from the given list of points which is nearest to the source point.

            :param pt: Source point
            :type pt: Point
            :param pts: A list of points through which to search
            :type pts: Point
            :result: A point from the list which is nearest to the source point
            :rtype: Point
            
            ::
            
                Point.near(pt_a,pts)
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
            
            ::
            
                Point.near_index(pt_a, pts)
                
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
            
            ::
            
                Point.far(pt_a, pts)
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
            
            ::
            
                Point.far_index(pt_a, pts)
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
            
            ::
            
                Point.interpolate(pt_a, pt_b)
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
            
            ::
            
                Point.centroid(pts)
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
            
            ::
            
                Point.random(Interval(0,10))
        """
        if interval is None:
            interval = Interval(-1.0,1.0)
        x = random.uniform(interval.a,interval.b)
        y = random.uniform(interval.a,interval.b)
        z = random.uniform(interval.a,interval.b)
        p = Point(x,y) if constrain2d else Point(x,y,z)
        return p
        
    @staticmethod
    def cull_duplicates(pts, threshold = EPSILON):
        """ Discards duplicate points from a list of points.
        
            :param pts: A list of points
            :type pts: list
            :param threshold: Tolerance of difference between points
            :type threshold: float
            :result: List of points without duplicates
            :rtype: List
            
            ::
            
                Point.cull_duplicates(pts)
        """
        if len(pts)==0: return pts
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




