from decodes.core import *
from . import dc_base, dc_vec, dc_point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "cs.py loaded"
import math, copy, collections

class CS(Geometry, IsBasis):
    """a ortho coordinate system class"""
    """a simple orthonormal cs floating around in R3"""
    """can describe any translation and rigid-body manipulation of the R3"""
    
    def __init__(self,a=None,b=None,c=None):
        """
        CS Constructor.

        .. todo:: write docstring detailing the different ways of constructing a CS
        """
        #TODO: make axes priviate and provide getters and setters that maintain orthagonality and right-handedness
        pt,vecX,vecY = Point(), Vec(1,0), Vec(0,1)
        if all( hasattr(a,i) for i in ['x','y','z'] ) :
            # a is something that acts like a point
            pt=a
            if b is not None : vecX = b
            if c is not None : vecY = c
            #TODO: handle situation when we've been passed three points
        else :
            # a cannont act like a point, let's try to make a point out of a,b,c
            pt = Point(a,b,c)

        try: self.origin = pt.basis_applied()
        except : self.origin = pt

        if vecX.length == 0 : raise GeometricError("vecX is a Vector of length 0")
        if vecY.length == 0 : raise GeometricError("vecY is a Vector of length 0")

        self.xAxis = vecX.normalized()
        self.zAxis = self.xAxis.cross(vecY).normalized()
        self.yAxis = self.zAxis.cross(self.xAxis).normalized()

    def __repr__(self):
        return "cs o[{0},{1},{2}] n[{3},{4},{5}]".format(self.origin.x,self.origin.y,self.origin.z,self.zAxis.x,self.zAxis.y,self.zAxis.z)

    """a CS can act as a basis for a point"""
    def eval(self,a=0,b=0,c=0):
        try:
            # try using a as a point
            x = a.x
            y = a.y
            z = a.z
        except:
            x = a
            y = b
            z = c
        return self.origin + ((self.xAxis*x)+(self.yAxis*y)+(self.zAxis*z))

    @property
    def xform(self):
        from .dc_xform import Xform
        return Xform.change_basis(CS(), self)
        
    @property
    def ixform(self): 
        from .dc_xform import Xform
        return Xform.change_basis(self, CS())
    

class CylCS(Geometry, IsBasis):
    """a cylindrical coordinate system"""
    def __init__(self,pt=Point(0,0)):
        self.origin = pt

        def __repr__(self):
            return "cylcs o[{0},{1},{2}]".format(self.origin.x,self.origin.y,self.origin.z)

    """a CylCS can act as a basis for a point"""
    def eval(self,other):
        try:
            radius = other.x
            radians = other.y
            z = other.z
        except TypeError:
            print("mallard can't quack()")
                
        return Point( radius * math.cos(radians), radius * math.sin(radians), z) + self.origin
        
        
