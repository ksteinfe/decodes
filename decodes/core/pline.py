from decodes.core import *
from . import base, vec, point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "pline.py loaded"

import copy, collections

class PLine(Geometry, HasVerts):
    """
    a simple polyline class
    """
    
    def __init__(self, verts=None):
        """Polyline constructor.
        
            :param verts: Vertices to build the pline.
            :type verts: list
            :returns: Polyline.
            :rtype: PLine
        """
        super(PLine,self).__init__()
        self._verts = []
        if (verts is not None) : 
            for v in verts: self.append(v)
    
    def basis_applied(self, copy_children=True): 
        pass
        #return self
        #TODO: copy this functionality from Mesh class
    
    def basis_stripped(self, copy_children=True): 
        pass
        #return self
        #TODO: copy this functionality from Mesh class
        
    @property
    def centroid(self):
        """Returns the centroid of a pline.
        
            :returns: Centroid (point).
            :rtype: Point
        """
        return Point.centroid(self.verts)
         
    def __repr__(self):
        return "pline[{0}v]".format(len(self._verts))