from decodes.core import *
from . import base, vec, point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
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
        """
        super(PLine,self).__init__() #HasPts constructor initializes list of verts and an empty basis
        if (vertices is not None) : 
            for v in vertices: self.append(v)
    

    def seg(self,index):
        """ Returns a segment of this polyline
        """
        if index >= len(self) : raise IndexError()
        return Segment(self[index],self[index+1])

    def __repr__(self):
        return "pline[{0}v]".format(len(self._verts))