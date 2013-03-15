import unittest
import decodes.core as dc
from decodes.core import *
import math


class Tests(unittest.TestCase):

    def test_empty_constructor(self):
        vec = Vec()
        self.assertEqual(Vec(0,0,0),vec,"vectors with empty constructors are at 0,0,0")
        self.assertEqual(0,vec.x,"vectors with empty constructors have an x value of 0")
        self.assertEqual(0,vec.y,"vectors with empty constructors have an y value of 0")
        self.assertEqual(0,vec.z,"vectors with empty constructors have an z value of 0")

    def test_operators(self):
        v1 = Vec(2,2,2)
        v2 = Vec(1,1,1)

        self.assertEqual(Vec(3,3,3),v1+v2)
        self.assertEqual(Vec(1,1,1),v1-v2)
        self.assertEqual(v1.cross(v2),v1*v2)
        self.assertEqual(Vec(1,1,1),v1/2)
        self.assertEqual(Vec(-2,-2,-2),-v1)
        
    def test_properties(self):
        v1 = Vec(2,2,2)
        v2 = Vec(1,1,1)
        v3 = Vec(-1,-1,-1)
        v4 = Vec(1,1,1)
        v5 = Vec(0,1)

        self.assertEqual((2,2,2),v1.to_tuple())
        self.assertEqual(True,v1>v2)
        self.assertEqual(True,v1>=v2)
        self.assertEqual(True,v2>=v3)
        self.assertEqual(False,v1<v2)
        self.assertEqual(False,v1<=v2)
        self.assertEqual(True,v2<=v3)

        self.assertEqual(False,v1==v2)
        self.assertEqual(False,v2==v3)
        self.assertEqual(True,v2==v4)
        self.assertEqual(True,v1!=v2)
        self.assertEqual(True,v2!=v3)
        self.assertEqual(False,v2!=v4)

        self.assertEqual(False,v1.is_identical(v2))
        self.assertEqual(False,v2.is_identical(v3))
        self.assertEqual(True,v2.is_identical(v4))

        self.assertEqual(True,v1.is_coincident(v2))
        self.assertEqual(False,v2.is_coincident(v3))
        self.assertEqual(True,v2.is_coincident(v4))

        self.assertEqual(False,v1.is_2d)
        self.assertEqual(True,v5.is_2d)

    def test_dot_and_cross_products(self):
        v1 = Vec(0,1)
        v2 = Vec(1,0)
        v3 = Vec(1,1)

        self.assertEqual(Vec(0,0,-1),v1.cross(v2))
        self.assertEqual(Vec(0,0,1),v2.cross(v1))
        self.assertEqual(0.0,v1.dot(v2))
        self.assertEqual(1.0,v1.dot(v3))

        va = Vec(4,4,4)
        vb = Vec(0,-2,0)
        self.assertEqual(-8.0,va.dot(vb))
        
    def test_angle(self):
        v1 = Vec(1,0,0)
        v2 = Vec(1,0,1)

        self.assertAlmostEqual(45,v1.angle_deg(v2),8,"angle between two vecs has a rounding problem")
        self.assertAlmostEqual(math.radians(45),v1.angle(v2),8,"angle between two vecs has a rounding problem")
        
    def test_static(self):
        v1 = Vec(2,2,2)
        v2 = Vec(1,1,1)

        self.assertEqual(Vec(1.25,1.25,1.25),Vec.interpolate(v2,v1,0.25))
        self.assertEqual(Vec(1.5,1.5,1.5),Vec.average([v1,v2]))
        
    def test_normalizing(self):
        vec = Vec()
        v1 = Vec(2,0,0)
        v2 = Vec(1,0,0)

        self.assertEqual(v2,v1.limited(1))
        self.assertEqual(v2,v1.normalized())









