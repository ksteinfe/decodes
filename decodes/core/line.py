import decodes.core as dc
from decodes.core import *
if dc.VERBOSE_FS: print "line.py loaded"

#from SYMPY
#http://code.google.com/p/sympy/source/browse/trunk.freezed/sympy/geometry/entity.py
#formerlly exteneded GeometryEntity
class LinearEntity(dc.Geometry):
    """
    A linear entity (line, ray, segment, etc) in space.

    This is an abstract class and is not meant to be instantiated.
    Subclasses should implement the following methods:
        __eq__
        __contains__
    """
    def __init__(self, a, b):
      self._pt = a if isinstance(a,dc.Point) else Point(a.x,a.y,a.z)
      if isinstance(b,dc.Point) : self._vec = b-a
      elif isinstance(b,dc.Vec) : self._vec = b
      else : raise TypeError("%s constructor requires Vec instances" % self.__class__.__name__)
    
    @property
    def spt(self): return self._pt
    @spt.setter
    def spt(self, point): self._pt = point
    @property
    def vec(self): return self._vec
    @vec.setter
    def vec(self, vec): self._vec = vec
    @property
    def ept(self): return self._pt+self._vec
    @ept.setter
    def ept(self, point): self._vec = point-self._pt
    
    
    
    @property
    def coefficients(self):
        """The coefficients (a,b,c) for equation ax+by+c=0"""
        raise NotImplementedError()
        return (self.p1[1]-self.p2[1],
                self.p2[0]-self.p1[0],
                self.p1[0]*self.p2[1] - self.p1[1]*self.p2[0])

    def is_concurrent(*lines):
        """
        Returns True if the set of linear entities are concurrent, False
        otherwise. Two or more linear entities are concurrent if they all
        intersect at a single point.

        Description of Method Used:
        ===========================
            Simply take the first two lines and find their intersection.
            If there is no intersection, then the first two lines were
            parallel and had no intersection so concurrenecy is impossible
            amongst the whole set. Otherwise, check to see if the
            intersection point of the first two lines is a member on
            the rest of the lines. If so, the lines are concurrent.
        """
        raise NotImplementedError()

    def is_parallel(l1, l2):
        """Returns True if l1 and l2 are parallel, False otherwise"""
        raise NotImplementedError()
        try:
            a1,b1,c1 = l1.coefficients
            a2,b2,c2 = l2.coefficients
            return bool(simplify(a1*b2 - b1*a2) == 0)
        except AttributeError:
            return False

    def is_perpendicular(l1, l2):
        """Returns True if l1 and l2 are perpendicular, False otherwise"""
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

        Description of Method Used:
        ===========================
            From the dot product of vectors v1 and v2 it is known that:
                dot(v1, v2) = |v1|*|v2|*cos(A)
            where A is the angle formed between the two vectors. We can
            get the directional vectors of the two lines and readily
            find the angle between the two using the above formula.
        """
        #v1 = l1.p2 - l1.p1
        #v2 = l2.p2 - l2.p1
        #return Basic.acos( (v1[0]*v2[0]+v1[1]*v2[1]) / (abs(v1)*abs(v2)) )
        raise NotImplementedError()

    def parallel_line(self, p):
        """
        Returns a new Line which is parallel to this linear entity and passes
        through the specified point.
        """
        return Line(p, self.vec)

    def perpendicular_line(self, p):
        """
        Returns a new Line which is perpendicular to this linear entity and
        passes through the specified point.
        """
        raise NotImplementedError()

    def perpendicular_segment(self, p):
        """
        Returns a new Segment which connects p to a point on this linear
        entity and is also perpendicular to this line. Returns p itself
        if p is on this linear entity.
        """
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()

    def __contains__(self, other):
        raise NotImplementedError()


class Line(LinearEntity):
    """A line in space."""

class Ray(LinearEntity):
    """A ray in space."""

class Segment(LinearEntity):
    """An undirected line segment in space."""

    @property
    def length(self): return self.vec.length        

    @property
    def midpoint(self): return Point.interpolate(self.spt, self.ept)
