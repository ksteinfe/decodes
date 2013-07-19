import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_bad_combonations(self):
        results = []
        with self.assertRaises(NotImplementedError): intersect(CS().xy_plane,Point(),results)
        with self.assertRaises(NotImplementedError): intersect("afsd",10,results)
        with self.assertRaises(NotImplementedError): intersect(Point(),Ray(Point(2,2,-1),Vec(0,0,1)),results)

    def test_ray_plane(self):
        ray = Ray(Point(2,2,1),Vec(0,0,-1))
        pln = CS().xy_plane
        results = XSec()
        self.assertEqual(intersect(ray,pln,results),True)
        self.assertEqual(results[0],Point(2,2,0))

        ray = Ray(Point(2,2,-1),Vec(0,0,1)) # ray behind plane
        results = XSec()
        self.assertEqual(intersect(ray,pln,results),True)
        self.assertEqual(results[0],Point(2,2,0))
        
        results = XSec()
        self.assertEqual(intersect(ray,pln,results,ignore_backface=True),False)
        self.assertEqual(len(results),0)

        ray = Ray(Point(2,2,1),Vec(0,0,1)) # plane behind ray
        results = XSec()
        self.assertEqual(intersect(ray,pln,results),False)
        self.assertEqual(len(results),0)
        
    def test_line_plane(self):
        line = Line(Point(2,2,1),Vec(0,0,-1))
        pln = CS().xy_plane
        results = XSec()
        self.assertEqual(intersect(line,pln,results),True)
        self.assertEqual(results[0],Point(2,2,0))

        line = Line(Point(2,2,-1),Vec(0,0,1)) # line behind plane
        results = XSec()
        self.assertEqual(intersect(line,pln,results),True)
        self.assertEqual(results[0],Point(2,2,0))

        results = XSec()
        self.assertEqual(intersect(line,pln,results,ignore_backface=True),False)
        self.assertEqual(len(results),0)

        line = Line(Point(2,2,1),Vec(0,0,1)) # plane behind line
        results = XSec()
        self.assertEqual(intersect(line,pln,results),True)
        self.assertEqual(results[0],Point(2,2,0))

    def test_circ_circ(self):
        circ_a = Circle(CS().xy_plane,1.0)
        circ_b = Circle(CS.on_xy(1,0).xy_plane,1.0)
        results = XSec()
        self.assertEqual(intersect(circ_a,circ_b,results),True)
        print results[0]