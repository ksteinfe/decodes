import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_item_access(self):
        pts = [Point(x,0,0) for x in range(10)]
        pline = PLine(pts)
        for n in range(len(pline)) : self.assertEqual(pts[n],pline[n],"points constructor appends points to verts list, and item access is working")
        
        self.assertEqual(pts[0:2],pline[0:2],"slicing item access is working")

        def func(): pline[0:2] = Point()
        self.assertRaises(TypeError,func) # confirms that an error is raised when this we try to set a point using slicing syntax

    def test_appending_points(self):
        pts = [Point(x,0,0) for x in range(10)]
        pgon = PGon(pts,basis=CS(Point(0,0,-1))) # the pts here are interpreted in local coordinates
        self.assertEqual(Point(0,0,-1),pgon[0],"when constructing with a defined basis, the given points are interpreted in local coordinates")

        pgon = PGon()

