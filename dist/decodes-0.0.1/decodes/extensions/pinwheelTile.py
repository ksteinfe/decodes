# FGC Part 4
# pinwheelTile.py
# provides classes that support pinwheel tile inflation
from .. import *
from ..core import *
from ..core import base, vec, point, cs, line, mesh, pgon
import math

# according to Radin, the pinwheel tiling contains one prototyle 
# a triangle with the following edge lenghts: 1, 2, sqrt(5)
# (http://www.ma.utexas.edu/users/radin/papers/pinwheel.pdf)
# (http://www.michaelwhittaker.ca/fractalpinwheel.pdf)
# some nice variation (color) here: http://tilings.math.uni-bielefeld.de/substitution_rules/pinwheel_1_2_0

class PwTile(object):    
    xf_scale = Xform.scale(1/math.sqrt(5))    #= 0.447213595
    basePts = [
        Point(),
        Point(2.0, 0.0),
        Point(0.0, 1.0),
        Point(0.2, 0.4),
        Point(1.2, 0.4),
        Point(0.4, 0.8),
        Point(1.0, 0.0),
    ]

    def __init__(self,lineage="RT",**kargs):
        self.lineage = lineage
        self.xf = kargs["xf"] if "xf" in kargs else Xform()
        
    def _CSFromBasePts(self,oPt,xPt,yPt):
        '''
        Returns a CS oriented to this tile's (world) points
        rlvl: the recursion level to scale the base points to
        oPt: index of origin point
        xPt: index of a point on the desired x-axis
        yPt: index of a point on the desired y-axis
        '''
        return CS(PwTile.basePts[oPt],PwTile.basePts[xPt]-PwTile.basePts[oPt],PwTile.basePts[yPt]-PwTile.basePts[oPt])
            
    def draw(self):
        msh = Mesh()
        msh.append(PwTile.basePts[0] * self.xf)
        msh.append(PwTile.basePts[1] * self.xf)
        msh.append(PwTile.basePts[2] * self.xf)
        msh.add_face(0,1,2)
        msh.name = self.lineage
        return msh
    
    def centroid(self): return Point.centroid([p*self.xf for p in PwTile.basePts])
    
    def inflate(self):
        cs = self._CSFromBasePts(3,6,5)
        tile0 = PwTile(self.lineage+",0", xf=self.xf * cs.xform * PwTile.xf_scale )
                                                                                                                                                                                     
        cs = self._CSFromBasePts(4,5,6)                                                                                                                
        tile1 = PwTile(self.lineage+",1", xf=self.xf * cs.xform * PwTile.xf_scale )
                                                                                                                                                                                     
        cs = self._CSFromBasePts(3,6,0)                                                                                                                
        tile2 = PwTile(self.lineage+",2", xf=self.xf * cs.xform * PwTile.xf_scale )
                                                                                                                                                                                     
        cs = self._CSFromBasePts(5,0,2)                                                                                                                
        tile3 = PwTile(self.lineage+",3", xf=self.xf * cs.xform * PwTile.xf_scale )
        
        cs = self._CSFromBasePts(4,1,6)
        tile4 = PwTile(self.lineage+",4", xf=self.xf * cs.xform * PwTile.xf_scale )
        
        return [tile0,tile1,tile2,tile3,tile4]



