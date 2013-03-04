import unittest, math
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_empty_constructor(self):
        pline = PLine()
        self.assertEqual(len(pline.pts),0,"a polyline constructed with no arguments contains an empty list of verts")
        
    def _test_segments(self):
        pline = PLine([Point(t,math.sin(t),0) for t in Interval(0,math.pi*2)/4])
        self.assertEqual(len(pline.pts),0,"a polyline constructed with no arguments contains an empty list of verts")
        
