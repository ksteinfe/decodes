from decodes.core import *
from . import dc_base, dc_interval, dc_vec, dc_point, dc_plane, dc_cs #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
import math, random, copy
if VERBOSE_FS: print("has_pts.py loaded")


class HasPts(HasBasis):
    """
    | A base class for anything that contains a list of vertices.
    | All HasPts classes also have bases.
    """
    
    class_attr = ['_pts','_centroid'] # this list of props is unset any time this HasPts object changes
    
    def __init__(self, vertices=None,basis=None):
        """ A constructor for a list of vertices with a shared basis.
        
            :param vertices: A list of Vecs.
            :type vertices: [Vec]
            :param basis: A basis
            :type basis: Basis
            :result: HasPts object
            :rtype: HasPts
        
        """
        self._verts = [] # a list of vecs that represent the local coordinates of this object's points
        if vertices is not None: self._append(vertices)
        self._basis = basis # set the basis after appending the points


    def __getitem__(self,slice):
        """ Returns item in this HasPts at given index.
        
            :param slice: Given index.
            :type slice: int
            :result: Vec
            :rtype: Vec
        
        """
        sliced = self._verts[slice] # may return a singleton or list
        return sliced
        try:
            #TODO: move slice indexing to subclasses and return object rather than point list
            return [Point(self._basis.eval(vec)) for vec in sliced]
        except:
            return sliced
    
    def __setitem__(self,index,other):
        """ Replaces vertices at given index with the given vertices.
        
            :param index: Index to replace.
            :type index: int
            :param other: New vertices.
            :type other: Vec
            :result: None
            :rtype: None
           
        """
    
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        try:
            self._verts[index] = self._compatible_vec(other)
        except:
                raise TypeError("You cannot set the vertices of this object using slicing syntax")
        self._vertices_changed() # call to trigger subclass handling of vertex manipulation
    
    @property
    def basis(self):
        """ Returns basis.
            
            :result: Basis
            :rtype Basis
        
        """
        warnings.warn("Altering the properties of the basis of a HasPts object will not automatically update the HasPts.pts. If you want to mess around with any properties of this HasPts object's basis, be sure to call HasPts._unset_attr() after doing so.")
        return self._basis

    @basis.setter
    def basis(self, basis): 
        """ Sets basis.
        
            :param basis: New Basis.
            :type basis: Basis.
            :result: None
            :rtype: None
            
        """
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        self._basis = basis

    def __len__(self): 
        """ Returns the length of the list of vertices.
        
            :result: Length of list.
            :rtype: int
        """
        return len(self._verts)



    def __add__(self, vec):
        """ Overloads the addition **(+)** operator. Adds the given vector to each vertex in this Geometry
        
            :param vec: Vec to be added.
            :type vec: Vec
            :result: None
            :rtype: None
        """
        self._unset_attr()  # call this when any of storable properties (subclass_attr or class_attr) changes
        for v in self._verts: v = v + vec
        self._vertices_changed() # call to trigger subclass handling of vertex manipulation

    def __mul__(self, other):
        """| Overloads the multiplication **(*)** operator. 
           | If given a scalar, multiplies each vertex in this Geometry by the given scalar.
           | If given an Xform, applies the given transformation to each vertex of this Geometry.
        
           :param vec: Object to be multiplied.
           :type vec: Vec or Xform
           :result: New Vec.
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
        """| Returns a copy of the vertices contained within this HasPts as Points.
           | Does not allow manipulation.
           | If you want to manipulate the vertices of this object, you should operate on the vertices directly (which are defined relative to this HasPts's basis) by calling HasPts[0].x = value

           :result: Point or list of points.
           :rtype: Point or [Point]
        """
        try:
            return copy.copy(self._pts)
        except:
            if self.is_baseless : self._pts =  tuple([Point(v) for v in self._verts])
            else : self._pts =  tuple([Point(self._basis.eval(v)) for v in self._verts])

            return copy.copy(self._pts)

     
    def append(self,pts):
        self._append(pts)
        
    def _append(self,pts):   
        self._unset_attr()
        try : 
            for p in pts : self._verts.append(self._compatible_vec(p))
        except : 
            self._verts.append(self._compatible_vec(pts))
        self._vertices_changed() # call to trigger subclass handling of vertex manipulation
    
    def clear(self):
        """Clears this Geometry of all the Points contained within it."""
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        del self._verts[:]

    @property
    def centroid(self):
        """ Returns the centroid of the points of this object.
        
            :returns: Centroid (point).
            :rtype: Point
        """
        try:
            return self._centroid
        except:
            self._centroid = Point.centroid(self.pts)
            return self._centroid
        
    
    def reverse(self):
        """ Reverses storable properties depending on class or subclass attribute changes.
        
            :result: HasPts object
            :rtype: HasPts
            
        """
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        self._verts.reverse()
        return self

    def rotate(self,n):
        """| Rotates the vertices in this object.
           | In the case of a PGon, this resets which point is the first point.
           
           :param n: Number of steps to rotate.
           :type n: int
           :result: HasPts object
           :rtype: HasPts
                
        """
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        if n > len(self._verts): n =  n%len(self._verts)
        if n < -len(self._verts): n =  -abs(n)%len(self._verts)
        self._verts = self._verts[n:] + self._verts[:n]
        return self

    def basis_applied(self): 
        """ Returns a new Geometry with basis applied. Coordinates will be interpreted in world space, appearing in the same position when drawn.
        
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
        """ Returns a new Geometry stripped of any bases. Coordinates will be interpreted in world space, in their analogous "local" position when drawn.
        
            :result: Object with basis stripped.
            :rtype: Object
        """
        # TODO: copy properties over
        clone = copy.copy(self)
        clone.basis = None
        clone._unset_attr()  # call this when any of storable properties (subclass_attr or class_attr) changes
        return clone


    def _compatible_vec(self,other):
        """ Returns a vector compatible with the collection of vectors in this object if possible.
        
            :param other: Vect to make compatible.
            :type other: Vec
            :result: New Vec.
            :rtype: Vec
            
        """
        if self.is_baseless: 
            # if this object is baseless, attempt to use the world coordinates of the other
            return Vec(other) 
        if isinstance(other, Point): 
            # if this object is based and the other is a Point, devaluate by this object's basis
            return Vec(self._basis.deval(other))
            
        try:
            # Vecs (and anything else from which we can read x,y,z values) are interpreted in local coordinates
            return Vec(other.x,other.y,other.z)
        except:
            raise GeometricError("Cannot find a representation of this thing that is compatible with a HasPts Geometry: "+str(other))
        

    def _unset_attr(self):
        """ Deletes class and sublcass attributes when possible.
        
            :result: None
            :rtype: None
        """
        try: 
            del self._pts
        except:
            pass
            
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