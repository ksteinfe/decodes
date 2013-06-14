import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_constructor(self):

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

    def test_division(self):
        pass

    def test_subdivide(self):
        pass

    def test_meshing(self):
        def func(u,v):
            return Point(u,v,math.sin(u+v))
        twopi = Interval.twopi()
        surf = Surface(func,twopi,twopi)

        msh = surf.to_mesh()

        print msh