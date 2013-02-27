import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_item_access(self):
        vecs = [Vec(x,0,0) for x in range(10)]
        pline = PLine(vecs)
        for n in range(len(pline)) : self.assertEqual(vecs[n],pline[n],"points constructor appends points to verts list, and item access is working")
        
        self.assertEqual(vecs[0:2],pline[0:2],"slicing item access returns a REFERENCE to the stored vectors")
        self.assertEqual(vecs[0:2],pline.pts[0:2],"the pts function returns a list of point objects with the same basis as this geometry")

        def func(): pline[0:2] = Point()
        self.assertRaises(TypeError,func) # confirms that an error is raised when this we try to set a point using slicing syntax

    def test_appending_points(self):
        pts = [Point(x,0,0) for x in range(10)]
        pgon = PGon(pts,basis=CS(Point(0,0,-1))) # the pts here are interpreted in local coordinates
        self.assertEqual(Vec(0,0,0),pgon[0],"when constructing with a defined basis, the given points are interpreted in local coordinates")
        self.assertEqual(Point(0,0,-1),pgon.pts[0],"when constructing with a defined basis, the given points are interpreted in local coordinates")

        pgon = PGon(basis=CS(1,2,3))
        pgon.append(Vec())
        self.assertEqual(Vec(),pgon[0],"new points appended to a object with an already defined basis will be interpreted in local coordinates")
        self.assertEqual(Point(1,2,3),pgon.pts[0],"new points appended to a object with an already defined basis will be interpreted in local coordinates")

        #todo: replace an existing point

    def test_manipulating_points(self):
        pts = [Point(x,0,0) for x in range(10)]
        pgon = PGon(pts,basis=CS(Point(0,0,-1))) # the pts here are interpreted in local coordinates
        
        pgon[0].z = 10
        self.assertEqual(Vec(0,0,10),pgon[0],"square bracket access returns a reference to stored vectors, allowing for manipulation")

        pgon.pts[1].z = 10
        self.assertEqual(Point(1,0,-1),pgon.pts[1],"access via the pts function returns a list of point objects, which does not permit manipulation")
