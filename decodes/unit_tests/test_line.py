import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_segment(self):
        p1 = Point(0,0,0)
        p2 = Point (1,0,0)
        segment = Segment(p1,p2)
        self.assertEqual(segment.spt,p1)
        self.assertEqual(segment.length,1)
        self.assertEqual(segment.midpoint,Point(0,0.5,0))
        
    def test_line(self):
        p1 = Point(0,0,0)
        p2 = Point (1,0,0)
        line = Line(p1,p2)
        self.assertEqual(line.spt,p1)

    def test_ray(self):
        p1 = Point(0,0,0)
        p2 = Point (1,0,0)
        ray = Ray(p1,p2)
        self.assertEqual(ray.spt,p1)


