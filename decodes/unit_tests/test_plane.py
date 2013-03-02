import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_empty_constructor(self):
        pln = Plane()
        self.assertEqual(Point(0,0,0),pln,"planes with empty constructors are at 0,0,0 with a normal of 0,0,1")
        self.assertEqual(Vec(0,0,1),pln.vec,"planes with empty constructors are at 0,0,0 with a normal of 0,0,1")


    def test_copy_constructors(self):
        pa = Point(1,2,3)
        va = Vec(-1,1,2)
        pln = Plane(pa,va)

        self.assertEqual(Point(1,2,3),pln)
        self.assertEqual(Point(1,2,3),pln.cpt)
        self.assertEqual(Vec(-1,1,2),pln.vec)

        pa = Point(10,20,30)
        va = Vec(1,2,3)
        self.assertEqual(Point(1,2,3),pln,"planes, like vecs, keep a copy of cpts")
        self.assertEqual(Vec(-1,1,2),pln.vec, "planes make a unitzed copy of their vecs")
