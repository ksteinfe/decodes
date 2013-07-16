import unittest
import decodes.core as dc
from decodes.core import *
from decodes.extensions.classical_surfaces import *

class Tests(unittest.TestCase):

    def test_rotational(self):
        def func(t):
            return Point(t,math.sin(t)+1.2)
        crv = Curve(func,Interval(0,math.pi*2))
        cs = CS(Point(2,2))
        rot_surf = RotationalSurface(cs,crv)

        # v isocurves result in based curves, which require basis-to-basis transformations
        # we currently do basis-to-basis xforms using rhino library
        # iso = rot_surf.isocurve(v_val=math.pi/2)

        iso = rot_surf.isocurve(u_val=0.25)

    def AssertPointsAlmostEqual(self,pa,pb,places=4):
        self.assertAlmostEqual(pa.x,pb.x,places)
        self.assertAlmostEqual(pa.y,pb.y,places)
        self.assertAlmostEqual(pa.z,pb.z,places)