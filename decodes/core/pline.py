from decodes.core import *
from . import base, vec, point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "pline.py loaded"

import copy, collections

class PLine(HasPts):
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
        super(PLine,self).__init__() #HasPts constructor initializes list of verts
        if (verts is not None) : 
            for v in verts: self.append(v)
    
    def __repr__(self):
        return "pline[{0}v]".format(len(self._verts))