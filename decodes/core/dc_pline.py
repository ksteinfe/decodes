from decodes.core import *
from . import dc_base, dc_vec, dc_point, dc_has_pts #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print("pline.py loaded")

import copy, collections

class PLine(HasPts):
    """
    a simple polyline class
    """
    # TOD: remove all subclass_attr for PLine
    subclass_attr = ['_edges','_length'] # this list of props is unset anytime this HasPts object changes
    
    def __init__(self, vertices=None, basis=None):
        """ Polyline constructor.
        
            :param vertices: Vertices to build the pline.
            :type vertices: list
            :param basis: Basis of polyline.
            :type basis: basis
            :returns: Polyline.
            :rtype: PLine
            
            ::
            
                pts=[Point(i,i,i) for i in range(10)]
                my_pline=PLine(pts)
        
        """
        #todo: check if passed an empty array of points
        if vertices is None or len(vertices)<2: raise GeometricError("Plines must be constructed with at least two points")
        super(PLine,self).__init__(vertices,basis) #HasPts constructor handles initialization of verts and basis
        #self.basis = CS() if (basis is None) else basis # set the basis after appending the points

    @property
    def edges(self):
        """ Returns the edges of a PLine.
       
            :result: List of edges of a PLine
            :rtype: [Segment]
            
            
            ::
            
                my_pline.edges
        """
        try:
            return copy.copy(self._edges)
        except:
            self._edges = tuple([ self.seg(n) for n in range(len(self)-1) ])
            return copy.copy(self._edges)

    @property
    def length(self):
        """ Returns the length of this PLine.
        
            :result: Length of this PLine
            :rtype: float
            
            TODO: better to not store this, but calculate as needed?
            
            ::
            
                my_pline.length
        """
        try:
            return self._length
        except:
            self._length = sum([self.pts[n].distance(self.pts[n+1]) for n in range(-1,len(self.pts)-1) ] )
            return self._length
        
    def reversed(self) :
        """ Returns a copy of this PLine with the vertices reversed
        
            :result: Polyline.
            :rtype: PLine
        """
        return PLine(reversed(self._verts),self.basis)


    def join (self, other, tol=False) :
        """ Joins this polyline with a given polyline.
            
            :param other: Polyline to join with this polyline.
            :type other: PLine
            :param tol: Tolerance of difference.
            :type tol: bool.
            :result: New joined Polyline.
            :rtype: PLine
            
            ::
            
                pts_2=[Point(i+1, i, i-1) for in range(5)]
                my_pline2=PLine(pts_2)
                
                my_pline.join(my_pline2)
            
        """
        if self._basis != other.basis: raise BasisError("The basis for this PLine and the PLine you're joining it to do not match.")
        self._unset_attr() # call this when any of storable properties (subclass_attr or class_attr) changes
        if self[-1].is_equal(other[0],tol) :
            pts = []
            for s in self : pts.append(s)
            for o in other : pts.append(o)
            pts.pop(len(self))
            print(len(self))
            jpline= PLine(pts)
            return jpline
            
        elif self[0].is_equal(other[-1],tol) :
            pts = []
            for o in other : pts.append(o)
            for s in self : pts.append(s)
            pts.pop(len(other))
            jpline= PLine(pts)
            return jpline
            
        elif self[0].is_equal(other[0],tol) : 
            other = other.reverse()
            pts = []
            for o in other : pts.append(o)
            for s in self : pts.append(s)
            pts.pop(len(other))
            jpline= PLine(pts)
            return jpline
            
        elif self[-1].is_equal(other[-1],tol) :
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
            print("new segment created")
            return jpline
            
    def seg(self,idx):
        """ Returns a segment of this polyline.
       
            :param index: Index of the polyline's segment
            :type index: Int
            :result: Line segment
            :rtype: Segment
            
            ::
                
                my_pline.seg(2)
        """
        idx = idx%(len(self)-1)
        return Segment(self.pts[idx],self.pts[idx+1])
        
    def eval(self,t):
        """| Evaluates this PLine at the specified parameter t.
           | A t-value of 0 will result in a point coincident with PLine.pts[0].
           | A t-value of 1 will result in a point coincident with PLine.pts[-1].
           
           :param t: A decimal number between [0:1]
           :type t: float
           :result: A point on the polyline.
           :rtype: Point
           
           ::
                
                my_pline.eval(0.5)
           
        """
        if t > 1 or t < 0 : raise IndexError("PLines must be evaluated with 0.0 <= t <= 1.0")
        if t == 0.0 : return self.pts[0]
        if t == 1.0 : return self.pts[-1]

        for seg,ival in zip(self.edges, Interval()//(len(self)-1)):
            if t in ival: return seg.eval(ival.deval(t))
        
    def near(self, p):
        """ Returns a tuple of the closest point to a given PLine, the index of the closest segment, and the distance from the Point to the near Point.
       
            :param p: Point to look for a near Point on the PLine.
            :type p: Point
            :result: Tuple of near point on PLine, index of near segment and distance from point to near point.
            :rtype: (Point, integer, float)
            
            ::
            
                my_pline.near(Point(1,2,3))
        """
        #KS: this does not function as advertised, after narrowing down to the nearest segment we need to project the given point
        return False
        npts = [seg.near(p) for seg in self.edges]
        ni = Point.near_index(p,[npt[0] for npt in npts])
        return (npts[ni][0],ni,npts[ni][2])

    def near_pt(self, p):
        """ Returns the closest point to a given PLine.
       
            :param p: Point to look for a near Point on the PLine.
            :type p: Point
            :result: Near point on Pline.
            :rtype: Point
        """
        return self.near(p)[0]
        
    def __repr__(self):
        return "pline[{0}v]".format(len(self._verts))