from decodes.core import *
from . import base, vec, point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "pline.py loaded"

import copy, collections

class PLine(Geometry, HasVerts):
    """a polyline class"""
    
    def __init__(self, verts=None):
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
         
    def __repr__(self):
        return "pline[{0}v]".format(len(self._verts))