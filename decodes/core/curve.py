from decodes.core import *
from . import base, vec, point, cs, line, mesh, pgon
if VERBOSE_FS: print "curve.py loaded"

import math



def circular_curve(ctr,rad):
    """ constructs a Curve object that describes a circle given: a center (Point) and radius (float)
        the plane of the circle will always be parallel to the xy-plane
    """
    def func(t):
        x = rad*math.cos(t)
        y = rad*math.sin(t)
        return Point(x,y)+ctr
    return Curve(func,Interval(0,math.pi*2))

def helical_curve(ctr,rad,rise_per_turn=1.0,number_of_turns=3.0):
    """ constructs a Curve object that describes a helix given: a center (Point), a radius (float), a rise_per_turn (float), and a number_of_turns (float)
        the plane of the circle of the helix will always be parallel to the xy-plane
    """
    b = rise_per_turn/(math.pi*2)
    def func(t):
        x = rad*math.cos(t)
        y = rad*math.sin(t)
        z = b*t
        return Point(x,y,z)+ctr
    return Curve(func,Interval(0,math.pi*2*number_of_turns))


class Curve(Geometry):
    """
    a simple curve class

    to construct a curve, pass in a function and an [optional] interval that determines a valid range of values
    the function should expect a single parameter t(float), and return a Point.
    """
    def __init__(self, function=None, domain=Interval(0,1)):
        if function is not None : self._func = function
        self._domain = domain
        self._tol = self._domain.delta / 20

    def eval(self,t):
        """
        other should be a float value that falls within the defined domain of this curve (by default 0->1)
        """
        return self._func(t)

    @property
    def domain(self): return self._domain
    @domain.setter
    def domain(self, ival): self._domain = ival

    @property
    def func(self): return self._func
    @func.setter
    def func(self, function): self._func = function
      
    @property
    def tol(self): 
        """
        the tolerence of this curve expressed in domain space
        for example, given an interval of 0->1, a tol of 0.1 will result in a curve constructed of 10 segments, evaulated with t-values 0.1 apart
        given an interval 0->PI, a tol of 0.1 will result in a curve constructed of 32 segments, evaluated with t-values less than 0.1 apart
        """
        return self._tol
    @tol.setter
    def tol(self, tolerance): self._tol = tolerance

    def to_pline(self):
        return PLine([self.eval(t) for t in self.domain.divide(int(math.ceil(self.domain.delta/self.tol)),True)])
