import unittest, math
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_empty_constructor(self):
        pline = PLine()
        self.assertEqual(len(pline.pts),0,"a polyline constructed with no arguments contains an empty list of verts")
        
    def test_segs_and_edges(self):
        pl = PLine([Point(t,t,0) for t in Interval(0,10).divide(10,True)])
        self.assertEqual(len(pl.edges),10,"len(PLine.edges) returns the number of segments in the Pline")
        self.assertEqual(len(pl),11,"len(PLine) returns the number of verts in the Pline")
        
        for n,ival in enumerate(Interval(0,10)//10):
          seg = Segment(Point(ival.a,ival.a),Point(ival.b,ival.b))
          self.assertEqual(seg.spt,pl.seg(n).spt)
          self.assertEqual(seg.ept,pl.seg(n).ept)
          self.assertEqual(seg.spt,pl.edges[n].spt)
          self.assertEqual(seg.ept,pl.edges[n].ept)

        
