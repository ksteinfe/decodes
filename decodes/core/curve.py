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
        """ Constructs a Curve object. If tolerance is None, Curve.tol = tol_max().
        
            :param function: A function returning points.
            :type function: function
            :param domain: Domain for curve points.
            :type domain: Interval
            :param tolerance: Distance between points.
            :type tolerance: float
            :result: Curve object.
            :rtype: Curve
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
        """overloads the division **(/)** operator. Calls Curve.divide(divs)
            :param divs: Number of curve planes to divide the curve in.
            :type divs: float
            :result: List of curve segments.
            :rtype: [Point]
        """
        return self.divide(divs)
    
    def __floordiv__(self, divs): 
        """
        overloads the integer division **(//)** operator. calls Interval.subdivide(divs)
            :param divs: Number of segments to divide the curve in.
            :type divs: float
            :result: List of curve segments.
            :rtype: [Curve]
        """
        return self.subdivide(divs)

    @property
    def surrogate(self): return self._surrogate

    @property
    def appx_length(self): 
        """
        Returns the approximate length of a curve
            :result: Approximate length of a curve.
            :rtype: float
        """
        return self._surrogate.length

    @property
    def domain(self): 
        """
        Returns the Interval domain of a curve
            :result: Domain of a curve.
            :rtype: Interval
        """
        return self._domain

    @property
    def func(self): return self._func
    
    @property
    def tol(self): 
        """the tolerence of this curve expressed in domain space
        for example, given an interval of 0->1, a tol of 0.1 will result in a curve constructed of 10 segments, evaulated with t-values 0.1 apart
        given an interval 0->PI, a tol of 0.1 will result in a curve constructed of 32 segments, evaluated with t-values less than 0.1 apart
            :result: Sets the distance between point of a curve.
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
            :param t: Value to evaluate the curve at.
            :type t: float
            :result: Plane.
            :rtype: Plane
        """
        # some rounding errors require something like this:
        if t < self.domain.a and t > self.domain.a-self.tol : t = self.domain.a
        if t > self.domain.b and t < self.domain.b+self.tol : t = self.domain.b

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
            :param t: Normalized value between 0 and 1, to evaluate a curve.
            :type t: float
            :result: Plane.
            :rtype: Plane
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
            :param domain: New curve with a new given interval.
            :type domain: Interval
            :result: Copy of curve with new domain.
            :rtype: Curve
        """
        return Curve(self.func,domain,self.tol)


    def near(self,pt,tolerance=None,max_recursion=20):
        """ Finds a location on this curve which is nearest to the given Point.
        Unstable and inaccurate.
        Recursive function that searches for further points until the search area shrinks to given tolerance (Curve.tol/10 by default) in domain space.
        Returns a tuple containing a Point, a t-value associated with this point, and the distance from this Point to the given Point
            
            :param pt: Point to look for the nearest point on a curve.
            :type pt: Point
            :param tolerance: Tolerance to search for the near point. Defaults to None.
            :type tolerance: float
            :param max_recursion: Maximum number of loops to look for the nearest point. Defaults to 20.
            :type max_recursion: integer
            :result: Tuple containing a Plane, a t-value associated with this point, and the distance from this Point to the given Point.
            :rtype: (Plane, float, float)
        """
        if tolerance is None : tolerance = self.tol/10.0
        t = self._nearfar(Point.near_index,pt,tolerance,max_recursion)
        result = self.deval(t)
        return(result,t,pt.distance(result.origin))

    def near_pt(self,pt,tolerance=None,max_recursion=20):
        """ Finds a location on this curve which is nearest to the given Point.
        Unstable and inaccurate.
        Recursive function that searches for further points until the search area shrinks to given tolerance (Curve.tol/10 by default) in domain space.
        Returns a Point
            
            :param pt: Point to look for the nearest point on a curve.
            :type pt: Point
            :param tolerance: Tolerance to search for the near point. Defaults to None.
            :type tolerance: float
            :param max_recursion: Maximum number of loops to look for the nearest point. Defaults to 20.
            :type max_recursion: integer
            :result: Plane.
            :rtype: Plane
        """

        return self.near(pt,tolerance,max_recursion)[0]
        
    def far(self,pt,tolerance=None,max_recursion=20):
        """ Finds a location on this curve which is furthest from the given Point.
        Unstable and inaccurate.
        Recursive function that searches for closer points until the search area shrinks to given tolerance (Curve.tol/10 by default) in domain space.
        Returns a tuple containing a Point, a t-value associated with this point, and the distance from this Point to the given Point
            :param pt: Point to look for the farthest point on a curve.
            :type pt: Point
            :param tolerance: Tolerance to search for the far point. Defaults to None.
            :type tolerance: float
            :param max_recursion: Maximum number of loops to look for the farthest point. Defaults to 20.
            :type max_recursion: integer
            :result: Tuple containing a Plane, a t-value associated with this point, and the distance from this Point to the given Point.
            :rtype: (Plane, float, float)
        """

        return(result,t,pt.distance(result.origin))

    def far_pt(self,pt,tolerance=None,max_recursion=20):
        """ Finds a location on this curve which is furthest to the given Point.
        Unstable and inaccurate.
        Recursive function that searches for further points until the search area shrinks to given tolerance (Curve.tol/10 by default) in domain space.
        Returns a Point
            
            :param pt: Point to look for the furthest point on a curve.
            :type pt: Point
            :param tolerance: Tolerance to search for the far point. Defaults to None.
            :type tolerance: float
            :param max_recursion: Maximum number of loops to look for the nearest point. Defaults to 20.
            :type max_recursion: integer
            :result: Plane.
            :rtype: Plane
        """

        return self.far(pt,tolerance,max_recursion)[0]

    def _nearfar(self,func_nf,pt,tolerance,max_recursion):
        def sub(crv):
            divs = 8 # number of divisions to cut the given curve into
            buffer = 1.5 # multiplier for resulting area
            ni = func_nf(pt,[pln.origin for pln in crv/divs]) # divide the curve and find the nearest or furthest point (depending on the function that was provided)
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
        """ Creates a PLine from a curve.

            :result: Returns a PLine built from a curve.
            :rtype: PLine
        """
        return PLine([self.deval(t) for t in self.domain.divide(int(math.ceil(self.domain.delta/self.tol)),True)])



    @staticmethod
    def circle(ctr,rad):
        """ constructs a Curve object that describes a circle given: a center (Point) and radius (float)
        the plane of the circle will always be parallel to the xy-plane
        
            :param ctr: Center point of the circle.
            :type ctr: Point
            :param rad: Radius of the circle.
            :type rad: float
            :result: Curve describing a circle.
            :rtype: Curve
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
            :param ctr: Center point of the helix.
            :type ctr: Point
            :param rad: Radius of the helix.
            :type rad: float
            :param rise_per_turn: Amount the helix rises in z per turn.
            :type rise_per_turn: float
            :param number_of_turns: Number of turns the helix has.
            :type number_of_turns: float
            :result: Helix Curve object.
            :rtype: Curve
        """
        b = rise_per_turn/(math.pi*2)
        def func(t):
            x = rad*math.cos(t)
            y = rad*math.sin(t)
            z = b*t
            return Point(x,y,z)+ctr
        return Curve(func,Interval(0,math.pi*2*number_of_turns))

    @staticmethod
    def bezier(cpts):
        """ Constructs a bezier curve.
        
            :param cpts: List of points the bezier curve is going to be built with.
            :type cpts: [Point]
        """
        def func(t):
            pts = cpts
            while len(pts) > 1: pts = [Point.interpolate(pts[n],pts[n+1],t) for n in range(len(pts)-1)]
            return pts[0]

        return Curve(func)

    @staticmethod
    def hermite(cpts):

        # from http://paulbourke.net/miscellaneous/interpolation/
        def hermite_interpolate(y0,y1,y2,y3,mu,tension,bias):
            mu2 = mu * mu
            mu3 = mu2 * mu
            m0 = (y1-y0)*(1+bias)*(1-tension)/2
            m0 += (y2-y1)*(1-bias)*(1-tension)/2
            m1 = (y2-y1)*(1+bias)*(1-tension)/2
            m1 += (y3-y2)*(1-bias)*(1-tension)/2
            a0 = 2*mu3 - 3*mu2 + 1
            a1 = mu3 - 2*mu2 + mu
            a2 = mu3 -   mu2
            a3 = -2*mu3 + 3*mu2
            return(a0*y1+a1*m0+a2*m1+a3*y2)
        
        # find total distance between given points, and construct intervals
        ivals = []
        a,b = 0,0
        for n in range(len(cpts)-1):
            b = a + cpts[n].distance(cpts[n+1])
            ivals.append(Interval(a,b))
            a = b

        # add tangent control points
        cpts.insert(0,cpts[0]+Vec(cpts[1],cpts[0]))
        cpts.append(cpts[-1]+Vec(cpts[-2],cpts[-1]))
        def func(t):
            #if t==1: t_index = len(cpts)-4
            #if t==0: t_index = 0
            #else : t_index = int(math.floor(t*(len(cpts)-3))) 
            
            t_index = int(Interval.remap(t,Interval(),Interval(0,len(cpts)-3)))
            t = t*ivals[-1].b # remap t from 0->1 to 0->length
            t_index = -1
            for n in range(len(ivals)) : 
                if t in ivals[n] : 
                    t_index = n
                    break
            p0 = cpts[t_index]
            p1 = cpts[t_index+1]
            p2 = cpts[t_index+2]
            p3 = cpts[t_index+3]
            x = hermite_interpolate(p0.x,p1.x,p2.x,p3.x,ivals[t_index].deval(t),0,0)
            y = hermite_interpolate(p0.y,p1.y,p2.y,p3.y,ivals[t_index].deval(t),0,0)
            z = hermite_interpolate(p0.z,p1.z,p2.z,p3.z,ivals[t_index].deval(t),0,0)
            return Point(x,y,z)
        
        return Curve(func)


