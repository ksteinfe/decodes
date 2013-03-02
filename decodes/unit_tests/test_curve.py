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

    def test_division(self):
        def func(t):
            return Point(t,t**2)
        crv = Curve(func,Interval(0,10))

        div_pts = crv.divide(10)
        self.assertEqual(len(div_pts),10+1,"crv.divide(n) results in n+1 Points")
        for n, pt in enumerate(div_pts) : self.assertEqual(pt,Point(n,n**2))

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

    def test_near(self):
        def func(t):
            return Point(t,t)
        crv = Curve(func,Interval(0,10))

        near_pt, near_t, dist = crv.near(Point(5,0)) #near() returns a tuple containing two values (Point, float)

        pt = Point(2.5,2.5,0)
        self.assertAlmostEqual(near_pt.x,pt.x)
        self.assertAlmostEqual(near_pt.y,pt.y)
        self.assertAlmostEqual(near_pt.z,pt.z)

        def func(t):
            return Point(t,math.sin(t))
        crv = Curve(func,Interval(0,math.pi*2))
        
        places = 3
        for t in Interval.twopi()/4:
            pt = Point(t,math.sin(t))
            near_pt, near_t, dist = crv.near(pt,0.001)
            self.assertAlmostEqual(near_pt.x,pt.x,places)
            self.assertAlmostEqual(near_pt.y,pt.y,places)
            self.assertAlmostEqual(near_pt.z,pt.z,places)

    def test_far(self):
        def func(t):
            return Point(t,t)
        crv = Curve(func,Interval(0,10))

        near_pt, near_t, dist = crv.near(Point(5,0)) #near() returns a tuple containing two values (Point, float)