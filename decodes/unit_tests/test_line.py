import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_segment(self):
        p1 = Point(0,0,0)
        p2 = Point (1,0,0)
        segment = Segment(p1,p2)
        self.assertEqual(segment.spt,Point(0,0,0))
        self.assertEqual(segment.length,1.0)
        self.assertEqual(segment.midpoint,Point(0.5,0,0))
        
    def test_line(self):
        p1 = Point(0,0,0)
        p2 = Point (1,0,0)
        line = Line(p1,p2)
        self.assertEqual(line.spt,Point(0,0,0))
        self.assertEqual(line.ept,Point(1,0,0))

    def test_ray(self):
        p1 = Point(0,0,0)
        p2 = Point (1,0,0)
        ray = Ray(p1,p2)
        self.assertEqual(ray.spt,p1)

    def test_near_pt(self):
        p1 = Point(0,0,0)
        p2 = Point (10,0,0)
        pt_a = Point(5,0,1)
        pt_b = Point(-5,0,1)
        pt_c = Point(15,0,1)

        le = Line(p1,p2)
        self.assertEqual(le.near_pt(pt_a),Point(5,0,0))
        self.assertEqual(le.near_pt(pt_b),Point(-5,0,0))
        self.assertEqual(le.near_pt(pt_c),Point(15,0,0))

        le = Ray(p1,p2)
        self.assertEqual(le.near_pt(pt_a),Point(5,0,0))
        self.assertEqual(le.near_pt(pt_b),Point(0,0,0))
        self.assertEqual(le.near_pt(pt_c),Point(15,0,0))

        le = Segment(p1,p2)
        self.assertEqual(le.near_pt(pt_a),Point(5,0,0))
        self.assertEqual(le.near_pt(pt_b),Point(0,0,0))
        self.assertEqual(le.near_pt(pt_c),Point(10,0,0))