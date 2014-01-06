from decodes.core import *
from . import dc_base, dc_interval, dc_vec, dc_point, dc_plane, dc_cs #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
import math, random, copy
if VERBOSE_FS: print "has_pts.py loaded"


class HasPts(HasBasis):
    """
    A base class for anything that contains a list of vertices.
    All HasPts classes also have bases
    """
    class_attr = ['_pts','_centroid'] # this list of props is unset anytime this HasPts object changes
    
    def __init__(self, vertices=None,basis=None):
        self._verts = [] # a list of vecs that represent the local coordinates of this object's points
        if vertices is not None: self.append(vertices)
        self.basis = basis # set the basis after appending the points


    def __getitem__(self,slice):
        sliced = self._verts[slice] # may return a singleton or list
        return sliced
        try:
            #TODO: move slice indexing to subclasses and return object rather than point list
            return [Point(vec,basis=self.basis) for vec in sliced]
        except:
            return sliced
    
    def __setitem__(self,index,other):
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        try:
            self._verts[index] = self._compatible_vec(other)
        except:
                raise TypeError("You cannot set the vertices of this object using slicing syntax")
        self._vertices_changed() # call to trigger subclass handling of vertex manipulation
    
    @property
    def basis(self): return self._basis

    @basis.setter
    def basis(self, basis): 
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        self._basis = basis

    def __len__(self): return len(self._verts)



    def __add__(self, vec):
        """Overloads the addition **(+)** operator. 
        Adds the given vector to each vertex in this Geometry
        
            :param vec: Vec to be added.
            :type vec: Vec
            :result: None
            :rtype: None
        """
        self._unset_attr()  # call this when any of storable properties (subclass_attr or class_attr) changes
        for v in _verts: v = v + vec
        self._vertices_changed() # call to trigger subclass handling of vertex manipulation

    '''
    def __sub__(self, vec): 
        """Overloads the addition **(-)** operator. 
        Returns a new vector that results from subtracting this vector's world coordinates to the other vector's world coordinates.
        
            :param vec: Vec to be subtracted.
            :type vec: Vec
            :result: New vec.
            :rtype: Vec
        """    
        return Vec(self.x-vec.x , self.y-vec.y, self.z-vec.z)
    def __truediv__(self,other): 
        return self.__div__(other)
    def __div__(self, scalar): 
        """Overloads the addition **(/)** operator. 
        Returns a new vector that results from dividing this vector's world coordinates by a given scalar.
        
            :param scalar: number to divide by
            :type scalar: Float
            :result: New vec.
            :rtype: Vec
        """  
        return Vec(self.x/float(scalar), self.y/float(scalar), self.z/float(scalar))
    def __invert__(self): 
        """Overloads the inversion **(~vec)** operator. 
        Inverts the direction of the vector
        Returns a new inverted vector.
        
            :result: Inverted Vec.
            :rtype: Vec
        """  
        return self.inverted()

    def __neg__(self): 
        """Overloads the arithmetic negation **(-vec)** operator. 
        Inverts the direction of the vector
        Returns a new inverted vector.
        
            :result: Inverted Vec.
            :rtype: Vec
        """  
        return self.inverted()
'''
    def __mul__(self, other):
        """Overloads the addition **(*)** operator. 
        If given a scalar, multiplys each vertex in this Geometry by the given scalar
        If given an Xform, applies the given transformation to the basis of this Geometry
        
            :param vec: Object to be multiplied.
            :type vec: Vec or Xform
            :result: New vec.
            :rtype: Vec
        """  
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        from .dc_xform import Xform
        if isinstance(other, Xform) : return other * self
        else : 
            for n in range(len(self._verts)): self._verts[n] = self._verts[n] * other
            self._vertices_changed() # call to trigger subclass handling of vertex manipulation


    @property
    def pts(self): 
        """Returns a copy of the vertices contained within this HasPts as Points.
            Does not allow manipulation.
            If you want to manipulate the vertices of this object, you should operate on the vertices directly (which are defined relative to this HasPts's basis) by calling HasPts[0].x = value

            :rtype: Point or [Point]
        """
        try:
            return tuple([Point(tup[0],tup[1],tup[2]) for tup in self._pts])
        except:
            if self.is_baseless : self._pts =  [vec.tup for vec in self._verts]
            else : self._pts =  [self.basis.eval(vec).tup for vec in self._verts]

            return tuple([Point(tup[0],tup[1],tup[2]) for tup in self._pts])

     
    def append(self,pts) : 
        """Appends the given Point to the stored list of points.
        Each Point is processed to ensure compatibilty with this geometry's basis 

            :param pts: Point(s) to append
            :type pts: Point or [Point]
            :result: Modfies this geometry by adding items to the stored list of points
        """
        self._unset_attr()
        try : 
            for p in pts : self._verts.append(self._compatible_vec(p))
        except : 
            self._verts.append(self._compatible_vec(pts))
        self._vertices_changed() # call to trigger subclass handling of vertex manipulation
    
    def clear(self):
        """Clears this Geometry of all the Points contained within it"""
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        del self._verts[:]

    @property
    def centroid(self):
        """Returns the centroid of the points of this object
        
            :returns: Centroid (point).
            :rtype: Point
        """
        try:
            return self._centroid
        except:
            self._centroid = Point.centroid(self.pts)
            return self._centroid
        
    
    def reverse(self):
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        self._verts.reverse
        return self

    def rotate(self,n):
        """
        rotates the vertices in this object.
        in the case of a PGon, this resets which pt is the first point
        """
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        if n > len(self._verts): n =  n%len(self._verts)
        if n < -len(self._verts): n =  -abs(n)%len(self._verts)
        self._verts = self._verts[n:] + self._verts[:n]
        return self

    def basis_applied(self): 
        """Returns a new Geometry with basis applied. Coords will be interpreted in world space, appearing in the same position when drawn
        
            :result: Object with basis applied.
            :rtype: Object
        """
        # TODO: copy properties over
        clone = copy.copy(self)
        clone._verts = [Vec(pt) for pt in self.pts]
        clone.basis = None
        clone._unset_attr()  # call this when any of storable properties (subclass_attr or class_attr) changes
        return clone
    
    def basis_stripped(self): 
        """Returns a new Geometry stripped of any bases. Coords will be interpreted in world space, in their analogous "local" position when drawn
        
            :result: Object with basis stripped.
            :rtype: Object
        """
        # TODO: copy properties over
        clone = copy.copy(self)
        clone.basis = None
        clone._unset_attr()  # call this when any of storable properties (subclass_attr or class_attr) changes
        return clone


    def _compatible_vec(self,other):
        """ Returns a vector compatible with the collection of vectors in this object if possible
        """
        if isinstance(other, Point):
            if self.is_baseless: return Vec(other) # if this object is baseless, then use the world coordinates of the other
            if (not hasattr(other, 'basis')) or other.basis is None : 
                 # if the other is baseless, then devaluate the point so that it is described in terms of this object's basis.
                 return Vec(self.basis.deval(other))

            if self.basis is other.basis : return Vec(other._x,other._y,other._z) # if we share a basis, then use the local coordinates of the other
            raise BasisError("The basis for this Geometry and the point you're adding do not match. Try applying or stripping the point of its basis, or describing the point in terms of this Geometry's basis")
        else:
            try:
                # Vecs (and anything else from which we can read x,y,z values) are interpreted in local coordinates
                return Vec(other.x,other.y,other.z)
            except:
                raise GeometricError("Cannot find a representation of this thing that is compatible with a HasPts Geometry: "+str(other))

    def _unset_attr(self):
        for attr in self.class_attr : 
            try: delattr(self, attr)
            except:
                #print "can't unset ",attr
                pass
        if hasattr(self, 'subclass_attr'):
            for attr in self.subclass_attr : 
                try: delattr(self, attr)
                except:
                    #print "can't unset ",attr
                    pass

    def _vertices_changed(self):
        pass