from decodes.core import *
from . import base, interval, vec, point, cs #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "polygon.py loaded"

import copy, collections
import math

class PGon(Geometry, HasBasis, HasVerts):
    """
    a very simple 2d polygon class
    Polygons limit their vertices to x and y dimensions, and enforce that they employ a basis.    Transformations of a polygon should generally be applied to the basis.    Any tranfromations of the underlying vertices should ensure that the returned vectors are limited to x and y dimensions
    """
    
    def __init__(self, verts=None, basis=None):
        """ PGon Constructor.
        
            :param verts: List of vertices to build the polygon.
            :type verts: list
            :param basis: Plane basis for the PGon.
            :type basis: Basis
            :returns: PGon object. 
            :rtype: PGon
        """ 
        super(PGon,self).__init__()
        self.basis = CS() if (basis is None) else basis
        self._verts = []
        if (verts is not None) : 
            for v in verts: self.append(v)
        
    def basis_applied(self, copy_children=True): 
        return self
    #TODO: copy this functionality from Mesh class
    
    def basis_stripped(self, copy_children=True): 
        return self
    #TODO: copy this functionality from Mesh class
        

    #TODO: update HasVerts to deal with bases and remove this method
    @property
    def verts(self):
        """ Returns the list of PGon vertices.
        
            :returns: List of vertices(points). 
            :rtype: list
        """ 
        if not self.is_baseless: return [ v.set_basis(self.basis) for v in self._verts]
        else : return self._verts
        
    #TODO: update HasVerts to deal with bases and remove this method
    @verts.setter
    def verts(self, verts):
        """ Sets the vertices of a PGon object.
        
            :param verts: Vertices to add to the PGon.
            :type verts: Point or list 
            :returns: Updates the PGon object. 
        """ 
        self._verts = []
        self.append(verts)
     
    #TODO: update HasVerts to deal with bases and remove this method
    def append(self,other) :
        """ Adds vertices to the PGon.

            :param other: Vertice to add.
            :type other: Point
            :returns: Updates the PGon. 

        .. todo:: Get rid of this function and get it from base.py
        """ 
        if isinstance(other, collections.Iterable) : 
            for v in other : self.add_vert(v)
        else : 
            if self.is_baseless : self._verts.append(other.basis_applied())
            elif self.basis is other.basis : 
                self._verts.append(other.basis_stripped())
            elif other.is_baseless : 
                # we assume here that the user is describing the point within the pgon's basis
                # they may, however, be trying to add a "world" point to a mesh with a defined basis
                # if this is the case, they should call pgon.basis_stripped()
                #TODO: shouldn't we apply the basis to this point?
                self._verts.append(other)
            else : raise BasisError("The basis for this PGon and the point you're adding do not match.    Try applying or stripping the point of its basis, or describing the point in terms of the PGon's basis")
        
        
    def __repr__(self): return "pgon[{0}v]".format(len(self._verts))
    
    @staticmethod
    def rectangle(cpt, w, h):
        """ Constructs a rectangle based on a center point, a width, and a height.
        
            :param cpt: Center point of a rectangle.
            :type cpt: Point
            :param w: Width of a rectangle.
            :type w: float
            :param h: Height of a rectangle.
            :type h: float
            :returns: Rectangle (PGon object). 
            :rtype: PGon
        """ 
        w2 = w/2
        h2 = h/2
        basis = CS(cpt)
        return PGon([Point(-w2,-h2),Point(w2,-h2),Point(w2,h2),Point(-w2,h2)],basis)

    @staticmethod
    def doughnut(cpt,radius_interval,angle_interval=Interval(0,math.pi*2),res=20):
        """ Constructs a doughnut based on a center point, two radii, and optionally a start angle, sweep angle, and resolution.
        
            :param cpt: Center point of a rectangle.
            :type cpt: Point
            :param angle_interval: Radii interval.
            :type angle_interval: Interval
            :param res: doughnut resolution.
            :type res: float
            :returns: Doughnut object. 
            :rtype: PGon
        """ 
        cs = CylCS(cpt)
        pts = []
        
        def cyl_pt(rad,ang): return Point(rad,ang,basis=cs).basis_applied()

        for t in angle_interval.divide(res,True):pts.append(cyl_pt(radius_interval.a,t))
        for t in angle_interval.invert().divide(res,True):pts.append(cyl_pt(radius_interval.b,t))
        return PGon(pts)

