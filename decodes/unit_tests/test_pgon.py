import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_empty_constructor(self):
        pgon = PGon()
        self.assertEqual(len(pgon.pts),0,"a polygon constructed with no arguments contains an empty list of verts")
        
    def test_segs_and_edges(self):
        p0 = Point(0,0,1)
        p1 = Point(1,0,1)
        p2 = Point(1,1,1)
        p3 = Point(0,1,1)
        pgon = PGon([p0,p1,p2,p3],CS(Point(0,0,2)) )
        self.assertEqual(len(pgon.edges),4,"len(PGon.edges) returns the number of segments in the PGon")
        self.assertEqual(len(pgon),4,"len(PGon) returns the number of verts in the PGon")
        
        def func(n,seg):
            self.assertEqual(seg.spt,pgon.seg(n).spt)
            self.assertEqual(seg.ept,pgon.seg(n).ept)
            self.assertEqual(seg.spt,pgon.edges[n].spt)
            self.assertEqual(seg.ept,pgon.edges[n].ept)
        
        func(0,Segment(Point(0,0,3),Point(1,0,3)))
        func(1,Segment(Point(1,0,3),Point(1,1,3)))
        func(2,Segment(Point(1,1,3),Point(0,1,3)))
        func(3,Segment(Point(0,1,3),Point(0,0,3)))
        

    def test_rgon_construction(self):
        argon = RGon.from_edge(Segment.by_coords2d(0,0,0,1),3)
        self.AssertPointsAlmostEqual( argon.pts[0] , Point() )
        self.AssertPointsAlmostEqual( argon.pts[-1] , Point(0,1) )


    def test_rgon_to_pgon(self):
        rgon = RGon(3,1.0)
        pgon = rgon.to_pgon()

        self.assertFalse(isinstance(pgon, RGon))
        for n in range(len(rgon)) : self.assertEqual(rgon.pts[n],pgon.pts[n])

    def test_inflation(self):
        tri_a = RGon(3,1.0)
        tri_b = tri_a.inflate()

        self.AssertPointsAlmostEqual( tri_b.pts[0] , tri_a.edges[0].midpoint )        



    def AssertPointsAlmostEqual(self,pa,pb,places=4):
        self.assertAlmostEqual(pa.x,pb.x,places)
        self.assertAlmostEqual(pa.y,pb.y,places)
        self.assertAlmostEqual(pa.z,pb.z,places)
