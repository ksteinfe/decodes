from decodes.core import *
from . import base, vec, point, cs, line, mesh, pgon
if VERBOSE_FS: print "curve.py loaded"

import math


class Curve(Geometry):
    """
    a simple curve class

    to construct a curve, pass in a function and an [optional] interval that determines a valid range of values
    the function should expect a single parameter t(float), and return a Point.

    """
    
    def __init__(self, function=None, domain=Interval(0,1), tolerance=None):
        """ Constructs a Curve object.

        If tolerance is None, Curve.tol = tol_max()
        """
        if function is not None : self._func = function
        self._domain = domain
        self._tol = self.tol_max
        if tolerance is not None : self.tol = tolerance

        if not isinstance(self.func(self.domain.a), Point) : raise GeometricError("Curve not valid: The given function does not return a point at parameter %s"%(self.domain.a))
        if not isinstance(self.func(self.domain.b), Point) : raise GeometricError("Curve not valid: The given function does not return a point at parameter %s"%(self.domain.b))

        self._surrogate = self._to_pline()


    def __truediv__(self,divs): return self.__div__(divs)
    def __div__(self, divs): 
        """
        overloads the division **(/)** operator
        calls Curve.divide(divs)
        """
        return self.divide(divs)
    
    def __floordiv__(self, other): 
        """
        overloads the integer division **(//)** operator
        calls Interval.subdivide(other)
        """
        return self.subdivide(other)

    @property
    def surrogate(self): return self._surrogate

    @property
    def domain(self): return self._domain

    @property
    def func(self): return self._func
    
    @property
    def tol(self): 
        """
        the tolerence of this curve expressed in domain space
        for example, given an interval of 0->1, a tol of 0.1 will result in a curve constructed of 10 segments, evaulated with t-values 0.1 apart
        given an interval 0->PI, a tol of 0.1 will result in a curve constructed of 32 segments, evaluated with t-values less than 0.1 apart
        """
        return self._tol
    @tol.setter
    def tol(self, tolerance): 
        self._tol = tolerance
        if self._tol > self.tol_max : 
            self._tol = self.tol_max
            #warnings.warn("Curve tolerance too high relative to curve domain - Resetting.  tolerance (%s) > Curve.max_tol(%s)"%(tolerance,self.tol_max))
        self._surrogate = self._to_pline()
    
    @property
    def tol_max(self):
        """Determines the maximium tolerance as Curve.domain.delta / 10
        """
        return self._domain.delta / 10.0
    

    def deval(self,t):
        """ Evaluates this Curve and returns a Plane.
        T is a float value that falls within the defined domain of this Curve.
        """
        if t<self.domain.a or t>self.domain.b : raise DomainError("Curve evaluated outside the bounds of its domain: deval(%s) %s"%(t,self.domain))
        pt = self._func(t)
        
        nudge = self.tol/100
        tv = t + nudge
        if tv > self.domain.b :  vec = Vec(pt, self._func(t - nudge)).inverted()
        else : vec = Vec(pt, self._func(tv))

        return Plane(pt, vec)

    def eval(self,t):
        """ Evaluates this Curve and returns a Plane.
        T is a normalized float value (0->1) which will be remapped to the domain defined by this Curve.
        equivalent to Curve.deval(Interval.remap(t,Interval(),Curve.domain))
        """
        if t<0 or t>1 : raise DomainError("eval() must be called with a number between 0->1: eval(%s)"%t)
        return self.deval(Interval.remap(t,Interval(),self.domain))

    def divide(self, divs=10, include_last=True):
        """Divides this Curve into a list of evaluated Planes equally spaced between Curve.domain.a and Curve.domain.b.
        If include_last is True (by default), returned list will contain divs+1 Points.
        If include_last is False, returned list will not include the point at Curve.domain.b
        
            :param divs: Number of segments to divide this curve into.
            :type divs: int
            :returns: List of points 
            :rtype: [Point]
        """
        return [self.deval(t) for t in self.domain.divide(divs,include_last)]

    def subdivide(self, divs):
        """Divides this Curve into a list of equal size sub-Curves.
        Each sub-Curve will adopt the tol of this curve, unless greater than the tol_max of the subcurve
        
            :param divs: Number of subcurves.
            :type divs: int
            :returns: List of sub-Curves. 
            :rtype: [Curve]
        """
        curves = []
        for subd in self.domain//divs: curves.append(self.subcurve(subd))
        return curves

    def subcurve(self,domain):
        """Returns a new Curve which is a copy of this Curve with the given Interval as the domain

        """
        return Curve(self.func,domain,self.tol)


    def near(self,pt,tolerance=None,max_recursion=20):
        """ Finds a location on this curve which is nearest to the given Point.
            Unstable and inaccurate.
            Recursive function that searches for further points until the search area shrinks to given tolerance (Curve.tol/10 by default) in domain space.
            Returns a tuple containing a Point, a t-value associated with this point, and the distance from this Point to the given Point
        """
        if tolerance is None : tolerance = self.tol/10.0
        t = self._nearfar(Point.near_index,pt,tolerance,max_recursion)
        result = self.deval(t)
        return(result,t,pt.distance(result.cpt))

    def far(self,pt,tolerance=None,max_recursion=20):
        """ Finds a location on this curve which is furthest from the given Point.
            Unstable and inaccurate.
            Recursive function that searches for closer points until the search area shrinks to given tolerance (Curve.tol/10 by default) in domain space.
            Returns a tuple containing a Point, a t-value associated with this point, and the distance from this Point to the given Point
        """
        if tolerance is None : tolerance = self.tol/10.0
        t = self._nearfar(Point.far_index,pt,tolerance,max_recursion)
        result = self.deval(t)
        return(result,t,pt.distance(result.cpt))


    def _nearfar(self,func_nf,pt,tolerance,max_recursion):
        def sub(crv):
            divs = 8 # number of divisions to cut the given curve into
            buffer = 1.5 # multiplier for resulting area
            ni = func_nf(pt,[pln.cpt for pln in crv/divs]) # divide the curve and find the nearest or furthest point (depending on the function that was provided)
            nd = crv.domain.eval(ni/float(divs)) # find the domain value associated with this point
            domain = Interval( nd-(buffer*crv.domain.delta/divs), nd+(buffer*crv.domain.delta/divs) ) #  create a new domain that may contain the nearest point
            if domain.a < crv.domain.a : domain.a = crv.domain.a
            if domain.b > crv.domain.b : domain.b = crv.domain.b
            return crv.subcurve(domain),domain.a == crv.domain.a, domain.b == crv.domain.b # return a new curve with this domain

        crv, force_spt, force_ept = sub(self)
        n = 1
        while crv.domain.delta > tolerance : 
            crv, at_spt, at_ept = sub(crv)
            force_spt = force_spt and at_spt
            force_ept = force_ept and at_ept
            n+=1
            if n >= max_recursion : break

        t = crv.domain.eval(0.5)
        if force_spt : t = crv.domain.eval(0.0)
        if force_ept : t = crv.domain.eval(1.0)
        return t


    def _to_pline(self):
        return PLine([self.deval(t) for t in self.domain.divide(int(math.ceil(self.domain.delta/self.tol)),True)])



    @staticmethod
    def circle(ctr,rad):
        """ constructs a Curve object that describes a circle given: a center (Point) and radius (float)
            the plane of the circle will always be parallel to the xy-plane
        """
        def func(t):
            x = rad*math.cos(t)
            y = rad*math.sin(t)
            return Point(x,y)+ctr
        return Curve(func,Interval(0,math.pi*2))

    @staticmethod
    def helix(ctr,rad,rise_per_turn=1.0,number_of_turns=3.0):
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