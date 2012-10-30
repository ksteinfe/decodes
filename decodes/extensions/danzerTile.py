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
    
  def __init__(self,lineage="RT",**kargs):
    self.lineage = lineage
    self.rlvl = kargs["rlvl"] if "rlvl" in kargs else 0 #recursion level, sets the size of tiles
    self.xf = kargs["xf"] if "xf" in kargs else Xform() #the transformation of this tile  (ignores scale)
    self.flip = kargs["flip"] if "flip" in kargs else False #is this tile flipped?
    
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
    if self.flip : 
      msh.add_face(0,1,2)
      msh.add_face(1,3,2)
      msh.add_face(2,3,0)
      msh.add_face(3,1,0)
    else :
      msh.add_face(0,2,1)
      msh.add_face(1,2,3)
      msh.add_face(2,0,3)
      msh.add_face(3,0,1)
    return msh
    
  def draw(self,drawCS=False):
    msh = self.toMesh()
    msh.name = self.lineage
    
    cs = CS()*self.xf
    cs.name = self.lineage
    if drawCS : return msh,cs
    return msh
    
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
  def _CSFromBasePts(cls,rlvl,oPt,xPt,yPt,flipBase=False):
    '''
    Returns a CS oriented to a scaled version of this tile's base points
    rlvl: the recursion level to scale the base points to
    oPt: index of origin point
    xPt: index of a point on the desired x-axis
    yPt: index of a point on the desired y-axis
    flipBase: useful when trying to orient a flipped tile
    '''
    sbasePts = cls()._scaledBasePts(rlvl)
    if flipBase : sbasePts[3].z *= -1
    return CS(sbasePts[oPt],sbasePts[xPt]-sbasePts[oPt],sbasePts[yPt]-sbasePts[oPt])
 
 
class DzTileA(DzTile):
  basePts= ( 
      Vec(0.0       , 0.0	      , 0.0   ),
      Vec(0.9510565	, 0.0   	  , 0.0   ),
      Vec(0.6881910 , 1.3763819 , 0.0   ),
      Vec(0.5257311 , 0.6881910	, 0.5   )
      )
      
  def inflate(self):
    #DzTileB by orienting defined CS on child to defined CS on parent
    csChild = DzTileB()._CSFromBasePts(self.rlvl+1,  2,1,0 )
    csParent = DzTileA()._CSFromBasePts(self.rlvl,  0,1,3 )
    tileB0 = self._PositionByChildAndParentCS(DzTileB(self.lineage+",B0"),csChild,csParent,flip=self.flip) # same handedness as parent

    #DzTileC by orienting defined CS on child to defined CS on parent
    csChild = DzTileC()._CSFromBasePts(self.rlvl+1,  1,2,0 )
    csParent = DzTileA()._CSFromBasePts(self.rlvl,  3,2,1 )
    tileC0 = self._PositionByChildAndParentCS(DzTileC(self.lineage+",C0"),csChild,csParent,flip=self.flip) # same handedness as parent
    
    #DzTileC by orienting defined CS on child to defined CS on parent
    csChild = DzTileC()._CSFromBasePts(self.rlvl+1,  2,3,1, True )
    csParent = DzTileA()._CSFromBasePts(self.rlvl,  2,0,1 )
    tileC1 = self._PositionByChildAndParentCS(DzTileC(self.lineage+",C1"),csChild,csParent,flip=not self.flip) # opposite handedness as parent
    
    #DzTileK by orienting defined CS on child to defined CS on parent
    csChild = DzTileK()._CSFromBasePts(self.rlvl+1,  2,0,3, True)
    csParent = DzTileA()._CSFromBasePts(self.rlvl,  3,1,0 )
    tileK0 = self._PositionByChildAndParentCS(DzTileK(self.lineage+",K0"),csChild,csParent,flip=not self.flip) # opposite handedness as parent
    #DzTileK by mirroring the previous tile
    cs = CS(tileK0._tilePts()[0],tileK0._tilePts()[1]-tileK0._tilePts()[0],tileK0._tilePts()[3]-tileK0._tilePts()[0])
    xf_mir = Xform.mirror(cs)
    tileK1 = DzTileK(self.lineage+",K1",xf=xf_mir*tileK0.xf,rlvl=self.rlvl+1,flip=self.flip)  # opposite handedness as parent
    
    #DzTileB by orienting defined CS on child to defined CS on parent
    csChild = DzTileB()._CSFromBasePts(self.rlvl+1,  2,3,1 )
    csParent = DzTileA()._CSFromBasePts(self.rlvl,  0,3,2 )
    tileB1 = self._PositionByChildAndParentCS(DzTileB(self.lineage+",B1"),csChild,csParent,flip=self.flip) # same handedness as parent
    tileB2 = self._PositionByChildAndParentCS(DzTileB(self.lineage+",B2"),csChild,csParent,flip=not self.flip) # opposite handedness as parent
    
    #DzTileK by orienting defined CS on child to defined CS on parent
    csChild = DzTileK()._CSFromBasePts(self.rlvl+1,  1,0,2, True)
    csParent = DzTileA()._CSFromBasePts(self.rlvl,  1,3,2 )
    tileK2 = self._PositionByChildAndParentCS(DzTileK(self.lineage+",K2"),csChild,csParent,flip=not self.flip) # opposite handedness as parent
    #DzTileK by mirroring the previous tile
    cs = CS(tileK2._tilePts()[0],tileK2._tilePts()[1]-tileK2._tilePts()[0],tileK2._tilePts()[3]-tileK2._tilePts()[0])
    xf_mir = Xform.mirror(cs)
    tileK3 = DzTileK(self.lineage+",K3",xf=xf_mir*tileK2.xf,rlvl=self.rlvl+1,flip=self.flip)  # same handedness as parent
    
    #2 DzTileK's by mirroring the previous two
    cs = CS(tileK2._tilePts()[0],tileK2._tilePts()[2]-tileK2._tilePts()[0],tileK2._tilePts()[3]-tileK2._tilePts()[0])
    xf_mir = Xform.mirror(cs)
    tileK4 = DzTileK(self.lineage+",K4",xf=xf_mir*tileK2.xf,rlvl=self.rlvl+1,flip=self.flip)  # same handedness as parent
    tileK5 = DzTileK(self.lineage+",K5",xf=xf_mir*tileK3.xf,rlvl=self.rlvl+1,flip=not self.flip)  # same handedness as parent
    
    #2 DzTileKs by rotation the previous two tiles
    #xf_rot = Xform.rotation(center=tileK2._tilePts()[0], angle=math.pi, axis=tileK2._tilePts()[3]-tileK2._tilePts()[0])
    #tileK4 = DzTileK(self.lineage+",K4",xf=xf_rot*tileK2.xf,rlvl=self.rlvl+1,flip=not self.flip)  # opposite handedness as parent
    #tileK5 = DzTileK(self.lineage+",K5",xf=xf_rot*tileK3.xf,rlvl=self.rlvl+1,flip=self.flip)  # same handedness as parent
    
    return [tileB0,tileC0,tileC1,tileK0,tileK1,tileB1,tileB2,tileK2,tileK3,tileK4,tileK5]
     
class DzTileB(DzTile):
  basePts= ( 
      Vec(0.0       , 0.0	      , 0.0   ),
      Vec(0.9510565	, 0.0   	  , 0.0   ),
      Vec(0.2628656 , 1.3763819	, 0.0   ),
      Vec(0.2628656 , 0.4253254 , 0.3090170)
    )
    
  def inflate(self):
    #DzTileB by orienting child origin to defined CS on parent
    csParent = DzTileB()._CSFromBasePts(self.rlvl,  3,0,1 )
    tileB0 = self._PositionByParentCS(DzTileB(self.lineage+",B0"),csParent,not self.flip)  # opposite handdeness as parent
    
    #DzTileK by orienting child origin to defined CS on parent
    csParent = DzTileB()._CSFromBasePts(self.rlvl,  3,0,2 )
    tileK0 = self._PositionByParentCS(DzTileK(self.lineage+",K0"),csParent,self.flip)# same handedness as parent
    #DzTileK by rotating the previous tile
    #xf_rot = Xform.rotation(center=tileK0._tilePts()[0], angle=math.pi, axis=tileK0._tilePts()[3]-tileK0._tilePts()[0])
    #tileK1 = DzTileK(self.lineage+",K1",xf=xf_rot*tileK0.xf,rlvl=self.rlvl+1,flip=self.flip)# same handedness as parent
    
    #DzTileK by orienting defined CS on child to defined CS on parent
    csChild = DzTileK()._CSFromBasePts(self.rlvl+1,  1,0,3 )
    csParent = DzTileB()._CSFromBasePts(self.rlvl,  0,3,1 )
    tileK1 = self._PositionByChildAndParentCS(DzTileK(self.lineage+",K2"),csChild,csParent,flip=not self.flip) # opposite handedness as parent
    #DzTileK by rotating the previous tile
    #xf_rot = Xform.rotation(center=tileK2._tilePts()[0], angle=math.pi, axis=tileK2._tilePts()[3]-tileK2._tilePts()[0])
    #tileK3 = DzTileK(self.lineage+",K3",xf=xf_rot*tileK2.xf,rlvl=self.rlvl+1,flip=not self.flip)  # opposite handedness as parent
    
    #2 DzTileK's by mirroring the previous two
    cs = CS(tileK0._tilePts()[0],tileK0._tilePts()[2]-tileK0._tilePts()[0],tileK0._tilePts()[3]-tileK0._tilePts()[0])
    xf_mir = Xform.mirror(cs)
    tileK2 = DzTileK(self.lineage+",K4",xf=xf_mir*tileK0.xf,rlvl=self.rlvl+1,flip=not self.flip)  # same handedness as parent
    tileK3 = DzTileK(self.lineage+",K5",xf=xf_mir*tileK1.xf,rlvl=self.rlvl+1,flip=self.flip)  # same handedness as parent    
    
    #DzTileB by orienting defined CS on child to defined CS on parent
    csChild = DzTileB()._CSFromBasePts(self.rlvl+1,  2,0,1 )
    csParent = DzTileB()._CSFromBasePts(self.rlvl,  1,3,2 )
    tileB1 = self._PositionByChildAndParentCS(DzTileB(self.lineage+",B1"),csChild,csParent,flip=self.flip) # same handedness as parent
    
    #DzTileC by orienting child origin to defined CS on parent
    csChild = DzTileC()._CSFromBasePts(self.rlvl+1,  2,1,3 )
    csParent = DzTileB()._CSFromBasePts(self.rlvl,  2,0,1 )
    tileC0 = self._PositionByChildAndParentCS(DzTileC(self.lineage+",C0"),csChild,csParent,flip=self.flip) # same handedness as parent
    
    return [tileB0,tileK0,tileK1,tileK2,tileK3,tileB1,tileC0]

class DzTileC(DzTile):
  basePts= (
      Vec(0.0       , 0.0	      , 0.0   ),
      Vec(0.5877853	, 0.0   	  , 0.0   ),
      Vec(0.8506509 , 1.3763819	, 0.0   ),
      Vec(0.4253254 , 0.6881910 , 0.50 )
    )
    
  def inflate(self):
    #DzTileA by orienting child origin to defined CS on parent
    csParent = DzTileA()._CSFromBasePts(self.rlvl,  0,1,3 )
    tileA0 = self._PositionByParentCS(DzTileA(self.lineage+",A0"),csParent,not self.flip)  # opposite handdeness as parent
    
    #DzTileK by orienting defined CS on child to defined CS on parent
    csChild = DzTileK()._CSFromBasePts(self.rlvl+1,  1,0,2)
    csParent = DzTileC()._CSFromBasePts(self.rlvl,  2,3,1 )
    tileK0 = self._PositionByChildAndParentCS(DzTileK(self.lineage+",K0"),csChild,csParent,flip=self.flip) # same handedness as parent
    #DzTileK by mirroring the previous tile
    cs = CS(tileK0._tilePts()[0],tileK0._tilePts()[2]-tileK0._tilePts()[0],tileK0._tilePts()[3]-tileK0._tilePts()[0])
    xf_mir = Xform.mirror(cs)
    tileK1 = DzTileK(self.lineage+",K1",xf=xf_mir*tileK0.xf,rlvl=self.rlvl+1,flip=not self.flip)  # opposite handedness as parent
    
    #DzTileC by orienting defined CS on child to defined CS on parent
    csChild = DzTileC()._CSFromBasePts(self.rlvl+1,  1,2,0)
    csParent = DzTileC()._CSFromBasePts(self.rlvl,  3,1,2 )
    tileC0 = self._PositionByChildAndParentCS(DzTileC(self.lineage+",C0"),csChild,csParent,flip=not self.flip) # opposite handedness as parent
    #DzTileC by mirroring the previous tile
    cs = CS(tileC0._tilePts()[0],tileC0._tilePts()[2]-tileC0._tilePts()[0],tileC0._tilePts()[3]-tileC0._tilePts()[0])
    xf_mir = Xform.mirror(cs)
    tileC1 = DzTileC(self.lineage+",C1",xf=xf_mir*tileC0.xf,rlvl=self.rlvl+1,flip=self.flip)  # same handedness as parent
    
    return [tileA0,tileK0,tileK1,tileC0,tileC1]

class DzTileK(DzTile):
  basePts= ( 
    Vec(0.0       , 0.0	      , 0.0   ),
    Vec(0.9510565	, 0.0   	  , 0.0   ),
    Vec(0.2628656 , 0.5257311 , 0.0   ),
    Vec(0.2628656 , 0.3440955 , 0.250 )
    )
  

  def inflate(self):
    #DzTileK by orienting defined CS on child to defined CS on parent
    csChild = DzTileK()._CSFromBasePts(self.rlvl+1,  3,1,0)
    csParent = DzTileK()._CSFromBasePts(self.rlvl,  3,0,2 )
    tileK0 = self._PositionByChildAndParentCS(DzTileK(self.lineage+",K0"),csChild,csParent,flip=self.flip) # same handedness as parent
    
    #DzTileB by orienting child origin to defined CS on parent
    csParent = DzTileK()._CSFromBasePts(self.rlvl,  2,0,1 )
    tileB0 = self._PositionByParentCS(DzTileB(self.lineage+",B0"),csParent,self.flip)  # opposite handdeness as parent
    
    return [tileK0,tileB0]


# Here we check the integrity of inflations for each tile type
# This section may be deleted when file distributed

def DanzerAxiom():
  outie = fp.makeOut(fp.outies.Rhino, "axiom")
  outie.iconscale = 0.1
  ta = DzTileA(xf=Xform.translation(Vec(1,0,0)),rlvl=1)
  tb = DzTileB(xf=Xform.translation(Vec(2,0,0)),rlvl=1)
  tc = DzTileC(xf=Xform.translation(Vec(3,0,0)),rlvl=1)
  tk = DzTileK(xf=Xform.translation(Vec(4,0,0)),rlvl=1)
  
  for t in [ta,tb,tc,tk] : outie.put(t.draw())
  outie.draw()


def inflationA(out_0,out_1,out_2):
  xform = Xform.translation(Point(1,1)) 
  xform *= Xform.rotation(center=Point(),angle=math.pi/3, axis=Vec(0,1,1))
  ta = DzTileA(xf=xform,rlvl=0)
  out_0.put(ta.draw())

  inflt1 = ta.inflate()
  for tile in inflt1 : 
    out_1.put(tile.draw())
    inflt2 = tile.inflate()
    for tile in inflt2 : out_2.put(tile.draw())

def inflationB(out_0,out_1,out_2):
  xform = Xform.translation(Point(2,1)) 
  xform *= Xform.rotation(center=Point(),angle=math.pi/3, axis=Vec(0,1,1))
  tb = DzTileB(xf=xform,rlvl=0)
  out_0.put(tb.draw())

  inflt1 = tb.inflate()
  for tile in inflt1 : 
    out_1.put(tile.draw())
    inflt2 = tile.inflate()
    for tile in inflt2 : out_2.put(tile.draw())

def inflationC(out_0,out_1,out_2):
  xform = Xform.translation(Point(3,1)) 
  xform *= Xform.rotation(center=Point(),angle=math.pi/3, axis=Vec(0,1,1))
  tc = DzTileC(xf=xform,rlvl=0)
  out_0.put(tc.draw())

  inflt1 = tc.inflate()
  for tile in inflt1 : 
    out_1.put(tile.draw())
    inflt2 = tile.inflate()
    for tile in inflt2 : out_2.put(tile.draw())

def inflationK(out_0,out_1,out_2):
  xform = Xform.translation(Point(4,1)) 
  xform *= Xform.rotation(center=Point(),angle=math.pi/3, axis=Vec(0,1,1))
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
    out_0 = fp.makeOut(fp.outies.Rhino, "0")
    out_0.set_color(0,0,0)
    out_0.iconscale = 0.2
    
    out_1 = fp.makeOut(fp.outies.Rhino, "1")
    out_1.set_color(0.5,0.5,1.0)
    out_1.iconscale = 0.1
  
    out_2 = fp.makeOut(fp.outies.Rhino, "2")
    out_2.set_color(1.0,0.5,1.0)
    out_2.iconscale = 0.05  
    
    DanzerAxiom()
    inflationA(out_0,out_1,out_2)
    inflationB(out_0,out_1,out_2)
    inflationC(out_0,out_1,out_2)
    inflationK(out_0,out_1,out_2)
    
    for outie in [out_0,out_1,out_2] : outie.draw()

