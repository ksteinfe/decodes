from decodes.core import *
from . import dc_base, dc_interval, dc_vec, dc_point, dc_plane, dc_cs #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "dc_circle.py loaded"

import copy, collections
import math

class Circle(Plane):
    """
    a circle class
    inherits all properties of the Plane class
    """
    
    def __init__(self,plane,radius):
        self.x = plane.x
        self.y = plane.y
        self.z = plane.z
        self._vec = plane._vec
        self.rad = radius
        
    @property
    def plane(self):
        return Plane(Point(self.x,self.y,self.z),self._vec)
        
    def __repr__(self): return "circ[{0},{1},{2},{3},{4},{5} r:{6}]".format(self.x,self.y,self.z,self._vec.x,self._vec.y,self._vec.z,self.rad)

    def intersections(self,other):
        '''
        returns intersections with another circle
        '''
        # TODO: this func currently assumes a circle on the xy axis?
        # TODO: move this functionality to the intersections class
        if not self.pln.is_coplanar( other.pln ) : 
            print self.pln.near(other.pln.origin)[0].distance(other.pln.origin)
            print 'circles not coplanar'
            return False
        d = self.cpt.distance(other.cpt)
        if d == 0 : 
            print 'circles share a center point'
            return False
        a = (self.rad**2 - other.rad**2 + d**2)/(2*d)
        h2 = self.rad**2 - a**2
        if h2 < 0 : 
            print 'what, huh?'
            return False
        h = math.sqrt(h2)
        pt = ( other.cpt - self.cpt ) * (a/d) + self.cpt
        if h == 0 : return pt
        vec = Vec(self.cpt,pt).cross(self.pln.vec).normalized(h)
        return [pt - vec, pt + vec]
      
    
