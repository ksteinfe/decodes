from decodes.core import *
from . import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon
if VERBOSE_FS: print "curve.py loaded"

import math


class IsParametrized(Geometry):
    """
    Abstract class for describing functionality common to Curves and Surfaces
    """
    def __truediv__(self,divs): return self.__div__(divs)
    def __div__(self, divs): 
        """Overloads the division **(/)** operator. Calls Curve.divide(divs).
        
            :param divs: Number of curve planes to divide the curve in.
            :type divs: float
            :result: List of curve segments.
            :rtype: [Point]
        """
        return self.divide(divs)
    
    def __floordiv__(self, divs): 
        """Overloads the integer division **(//)** operator. Calls Interval.subdivide(divs).
        
            :param divs: Number of segments to divide the curve in.
            :type divs: float
            :result: List of curve segments.
            :rtype: [Curve]
        """
        return self.subdivide(divs)

    @property
    def func(self): return self._func


    def near(self,pt,tolerance=None,max_recursion=20,resolution=8):
        """| Finds a location on this curve which is nearest to the given Point.
           | Unstable and inaccurate.
           | Recursive function that searches for closer points (at a given division resolution) until the search area shrinks to given tolerance (Curve.tol/10 by default) in domain space.
           | Returns a tuple containing a Point, a t-value associated with this point, and the distance from this Point to the given Point.
            
           :param pt: Point to look for the nearest point on a curve.
           :type pt: Point
           :param tolerance: Tolerance to search for the near point. Defaults to None.
           :type tolerance: float
           :param max_recursion: Maximum number of loops to look for the nearest point. Defaults to 20.
           :type max_recursion: int
           :result: Tuple containing a Point, a t-value associated with this point, and the distance from this Point to the given Point.
           :rtype: (Point, float, float)
           
           ::

                def func(u):
                    return Point(math.sin(u),u)
                Inv=Interval(0,20)
                crv = Curve(func,Inv)

                n_tup=crv.near(Point(0,0,0))

        """
        if tolerance is None : tolerance = self.tol/10.0
        t = self._nearfar(Point.near_index,pt,tolerance,max_recursion,resolution)
        result = self.deval(t)
        return(result,t,pt.distance(result))

    def near_pt(self,pt,tolerance=None,max_recursion=20,resolution=8):
        """| Finds a location on this curve which is nearest to the given Point.
           | Unstable and inaccurate.
           | Recursive function that searches for closer points (at a given division resolution) until the search area shrinks to given tolerance (Curve.tol/10 by default) in domain space.
           | Returns a Point.
            
           :param pt: Point to look for the nearest point on a curve.
           :type pt: Point
           :param tolerance: Tolerance to search for the near point. Defaults to None.
           :type tolerance: float
           :param max_recursion: Maximum number of loops to look for the nearest point. Defaults to 20.
           :type max_recursion: int
           :result: Point.
           :rtype: Point
        """

        return self.near(pt,tolerance,max_recursion,resolution)[0]
        
    def far(self,pt,tolerance=None,max_recursion=20,resolution=8):
        """| Finds a location on this curve which is furthest from the given Point.
           | Unstable and inaccurate.
           | Recursive function that searches for further points (at a given division resolution) until the search area shrinks to given tolerance (Curve.tol/10 by default) in domain space.
           | Returns a tuple containing a Point, a t-value associated with this Point, and the distance from this Point to the given Point.
            
           :param pt: Point to look for the farthest point on a curve.
           :type pt: Point
           :param tolerance: Tolerance to search for the far point. Defaults to None.
           :type tolerance: float
           :param max_recursion: Maximum number of loops to look for the farthest point. Defaults to 20.
           :type max_recursion: int
           :result: Tuple containing a Point, a t-value associated with this point, and the distance from this Point to the given Point.
           :rtype: (Point, float, float)
           
           ::
           
                def func(u):
                    return Point(math.sin(u),u)
                Inv=Interval(0,20)
                crv = Curve(func,Inv)   
                
                f_tup=crv.far(Point(0,0,0))
                      
        """
        if tolerance is None : tolerance = self.tol/10.0
        t = self._nearfar(Point.far_index,pt,tolerance,max_recursion,resolution)
        result = self.deval(t)
        return(result,t,pt.distance(result))

    def far_pt(self,pt,tolerance=None,max_recursion=20,resolution=8):
        """| Finds a location on this curve which is furthest from the given Point.
           | Unstable and inaccurate.
           | Recursive function that searches for further points u (at a given division resolution) ntil the search area shrinks to given tolerance (Curve.tol/10 by default) in domain space.
           | Returns a Point.
            
           :param pt: Point to look for the furthest point on a curve.
           :type pt: Point
           :param tolerance: Tolerance to search for the far point. Defaults to None.
           :type tolerance: float
           :param max_recursion: Maximum number of loops to look for the nearest point. Defaults to 20.
           :type max_recursion: int
           :result: Point.
           :rtype: Point
        """

        return self.far(pt,tolerance,max_recursion,resolution)[0]



class Curve(HasBasis,IsParametrized):
    """
    A simple curve class.

    To construct a curve, pass in a function and an [optional] interval that determines a valid range of values.
    The function should expect a single parameter t(float), and return a Point.

    """
    
    def __init__(self, function=None, domain=Interval(0,1), tolerance=None, basis=None):
        """ Constructs a Curve object. If tolerance is None, Curve.tol = tol_max().
        
           :param function: A function returning points.
           :type function: function
           :param domain: Domain for curve points.
           :type domain: Interval
           :param tolerance: The tolerance of this curve expressed in domain space.
           :type tolerance: float
           :result: Curve object.
           :rtype: Curve
            
           :: 
           
                def func(u):
                    return Point(math.sin(u),u)
                Inv=Interval(0,20)
                crv = Curve(func,Inv)
        """
        if function is not None : self._func = function
        self._dom = domain
        self._tol = self.tol_max
        if tolerance is not None : self.tol = tolerance
        if basis is not None : self._basis = basis

        for t in [domain.a,domain.b]:
            try:
                pt = self.func(t)
                pt.x
                pt.y
                pt.z
            except:
                raise GeometricError("Curve not valid: The given function does not return a point or plane at parameter %s"%(t))

        self._rebuild_surrogate()


    @property
    def surrogate(self): 
        """ Returns a polyline representation of this curve. The number of points in the resulting PLine is related to the tolerance (tol) of this curve.
        
            :result: Polyline of curve.
            :rtype: PLine
            
            ::
            
                surg=crv.surrogate
        
        """
        return self._surrogate

    @property
    def appx_length(self): 
        """Returns the approximate length of a curve.
            
            :result: Approximate length of a curve.
            :rtype: float
            
            ::
            
                a_len=crv.appx_length
        """
        return self._surrogate.length

    @property
    def domain(self): 
        """Returns the Interval domain of a curve.
        
            :result: Domain of a curve.
            :rtype: Interval
        """
        return self._dom

    @property
    def tol_max(self):
        """Returns Curve.domain.delta / 10, which is understood to be the maximum tolerance (tol) of this curve.
        
            :result: maximum tolerance
            :rtype: float
            
        """
        return self._dom.delta / 10.0
    
    @property
    def tol(self): 
        #TODO: express tolerance as a percentage of domain delta instead... surfaces may have radically different domains in either direction
        """| The tolerance of this Parameterized Object expressed in domain space.
           | For example, given an interval of 0->1, a tol of 0.1 will result in a curve constructed of 10 segments, evaulated with t-values 0.1 apart
           | Given an interval 0->PI, a tol of 0.1 will result in a curve constructed of 32 segments, evaluated with t-values less than 0.1 apart
            
           :result: Sets the distance between point of a curve.
           :rtype: float
            
        """
        return self._tol
    @tol.setter
    def tol(self, tolerance):
        """ Sets tolerance of this Curve.
        
            :param tolerance: Distance between a point of a curve.
            :type tolerance: float
            :result: Distance between a point of a curve.
            :rtype: None
            
        """
        
        self._tol = tolerance
        if self._tol > self.tol_max : 
            self._tol = self.tol_max
            warnings.warn("Curve tolerance too high relative to curve domain - Resetting to max tol.  tolerance (%s) > Curve.max_tol(%s)"%(tolerance,self.tol_max),stacklevel=4)
        self._rebuild_surrogate()

    @property
    def tol_nudge(self):
        return self.tol/100.0

    def deval(self,t):
        """| Evaluates this Curve and returns a Point.
           | t is a float value that falls within the defined domain of this Curve.

           :param t: Value to evaluate the curve at.
           :type t: float
           :result: Point on the Curve.
           :rtype: Point
           
           ::
           
                d_pt=curv.deval(0.5)

            
        """
        if t<self.domain.a or t>self.domain.b : 
            t = round(t,7) # this may be due to a rounding problem, try rounding to 7 decimal places
            if t<self.domain.a or t>self.domain.b : raise DomainError("Curve evaluated outside the bounds of its domain: deval(%s) %s"%(t,self.domain))
        pt = self.func(t)

        #transform result to curve basis
        if not self.is_baseless:
            #pt.basis = self.basis
            #pt = pt.basis_applied()
            # TODO: evaluate basis instead... not all bases will have xforms!
            pt = pt * self.basis.xform
        
        return pt

    def deval_pln(self,t):
        """| Evaluates this Curve and returns a Plane.
           | t is a float value that falls within the defined domain of this Curve.
           |  Tangent vector determined by a nearest neighbor at distance Curve.tol/100

           :param t: Value to evaluate the curve at.
           :type t: float
           :result: Plane on the Curve.
           :rtype: Plane
        """
        if t<self.domain.a or t>self.domain.b : 
            t = round(t,7) # this may be due to a rounding problem, try rounding to 7 decimal places
            if t<self.domain.a or t>self.domain.b : raise DomainError("Curve evaluated outside the bounds of its domain: deval(%s) %s"%(t,self.domain))

        pt, vec, neg_vec = self._nudged(t)
        
        #transform result to curve basis
        if not self.is_baseless:
            #pt.basis = self.basis
            #pt = pt.basis_applied()
            # TODO: evaluate basis instead... not all bases will have xforms!
            pt = pt * self.basis.xform
            vec = vec * self.basis.xform.strip_translation()
        
        return Plane(pt,vec)


    def deval_crv(self,t):
        """ Calculates approximate curvature at the given t-value.
        
            :param t: Value to evaluate the curve at.
            :type t: float
            :result: (Curvature at t-value, osculating Circle)
            :rtype: (float, Circle)
        
        """
        # caluculates approximate curvature
        # returns curvature value and osc circle
        pt, vec_pos, vec_neg = self._nudged(t)

        # if given a curve endpoint, nudge vectors a bit so we don't get zero curvature, but leave origin the same
        if (t-self.tol_nudge <= self.domain.a):
            nhood = self._nudged(self.tol_nudge)
            vec_pos = nhood[1]
            vec_neg = nhood[2]
        if (t+self.tol_nudge >= self.domain.b):
            nhood = self._nudged(self.domain.b-self.tol_nudge)
            vec_pos = nhood[1]
            vec_neg = nhood[2]

        return Curve._curvature_from_vecs(pt,vec_pos,vec_neg)

    def eval(self,t):
        """| Evaluates this Curve and returns a Point.
           | t is a normalized float value (0->1) which will be remapped to the domain defined by this Curve.
           | Equivalent to Curve.deval(Interval.remap(t,Interval(),Curve.domain)).
            
           :param t: Normalized value between 0 and 1, to evaluate a Curve.
           :type t: float
           :result: a Point on the Curve.
           :rtype: Point

        """
        if t<0 or t>1 : raise DomainError("eval() must be called with a number between 0->1: eval(%s)"%t)
        return self.deval(Interval.remap(t,Interval(),self.domain))

    def eval_pln(self,t):
        """| Evaluates this Curve and returns a Plane.
           | t is a normalized float value (0->1) which will be remapped to the domain defined by this Curve.
           | Equivalent to Curve.deval(Interval.remap(t,Interval(),Curve.domain))
            
           :param t: Normalized value between 0 and 1, to evaluate a curve.
           :type t: float
           :result: a Plane on the Curve.
           :rtype: Plane
        """
        
        if t<0 or t>1 : raise DomainError("eval() must be called with a number between 0->1: eval(%s)"%t)
        return self.deval_pln(Interval.remap(t,Interval(),self.domain))

    def eval_crv(self,t):
        """ Returns curvature of this Curve at given t-value.
        
            :param t: Normalized value between 0 and 1, to evaluate a curve.
            :type t: float
            :result: (Curvature at t-value, osculating Circle)
            :rtype: (float, Circle)
        
        """
        if t<0 or t>1 : raise DomainError("eval_curvature() must be called with a number between 0->1: eval(%s)"%t)
        return self.deval_crv(Interval.remap(t,Interval(),self.domain))

    def tangent(self, t):
        """ Returns the tangent Vector to this Curve at given t-value
        
            :param t: Normalized value between 0 and 1, to evaluate a curve.
            :type t: float
            :result: Tangent Vector at t-value
            :rtype: Vec
        
        """
        pln = self.eval_pln(t)
        return pln.normal        
        
        
    @staticmethod
    def _curvature_from_vecs(pt, vec_pos, vec_neg, calc_circles=False):
        """ Returns the curvature at a point.
        
            :param pt: Point on Curve.
            :type pt: Point
            :param vec_pos: First vector for curvature.
            :type vec_pos: Vec
            :param vec_neg: Second vector for curvature.
            :type vec_neg: Vec
            :param calc_circles: Boolean Value.
            :type calc_circles: bool
            :result: (Curvature at point, osculating Circle)
            :rtype: (float, Circle)
            
            
        """
    
        pt_plus = pt + vec_pos
        pt_minus = pt + vec_neg
        
        v1 = vec_pos
        v2 = vec_neg
        v3 = Vec(vec_pos - vec_neg)
        
        xl = v1.cross(v3).length
        if xl == 0 : return 0,Ray(pt,vec_pos)
        
        rad_osc = 0.5*v1.length*v2.length*v3.length/xl
        if not calc_circles: return 1/rad_osc
        
        denom = 2*xl*xl
        a1 = v3.length*v3.length*v1.dot(v2)/denom
        a2 = v2.length*v2.length*v1.dot(v3)/denom
        a3 = v1.length*v1.length*(-v2.dot(v3))/denom
        center_osc = pt*a1 + pt_plus*a2 + pt_minus*a3
        
        pln_out = Plane(center_osc, v1.cross(v2))
        circ_out = Circle(pln_out,rad_osc)
        return (1/rad_osc, center_osc, circ_out)


    def _nudged(self,t):
        """ Returns the nearest neighbors of a point on this Curve at the given t-value. Used for discrete approximations calculations.
        
            :param t: Value to evaluate the curve at.
            :type t: float
            :result: Point at t-value, nearest Vec, nearest Vec.
            :rtype: Point, Vec, Vec
        """
        
        #nearest neighbors of a point t; used for discrete approximations calculations 
        if t<self.domain.a or t>self.domain.b : raise DomainError("Curve evaluated outside the bounds of its domain: deval(%s) %s"%(t,self.domain))

        pt_t = self.func(t)
        vec_minus = False
        vec_plus = False

        if (t-self.tol_nudge >= self.domain.a): vec_minus = Vec(pt_t,self.func(t - self.tol_nudge))
        if (t+self.tol_nudge <= self.domain.b): vec_plus = Vec(pt_t,self.func(t + self.tol_nudge))

        if not vec_plus: vec_plus = vec_minus.inverted()
        if not vec_minus: vec_minus = vec_plus.inverted()

        return pt_t,vec_plus,vec_minus


    def divide(self, divs=10, include_last=True):
        """| Divides this Curve into a list of evaluated Planes equally spaced between Curve.domain.a and Curve.domain.b.
           | If include_last is True (by default), returned list will contain divs+1 Points.
           | If include_last is False, returned list will not include the point at Curve.domain.b
        
           :param divs: Number of segments to divide this curve into.
           :type divs: int
           :param include_last: Boolean Value.
           :type include_last: bool
           :returns: List of points 
           :rtype: [Point]
           
           ::
           
                divs=crv.divide(5)
        """
        return [self.deval(t) for t in self.domain.divide(divs,include_last)]

    def subdivide(self, divs):
        """| Divides this Curve into a list of equal size sub-Curves.
           | Each sub-Curve will adopt the tol of this curve, unless greater than the tol_max of the subcurve.
        
           :param divs: Number of subcurves.
           :type divs: int
           :returns: List of sub-Curves. 
           :rtype: [Curve]
           
        """
        curves = []
        for subd in self.domain//divs: curves.append(self.subcurve(subd,self.tol/divs))
        return curves

    def subcurve(self,domain,tol=None):
        """ Returns a new Curve which is a copy of this Curve with the given Interval as the domain.
        
           :param domain: New curve with a new given interval.
           :type domain: Interval
           :param tol: Tolerance of point on a subcurve.
           :type tol: float
           :result: Copy of curve with new domain.
           :rtype: Curve
            
           ::
                
                sub_curv=crv.subcurve(Interval(5,10))            
        """
        if tol is None: tol = self.tol
        if tol > domain.delta/10.0 : tol = domain.delta/10.0
        return Curve(self.func,domain,tol)

    def _nearfar(self,func_nf,pt,tolerance,max_recursion,idivs=8):
        """ Calculates curve subdivisions.
        
            :param func_nf: Function to produce a curve.
            :type func_nf: function
            :param pt: Point to begin recursion.
            :type pt: Point
            :param tolerance: Tolerance for point on a Curve.
            :type tolerance: float.
            :param max_recursion: Maximum number of recursions.
            :type max_recursion: int
            :param idivs: Number of initial divisions
            :type idivs: int
            :result: Curve
            :rtype: Curve
            
        """
        
        def sub(crv,divs):
            buffer = 1.5 # multiplier for resulting area
            ni = func_nf(pt,crv/divs) # divide the curve and find the nearest or furthest point (depending on the function that was provided)
            nd = crv.domain.eval(ni/float(divs)) # find the domain value associated with this point
            domain = Interval( nd-(buffer*crv.domain.delta/divs), nd+(buffer*crv.domain.delta/divs) ) #  create a new domain that may contain the nearest point
            if domain.a < crv.domain.a : domain.a = crv.domain.a
            if domain.b > crv.domain.b : domain.b = crv.domain.b
            return crv.subcurve(domain),domain.a == crv.domain.a, domain.b == crv.domain.b # return a new curve with this domain

        crv, force_spt, force_ept = sub(self,idivs)
        n = 1
        while crv.domain.delta > tolerance : 
            divs = 8 # number of subsequent divisions to cut the given curve into
            crv, at_spt, at_ept = sub(crv,divs)
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


    def _rebuild_surrogate(self):
        self._surrogate = self._to_pline()


    @staticmethod
    def circle(ctr,rad):
        """| Constructs a Curve object that describes a circle given: a center (Point) and radius (float).
           | The plane of the circle will always be parallel to the xy-plane.
        
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
        """| Constructs a Curve object that describes a helix given: a center (Point), a radius (float), a rise_per_turn (float), and a number_of_turns (float).
           | The plane of the circle of the helix will always be parallel to the xy-plane.
            
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
            :result: Bezier curve.
            :rtype: Curve
            
        """
        if len(cpts) <= 1 : raise GeometricError("Curve not valid: A Bezier requires a minimum of two points.  You gave me %s"%(len(cpts)))
        def func(t):
            pts = cpts
            while len(pts) > 1: pts = [Point.interpolate(pts[n],pts[n+1],t) for n in range(len(pts)-1)]
            return pts[0]

        return Curve(func)

    @staticmethod
    def hermite(cpts):
        """ Constructs a hermite curve. It has nice tension and biasing controls. 
            
            :param cpts: List of control points to build the curve.
            :type cpts: [Point]
            :result: Hermite Curve object.
            :rtype: Curve
        """
        # from http://paulbourke.net/miscellaneous/interpolation/
        if len(cpts) <= 1 : raise GeometricError("Curve not valid: A Hermite requires a minimum of two points.  You gave me %s"%(len(cpts)))
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


