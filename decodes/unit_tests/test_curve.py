import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_constructor(self):

        def func(t):
            return Point(t,math.sin(t))
        crv = Curve(func,Interval(0,math.pi*2))

        for t in crv.domain/20: self.assertEqual(crv.deval(t).y,math.sin(t),"deval() calls Curve.func(t) and is valid for all numbers within domain of the Curve") 
        for t in Interval()/20: self.assertEqual(crv.eval(t).y,math.sin(Interval(0,math.pi*2).eval(t)),"eval() calls Curve.func(t) and is valid for 0->1") 

        with self.assertRaises(DomainError):  crv.eval(-0.5) # this test succeeds if a geometric error is raised in the contained block of code
        with self.assertRaises(DomainError):  crv.eval(1.5) # this test succeeds if a geometric error is raised in the contained block of code
        with self.assertRaises(DomainError):  crv.deval(-10) # this test succeeds if a geometric error is raised in the contained block of code
        with self.assertRaises(DomainError):  crv.deval(10) # this test succeeds if a geometric error is raised in the contained block of code

    def test_tolerance(self):
        def func(t):
            return Point(t,0)

        crv = Curve(func,Interval(0,10))
        for n in range(10):
            self.AssertPointsAlmostEqual(crv.surrogate.pts[n],Point(n,0)) # default tol is 1/10th the domain

        crv.tol = 0.5 
        for n in range(20):
            self.AssertPointsAlmostEqual(crv.surrogate.pts[n],Point(Interval(0,10).eval(n/20.0),0)) # a tol of 0.5 results in 20 divisions of a 10-unit domain

        crv = Curve(func)
        for n in range(10):
            self.AssertPointsAlmostEqual(crv.surrogate.pts[n],Point(n/10.0,0)) # default tol is 1/10th the domain

        crv.tol = 0.05
        for n in range(20):
            self.AssertPointsAlmostEqual(crv.surrogate.pts[n],Point(n/20.0,0)) # a tol of 0.05 results in 20 divisions of a 1-unit domain

    def test_division(self):
        def func(t):
            return Point(t,t**2)
        crv = Curve(func,Interval(0,10))

        div_pts = crv.divide(10)
        self.assertEqual(len(div_pts),10+1,"crv.divide(n) results in n+1 Points")
        for n, pln in enumerate(div_pts) : self.assertEqual(pln.origin,Point(n,n**2))

        div_pts_op = crv/10
        self.assertEqual(len(div_pts_op),10+1,"crv/10 results in n+1 Points")
        for n in range(10+1): self.assertEqual(div_pts[n],div_pts_op[n],"crv.divide(n) is equivalent to crv/n")

    def test_subdivide(self):
        def func(t):
            return Point(t,t**2)
        crv = Curve(func,Interval(0,10))

        subcrvs = crv.subdivide(10)
        for n,ival in enumerate(crv.domain//10) : 
            self.assertEqual(subcrvs[n].domain,ival,"")

        subcrvs = crv//10
        for n,ival in enumerate(crv.domain//10) : 
            self.assertEqual(subcrvs[n].domain,ival,"")

    def _test_near(self):
        #NOTE: this test takes 1 sec.  disabled for now.
        def func(t):
            return Point(t,t)
        crv = Curve(func,Interval(0,10))

        near_pt, near_t, dist = crv.near(Point(5,0)) #near() returns a tuple containing three values (Plane, float)

        pt = Point(2.5,2.5,0)
        self.assertAlmostEqual(near_pt.x,pt.x)
        self.assertAlmostEqual(near_pt.y,pt.y)
        self.assertAlmostEqual(near_pt.z,pt.z)

        def func(t):
            return Point(t,math.sin(t))
        crv = Curve(func,Interval(0,math.pi*2))
        
        for t in Interval.twopi()/4:
            pt = Point(t,math.sin(t))
            near_pln, near_t, dist = crv.near(pt,0.01)
            self.AssertPointsAlmostEqual(pt,near_pln.origin)

    def _test_far(self):
        #NOTE: this test takes a long time.  disabled for now.
        crv = Curve.circle(Point(),10)
        far_pln, far_t, dist = crv.far(Point(0,1)) #far() returns a tuple containing three values (Plane, float)
        self.AssertPointsAlmostEqual(Point(0,-10),far_pln.origin)


    def test_bezier(self):
        pt_a = Point()
        pt_b = Point(1,0)
        pt_c = Point(1,1)
        crv = Curve.bezier([pt_a,pt_b,pt_c])
        self.assertEqual(crv.eval(0).origin,pt_a,"Curve.eval(0) returns first control point")
        self.assertEqual(crv.eval(1).origin,pt_c,"Curve.eval(1) returns last control point")
        #TODO: evaluate point in the middle somehow

    def test_hermite(self):
        pt_a = Point()
        pt_b = Point(1,0)
        pt_c = Point(1,1)
        crv = Curve.hermite([pt_a,pt_b,pt_c])
        self.assertEqual(crv.eval(0).origin,pt_a,"Curve.eval(0) returns first control point")
        self.assertEqual(crv.eval(1).origin,pt_c,"Curve.eval(1) returns last control point")
        #TODO: evaluate point in the middle somehow

    def AssertPointsAlmostEqual(self,pa,pb,places=4):
        self.assertAlmostEqual(pa.x,pb.x,places)
        self.assertAlmostEqual(pa.y,pb.y,places)
        self.assertAlmostEqual(pa.z,pb.z,places)