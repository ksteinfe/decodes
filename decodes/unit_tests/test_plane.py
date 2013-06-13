import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_empty_constructor(self):
        pln = Plane()
        self.assertEqual(Point(0,0,0),pln,"planes with empty constructors are at 0,0,0 with a normal of 0,0,1")
        self.assertEqual(Vec(0,0,1),pln._vec,"planes with empty constructors are at 0,0,0 with a normal of 0,0,1")
        self.assertEqual(Vec(0,0,1),pln.normal,"planes with empty constructors are at 0,0,0 with a normal of 0,0,1")

    def test_copy_constructors(self):
        pa = Point(1,2,3)
        va = Vec(-1,1,2)
        pln = Plane(pa,va)

        self.assertEqual(Point(1,2,3),pln)
        self.assertEqual(Point(1,2,3),pln.origin)
        self.assertEqual(Vec(-1,1,2).normalized(),pln._vec)

        pa = Point(10,20,30)
        va = Vec(1,2,3)
        self.assertEqual(Point(1,2,3),pln,"planes, like vecs, keep a copy of cpts (and not a reference)")
        self.assertEqual(Vec(-1,1,2).normalized(),pln._vec, "planes make a unitzed copy of their vecs")
        self.assertEqual(Vec(-1,1,2).normalized(),pln.normal, "planes make a unitzed copy of their vecs")

    def test_near(self):
        pa = Point(2,2,2)
        va = Vec(0,0,1)
        pln = Plane(pa,va)

        pt_a = Point(1,1,0)
        pt_b = Point(1,1,3)
        pt_c = Point(2,2,2)

        self.assertEqual(Point(1,1,2),pln.near_pt(pt_a),"behind plane")
        self.assertEqual(Point(1,1,2),pln.near_pt(pt_a),"in front of plane")
        self.assertEqual(Point(2,2,2),pln.near_pt(pt_c),"on plane at center point")


    def test_xform(self):
        pa = Point(2,2,2)
        va = Vec(1,0,0)
        pln = Plane(pa,va)

        xf = Xform.scale(2.0)
        pln_scaled = pln * xf
        self.assertEqual(Point(4,4,4),pln_scaled.origin,"scaling transforms plane origin")
        self.assertEqual(Vec(1,0,0),pln_scaled.normal,"scaling does not transform plane normal")

        xf = Xform.rotation(axis=Vec(0,0,1),angle=math.pi/2)
        pln_rotated = pln * xf
        self.AssertPointsAlmostEqual(Point(-2.0,2.0,2.0),pln_rotated.origin)
        self.AssertPointsAlmostEqual(Vec(0,1,0),pln_rotated.normal)

    def AssertPointsAlmostEqual(self,pa,pb,places=4):
        self.assertAlmostEqual(pa.x,pb.x,places)
        self.assertAlmostEqual(pa.y,pb.y,places)
        self.assertAlmostEqual(pa.z,pb.z,places)