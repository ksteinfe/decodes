from decodes.core import *
from . import base, interval, vec, point, cs #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "polygon.py loaded"

import copy, collections
import math

class PGon(HasVerts):
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
        super(PGon,self).__init__() #HasVerts constructor initializes list of verts
        self.basis = CS() if (basis is None) else basis
        if (verts is not None) : 
            for v in verts: self.append(v)
        
        
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

