import unittest
import decodes.core as dc
from decodes.core import *
from decodes.extensions.voxel import *

class Tests(unittest.TestCase):

    def test_constructor(self):
        bounds = Bounds(center=Point(),dim_x=8,dim_y=8,dim_z=8)
        vf = VoxelField(bounds,4,4,4)

        vf.set(0,0,0,10.0)
        vf.set(3,3,3,10.0)
        self.assertEqual(vf.get(0,0,0),10.0)
        self.assertEqual(vf.get(3,3,3),10.0)
        self.assertEqual(vf.get(2,2,2),0.0)

    def test_bounds_and_cpt(self):
        bounds = Bounds(center=Point(),dim_x=8,dim_y=8,dim_z=8)
        vf = VoxelField(bounds,4,4,4)

        self.assertEqual(vf.dim_pixel,Vec(2,2,2))
        self.assertEqual(vf.cpt_at(0,0,0),Point(-3,-3,-3))

        vf.bounds = Bounds(center=Point(),dim_x=12,dim_y=12,dim_z=8)
        self.assertEqual(vf.dim_pixel,Vec(3,3,2))
        self.assertEqual(vf.cpt_at(0,0,0),Point(-4.5,-4.5,-3))


        