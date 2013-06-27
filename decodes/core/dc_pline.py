from decodes.core import *
from . import dc_base, dc_vec, dc_point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "pline.py loaded"

import copy, collections

class PLine(HasPts):
    """
    a simple polyline class
    """
    subclass_attr = ['_edges','_length'] # this list of props is unset anytime this HasPts object changes

    def __init__(self, vertices=None, basis=None):
        """Polyline constructor.
        
            :param vertices: Vertices to build the pline.
            :type vertices: list
            :returns: Polyline.
            :rtype: PLine

        .todo: check if passed an empty array of points
        """
        super(PLine,self).__init__(vertices,basis) #HasPts constructor handles initalization of verts and basis
        self.basis = CS() if (basis is None) else basis # set the basis after appending the points

    @property
    def edges(self):
        """Returns the edges of a PLine.
       
            :result: List of edges of a PLine
            :rtype: [Segment]
        """
        try:
            return self._edges
        except:
            self._edges = [ self.seg(n) for n in range(len(self._verts)-1) ]
            return self._edges

    @property
    def length(self):
        """ Returns the length of this polyline.
        
            :result: Length of this PLine
            :rtype: float
        """
        try:
            return self._length
        except:
            self._length = sum([self.pts[n].distance(self.pts[n+1]) for n in range(-1,len(self.pts)-1) ] )
            return self._length
        
    def reverse(self) :
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        pts = []
        for pt in reversed(self): pts.append(pt)
        rpline = PLine(pts)
        return rpline


    def join (self, other, tol=False) :
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        if self[-1].is_identical(other[0],tol) :
            pts = []
            for s in self : pts.append(s)
            for o in other : pts.append(o)
            pts.pop(len(self))
            print len(self)
            jpline= PLine(pts)
            return jpline
            
        elif self[0].is_identical(other[-1],tol) :
            pts = []
            for o in other : pts.append(o)
            for s in self : pts.append(s)
            pts.pop(len(other))
            jpline= PLine(pts)
            return jpline
            
        elif self [0].is_identical(other[0],tol) : 
            other = other.reverse()
            pts = []
            for o in other : pts.append(o)
            for s in self : pts.append(s)
            pts.pop(len(other))
            jpline= PLine(pts)
            return jpline
            
        elif self [-1].is_identical(other[-1],tol) :
            other = other.reverse()
            pts = []
            for s in self : pts.append(s)
            for o in other : pts.append(o)
            pts.pop(len(self))
            jpline= PLine(pts)
            return jpline
            
        else :
            pts = []
            for s in self : pts.append(s)
            for o in other : pts.append(o)
            jpline= PLine(pts)
            print "new segment created"
            return jpline
            
    def seg(self,index):
        """ Returns a segment of this polyline
       
            :param index: Index of the polyline's segment
            :type index: Int
            :result: Line segment
            :rtype: Segment
        """
        if index >= len(self._verts) : raise IndexError()
        return Segment(self.pts[index],self.pts[index+1])
        
    def eval(self,t):
        """
        evaluates this HasPts at the specified parameter t
        a t-value of 0 will result in a point conincident with HasPts[0]
        a t-value of 1 will result in a point conincident with HasPts[-1]
        """
        if t > 1 : t = t%1.0
        if t < 0 : t = 1.0 - abs(t)%1.0
        for n, ival in enumerate(Interval()//(len(self)-1)):
            if t in ival:
                pa = self.pts[n]
                pb = self.pts[n+1]
                return Point.interpolate(pa,pb,ival.deval(t))
        
    def near(self, p):
        """Returns a tuple of the closest point to a given PLine, the index of the closest segment and the distance from the Point to the near Point.
       
            :param p: Point to look for a near Point on the PLine.
            :type p: Point
            :result: Tuple of near point on PLine, index of near segment and distance from point to near point.
            :rtype: (Point, integer, float)
        """
        #KS: this does not function as advertised, after narrowing down to the nearest segment we need to project the given point
        return False
        npts = [seg.near(p) for seg in self.edges]
        ni = Point.near_index(p,[npt[0] for npt in npts])
        return (npts[ni][0],ni,npts[ni][2])

    def near_pt(self, p):
        """Returns the closest point to a given PLine
       
            :param p: Point to look for a near Point on the PLine.
            :type p: Point
            :result: Near point on Pline.
            :rtype: Point
        """
        return self.near(p)[0]
        
    def __repr__(self):
        return "pline[{0}v]".format(len(self._verts))