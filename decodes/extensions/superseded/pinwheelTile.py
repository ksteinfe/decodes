# FGC Part 4
# pinwheelTile.py
# provides classes that support pinwheel tile inflation
import fieldpack as fp
from fieldpack import *
import math

# according to Radin, the pinwheel tiling contains one prototyle 
# a triangle with the following edge lenghts: 1, 2, sqrt(5)
# (http://www.ma.utexas.edu/users/radin/papers/pinwheel.pdf)
# (http://www.michaelwhittaker.ca/fractalpinwheel.pdf)
# some nice variation (color) here: http://tilings.math.uni-bielefeld.de/substitution_rules/pinwheel_1_2_0
# scale = 0.44721

class PwTile(object):
  factor = 1/math.sqrt(5)     #= 0.447213595
  divPts = [
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
    self.rlvl = kargs["rlvl"] if "rlvl" in kargs else 0 #recursion level, sets the size of tiles
    self.xf = kargs["xf"] if "xf" in kargs else Xform() #the transformation of this tile (ignores scale)
    self.flip = kargs["flip"] if "flip" in kargs else False #is this tile flipped?
    
  def _scaledDivPts(self,rlvl):
    xf_scale = Xform.scale(math.pow(self.factor,rlvl))
    return map(lambda pt: pt*xf_scale,self.divPts)
    
  def _CSFromBasePts(self,oPt,xPt,yPt):
    '''
    Returns a CS oriented to a scaled version of this tile's div points
    rlvl: the recursion level to scale the div points to
    oPt: index of origin point
    xPt: index of a point on the desired x-axis
    yPt: index of a point on the desired y-axis
    '''
    placedPts = [p * self.xf for p in self._scaledDivPts(self.rlvl)]
    return CS(placedPts[oPt],placedPts[xPt]-placedPts[oPt],placedPts[yPt]-placedPts[oPt])
      
  def draw(self,drawCS=False):
    msh = Mesh()
    msh.basis = self.xf
    msh.add_vert(self._scaledDivPts(self.rlvl)[0])
    msh.add_vert(self._scaledDivPts(self.rlvl)[1])
    msh.add_vert(self._scaledDivPts(self.rlvl)[2])
    msh.add_face(0,1,2)
    msh.name = self.lineage
    
    cs = CS()*self.xf
    cs.name = self.lineage
    if drawCS : return msh,cs
    return msh
    
  def inflate(self):
    cs = self._CSFromBasePts(3,6,5)
    tile0 = PwTile(self.lineage+",0", xf=cs.xform, rlvl=self.rlvl+1, flip=self.flip)
    
    cs = self._CSFromBasePts(4,5,6)
    tile1 = PwTile(self.lineage+",1", xf=cs.xform, rlvl=self.rlvl+1, flip=self.flip)
    
    cs = self._CSFromBasePts(3,6,0)
    tile2 = PwTile(self.lineage+",2", xf=cs.xform, rlvl=self.rlvl+1, flip=not self.flip)

    cs = self._CSFromBasePts(5,0,2)
    tile3 = PwTile(self.lineage+",3", xf=cs.xform, rlvl=self.rlvl+1, flip=not self.flip)

    cs = self._CSFromBasePts(4,1,6)
    tile4 = PwTile(self.lineage+",4", xf=cs.xform, rlvl=self.rlvl+1, flip=not self.flip)
    
    return [tile0,tile1,tile2,tile3,tile4]



