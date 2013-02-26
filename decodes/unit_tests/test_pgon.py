import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    def test_empty_constructor(self):
        pgon = PGon()
        self.assertEqual(len(pgon.verts),0,"a polygon constructed with no arguments contains an empty list of verts")
        
    def test_nothing(self):
        self.fail("i will always fail this test!")
