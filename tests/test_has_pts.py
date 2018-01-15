import unittest
import decodes.core as dc
from decodes.core import *

class Tests(unittest.TestCase):

    def test_item_access(self):
        vecs = [Point(x,0,0) for x in range(10)]
        pline = PLine(vecs)
        for n in range(len(pline)) : self.assertEqual(vecs[n],pline[n],"points constructor appends points to verts list, and item access is working")
        
        self.assertEqual(vecs[0:2],pline[0:2],"slicing item access returns a REFERENCE to the stored vectors")
        
        sliced_pts = pline.pts[2:3]
        sliced_vecs = vecs[2:3]
        for n in range(len(sliced_vecs)):
            self.assertEqual(sliced_vecs[n],sliced_pts[n],"the pts function returns a tuple of point objects")

        def func(): pline[0:2] = Point()
        self.assertRaises(TypeError,func) # confirms that an error is raised when this we try to set a point using slicing syntax

        vecs = [Point(x,0,0) for x in range(10)]
        pline = PLine(vecs)
        pline[1] = Point(1.1,-2)
        pline[2] = Point(2.1,-2)
        self.assertEqual(pline.pts[0],Point(0,0,0))
        self.assertEqual(pline.pts[1],Point(1.1,-2,0))
        self.assertEqual(pline.pts[2],Point(2.1,-2,0))

        def func(): pline[1:2] = [Point(1.1,-2),Point(2.1,-2)]
        self.assertRaises(TypeError,func) # confirms that an error is raised when this we try to set a point using slicing syntax

    def test_swap_basis(self):
        vecs = [Vec(1.0,n,n) for n in Interval(0,math.pi)/10]
        cs_a = CS(0,0,-1)

        pl = PLine(vecs,basis=cs_a)
        for n, val in enumerate(Interval(0,math.pi)/10): self.assertEqual(Point(1.0,val,val-1),pl.pts[n])

        pl.basis = CylCS()
        for n, val in enumerate(Interval(0,math.pi)/10): 
            self.assertEqual(Point( math.cos(val), math.sin(val), val) ,pl.pts[n])



    def test_appending_points(self):
        pts = [Point(x,0,0) for x in range(10)]
        pgon = PGon(pts,basis=CS(Point(0,0,-1))) # the pts here are interpreted in local coordinates
        self.assertEqual(Vec(0,0,0),pgon[0],"when constructing with a defined basis, the given points are interpreted in local coordinates")
        self.assertEqual(Point(0,0,-1),pgon.pts[0],"when constructing with a defined basis, the given points are interpreted in local coordinates")

        pgon = PGon(basis=CS(1,2,3))
        pgon.append(Point())
        self.assertEqual(Vec(-1,-2,-3),pgon[0],"Points appended to a object with an already defined basis will be interpreted in world coordinates")
        self.assertEqual(Point(0,0,0),pgon.pts[0],"Points appended to a object with an already defined basis will be interpreted in world coordinates")

        pgon.append(Vec())
        self.assertEqual(Vec(0,0,0),pgon[1],"Vecs appended to a object with an already defined basis will be interpreted in local coordinates")
        self.assertEqual(Point(1,2,3),pgon.pts[1],"Vecs appended to a object with an already defined basis will be interpreted in local coordinates")

        #todo: replace an existing point

    def test_manipulating_points(self):
        pts = [Point(x,0,0) for x in range(10)]
        pgon = PGon(pts,basis=CS(Point(0,0,-1))) # the pts here are interpreted in local coordinates
        
        pgon[0].z = 100
        self.assertEqual(Vec(0,0,100),pgon[0],"square bracket access returns a reference to stored vectors, allowing for manipulation")
        self.assertEqual(Point(0,0,99),pgon.pts[0],"square bracket access returns a reference to stored vectors, allowing for manipulation")

        pgon.pts[1].z = 88
        self.assertEqual(Point(1,0,-1),pgon.pts[1],"access via the pts function returns a list of point objects, which does not permit manipulation")

    def test_centroid(self):
        nums = range(10)
        pgon = PGon([Point(x,0,0) for x in nums],basis=CS(Point(0,0,-1)))
        avg = sum(nums)/float(len(nums))
        self.assertEqual(Point(avg,0,-1),pgon.centroid,"centroid generates based points")

    def test_basis_applied_and_stripped(self):
        pts = [Point(x,0,0) for x in range(10)]
        pgon = PGon(pts,basis=CS(Point(0,0,-1))) # the pts here are interpreted in local coordinates
        pgon.set_weight(10)

        pgon_bapplied = pgon.basis_applied()
        pgon_bstripped = pgon.basis_stripped()

        for x in range(10) : self.assertEqual(Vec(x,0,-1),pgon_bapplied[x])
        self.assertEqual(10,pgon_bapplied.props['weight'])

        for x in range(10) : self.assertEqual(Vec(x,0,0),pgon_bstripped[x])
        self.assertEqual(10,pgon_bstripped.props['weight'])


    def test_unsetting(self):
        verts = [Vec(-1,-1),Vec(1,-1),Vec(1,1),Vec(-1,1)]
        pgon = PGon(verts,basis=CS(Point(0,0,-1))) # the pts here are interpreted in local coordinates

        cent = pgon.centroid
        self.assertEqual(Point(0,0,-1),cent)

        pts = pgon.pts
        for n in range(4): self.assertEqual(Point(verts[n].x,verts[n].y,-1),pts[n])

        edges = pgon.edges
        for n in range(3): self.assertEqual(Segment(Point(verts[n].x,verts[n].y,-1),Point(verts[n+1].x,verts[n+1].y,-1)),edges[n])

        class_attr = ['_pts','_edges','_centroid']