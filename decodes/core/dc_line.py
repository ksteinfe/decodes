from decodes.core import *

from . import dc_base, dc_interval, dc_color, dc_vec, dc_point #here we may only import modules that have been loaded before this one.  see core/__init__.py for proper order
if VERBOSE_FS: print "line.py loaded"

#from SYMPY
#http://code.google.com/p/sympy/source/browse/trunk.freezed/sympy/geometry/entity.py
#formerlly exteneded GeometryEntity
class LinearEntity(Geometry):
    """
    A linear entity (line, ray, segment, etc) in space.
    
    .. warning:: This is an abstract class and is not meant to be instantiated.

    """
    def __init__(self, a, b):
        """LinearEntity Constructor

            :param a: Starting point.
            :type a: Point
            :param b: Second point or Vector.
            :type b: Point or Vector
            :result: LinearEntity object.
            :rtype: LinearEntity
        """
        self._pt = a if isinstance(a,Point) else Point(a.x,a.y,a.z)
        if isinstance(b,Point) : self._vec = Vec(b-a)
        elif isinstance(b,Plane) : self._vec = Vec(b.origin-a)
        elif isinstance(b,Vec) : self._vec = b
        else : raise TypeError("Incorrect parameters provided to %s constructor" % self.__class__.__name__)
    
    @property
    def spt(self): 
        """Returns the starting Point of a LinearEntity

            :result: Starting Point.
            :rtype: Point
        """
        return self._pt
    @spt.setter
    def spt(self, point): 
        """Sets the starting Point of a LinearEntity

            :result: Sets a starting point.
        """
        self._pt = point
    @property
    def vec(self): 
        """Returns the Vec direction of a LinearEntity

            :result: Vector.
            :rtype: Vec
        """
        return self._vec
    @vec.setter
    def vec(self, vec):
        """Sets the Vec direction of a LinearEntity

            :result: Sets the Vec direction.
        """    
        self._vec = vec
    @property
    def ept(self): 
        """Returns the end Point of a LinearEntity

            :result: End Point.
            :rtype: Point
        """
        return self._pt+self._vec
    @ept.setter
    def ept(self, point): 
        """Sets the end Point of a LinearEntity

            :result: End Point.
        """
        self._vec = point-self._pt
    
    @property
    def coefficients(self):
        """The coefficients (a,b,c) of this line for equation ax+by+c=0"""
        raise NotImplementedError()
        return (self.p1[1]-self.p2[1],
                self.p2[0]-self.p1[0],
                self.p1[0]*self.p2[1] - self.p1[1]*self.p2[0])

    def is_concurrent(*lines):
        """
        Returns True if the set of linear entities are concurrent, False
        otherwise. Two or more linear entities are concurrent if they all
        intersect at a single point.

        .. note:: **Description of Method:**  First, take the first 
          two lines and find their intersection. If there is no intersection, 
          then the first two lines were parallel and had no intersection so 
          concurrenecy is impossible amongst the whole set. Otherwise, check 
          to see if the intersection point of the first two lines is a member 
          on the rest of the lines. If so, the lines are concurrent.
        
        .. todo:: Implement this method.
        """
        raise NotImplementedError()

    def is_parallel(l1, l2):
        """Returns True if l1 and l2 are parallel, False otherwise

            :param l1: First LinearEntity
            :type l1: LinearEntity
            :param l2: Second LinearEntity
            :type l2: LinearEntity
            :result: True if parallel.
            :rtype: bool
        
            .. todo:: Implement this method.
        """
        raise NotImplementedError()
        try:
            a1,b1,c1 = l1.coefficients
            a2,b2,c2 = l2.coefficients
            return bool(simplify(a1*b2 - b1*a2) == 0)
        except AttributeError:
            return False

    def is_perpendicular(l1, l2):
        """Returns True if l1 and l2 are perpendicular, False otherwise
           
            :param l1: First LinearEntity
            :type l1: LinearEntity
            :param l2: Second LinearEntity
            :type l2: LinearEntity
            :result: True if perpendicular.
            :rtype: bool
            
        .. todo:: Implement this method.
        """
        raise NotImplementedError()
        try:
            a1,b1,c1 = l1.coefficients
            a2,b2,c2 = l2.coefficients
            return bool(simplify(a1*a2 + b1*b2) == 0)
        except AttributeError:
            return False

    def angle_between(l1, l2):
        """
        Returns an angle formed between the two linear entities.

        .. note:: **Description of Method:**  
          From the dot product of vectors v1 and v2 it is known that::

              dot(v1, v2) = |v1|*|v2|*cos(A)

          where A is the angle formed between the two vectors. We can
          get the directional vectors of the two lines and readily
          find the angle between the two using the above formula.

        .. todo:: Implement this method.
        """
        #v1 = l1.p2 - l1.p1
        #v2 = l2.p2 - l2.p1
        #return Basic.acos( (v1[0]*v2[0]+v1[1]*v2[1]) / (abs(v1)*abs(v2)) )
        raise NotImplementedError()

    def parallel_line(self, p):
        """
        Returns a new Line which is parallel to this linear entity and passes through the specified point.
        
            :param p: Point that the LinearEntity will pass through.
            :type p: Point
            :result: New LinearEntity.
            :rtype: LinearEntity
        """
        return Line(p, self.vec)

    def perpendicular_line(self, p):
        """
        Returns a new Line which is perpendicular to this linear entity and passes through the specified point.

            :param p: Point that the LinearEntity will pass through.
            :type p: Point
            :result: New LinearEntity.
            :rtype: LinearEntity
            
        .. todo:: Implement this method.
        """
        raise NotImplementedError()

    def perpendicular_segment(self, p):
        """
        Returns a new Segment which connects p to a point on this linear entity and is also perpendicular to this line. Returns p itself if p is on this linear entity.

            :param p: Point that the LinearEntity will pass through.
            :type p: Point
            :result: New LinearEntity.
            :rtype: LinearEntity
            
        .. todo:: Implement this method.
        """
        raise NotImplementedError()

    def __eq__(self, other):  raise NotImplementedError()
    def __contains__(self, other):  raise NotImplementedError()

    def near(self, p):
        """Returns a tuple of the closest point to a given LinearEntity, its t value and the distance from the Point to the near Point.
       
            :param p: Point to look for a near Point on the LinearEntity.
            :type p: Point
            :result: Tuple of near point on LinearEntity, t value and distance from point to near point.
            :rtype: (Point, float, float)
        """
        t = Vec(self.spt,p).dot(self.vec)/self.vec.dot(self.vec)
        point = self.eval(t)
        return (point, t,point.distance(p))

    def near_pt(self, p):
        """Returns the closest point to a given LinearEntity
       
            :param p: Point to look for a near Point on the LinearEntity.
            :type p: Point
            :result: Near point on LinearEntity.
            :rtype: Point
        """
        return self.near(p)[0]
        
    def eval(self, t):
        """Evaluates a LinearEntity at a given number.
        
            :param t: Number between 0 and 1 to evaluate the LinearEntity at.
            :type t: float
            :result: Evaluated Point on LinearEntity.
            :rtype: Point
        """
        return self.spt+(self.vec.normalized(self.vec.length*t))

    

class Line(LinearEntity):
    """A line in space."""
    def __eq__(self, other):  raise NotImplementedError()
    def __contains__(self, other):  raise NotImplementedError()
    def __repr__(self): return "line[{0} {1}]".format(self._pt,self._vec)


class Ray(LinearEntity):
    """A ray in space."""
    def __eq__(self, other):  
        return self._pt == other._pt and self._vec.is_coincident(other._vec)

    def __contains__(self, other):  raise NotImplementedError()
    def __repr__(self): return "ray[{0} {1}]".format(self._pt,self._vec)
    
    def near(self,p):
        near = super(Ray,self).near(p)
        if near[1] < 0:
            near = (self.spt,0,p.distance(self.spt))
        return near
    

class Segment(LinearEntity):
    """A directed line segment in space."""
    def __eq__(self, other):  
        return self._pt == other._pt and self._vec == other._vec

    def __contains__(self, other):  raise NotImplementedError()
    def __repr__(self): return "seg[{0} {1}]".format(self.spt,self._vec)
    
    def near(self,p):
        near = super(Segment,self).near(p)
        if near[1] < 0:
            near = (self.spt,0.0,p.distance(self.spt))
        elif near[1] > 1:
            near = (self.ept,1.0,p.distance(self.ept))
        return near
        
        
    @property
    def length(self): 
      """Returns the length of this segment"""
      return self.vec.length        

    @property
    def midpoint(self): 
      """Returns the midpoint of this segment"""
      return Point.interpolate(self.spt, self.ept)

    def inverted(self):
        """Return a new Segment between the ept and spt of this Segment, but pointing in the opposite direction
        
            :result: Inverted vector.
            :rtype: Vec
        """ 
        return Segment(self.ept,self._vec.inverted())


class VecField(PixelGrid):
    """
    a raster grid of vectors
    each pixel contains a positioned 3d vector (a Ray)
    """
    def __init__(self, pixel_res=Interval(8,8), spatial_origin=Point(), spatial_dim=Interval(4,4), initial_value = Vec(),include_corners=False,wrap=True):
        self._res = Interval(int(pixel_res.a),int(pixel_res.b))
        self._pixels = [initial_value]*(self.px_width*self.px_height)
        self._sp_org = spatial_origin
        self._sp_dim = spatial_dim
        super(VecField,self).__init__(include_corners)

        self._sp_ival_x = Interval(self._sp_org.x - self._sp_dim.a/2, self._sp_org.x + self._sp_dim.a/2)
        self._sp_ival_y = Interval(self._sp_org.y - self._sp_dim.b/2, self._sp_org.y + self._sp_dim.b/2)
        self._base_pts = []
        for ival_y in self._sp_ival_y//pixel_res.b:
            for ival_x in self._sp_ival_x//pixel_res.a:
                self._base_pts.append(Point(ival_x.mid, ival_y.mid)) 

    def to_rays(self):
        return [Ray(pt,vec) for vec,pt in zip(self._pixels, self._base_pts )]

    def vec_near(self,sample_pt):
        x,y = self.address_near(sample_pt)
        return self.get(x,y)

    def address_near(self,sample_pt):
        x = min(1.0,max(0.0,self._sp_ival_x.deval(sample_pt.x)))
        y = min(1.0,max(0.0,self._sp_ival_y.deval(sample_pt.y)))

        x = int(math.floor(Interval(0,self.px_width).eval(x)))
        y = int(math.floor(Interval(0,self.px_height).eval(y)))
        if x == self.px_width : x = self.px_width-1
        if y == self.px_height : y = self.px_height-1
        return x,y