import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_bad_combonations(self):
        xsec = Intersector()
        with self.assertRaises(NotImplementedError): xsec.of(CS().xy_plane,Point())
        with self.assertRaises(NotImplementedError): xsec.of("afsd",10)
        with self.assertRaises(NotImplementedError): xsec.of(Point(),Ray(Point(2,2,-1),Vec(0,0,1)))

    def test_ray_plane(self):
        xsec = Intersector()

        ray = Ray(Point(2,2,1),Vec(0,0,-1))
        pln = CS().xy_plane
        self.assertEqual(xsec.of(ray,pln),True)
        self.assertEqual(xsec[0],Point(2,2,0))

        ray = Ray(Point(2,2,-1),Vec(0,0,1)) # ray behind plane
        self.assertEqual(xsec.of(ray,pln),True)
        self.assertEqual(xsec[0],Point(2,2,0))
        
        self.assertEqual(xsec.of(ray,pln,ignore_backface=True),False)
        self.assertEqual(len(xsec),0)

        ray = Ray(Point(2,2,1),Vec(0,0,1)) # plane behind ray
        self.assertEqual(xsec.of(ray,pln),False)
        self.assertEqual(len(xsec),0)
        
    def test_line_plane(self):
        xsec = Intersector()

        line = Line(Point(2,2,1),Vec(0,0,-1))
        pln = CS().xy_plane
        self.assertEqual(xsec.of(line,pln),True)
        self.assertEqual(xsec[0],Point(2,2,0))

        line = Line(Point(2,2,-1),Vec(0,0,1)) # line behind plane
        self.assertEqual(xsec.of(line,pln),True)
        self.assertEqual(xsec[0],Point(2,2,0))

        self.assertEqual(xsec.of(line,pln,ignore_backface=True),False)
        self.assertEqual(len(xsec),0)

        line = Line(Point(2,2,1),Vec(0,0,1)) # plane behind line
        self.assertEqual(xsec.of(line,pln),True)
        self.assertEqual(xsec[0],Point(2,2,0))

        line = Line(Point(2,2,0),Vec(0,1)) # line lies in plane
        self.assertEqual(xsec.of(line,pln),False)
        self.assertEqual(len(xsec),0)

        line = Line(Point(2,2,2),Vec(0,1)) # line parallel to plane
        self.assertEqual(xsec.of(line,pln),False)
        self.assertEqual(len(xsec),0)

    def test_seg_plane(self):
        xsec = Intersector()

        seg = Segment(Point(2,2,0.5),Vec(0,0,-1)) # seg crosses plane from front
        pln = CS().xy_plane
        self.assertEqual(xsec.of(seg,pln),True)
        self.assertEqual(xsec[0],Point(2,2,0))

        seg = Segment(Point(2,2,-0.5),Vec(0,0,1)) # seg crosses plane from behind
        self.assertEqual(xsec.of(seg,pln),True)
        self.assertEqual(xsec[0],Point(2,2,0))

        seg = Segment(Point(2,2,0.5),Vec(0,0,1)) # seg points away from plane
        self.assertEqual(xsec.of(seg,pln),False)
        self.assertEqual(len(xsec),0)

        seg = Segment(Point(2,2,1.5),Vec(0,0,-1)) # seg points toward plane
        self.assertEqual(xsec.of(seg,pln),False)
        self.assertEqual(len(xsec),0)

        seg = Segment(Point(2,2,0),Vec(0,1)) # seg lies in plane
        self.assertEqual(xsec.of(seg,pln),False)
        self.assertEqual(len(xsec),0)

        seg = Segment(Point(2,2,2),Vec(0,1)) # seg parallel to plane
        self.assertEqual(xsec.of(seg,pln),False)
        self.assertEqual(len(xsec),0)

    def test_circ_circ(self):
        xsec = Intersector()

        circ_a = Circle(CS().xy_plane,1.0)
        circ_b = Circle(CS.on_xy(1,0).xy_plane,1.0)
        self.assertEqual(xsec.of(circ_a,circ_b),True)
        
    def test_ray_pgon(self):
        xsec = Intersector()
        pgon = RGon(4, radius=1.0)
        
        ray = Ray(Point(0.5,0.5,1),Vec(0,0,-1)) # ray intersects pgon
        self.assertEqual(xsec.of(ray,pgon),True)
        self.assertEqual(xsec[0],Point(0.5,0.5,0))

        ray = Ray(Point(2,2,1),Vec(0,0,-1)) # ray intersects plane of pgon, but misses pgon
        self.assertEqual(xsec.of(ray,pgon),False)
        self.assertIsNotNone(xsec.log)


        ray = Ray(Point(0.5,0.5,-1),Vec(0,0,1)) # ray behind pgon
        self.assertEqual(xsec.of(ray,pgon),True)
        self.assertEqual(xsec[0],Point(0.5,0.5,0))
        
        self.assertEqual(xsec.of(ray,pgon,ignore_backface=True),False) # ray behind pgon, ignoring backfaces
        self.assertEqual(len(xsec),0)
        self.assertIsNotNone(xsec.log)


        ray = Ray(Point(0,0,1),Vec(0,0.25,-0.75)) # results in a pt slightly off of base plane, tests for tolerence of pgon.contains point
        pgon = RGon(4,1.0)
        test = xsec.of(ray,pgon)
        self.assertEqual(xsec.of(ray,pgon),True)

    def test_plane_plane(self):
        xsec = Intersector()

        pln_a = CS().xy_plane
        pln_b = CS().xz_plane
        self.assertEqual(xsec.of(pln_a,pln_b),True)
        self.assertEqual(xsec[0]._vec,Vec(1,0,0))

    def test_line_line(self):
        xsec = Intersector()

        ln_a = Line(Point(2,1),Vec(1,1))
        ln_b = Line(Point(-1,0),Vec(2,0))
        self.assertEqual(xsec.of(ln_a,ln_b),True)
        self.assertEqual(xsec[0],Point(1,0))
        self.assertEqual(ln_a.eval(xsec.ta),xsec[0])
        self.assertEqual(ln_b.eval(xsec.tb),xsec[0])

        ln_a = Line(Point(2,1),Vec(10,10))
        ln_b = Line(Point(-1,0),Vec(2,0))
        self.assertEqual(xsec.of(ln_a,ln_b),True)
        self.assertEqual(xsec[0],Point(1,0))
        self.assertEqual(ln_a.eval(xsec.ta),xsec[0])
        self.assertEqual(ln_b.eval(xsec.tb),xsec[0])

        ln_a = Line(Point(2,1),Vec(1,1))
        ln_b = Line(Point(-1,0),Vec(20,0))
        self.assertEqual(xsec.of(ln_a,ln_b),True)
        self.assertEqual(xsec[0],Point(1,0))
        self.assertEqual(ln_a.eval(xsec.ta),xsec[0])
        self.assertEqual(ln_b.eval(xsec.tb),xsec[0])

        ln_a = Line(Point(2,1),Vec(10,10))
        ln_b = Line(Point(-1,0),Vec(20,0))
        self.assertEqual(xsec.of(ln_a,ln_b),True)
        self.assertEqual(xsec[0],Point(1,0))
        self.assertEqual(ln_a.eval(xsec.ta),xsec[0])
        self.assertEqual(ln_b.eval(xsec.tb),xsec[0])

