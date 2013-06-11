from decodes.core import *
from . import dc_base, dc_interval, dc_vec, dc_point, dc_cs #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
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
        #TODO: if i pass in verices but no basis, try and figure out what the CS should be and project all points to plane

        super(PGon,self).__init__() #HasPts constructor initializes list of verts and an empty basis
        self.basis = CS() if (basis is None) else basis
        if (vertices is not None) : 
            for v in vertices: self.append(v)
    
        
    def seg(self,index):
        """ Returns a segment of this Polygon
        The returned line segment will contain a copy of the Points stored in the segment.
        
            :param index: Index of the desired segment.
            :type index: Int
            :returns: Segment object. 
            :rtype: Segment
        """
        if index >= len(self) : raise IndexError()
        if index == len(self)-1 : return Segment(self.pts[index],self.pts[0])
        #TODO: handle negative indices
        return Segment(self.pts[index],self.pts[index+1])
        

    @property
    def edges(self):
        """Returns the edges of a PGon.
       
            :result: List of edges of a PGon
            :rtype: [Segment]
        """
        edges = []
        for n in range(len(self)):
            edges.append(self.seg(n))
        return edges
        
    def near(self, p):
        """Returns a tuple of the closest point to a given PGon, the index of the closest segment and the distance from the Point to the near Point.
       
            :param p: Point to look for a near Point on the PGon.
            :type p: Point
            :result: Tuple of near point on PGon, index of near segment and distance from point to near point.
            :rtype: (Point, integer, float)
        """
        #KS: this does not function as advertised, after narrowing down to the nearest segment we need to project the given point
        return False
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
        return self.near(p)[0]

    def __repr__(self): return "pgon[{0}v]".format(len(self._verts))
    
    def basis_applied(self):
        clone = super(PGon,self).basis_applied()
        clone.basis = CS()
        return clone

    def basis_stripped(self):
        clone = super(PGon,self).basis_stripped()
        clone.basis = CS()
        return clone

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
        w2 = w/2.0
        h2 = h/2.0
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

class Bounds2d(Geometry):
    """
    A 2d rectangular boudary class with centerpoint, width and height
    """
    def __init__ (self, center, w, h):
        self.cpt = center
        self._halfwidth = w/2
        self._halfheight = h/2
        
    @property
    def iterval_x():
        return Interval(self.cpt.x-(self._halfwidth),self.cpt.x+(self._halfwidth))
    @property
    def iterval_y():
        return Interval(self.cpt.y-(self._halfheight),self.cpt.y+(self._halfheight))

    @property
    def corners(self):
        """
        starts at bottom left and moves clockwise
        """
        cpts = []
        cpts.append(Point(self.cpt.x-(self._halfwidth),self.cpt.y-(self._halfheight)))
        cpts.append(Point(self.cpt.x-(self._halfwidth),self.cpt.y+(self._halfheight)))
        cpts.append(Point(self.cpt.x+(self._halfwidth),self.cpt.y+(self._halfheight)))
        cpts.append(Point(self.cpt.x+(self._halfwidth),self.cpt.y-(self._halfheight)))
        return cpts
        
    def contains(self, pt):
        lbx = self.cpt.x - self._halfwidth
        ubx = self.cpt.x + self._halfwidth
        lby = self.cpt.y - self._halfheight
        uby = self.cpt.y + self._halfheight
        if lbx < pt.x < ubx and lby < pt.y < uby : return True
        else:return False
    
    def intersects(self, other) :
        for p in other.corners :
            if self.contains(p) : return True
        for p in self.corners :
            if other.contains(p) : return True
        return False