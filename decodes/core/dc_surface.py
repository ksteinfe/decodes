from decodes.core import *
from . import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_curve
if VERBOSE_FS: print "surface.py loaded"



class Surface(IsParametrized):
    """
    a simple surface class

    to construct a surface, pass in a function and [optionally] two intervals that determine the a valid range of u&v values
    the function should expect two parameters u and v (float), and return a Point.

    """
    
    def __init__(self, function=None, dom_u=Interval(0,1), dom_v=Interval(0,1), tolerance=None):
        """ Constructs a Curve object. If tolerance is None, Curve.tol = tol_max().
        
            :param function: A function returning points.
            :type function: function
            :param domain: Domain for curve points.
            :type domain: Interval
            :param tolerance: The tolerance of this Surface expressed in domain space
            :type tolerance: float
            :result: Surface object.
            :rtype: Surface
        """
        if function is not None : self._func = function
        self._dom = ival_u, ival_v
        self._tol = self.tol_max
        if tolerance is not None : self.tol = tolerance

        if not isinstance(self.func(self.domain.a), Point) : raise GeometricError("Curve not valid: The given function does not return a point at parameter %s"%(self.domain.a))
        if not isinstance(self.func(self.domain.b), Point) : raise GeometricError("Curve not valid: The given function does not return a point at parameter %s"%(self.domain.b))

        self._surrogate = self._to_pline()


    @property
    def domain_u(self): 
        """
        Returns the Interval domain for the U-direction of this Surface
            :result: Domain of this Surface in the U-direction.
            :rtype: Interval
        """
        return self._dom[0]

    @property
    def u0(self):
        """
        Returns the minimum value for the U domain of this Surface
        """
        return self._dom[0].a

    @property
    def u1(self):
        """
        Returns the maximum value for the U domain of this Surface
        """
        return self._dom[0].b

    @property
    def v0(self):
        """
        Returns the minimum value for the U domain of this Surface
        """
        return self._dom[1].a

    @property
    def v1(self):
        """
        Returns the maximum value for the U domain of this Surface
        """
        return self._dom[1].b

    @property
    def domain_v(self): 
        """
        Returns the Interval domain for the V-direction of this Surface
            :result: Domain of this Surface in the V-direction.
            :rtype: Interval
        """
        return self._dom[1]

    @property
    def tol_max(self):
        """Determines the maximium tolerance as Surface.domain_u.delta / 10 , Surface.domain_v.delta / 10
        """
        return self._dom[0].delta / 10.0, self._dom[1].delta / 10.0

    def deval(self,u,v):
        """ Evaluates this Surface and returns a Plane.
        T is a float value that falls within the defined domain of this Curve.
        Tangent vector determined by a nearest neighbor at distance Curve.tol/100

            :param u: U-value to evaluate the Surface at.
            :type t: float
            :param v: V-value to evaluate the Surface at.
            :type t: float
            :result: Plane.
            :rtype: Plane
        """
        # some rounding errors require something like this:
        if u < self.u0 and u > self.u0-self.tol : u = self.domain_u.a
        if u > self.domain.b and u < self.domain_u.b+self.tol : u = self.domain_u.b

        if t<self.domain.a or t>self.domain.b : raise DomainError("Curve evaluated outside the bounds of its domain: deval(%s) %s"%(t,self.domain))
        pt = self._func(t)
        
        nudge = self.tol/100
        tv = t + nudge
        if tv > self.domain.b :  vec = Vec(pt, self._func(t - nudge)).inverted()
        else : vec = Vec(pt, self._func(tv))
        
        #transform result to curve basis
        if not self.is_baseless:
            #pt.basis = self.basis
            #pt = pt.basis_applied()
            pt = pt * self.basis.xform
            vec = vec * self.basis.xform.strip_translation()
        
        return Plane(pt, vec)

    def eval(self,t):
        """ Evaluates this Curve and returns a Plane.
        T is a normalized float value (0->1) which will be remapped to the domain defined by this Curve.
        equivalent to Curve.deval(Interval.remap(t,Interval(),Curve.domain))
            :param t: Normalized value between 0 and 1, to evaluate a curve.
            :type t: float
            :result: Plane.
            :rtype: Plane
        """
        if t<0 or t>1 : raise DomainError("eval() must be called with a number between 0->1: eval(%s)"%t)
        return self.deval(Interval.remap(t,Interval(),self.domain))
