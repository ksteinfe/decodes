from decodes.core import *
from . import base, interval, vec, point, cs #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "polygon.py loaded"

import copy, collections
import math

class PGon(HasPts):
    """
    a very simple 2d polygon class
    Polygons limit their vertices to x and y dimensions, and enforce that they employ a basis.    Transformations of a polygon should generally be applied to the basis.    Any tranfromations of the underlying vertices should ensure that the returned vectors are limited to x and y dimensions
    """
    
    def __init__(self, vertices=None, basis=None):
        """ PGon Constructor.
        
            :param vertices: List of vertices to build the polygon.
            :type vertices: list
            :param basis: Plane basis for the PGon.
            :type basis: Basis
            :returns: PGon object. 
            :rtype: PGon
        """ 
        super(PGon,self).__init__() #HasPts constructor initializes list of verts and an empty basis
        self.basis = CS() if (basis is None) else basis
        if (vertices is not None) : 
            for v in vertices: self.append(v)
        
        
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
        
    def edges(self):
        """Returns the edges of a PGon.
       
            :result: List of edges of a PGon.
            :rtype: [Segment]
        """
        edges = []
        while i < len(self):
            edges.append(Segment(self[i],self[i+1]))
        edges.append(Segment(self[0], self[-1]))
        return edges
        
    def near(self, p):
        """Returns a tuple of the closest point to a given PGon, the index of the closest segment and the distance from the Point to the near Point.
       
            :param p: Point to look for a near Point on the PGon.
            :type p: Point
            :result: Tuple of near point on PGon, index of near segment and distance from point to near point.
            :rtype: (Point, integer, float)
        """
        npts = [seg.near(p) for seg in self.edges]
        ni = Point.near_index(p,[npt[0] for npt in npts])
        return (npts[ni][0],ni,npts[ni][2])

    def near_pt(self, p):
        """Returns the closest point to a given PGon
       
            :param p: Point to look for a near Point on the PGon.
            :type p: Point
            :result: Near point on PGon.
            :rtype: Point
        """
        npts = [seg.near(p) for seg in self.edges]
        ni = Point.near_index(p,[npt[0] for npt in npts])
        return npts[ni][0]

