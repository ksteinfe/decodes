from decodes.core import *
from . import base, vec, point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "plane.py loaded"
import math


class Plane(Vec):
    """
    a simple plane class


    """
    
    def __init__(self, point=Point(), normal=Vec(0,0,1)):
        """ Constructs a Plane object.

        """
        super(Plane,self).__init__(point)
        self._vec = normal.normalized()

    
    @property
    def vec(self): return self._vec
    @vec.setter
    def vec(self, v): self._vec = v.normalized()

    @property
    def normal(self): return self._vec
    @normal.setter
    def normal(self, v): self._vec = v.normalized()

    @property
    def cpt(self): return Point(self.x,self.y,self.z)
    @cpt.setter
    def cpt(self, pt): 
        self.x = pt.x
        self.y = pt.y
        self.z = pt.z