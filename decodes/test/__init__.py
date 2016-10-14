print("unit_tests loaded")
import unittest, importlib, sys, inspect, os


#__all__ = ["test_has_basis","test_cs","test_interval","test_line","test_mesh","test_pgon","test_point","test_vec","test_xform"]
__all__=["test_voxel","test_xsect","test_classical_surface","test_pgon", "test_pline","test_mesh","test_point","test_has_pts","test_curve","test_surface","test_plane","test_interval","test_line","test_vec","test_xform"]


filename = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+os.sep+'log.txt'
logfile = open(filename, "w")
for submod in __all__:
    logfile.write( "\n\n== "+submod.upper()+" ==\n" )
    mod = importlib.import_module("decodes.test."+submod)
    suite = unittest.TestLoader().loadTestsFromTestCase(mod.Tests)
    unittest.TextTestRunner(logfile,verbosity=2).run(suite)
logfile.close

