import unittest, math
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_empty_constructor(self):
        pline = PLine()
        self.assertEqual(len(pline.pts),0,"a polyline constructed with no arguments contains an empty list of verts")
        
    def test_segments(self):
        pl = PLine([Point(t,t,0) for t in Interval(0,10)/10])
        self.assertEqual(len(pl),10,"len(PLine) returns the number of verts in the Pline")
        seg = Segment(Point(1,1),Point(2,2))
        self.assertEqual(seg.spt,pl.edges[1].spt)
        self.assertEqual(seg.ept,pl.edges[1].ept)

        pl = PLine([Point(0,0),Point(1,1),Point(2,2)])
        segs = pl.edges
        self.assertEqual(seg.ept,pl.edges[1].ept)
