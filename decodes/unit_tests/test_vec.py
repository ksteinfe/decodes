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
        self.assertEqual(Vec(2,2,2),v1*v2)
        self.assertEqual(Vec(2,2,2),v1/v2)
        self.assertEqual(Vec(-2,-2,-2),-v1)
        
    def test_properties(self):
        v1 = Vec(2,2,2)
        v2 = Vec(1,1,1)

        self.assertEqual((2,2,2),v1.to_tuple())
        self.assertEqual(True,v1>v2)
        self.assertEqual(True,v1>=v2)
        self.assertEqual(False,v1<v2)
        self.assertEqual(False,v1<=v2)
        self.assertEqual(False,v1==v2)
        self.assertEqual(False,v1!=v2)
        self.assertEqual(False,v1.is_identical(v2))
        self.assertEqual(False,v1.is_coincident(v2))
        self.assertEqual(False,v1.is_2d)
        self.assertEqual(False,v1!=v2)
   
    def test_products(self):
        v1 = Vec(2,2,2)
        v2 = Vec(1,1,1)

        self.assertEqual(-v1,v1.cross(v2))
        self.assertEqual(2,v1.dot(v2))
        
    def test_angle(self):
        v1 = Vec(1,0,0)
        v2 = Vec(1,0,1)

        self.assertEqual(90,v1.angle_deg(v2))
        self.assertEqual(math.radians(90),v1.angle(v2))
        
    def test_static(self):
        v1 = Vec(2,2,2)
        v2 = Vec(1,1,1)

        self.assertEqual(Vec(1.25,1.25,1.25),Vec.interpolate(v0,v1))
        self.assertEqual(Vec(1.5,1.5,1.5),Vec.average([v0,v1]))
        
    def test_methods(self):
        vec = Vec()
        v1 = Vec(2,2,2)
        v2 = Vec(1,1,1)

        self.assertEqual(Vec(),vec.limited(0))









