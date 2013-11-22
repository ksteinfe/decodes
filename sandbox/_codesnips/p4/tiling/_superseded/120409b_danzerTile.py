# FGC Part 4
# danzerTile.py
# provides classes that support danzer tile inflation
import fieldpack as fp
from fieldpack import *
import math

# according to Danzer, the basic tile set contains tets with 
# lengths that are combonations of four possible values:
# (http://www.cs.williams.edu/~98bcc/tiling/danztable.html)
# a = (sqrt(10+2*sqrt(5)))/4  = 0.951056516
# b = sqrt(3) / 2             = 0.866025404
# t = (1 + sqrt(5)) / 2       = 1.61803399
# ti = 1/t                    = 0.618033989
#
# edge lengths are given by the table below
# [dihedral angles between the tet faces shared by these edges
# are shown in brackets]
# 
# (tile)  (e1-2)    (e2-3)   (e3-1)    (e2-4)    (e1-4)     (e3-4)
# ATile   [36]a     [60]Tb   [72]Ta    [108]a    [90]1      [60]b
# B       [36]a	    [36]Ta   [60]Tb	   [120]b	   [108]Tia   [90]1
# C       [36]Tia	  [60]Tb   [90]T	   [120]b    [72]a	    [36]a
# K       [36]a	    [60]b	   [72]Tia   [90]T/2   [90]1/2    [90]Ti/2

# here's every possible combonation of edge lengths
# a = (sqrt(10+2*sqrt(5)))/4  = 0.951056516
# b = sqrt(3) / 2             = 0.866025404
# t = (1 + sqrt(5)) / 2       = 1.61803399 
# ti = 1/t                    = 0.618033989
# t*b = 	1.40125854	
# t*a = 	1.53884177  
# ti*a =	0.587785252 
# t/2 = 	0.809016995 
# ti/2 = 	0.309016994



class DzTile(object):
  tau = (1 + math.sqrt(5)) / 2     #= 1.61803399
  taui = 1/tau  #= 0.618033989
    
  def __init__(self,**kargs):
    self.rlvl = kargs["rlvl"] if "rlvl" in kargs else 0 #recursion level, sets the size of tiles
    self.xf = kargs["xf"] if "xf" in kargs else Xform() #the transformation of this tile
    self.flip = kargs["flip"] if "flip" in kargs else False #the transformation of this tile
    
  def _tilePts(self):
    #pts = map(lambda pt:pt*self.xf,self.basePts)
    factor = math.pow(DzTile.taui,self.rlvl)
    xf_scale = Xform.scale(factor)
    return map(lambda pt:(pt*xf_scale)*self.xf,self.basePts)
  
  def _scaledBasePts(self,rlvl):
    #return map(lambda pt: pt*(1/DzTile.tau),self.basePts)
    factor = math.pow(DzTile.taui,rlvl)
    xf_scale = Xform.scale(factor)
    return map(lambda pt: pt*xf_scale,self.basePts)
    
  def toMesh(self):
    msh = Mesh()
    for v in self._tilePts() : msh.add_vert(v)
    msh.add_face(0,1,2)
    msh.add_face(1,2,3)
    msh.add_face(2,3,0)
    msh.add_face(3,0,1)
    return msh
    
  def draw(self):
    return self.toMesh(),CS()*self.xf
    
  def _PositionByChildAndParentCS(self,childTile,csChild,csParent,flip):
    '''
    Finds the proper XForm for a child tile given:
    csChild : a source CS positioned on child's base points at rlvl = 1
    csParent : a target CS positioned on parent's base points at rlvl = 0
    flip: flip this child tile?
    '''
    xfBase = Xform.change_basis(csChild,csParent) # defines the transformation that takes us from idealized parent to idealized child
    csBase = CS()*xfBase # the coordinate system at xfIdeal
    csTile = csBase*self.xf # CS at real parent
    xf = Xform.change_basis(CS(),csTile) # defines the transformation that takes us from idealized parent to real parent
    if flip : xf = xf * Xform.mirror()
    childTile.xf = xf
    childTile.flip = flip
    childTile.rlvl = self.rlvl + 1
    return childTile

  def _PositionByParentCS(self,childTile,csParent,flip):
    '''
    Finds the proper XForm for a child tile given:
    childTile: a child tile (using default construction, ex: DxTileA()
    csParent : a target CS positioned on parent's base points at rlvl = 0
    flip: flip this child tile?
    '''
    cbPts = childTile._scaledBasePts(self.rlvl+1) # child's base points (inflated to rlvl+1)
    csChild = CS()
    childTile = self._PositionByChildAndParentCS(childTile,csChild,csParent,flip)
    return childTile
  
  @classmethod
  def _CSFromBasePts(cls,rlvl,oPt,xPt,yPt):
    '''
    Returns a CS oriented to this tile's base points scaled to a given rlvl
    rlvl:
    oPt: index of origin point
    xPt: index of a point on the desired x-axis
    yPt: index of a point on the desired y-axis
    '''
    sbasePts = cls()._scaledBasePts(rlvl)
    return CS(sbasePts[oPt],sbasePts[xPt]-sbasePts[oPt],sbasePts[yPt]-sbasePts[oPt])
 
 
class DzTileA(DzTile):
  basePts= ( 
      Vec(0.0       , 0.0	      , 0.0   ),
      Vec(0.9510565	, 0.0   	  , 0.0   ),
      Vec(0.6881910 , 1.3763819 , 0.0   ),
      Vec(0.5257311 , 0.6881910	, 0.5   )
      )
      
  def inflate(self):
    iTiles = []
    pbPts = DzTileA()._scaledBasePts(self.rlvl) # parent's base points

    #DzTileB by orienting defined CS on child to defined CS on parent
    cbPts = DzTileB()._scaledBasePts(self.rlvl+1) # child's base points (inflated to rlvl+1)
    csChild = CS(cbPts[2],cbPts[1]-cbPts[2],cbPts[0]-cbPts[2])
    csParent = CS(pbPts[0],pbPts[1]-pbPts[0],pbPts[3]-pbPts[0])
    tileB0 = self._PositionByChildAndParentCS(DzTileB(),csChild,csParent,flip=self.flip) # same handedness as parent

    #DzTileC by orienting defined CS on child to defined CS on parent
    cbPts = DzTileC()._scaledBasePts(self.rlvl+1) # child's base points (inflated to rlvl+1)
    csChild = CS(cbPts[1],cbPts[2]-cbPts[1],cbPts[0]-cbPts[1])
    csParent = CS(pbPts[3],pbPts[2]-pbPts[3],pbPts[1]-pbPts[3])
    tileC0 = self._PositionByChildAndParentCS(DzTileC(),csChild,csParent,flip=self.flip) # same handedness as parent
    
    for t in [tileB0,tileC0] : iTiles.append(t)
    return iTiles
     
class DzTileB(DzTile):
  basePts= ( 
      Vec(0.0       , 0.0	      , 0.0   ),
      Vec(0.9510565	, 0.0   	  , 0.0   ),
      Vec(0.2628656 , 1.3763819	, 0.0   ),
      Vec(0.2628656 , 0.4253254 , 0.3090170)
    )
    
  def inflate(self):
    iTiles = []
    pbPts = DzTileB()._scaledBasePts(self.rlvl) # parent's base points

    #DzTileB by orienting child origin to defined CS on parent
    parentCS = CS(pbPts[3], pbPts[0]-pbPts[3], pbPts[1]-pbPts[3])
    tileB0 = self._PositionByParentCS(DzTileB(),parentCS,not self.flip)  # opposite handdeness as parent
    
    #DzTileK by orienting child origin to defined CS on parent
    parentCS = CS(pbPts[3], pbPts[0]-pbPts[3], pbPts[2]-pbPts[3])
    tileK0 = self._PositionByParentCS(DzTileK(),parentCS,self.flip)# same handedness as parent
    #DzTileK by rotating the previous tile
    xf_rot = Xform.rotation(center=tileK0._tilePts()[0], angle=math.pi, axis=tileK0._tilePts()[3]-tileK0._tilePts()[0])
    tileK1 = DzTileK(xf=xf_rot*tileK0.xf,rlvl=self.rlvl+1,flip=self.flip)# same handedness as parent
    
    #DzTileK by orienting defined CS on child to defined CS on parent
    cbPts = DzTileK()._scaledBasePts(self.rlvl+1) # child's base points (inflated to rlvl+1)
    csChild = CS(cbPts[1],cbPts[0]-cbPts[1],cbPts[3]-cbPts[1])
    csParent = CS(pbPts[0],pbPts[3]-pbPts[0],pbPts[1]-pbPts[0])
    tileK2 = self._PositionByChildAndParentCS(DzTileK(),csChild,csParent,flip=not self.flip) # opposite handedness as parent
    #DzTileK by rotating the previous tile
    xf_rot = Xform.rotation(center=tileK2._tilePts()[0], angle=math.pi, axis=tileK2._tilePts()[3]-tileK2._tilePts()[0])
    tileK3 = DzTileK(xf=xf_rot*tileK2.xf,rlvl=self.rlvl+1,flip=not self.flip)  # opposite handedness as parent
    
    #DzTileB by orienting defined CS on child to defined CS on parent
    cbPts = DzTileB()._scaledBasePts(self.rlvl+1) # child's base points (inflated to rlvl+1)
    csChild = CS(cbPts[2],cbPts[0]-cbPts[2],cbPts[1]-cbPts[2])
    csParent = CS(pbPts[1],pbPts[3]-pbPts[1],pbPts[2]-pbPts[1])
    tileB1 = self._PositionByChildAndParentCS(DzTileB(),csChild,csParent,flip=self.flip) # same handedness as parent
    
    #DzTileC by orienting child origin to defined CS on parent
    parentCS = CS(pbPts[3],tileK0._tilePts()[2]-pbPts[3], pbPts[2]-pbPts[3])
    tileC0 = self._PositionByParentCS(DzTileC(),parentCS,self.flip)  # same handedness as parent
    
    #for t in [tileB0,tileK0,tileK1,tileK2,tileK3,tileB1,tileC0] : iTiles.append(t)
    for t in [tileB0,tileK0,tileK1,tileK2,tileK3,tileB1] : iTiles.append(t)
    return iTiles

class DzTileC(DzTile):
  basePts= (
      Vec(0.0       , 0.0	      , 0.0   ),
      Vec(0.5877853	, 0.0   	  , 0.0   ),
      Vec(0.8506509 , 1.3763819	, 0.0   ),
      Vec(0.4253254 , 0.6881910 , 0.50 )
    )
    
  def inflate(self):
    pass

class DzTileK(DzTile):
  basePts= ( 
    Vec(0.0       , 0.0	      , 0.0   ),
    Vec(0.9510565	, 0.0   	  , 0.0   ),
    Vec(0.2628656 , 0.5257311 , 0.0   ),
    Vec(0.2628656 , 0.3440955 , 0.250 )
    )
  

  def inflate(self):
    iTiles = []
    pbPts = DzTileK()._scaledBasePts(self.rlvl) # parent's base points
    
    #DzTileK by orienting defined CS on child to defined CS on parent
    cbPts = DzTileK()._scaledBasePts(self.rlvl+1) # child's base points (inflated to rlvl+1)
    csChild = CS(cbPts[3],cbPts[1]-cbPts[3],cbPts[0]-cbPts[3])
    csParent = CS(pbPts[3],pbPts[0]-pbPts[3],pbPts[2]-pbPts[3])
    tileK0 = self._PositionByChildAndParentCS(DzTileK(),csChild,csParent,self.flip) # same handedness as parent
    
    #DzTileB by orienting child origin to defined CS on parent
    parentCS = CS(pbPts[2],pbPts[2]*-1,Vec(1,0,0))
    tileB0 = self._PositionByParentCS(DzTileB(),parentCS,self.flip)# same handedness as parent
    
    for t in [tileK0,tileB0] : iTiles.append(t)
    return iTiles


def DanzerAxiom():
  outie = fp.make_out(fp.outies.Rhino, "axiom")
  outie.iconscale = 0.1
  ta = DzTileA(xf=Xform.translation(Vec(1,0,0)),rlvl=1)
  tb = DzTileB(xf=Xform.translation(Vec(2,0,0)),rlvl=1)
  tc = DzTileC(xf=Xform.translation(Vec(3,0,0)),rlvl=1)
  tk = DzTileK(xf=Xform.translation(Vec(4,0,0)),rlvl=1)
  
  for t in [ta,tb,tc,tk] : outie.put(t.draw())
  outie.draw()


# Here we check the inflations for each tile type


def inflationA(out_0,out_1,out_2):
  xform = Xform.rotation(center=Point(0,1), angle=math.pi/2, axis=Vec(0,0,1))
  tb = DzTileA(xf=Xform(),rlvl=0)
  out_0.put(tb.draw())
  
  inflt1 = tb.inflate()
  for tile in inflt1 : 
    out_1.put(tile.draw())
    #inflt2 = tile.inflate()
    #for tile in inflt2 : out_2.put(tile.draw())

def inflationB(out_0,out_1,out_2):
  xform = Xform.rotation(center=Point(0,1), angle=math.pi/2, axis=Vec(0,0,1))
  tb = DzTileB(xf=Xform(),rlvl=0)
  out_0.put(tb.draw())
  
  inflt1 = tb.inflate()
  for tile in inflt1 : 
    out_1.put(tile.draw())
    inflt2 = tile.inflate()
    for tile in inflt2 : out_2.put(tile.draw())

def inflationK(out_0,out_1,out_2):
  xform = Xform.rotation(center=Point(0,1), angle=math.pi/2, axis=Vec(0,0,1))
  tk = DzTileK(xf=xform,rlvl=0)
  out_0.put(tk.draw())

  inflt1 = tk.inflate()
  for tile in inflt1 : 
    out_1.put(tile.draw())
    inflt2 = tile.inflate()
    for tile in inflt2 : out_2.put(tile.draw())


# Here we check to see if this file is being executed as the "main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if __name__ == '__main__' :
    out_0 = fp.make_out(fp.outies.Rhino, "0")
    out_0.set_color(0,0,0)
    out_0.iconscale = 0.2
    
    out_1 = fp.make_out(fp.outies.Rhino, "1")
    out_1.set_color(0.5,0.5,1.0)
    out_1.iconscale = 0.1
  
    out_2 = fp.make_out(fp.outies.Rhino, "2")
    out_2.set_color(1.0,0.5,1.0)
    out_2.iconscale = 0.05  
    
    #DanzerAxiom()
    inflationA(out_0,out_1,out_2)
    #inflationB(out_0,out_1,out_2)
    #inflationK(out_0,out_1,out_2)
    
    for outie in [out_0,out_1,out_2] : outie.draw()
