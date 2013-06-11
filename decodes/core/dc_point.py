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

class Point(Vec,HasBasis):
    """
    a simple point class
    """
    
    def __init__(self, a=0, b=0, c=0, basis=None):
        """Point Constructor

            :param a: a value.
            :type a: float
            :param b: b value
            :type b: float
            :param c: c value
            :type c: float
            :result: Point object.
            :rtype: Point
        """
        super(Point,self).__init__(a,b,c)
        self.basis = basis

        # there's a unique case where we've been passed a based point along with a defined basis here.
        # in this case, we should take the local coordinates of the given point interpreted through the given basis
        if isinstance(a, Point) and b==0 and c == 0 and basis !=None :  self._x , self._y, self._z = a._x , a._y, a._z
    
    @property
    def x(self): 
        """The x-coordinate of this point. Setting the x-value of a point with a basis requires stripping the basis of the point. Set pt._x to alter the local coordinate instead.

            :result: x value.
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
        """The y-coordinate of this point. Setting the y-value of a point with a basis requires stripping the basis of the point. Set pt._y to alter the local coordinate instead
        
            :result: y value.
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
        """The z-coordinate of this point. Setting the z-value of a point with a basis requires stripping the basis of the point.    Set pt._z to alter the local coordinate instead
        
            :result: z value.
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
        """Returns a new point with basis applied. Coords will be interpreted in world space. Points will appear in the same position when drawn
        
            :param copy_children: If True, creates a new Point object with 'world' coordinates.
            :type copy_children: bool
            :result: Point object with basis applied.
            :rtype: Point
        """
        pt = Point(self.x,self.y,self.z)
        if hasattr(self, 'props') : pt.props = self.props
        return pt
    
    def basis_stripped(self, copy_children=True): 
        """Returns a new point stripped of any bases. Coords will be interpreted in world space, and points will appear in their "local" position when drawn
        
            :param copy_children: If True, creates a new Point object with 'local' coordinates.
            :type copy_children: bool
            :result: Point object with basis stripped.
            :rtype: Point
        """
        pt = Point(self._x,self._y,self._z)
        if hasattr(self, 'props') : pt.props = self.props
        return pt
    
    def set_basis(self,basis): 
        """Returns a new point whose local coordniates are the same as this point, but whose basis is set by the basis provided.
        
            :param basis: New basis for the point.
            :type basis: Basis
            :result: Point object with new basis.
            :rtype: Point
        """
        return Point(self._x,self._y,self._z,basis=basis)

    def __add__(self, other): 
        """Overloads the addition **(+)** operator. 
        Returns a new point that results from adding this point's world coordinates to the other point's (or vector's) world coordinates.
        No matter the basis of the inputs, the resulting point will have no basis.
        
            :param other: Point or Vec to be added.
            :type other: Point or Vec
            :result: New point.
            :rtype: Point
        """
        return Point(self.x+other.x , self.y+other.y, self.z+other.z)
    
    def __sub__(self, other): 
        """Overloads the subtraction **(-)** operator
        Returns a new point that results from subtracting the other point's (or vector's) worldcoordinates from this point's world coordinates.
        No matter the basis of the inputs, the resulting point will have no basis.

            :param other: Point or Vec to be subtracted.
            :type other: Point or Vec
            :result: New point.
            :rtype: Point
        """
        return Point(self.x-other.x , self.y-other.y, self.z-other.z)

    def __truediv__(self,other): return self.__div__(other)
    def __div__(self, other): 
        """Overloads the division **(/)** operator
        Returns a new point that results from divding each of this point's world coordinates by the value provided.
        No matter the basis of the inputs, the resulting point will have no basis.
        
            :param other: Point or Vec to be divided.
            :type other: Point or Vec
            :result: New point.
            :rtype: Point
        """
        return Point(self.x/float(other), self.y/float(other), self.z/float(other))

    def __mul__(self, other):
        """Overloads the multiplication **(*)** operator.
        If a transformation is provided, applies the transformation to this point in a way equivilent to the expression ``other * self``.
        otherwise, returns a new point that results from multiplying each of this point's world coordinates by the value provided.    no matter the basis of the inputs, the resulting point will have no basis.
        
            :param other: Point or Vec to be multiplied.
            :type other: Point or Vec
            :result: New point.
            :rtype: Point
        """
        from .dc_xform import Xform
        if isinstance(other, Xform) :
            return other*self
        else : 
            return Xform.scale(other) * self

    def __repr__(self):
        #TODO: provide mechanism to print basis info if desired
        #if not self.is_baseless : return "pt[{0},{1},{2}] basis: {3}".format(self._x,self._y,self._z,self.basis)
        if not self.is_baseless : return "wpt[{0},{1},{2}]".format(self.x,self.y,self.z)
        return "pt[{0},{1},{2}]".format(self.x,self.y,self.z)

    '''comparisons are always done in world space'''
    def __lt__(self, other):
        """Overloads the less than **(<)** operator.
        
            :param other: Point to be compared.
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        if self.z < other.z : return True
        if self.z == other.z and self.y < other.y : return True
        if self.z == other.z and self.y == other.y and self.x < other.x : return True
        return False
        
    def __gt__(self, other): 
        """Overloads the greater than **(>)** operator.
        
            :param other: Point to be compared.
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        if self.z > other.z : return True
        if self.z == other.z and self.y > other.y : return True
        if self.z == other.z and self.y == other.y and self.x > other.x : return True
        return False
            
    def __le__(self, other): 
        """Overloads the less or equal **(<=)** operator.
        
            :param other: Point to be compared.
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        return True if (self < other or self == other) else False
        
    def __eq__(self, other): 
        """Overloads the equal **(==)** operator.
        
            :param other: Point to be compared.
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        return all([self.x==other.x,self.y==other.y,self.z==other.z])
        
    def __ne__(self, other): 
        """Overloads the nor equal **(!=)** operator.
        
            :param other: Point to be compared.
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        return not all([self.x==other.x,self.y==other.y,self.z==other.z])
        
    def __ge__(self, other): 
        """Overloads the greater or equal **(>=)** operator.
        
            :param other: Point to be compared.
            :type other: Point
            :result: Boolean result of comparison
            :rtype: bool
        """
        return True if (self > other or self == other) else False 

    def _distance2(self, other):
        """Distance squared in local space. Cheaper to calculate than distance.
        
            :param other: Point to calculate the distance from.
            :type other: Point
            :result: Distance between points.
            :rtype: float
        """
        
        if self.basis is not other.basis : raise BasisError("Cannot measure '_distance2' between points with different bases.    Use 'distance2' instead")
        return Vec(self,other).length2

    def _distance(self, other): 
        """Returns the distance between this point and the other point in local space. Both points must use the same basis.
        
            :param other: Point to calculate the distance from.
            :type other: Point
            :result: Distance between points.
            :rtype: float
        """
        if self.basis is not other.basis : raise BasisError("Cannot measure '_distance' between points with different bases.    Use 'distance' instead")
        return Vec(self,other).length
    
    def distance2(self,other): 
        """Returns the distance between this point and the other point in local space. Both points must use the same basis.
        
            :param other: Point to calculate the distance from.
            :type other: Point
            :result: Distance between points.
            :rtype: float
        """
        return Vec(self.basis_applied(),other.basis_applied()).length2

    def distance(self,other): 
        """Returns the distance between this point and the other point in local space. Both points must use the same basis.
        
            :param other: Point to calculate the distance from.
            :type other: Point
            :result: Distance between points.
            :rtype: float
        """
        return Vec(self.basis_applied(),other.basis_applied()).length
    
    def projected(self, other): 
        """Returns a new point projected onto a destination vector
        
            :param other: Destination vector.
            :type other: Vec
            :result: A Point projected onto a Vector.
            :rtype: Point
            
            .. todo:: think about what this function will mean for new "basis" construct.    probably eliminate, in favor of projecting onto lines and such in world space
        """
        return Point( Vec(self.x,self.y,self.z).projected(other) )

    @staticmethod
    def near(pt, pts):
        """ Returns a reference to a Point from the given list of Points which is nearest to the source Point.

            :param pt: Source Point
            :type pt: Point
            :param pt: A list of Points through which to search
            :type pts: [Point]
            :result: A reference to a Point from the list which is nearest to the source Point
            :rtype: Point
        """
        return pts[Point.near_index(pt,pts)]

    @staticmethod
    def near_index(pt, pts):
        """ Returns the index of the Point within the given list of Points which is nearest to the source Point.

            :param pt: Source Point
            :type pt: Point
            :param pt: A list of Points through which to search
            :type pts: [Point]
            :result: The index of the nearest Point
            :rtype: int
        """
        dists = [pt.distance2(p) for p in pts]
        return dists.index(min(dists))

    @staticmethod
    def far(pt, pts):
        """ Returns a reference to a Point from the given list of Points which is furthest from the source Point.

            :param pt: Source Point
            :type pt: Point
            :param pt: A list of Points through which to search
            :type pts: [Point]
            :result: A reference to a Point from the list which is furthest from the source Point
            :rtype: Point
        """
        return pts[Point.far_index(pt,pts)]

    @staticmethod
    def far_index(pt, pts):
        """ Returns the index of the Point within the given list of Points which is furthest from the source Point.

            :param pt: Source Point
            :type pt: Point
            :param pt: A list of Points through which to search
            :type pts: [Point]
            :result: The index of the furthest Point
            :rtype: int
        """
        dists = [pt.distance2(p) for p in pts]
        return dists.index(max(dists))


    @staticmethod
    def interpolate(p0,p1,t=0.5): 
        """Returns a new point which is the result of an interpolation between the two given points at the given t-value
        
            :param p0: First point to interpolate.
            :type p0: Point
            :param p0: Second point to interpolate.
            :type p0: Point
            :param p0: t-value of interpolation.
            :type p0: float
            :result: Interpolated point.
            :rtype: Point
        """
        if p0.basis is p1.basis : 
            v = Vec.interpolate(p0,p1,t)
            return Point(v.x,v.y,v.z,p0.basis)
        else : 
            v = Vec.interpolate(p0.basis_applied(),p1.basis_applied(),t)
            return Point(v.x,v.y,v.z)

    @staticmethod
    def _centroid(points): 
        """Returns the centroid of a point cloud in local coordinates.
        All given points will be evaluated with their bases stripped, and the basis of the returned point will adopt the basis of the given points.
        Mixed bases among the given points will throw an error.

            :param points: Point cloud
            :type p0: list
            :result: Centroid of point cloud.
            :rtype: Point
        """
        if all( points[0].basis is p.basis for p in points ) : 
            cent = Vec.average([p.basis_stripped() for p in points])
            return Point(cent).set_basis(points[0].basis)
        raise BasisError("Cannot calculate '_centroid' for points of mixed bases.    Use 'centroid' instead")
        
    @staticmethod
    def centroid(points): 
        """Returns the centroid of a point cloud.
        All given points will be evaluated with their bases applied, and the returned point will be baseless
        
            :param points: Point cloud
            :type p0: list
            :result: Centroid of point cloud.
            :rtype: Point
        """
        return Point( Vec.average([p.basis_applied() for p in points]) )
        
    
    @staticmethod
    def random(interval=None,constrain2d=False):
        """Returns a random point within the given (optional) range
        
            :param interval: Range to get the random value from.
            :type interval: Interval
            :param constrain2d: Constrain the point to 2d space
            :type constrain2d: bool
            :result: Random point.
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


class HasPts(HasBasis):
    """
    A base class for anything that contains a list of vertices.
    All HasPts classes also have bases
    """
    def __init__(self):
        self._verts = [] # a list of vecs that represent the local coordinates of this object's points
        self.basis = None

    def __getitem__(self,slice):
        sliced = self._verts[slice] # may return a singleton or list
        try:
            #TODO: move slice indexing to subclasses and return object rather than point list
            return [Point(vec,basis=self.basis) for vec in sliced]
        except:
            return sliced
            #return Point(sliced)
    
    def __setitem__(self,index,other):
        try:
            self._verts[index] = self._compatible_vec(other)
        except TypeError, e:
                raise TypeError("You cannot set the vertices of this object using slicing syntax")
    
    def __len__(self): return len(self._verts)

    @property
    def pts(self): 
        """Returns the points contained within this geometry.

            :rtype: Point or [Point]
        """
        return [Point(vec,basis=self.basis) for vec in self._verts]
    
    @pts.setter
    def pts(self, pts): 
        """Sets the points contained within this geometry.  
        The list of vectors currently stored within this geometry are cleared, and the given points are each appended in sequence, following the uusual rules regarding bases

            :param pts: Point(s) to store
            :type pts: Point or [Point]
            :result: Modfies this geometry by redefining the stored list of points
        """
        self._verts = []
        self.append(verts)
        
    def append(self,pts) : 
        """Appends the given Point to the stored list of points.
        Each Point is processed to ensure compatibilty with this geometry's basis 

            :param pts: Point(s) to append
            :type pts: Point or [Point]
            :result: Modfies this geometry by adding items to the stored list of points
        """
        if isinstance(pts, collections.Iterable) : 
            for p in pts : self.append(p)
        else : 
            self._verts.append(self._compatible_vec(pts))
    
    def clear(self):
        """Clears this Geometry of all the Points contained within it"""
        del self._verts[:]

    @property
    def centroid(self):
        """Returns the centroid of the points of this object
        
            :returns: Centroid (point).
            :rtype: Point
        """
        return Point._centroid(self.pts) 
    

    def basis_applied(self): 
        """Returns a new Geometry with basis applied. Coords will be interpreted in world space, appearing in the same position when drawn
        
            :result: Object with basis applied.
            :rtype: Object
        """
        clone = copy.copy(self)
        clone._verts = [Vec(pt.basis_applied()) for pt in self.pts]
        clone.basis = None
        return clone
    
    def basis_stripped(self): 
        """Returns a new Geometry stripped of any bases. Coords will be interpreted in world space, in their analogous "local" position when drawn
        
            :result: Object with basis stripped.
            :rtype: Object
        """
        clone = copy.copy(self)
        clone._verts = [Vec(pt.basis_stripped()) for pt in self.pts]
        clone.basis = None
        return clone


    def _compatible_vec(self,other):
        """ Returns a vector compatible with the collection of vectors in this object if possible
        """
        if self.is_baseless: return Vec(other) # if this object is baseless, then use the world coordinates of the other
        if (not hasattr(other, 'basis')) or other.basis is None : 
             # if the other is baseless, then use its world coordinates.  
             # we assume here that the user is describing the point within this object's basis.
             # they may, however, be trying to add a "world" point to a mesh with a defined basis
             # if this is the case, we would have to describe this world point in terms of this object's basis... which isn't always possible
             # we'll try and warn them.
             #warnings.warn("You've just added a baseless point to a based object.  The world coordinates of the point have been interpreted as local coordinates of the object.  Is this what you wanted?")
             return Vec(other)
        if self.basis is other.basis : return Vec(other._x,other._y,other._z) # if we share a basis, then use the local coordinates of the other
        raise BasisError("The basis for this Geometry and the point you're adding do not match. Try applying or stripping the point of its basis, or describing the point in terms of this Geometry's basis")


class QuadTree():
    def __init__ (self, capacity, bounds):
        self.cap = capacity
        self.bnd = bounds
        self.pts = []
        
    @property
    def has_children(self):
        if hasattr(self,'children'):return True 
        return False
        
    def append(self, pt) :
        if not self.contains(pt) : return False
        if not self.has_children and len(self.pts) < self.cap:
            self.pts.append(pt)
            return True
        else :
            if not self.has_children : self.divide()
            for child in self.children:
                if child.append : return True
            return False
        
    def divide(self) :
        """
        divides self into sub regions.
        starts at bottom left and moves clockwise
        """
        if self.has_children: return False
        from .dc_pgon import Bounds
        
        cpts = self.bnd.corners
        ivals_x = self.bnd.iterval_x/4
        ivals_y = self.bnd.iterval_y/4
        
        cpts = []
        cpts.append(Point(ivals_x[1],ivals_y[1]))
        cpts.append(Point(ivals_x[1],ivals_y[3]))
        cpts.append(Point(ivals_x[3],ivals_y[3]))
        cpts.append(Point(ivals_x[3],ivals_y[1]))
        
        self.children = [QuadTree(self.cap,Bounds(pt,self.bnd.w2,self.bnd.h2)) for pt in cpts]
        for pt in self.pts : self.append(pt)
        self.pts = None
        return True
    
    def contains(self,pt):
        if self.has_children:
            return any([child.contains(pt) for child in self.children])
        else:
            return self.bnd.contains(pt)
            

