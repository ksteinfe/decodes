from decodes.core import *

from . import dc_base, dc_interval, dc_color, dc_vec, dc_point #here we may only import modules that have been loaded before this one.  see core/__init__.py for proper order
if VERBOSE_FS: print("line.py loaded")

#from SYMPY
#http://code.google.com/p/sympy/source/browse/trunk.freezed/sympy/geometry/entity.py
#formerlly exteneded GeometryEntity
class LinearEntity(Geometry):
    """
    A linear entity (line, ray, segment, etc) in space.
    
    .. warning:: This is an abstract class and is not meant to be instantiated.

    """
    def __init__(self, a, b):
        """LinearEntity Constructor.

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
    
    def __add__(self, other): 
        """| Overloads the addition **(+)** operator. 
           | Adds the given vector to LinearEntity._pt, effectively translating this LinearEntity.
        
           :param other: Vec to be added.
           :type other: Vec
           :result: LinearEntity
           :rtype: LinearEntity
        """
        self._pt = self._pt + other
        return self
    
    def __mul__(self, other):
        """| Overloads the multiplication **(*)** operator. 
           | If given a scalar, transforms this LinearEntity by multiplying the vector of this LinearEntity by the scalar, and returns this LinearEntity
        
           :param other: Scalar to be multiplied.
           :type other: float
           :result: This LinearEntity
           :rtype: LinearEntity
           
           ::
           
                my_le * float
        """  
        from .dc_xform import Xform
        if isinstance(other, Xform) : return other * self
        else :        
            self._vec *= other
            return self
    
    def __eq__(self, other):
        """| Overloads the equality **(==)** operator. 
           | Calls the is_equal method
           
           ::
           
                my_le == other_le
        """  
        return self.is_equal(other)
    
    def __contains__(self, other):
        """ Overloads the containment **(in)** operator
        
            :param number: Point whose containment must be determined.
            :type number: Point
            :result: Boolean result of containment.
            :rtype: bool
            
        """
        return self.contains(other)
    
    @property
    def spt(self): 
        """ Returns the starting Point of a LinearEntity.

            :result: Starting Point.
            :rtype: Point
        """
        return self._pt
    @spt.setter
    def spt(self, point): 
        """ Sets the starting Point of a LinearEntity.

            :param point: Starting Point.
            :type point: Point
            :result: Sets a starting point.
            :rtype: None
        """
        self._pt = point  
    @property
    def vec(self): 
        """ Returns the Vec direction of a LinearEntity.

            :result: Vector.
            :rtype: Vec
        """
        return self._vec
    @vec.setter
    def vec(self, vec):
        """ Sets the Vec direction of a LinearEntity.

            :param vec: New Vec direction.
            :type vec:Vec
            :result: Sets the Vec direction.
            :rtype: None
        """    
        self._vec = vec

    
    @property
    def coefficients(self):
        """ Returns the coefficients (a,b,c) of this line for equation ax+by+c=0
        
            :result: coefficients of the equation of a line (a,b,c).
            :rtype: tuple
        
            .. warning:: This method is not yet implemented.
        """
        raise NotImplementedError()
        return (self.p1[1]-self.p2[1],
                self.p2[0]-self.p1[0],
                self.p1[0]*self.p2[1] - self.p1[1]*self.p2[0])
    
    def is_equal(self, other):  raise NotImplementedError()
    def is_identical(self,other): return self.is_coincident(other)
    def is_coincident(self, other):  raise NotImplementedError()
    
    def is_parallel(self,other,tol=None):
        """ Returns True if the LinearEntities contain vectors with equal or opposite direction within a given tolerance.

            :param other: LinearEntity to be compared.
            :type other: LinearEntity
            :param tol: Tolerance of difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.
            :type tol: float              
            :result: Boolean result of comparison.
            :rtype: bool
        
            
        """
        return self.vec.is_parallel(other.vec,tol)

    def is_perpendicular(self,other, tol=None):
        """ Returns True if the LinearEntities contain vectors with perpendicular to one another within a given tolerance.
           
            :param other: LinearEntity to be compared.
            :type other: LinearEntity
            :param tol: Tolerance of vector direction difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.
            :type tol: float              
            :result: Boolean result of comparison.
            :rtype: bool
                     
        """
        if self.vec.is_perpendicular(other.vec,tol):
            la = Line(self.spt, self.vec)
            lb = Line(other.spt, other.vec)
            from .dc_intersection import Intersector
            xsec = Intersector()
            if xsec.of(la,lb): return True
        return False
        
    def is_collinear(self,other, pos_tol=None, ang_tol=None):
        """ Returns True if the LinearEntities are parallel within a given tolerance ang_tol, and lie on the same line within another tolerance pos_tol.
           
            :param other: LinearEntity to be compared.
            :type other: LinearEntity
            :param pos_tol: Tolerance of point projection distance.
            :type pos_tol: float               
            :param ang_tol: Tolerance of vector direction difference 
            :type ang_tol: float              
            :result: Boolean result of comparison.
            :rtype: bool
                     
        """
        if self.vec.is_parallel(other.vec,ang_tol):
            if pos_tol is None: pos_tol = EPSILON
            la, lb = Line(self.spt, self.vec), Line(other.spt, other.vec)
            if la.near(other.spt)[2] <= pos_tol and lb.near(self.spt)[2] <= pos_tol : return True
        return False
        
    def is_coplanar(self,other, tol=None):
        """ Returns True if the LinearEntities lie on the same plane within a given tolerance tol
           
            :param other: LinearEntity to be compared.
            :type other: LinearEntity
            :param tol: Tolerance of vector direction difference
            :type tol: float  
            :result: Boolean result of comparison.
            :rtype: bool
                     
        """
        p0,p1 = self.spt,self.spt+self.vec
        q0,q1 = other.spt, other.spt+other.vec
        n_vec = Vec(q0,p1).cross(Vec(q0,p0))
        if tol is None: tol = EPSILON
        if n_vec.dot(Vec(q0,q1)) < tol: return True
        return False
 
    
    def contains(self,pt,tol=None):
        """ Returns True if the given Point lines along this Segment within a given tolerance

            :param other: Point to be appraised.
            :type other: Point             
            :param tol: Tolerance of point projection.
            :type tol: float
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_seg.contains(pt)
        """
        if tol is None: tol = EPSILON
        if self.near(pt)[2] < tol: return True
        return False
 

    def angle(self, other):
        """ Returns an angle formed between the two linear entities.
        
            :param other: Other LinearEntity
            :type other: LinearEntity
            :result: Angle in radians.
            :rtype: float      
       """
        return self.vec.angle(other.vec)

    def parallel_line_through(self, p):
        """ Returns a new Line which is parallel to this linear entity and passes through the specified point.
        
            :param p: Point that the LinearEntity will pass through.
            :type p: Point
            :result: New LinearEntity.
            :rtype: LinearEntity
        """
        return Line(p, self.vec)

    def near(self, p):
        """ Returns a tuple of the closest point to a given LinearEntity, its t value and the distance from the Point to the near Point.
       
            :param p: Point to look for a near Point on the LinearEntity.
            :type p: Point
            :result: Tuple of near point on LinearEntity, t value and distance from point to near point.
            :rtype: (Point, float, float)
        """
        t = Vec(self.spt,p).dot(self.vec)/self.vec.dot(self.vec)
        point = self.eval(t)
        return (point, t,point.distance(p))

    def near_pt(self, p):
        """ Returns the closest point to a given LinearEntity
       
            :param p: Point to look for a near Point on the LinearEntity.
            :type p: Point
            :result: Near point on LinearEntity.
            :rtype: Point
        """
        return self.near(p)[0]
        
    def eval(self, t):
        """ Evaluates a LinearEntity at a given number.
        
            :param t: Number between 0 and 1 to evaluate the LinearEntity at.
            :type t: float
            :result: Evaluated Point on LinearEntity.
            :rtype: Point
        """
        return self.spt + (self.vec * t)

    def to_line(self):
        return Line(self.spt,self.vec)

class Line(LinearEntity):
    """A line in space."""
    def __repr__(self): return "line[{0} {1}]".format(self._pt,self._vec)
    @property
    def pt(self): 
        """ Returns the reference Point of a Line.

            :result: the reference Point.
            :rtype: Point
        """
        return self._pt
    @pt.setter
    def pt(self, point): 
        """ Sets the reference Point of a Line.

            :param point: the the reference Point.
            :type point: Point
            :result: Sets a reference point.
            :rtype: None
        """
        self._pt = point
        
    def is_equal(self,other,pt_tol=None, vec_tol=None):
        """ Returns True if the given Line shares the Point and coincident directions with this Line
        
            :param other: Line to be compared.
            :type other: Line
            :param pos_tol: Tolerance of point distance.
            :type pos_tol: float               
            :param vec_tol: Tolerance of vector direction difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.
            :type vec_tol: float
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_line.is_equal(other_line)
        """
        return self.pt.is_equal(other.pt,pt_tol) and self.vec.is_coincident(other.vec,vec_tol)

    def is_coincident(self,other,pt_tol=None, vec_tol=None):
        """ Returns True if the Lines share any Point along their length and have parallel direction Vecs. Equivalent to LinearEntity.is_colinear()
        
            :param other: Line to be compared.
            :type other: Line
            :param pos_tol: Tolerance of point distance.
            :type pos_tol: float               
            :param vec_tol: Tolerance of vector direction difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.          
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_line.is_coincident(other_line)
        """
        return self.is_collinear(other,pt_tol, vec_tol) and self.vec.is_coincident(other.vec,vec_tol)
        

class Ray(LinearEntity):
    """A ray in space."""
    def __repr__(self): return "ray[{0} {1}]".format(self._pt,self._vec)
    
    def is_coincident(self,other,pt_tol=None, vec_tol=None):
        """ Returns True if the given Ray shares a start Point and normalized direction vector with this Ray. Equivalent to Ray.is_equal()
        
            :param other: Ray to be compared.
            :type other: Ray
            :param pos_tol: Tolerance of point projection distance.
            :type pos_tol: float               
            :param vec_tol: Tolerance of vector direction difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.
            :type vec_tol: float
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_ray.is_equal(other_ray)
        """    
        return self.is_equal(other,pt_tol, vec_tol)    
        
    def is_equal(self,other,pt_tol=None, vec_tol=None):
        """ Returns True if the given Ray shares a start Point and normalized direction vector with this Ray
        
            :param other: Ray to be compared.
            :type other: Ray
            :param pos_tol: Tolerance of point projection distance.
            :type pos_tol: float               
            :param vec_tol: Tolerance of vector direction difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.
            :type vec_tol: float
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_ray.is_equal(other_ray)
        """
        return self.spt.is_equal(other.spt,pt_tol) and self.vec.is_coincident(other.vec,vec_tol)
    
    def near(self,p):
        """ Returns a tuple of the closest point to a given Ray, its t value and the distance from the Point to the near Point.
       
            :param p: Point to look for a near Point on the Ray.
            :type p: Point
            :result: Tuple of near point on Ray, t value and distance from point to near point.
            :rtype: (Point, float, float)
        """
        near = super(Ray,self).near(p)
        if near[1] < 0:
            near = (self.spt,0,p.distance(self.spt))
        return near
    

class Segment(LinearEntity):
    """A directed line segment in space."""

    def __truediv__(self,divs): return self.__div__(divs)
    def __div__(self, divs): 
        """ Overloads the division **(/)** operator. Calls Segment.divide(divs).
        
           :param divs: Number of divisions.
           :type divs: int        
           :result: List of Points equally spaced along this Segment
           :rtype: list
        """
        return self.divide(divs)

    def __floordiv__(self, divs): 
        """ Overloads the integer division **(//)** operator. Calls Segment.subinterval(divs).
            
            :param divs: Number of subsegments.
            :type divs: int
            :result: List of smaller Segments. 
            :rtype: list
            
        """
        return self.subsegment(divs)
        
    
    def __repr__(self): return "seg[{0} {1}]".format(self.spt,self._vec)
       
    @property
    def ept(self): 
        """ Returns the end Point of a LinearEntity.

            :result: End Point.
            :rtype: Point
        """
        return self._pt+self._vec
    @ept.setter
    def ept(self, point): 
        """ Sets the end Point of a LinearEntity.

            :param point: End Point.
            :type point: Point
            :result: End Point.
            :rtype: None
        """
        self._vec = point-self._pt    
    
    @property
    def length(self): 
      """ Returns the length of this segment.
            
            :result: Length of line segment.
            :rtype: float
      
      """
      return self.vec.length        

    @property
    def midpoint(self): 
      """ Returns the midpoint of this segment
      
            :result: Midpoint of Segment.
            :rtype: Point
      
      """
      return Point.interpolate(self.spt, self.ept)

    @property
    def pts(self): 
      """ Returns the start and end points of this Segment.
            
            :result: The start and end Points of this Segment.
            :rtype: [Point]
      
      """
      return self.spt, self.ept


    def is_equal(self,other,pt_tol=None, vec_tol=None):
        """ Returns True if the given Segment shares termination Points and direction with this Segment
        
            :param other: Segment to be compared.
            :type other: Segment
            :param pos_tol: Tolerance of point projection distance.
            :type pos_tol: float               
            :param vec_tol: Tolerance of vector direction difference that does not correspond to an angular dimension or distance, but is treated as a separate numeric delta for x, y, and z coordinates of the normalized vectors.
            :type vec_tol: float
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_seg.is_equal(other_seg)
        """
        return self.spt.is_equal(other.spt,pt_tol) and self.vec.is_equal(other.vec,vec_tol)
        
    def is_coincident(self,other,tol=None):
        """ Returns True if the given Segment shares termination Points but not necessarily direction with this Segment
        
            :param other: Segment to be compared.
            :type other: Segment             
            :param tol: Tolerance of point difference that does not correspond to an actual distance, but is treated as a separate numeric delta for x, y, and z coordinates.
            :type tol: float
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_seg.is_equal(other_seg)
        """
        if self.spt.is_equal(other.spt,tol) and self.ept.is_equal(other.ept,tol): return True
        if self.spt.is_equal(other.ept,tol) and self.ept.is_equal(other.spt,tol): return True
        return False
        

    def is_overlapping(self,other,tol=None):
        """ Returns True if the given Segment shares any Points along its length with this Segment
        
            :param other: Segment to be compared.
            :type other: Segment             
            :param tol: Tolerance of point projection.
            :type tol: float
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_seg.is_overlapping(other_seg)
        """
        if not self.is_collinear(other): return False
        if self.contains(other.spt) or self.contains(other.ept): return True
        if other.is_encompassing(self): return True
        return False
        
    def is_encompassing(self,other,tol=None):
        """ Returns True if the given Segment shares all the Points along its length with this Segment
        
            :param other: Segment to be compared.
            :type other: Segment             
            :param tol: Tolerance of point projection.
            :type tol: float
            :result: Boolean result of comparison.
            :rtype: bool
            
            ::
            
                my_seg.is_encompassing(other_seg)
        """
        return self.contains(other.spt) and self.contains(other.ept)
    
    def near(self,p):
        """ Returns a tuple of the closest point to a given line segment, its t value and the distance from the Point to the near Point.
       
            :param p: Point to look for a near Point on the Segment.
            :type p: Point
            :result: Tuple of near point on Segment, t value and distance from point to near point.
            :rtype: (Point, float, float)
        """
        
        near = super(Segment,self).near(p)
        if near[1] < 0:
            near = (self.spt,0.0,p.distance(self.spt))
        elif near[1] > 1:
            near = (self.ept,1.0,p.distance(self.ept))
        return near
        
        

      
    def inverted(self):
        """ Return a new Segment between the ept and spt of this Segment, but pointing in the opposite direction.
        
            :result: Inverted vector.
            :rtype: Vec
        """ 
        return Segment(self.ept,self._vec.inverted())

        
    def divide(self, divs):
        """| Divides this segment into a list of Points equally spaced between its start-point and endpoint.
           | Number of Points returned will be one more than integer divs, such that if this Segment is divided into two, three Points are returned.
        
           :param divs: Number of divisions.
           :type divs: int        
           :result: List of Points equally spaced along this Segment
           :rtype: list
        """
        tt = Interval().divide(divs, True)
        return [self.eval(t) for t in tt]
    
    def subsegment(self, divs):
        """ Divides this Segment into a list of smaller equally-sized Segments.
        
            :param divs: Number of subsegments.
            :type divs: int
            :result: List of smaller Segments. 
            :rtype: list
        """
        pts = self.divide(divs)
        return [Segment(pa,pb) for pa,pb in zip(pts[:-1],pts[1:]) ]
        
        
    @staticmethod
    def by_coords2d(x0=0.0,y0=0.0,x1=1.0,y1=1.0): 
        """ Returns a 2D LinearEntity from two sets of x and y coordinates.
        
            :param x0: First x-coord.
            :type x0: float
            :param y0: First y-coord.
            :type y0: float
            :param x1: Second x-coord.
            :type x1: float
            :param y1: Second y-coord.
            :type y1: float
            :result: Segment
            :rtype: Segment
            
        """
    
        return Segment(Point(x0,y0),Point(x1,y1))

    @staticmethod
    def by_coords3d(x0=0.0,y0=0.0,z0=0.0,x1=1.0,y1=1.0,z1=1.0): 
        """ Returns a 3D LinearEntity from two sets of x,y and z coordinates.
        
            :param x0: First x-coord.
            :type x0: float
            :param y0: First y-coord.
            :type y0: float
            :param z0: First z-coord.
            :type z0: float
            :param x1: Second x-coord.
            :type x1: float
            :param y1: Second y-coord.
            :type y1: float
            :param z1: Second z-coord.
            :type z1: float
            :result: Segment
            :rtype: Segment
            
        """
        return Segment(Point(x0,y0,z0),Point(x1,y1,z1))        

    @staticmethod
    def merge(seg_a, seg_b, tol=None):
        if not seg_a.is_overlapping(seg_b,tol): return False
        pts = [seg_a.spt,seg_a.ept,seg_b.spt,seg_b.ept]
        t_vals = sorted([seg_a.to_line().near(p)[1] for p in pts])
        return Segment(seg_a.eval(t_vals[0]), seg_a.eval(t_vals[-1]))
        
    @staticmethod
    def chain(pts,periodic=None):
        if periodic is None: return [Segment(pa,pb) for pa,pb in zip(pts[:-1],pts[1:])]
        return [Segment(pts[-1],pts[0])]+[Segment(pa,pb) for pa,pb in zip(pts[:-1],pts[1:])]        

