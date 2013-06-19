import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def _test_constructor(self):

        def func(u,v):
            return Point(u,v,math.sin(u+v))
        twopi = Interval.twopi()
        surf = Surface(func,twopi,twopi)

        for u in twopi/4: 
            for v in twopi/4:
                srf_pt = surf.deval(u,v)
                sin_val = math.sin(u+v)
                self.assertEqual(srf_pt.z,sin_val,"deval() calls Surface.func(t) and is valid for all numbers within domain of the Surface") 
        
        for u in Interval()/4: 
            for v in Interval()/4: 
                srf_pt = surf.eval(u,v)
                sin_val = math.sin(twopi.eval(u)+twopi.eval(v))
                self.assertEqual(srf_pt.z,sin_val,"eval() calls Surface.func(t) and is valid for 0->1") 

        with self.assertRaises(DomainError):  surf.eval(-0.5,0.5) # this test succeeds if a domain error is raised in the contained block of code
        with self.assertRaises(DomainError):  surf.eval(4.5,0.5) # this test succeeds if a domain error is raised in the contained block of code
        with self.assertRaises(DomainError):  surf.deval(-10,0.5) # this test succeeds if a domain error is raised in the contained block of code
        with self.assertRaises(DomainError):  surf.deval(10,0.5) # this test succeeds if a domain error is raised in the contained block of code
        with self.assertRaises(DomainError):  surf.eval(0.5,-0.5) # this test succeeds if a domain error is raised in the contained block of code
        with self.assertRaises(DomainError):  surf.eval(0.5,4.5) # this test succeeds if a domain error is raised in the contained block of code
        with self.assertRaises(DomainError):  surf.deval(0.5,-10) # this test succeeds if a domain error is raised in the contained block of code
        with self.assertRaises(DomainError):  surf.deval(0.5,10) # this test succeeds if a domain error is raised in the contained block of code

    def _test_division(self):
        pass

    def _test_subdivide(self):
        pass

    def _test_meshing(self):
        def func(u,v):
            return Point(0,u,v)
        surf = Surface(func)
        msh = surf.to_mesh()
        #TODO: really test this mesh

    def test_tolerance(self):
        def func(u,v):
            return Point(0,u,v)

        srf = Surface(func)
        divs_u = 10  # default tol is 1/10th the domain
        divs_v = 10  # default tol is 1/10th the domain
        for v in range(divs_v+1):
            row = v*(divs_u+1)
            for u in range(divs_u+1):
                pt = Point(0,float(u)/divs_u,float(v)/divs_v)
                pt_s = srf.surrogate.pts[row+u]
                self.AssertPointsAlmostEqual(pt_s,pt)
        
        srf = Surface(func,tol_u = 0.05)
        srf.tol_u = 0.05 # a tol of 0.05 on a domain of 0->1 is 1/20th the domain
        divs_u = 20
        for v in range(divs_v+1):
            row = v*(divs_u+1)
            for u in range(divs_u+1):
                pt = Point(0,float(u)/divs_u,float(v)/divs_v)
                pt_s = srf.surrogate.pts[row+u]
                self.AssertPointsAlmostEqual(pt_s,pt)

    def AssertPointsAlmostEqual(self,pa,pb,places=4):
        self.assertAlmostEqual(pa.x,pb.x,places)
        self.assertAlmostEqual(pa.y,pb.y,places)
        self.assertAlmostEqual(pa.z,pb.z,places)