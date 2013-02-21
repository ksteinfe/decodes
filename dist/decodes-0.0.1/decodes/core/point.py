from decodes.core import *
from . import base, vec #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
import math, random
if VERBOSE_FS: print "point.py loaded"


# points may define a "basis"
# interpreted as any object that may be "evaluated" (passed three coords) and return a position in R3
# if no basis is defined for a point, R3 is assumed
# the _x,_y, and _z properties of a point return values in "basis space" (unevaluated by basis)
# the x,y,and z properties of a point return values in "world space" (evaluated by basis)
# if no basis has been defined, these values are the same

class Point(Vec,HasBasis):
    """
    a simple vector class
    """
    
    def __init__(self, a=0, b=0, c=0, basis=None):
        super(Point,self).__init__(a,b,c)
        self.basis = basis
    
    @property
    def x(self): 
        """
        The x-coordinate of this point
        Setting the x-value of a point with a basis requires stripping the basis of the point.    Set pt._x to alter the local coordinate instead
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
        """
        The y-coordinate of this point
        Setting the y-value of a point with a basis requires stripping the basis of the point.    Set pt._y to alter the local coordinate instead
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
        """
        The z-coordinate of this point
        Setting the z-value of a point with a basis requires stripping the basis of the point.    Set pt._z to alter the local coordinate instead
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
        """
        returns a new point with basis applied. 
        coords will be interpreted in world space
        points will appear in the same position when drawn
        """
        pt = Point(self.x,self.y,self.z)
        if hasattr(self, 'props') : pt.props = self.props
        return pt
    
    def basis_stripped(self, copy_children=True): 
        """
        returns a new point stripped of any bases.
        coords will be interpreted in world space, and points will appear in their "local" position when drawn
        """
        pt = Point(self._x,self._y,self._z)
        if hasattr(self, 'props') : pt.props = self.props
        return pt
    
    def set_basis(self,basis): 
        """
        returns a new point whose local coordniates are the same as this point, but whose basis is set by the basis provided.
        """
        return Point(self._x,self._y,self._z,basis=basis)

    def __add__(self, other): 
        """
        overloads the addition **(+)** operator
        returns a new point that results from adding this point's world coordinates to the other point's (or vector's) world coordinates.
        no matter the basis of the inputs, the resulting point will have no basis.
        """
        return Point(self.x+other.x , self.y+other.y, self.z+other.z)
    
    def __sub__(self, other): 
        """
        overloads the subtraction **(+)** operator
        returns a new point that results from subtracting the other point's (or vector's) worldcoordinates from this point's world coordinates.
        no matter the basis of the inputs, the resulting point will have no basis.
        :rtype: Point
        """
        return Point(self.x-other.x , self.y-other.y, self.z-other.z)

    def __div__(self, other): 
        """
        overloads the division **(/)** operator
        returns a new point that results from divding each of this point's world coordinates by the value provided.
        no matter the basis of the inputs, the resulting point will have no basis.
        """
        return Point(self.x/float(other), self.y/float(other), self.z/float(other))

    def __mul__(self, other):
        """
        overloads the multiplication **(*)** operator
        if a transformation is provided, applies the transformation to this point in a way equivilent to the expression ``other * self``
        otherwise, returns a new point that results from multiplying each of this point's world coordinates by the value provided.    no matter the basis of the inputs, the resulting point will have no basis.
        """
        from .xform import Xform
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
        if self.z < other.z : return True
        if self.z == other.z and self.y < other.y : return True
        if self.z == other.z and self.y == other.y and self.x < other.x : return True
        return False
    def __gt__(self, other): 
        if self.z > other.z : return True
        if self.z == other.z and self.y > other.y : return True
        if self.z == other.z and self.y == other.y and self.x > other.x : return True
        return False
            
    def __le__(self, other): return True if (self < other or self == other) else False 
    def __eq__(self, other): return all([self.x==other.x,self.y==other.y,self.z==other.z])
    def __ne__(self, other): return not all([self.x==other.x,self.y==other.y,self.z==other.z])
    def __ge__(self, other): return True if (self > other or self == other) else False 


    def _distance2(self, other):
        """
        distance squared in local space. Cheaper to calculate than distance.
        """
        if self.basis is not other.basis : raise BasisError("Cannot measure '_distance2' between points with different bases.    Use 'distance2' instead")
        return Vec(self,other).length2

    def _distance(self, other): 
        """
        returns the distance between this point and the other point in local space.
        both points must use the same basis.
        """
        if self.basis is not other.basis : raise BasisError("Cannot measure '_distance' between points with different bases.    Use 'distance' instead")
        return Vec(self,other).length
    
    def distance2(self,other): 
        """
        distance squared in world space. Cheaper to calculate than distance.
        """
        return Vec(self.basis_applied(),other.basis_applied()).length2

    def distance(self,other): 
        """
        returns the distance between this point and the other point in world space.
        both points must use the same basis.
        """
        return Vec(self.basis_applied(),other.basis_applied()).length
    
    @staticmethod
    def interpolate(p0,p1,t=0.5): 
        """
        returns a new point which is the result of an interpolation between the two given points at the given t-value
        """
        if p0.basis is p1.basis : 
            v = Vec.interpolate(p0,p1,t)
            return Point(v.x,v.y,v.z,p0.basis)
        else : 
            v = Vec.interpolate(p0.basis_applied(),p1.basis_applied(),t)
            return Point(v.x,v.y,v.z)

    @staticmethod
    def _centroid(points): 
        if all( points[0].basis is p.basis for p in points ) : 
            cent = Vec.average([p.basis_stripped() for p in points])
            return Point(cent).set_basis(points[0].basis)
        raise BasisError("Cannot calculate '_centroid' for points of mixed bases.    Use 'centroid' instead")
        
    @staticmethod
    def centroid(points): 
        return Point( Vec.average([p.basis_applied() for p in points]) )
        

    def projected(self, other): 
        """
        Returns a new point projected onto a destination vector
        .. todo:: think about what this function will mean for new "basis" construct.    probably eliminate, in favor of projecting onto lines and such in world space
        """
        return Point( Vec(self.x,self.y,self.z).projected(other) )
    
    @staticmethod
    def random(rnge=[-1.0,1.0],constrain2d=False):
        """
        Returns a random point within the given (optional) range
        """
        x = random.uniform(rnge[0],rnge[1])
        y = random.uniform(rnge[0],rnge[1])
        z = random.uniform(rnge[0],rnge[1])
        p = Point(x,y) if constrain2d else Point(x,y,z)
        return p
        
