from decodes.core import *
from . import dc_base, dc_vec, dc_point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "pline.py loaded"

import copy, collections

class PLine(HasPts):
    """
    a simple polyline class
    """
    
    def __init__(self, vertices=None):
        """Polyline constructor.
        
            :param vertices: Vertices to build the pline.
            :type vertices: list
            :returns: Polyline.
            :rtype: PLine

        .todo: check if passed an empty array of points
        """
        super(PLine,self).__init__() #HasPts constructor initializes list of verts and an empty basis
        if (vertices is not None) : 
            for v in vertices: self.append(v)
    
    @property
    def edges(self):
        """Returns the edges of a PLine.
       
            :result: List of edges of a PLine
            :rtype: [Segment]
        """
        edges = []
        for n in range(len(self)-1):
            edges.append(self.seg(n))
        return edges

    @property
    def length(self):
        """ Returns the length of this polyline.
        
            :result: Length of this PLine
            :rtype: float
        """
        return sum([edge.length for edge in self.edges])

    def seg(self,index):
        """ Returns a segment of this polyline
       
            :param index: Index of the polyline's segment
            :type index: Int
            :result: Line segment
            :rtype: Segment
        """
        if index >= len(self) : raise IndexError()
        return Segment(self.pts[index],self.pts[index+1])
        
        
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