from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_xform
import math

# according to Danzer, the basic tile set contains tets with 
# lengths that are combonations of four possible values:
# (http://www.cs.williams.edu/~98bcc/tiling/danztable.html)
# a = (sqrt(10+2*sqrt(5)))/4    = 0.951056516
# b = sqrt(3) / 2                         = 0.866025404
# t = (1 + sqrt(5)) / 2             = 1.61803399
# ti = 1/t                                        = 0.618033989
#
# edge lengths are given by the table below
# [dihedral angles between the tet faces shared by these edges
# are shown in brackets]
# 
# (tile)    (e1-2)        (e2-3)     (e3-1)        (e2-4)        (e1-4)         (e3-4)
# ATile     [36]a         [60]Tb     [72]Ta        [108]a        [90]1            [60]b
# B             [36]a                [36]Ta     [60]Tb             [120]b             [108]Tia     [90]1
# C             [36]Tia            [60]Tb     [90]T             [120]b        [72]a                [36]a
# K             [36]a                [60]b             [72]Tia     [90]T/2     [90]1/2        [90]Ti/2

# here's every possible combonation of edge lengths
# a = (sqrt(10+2*sqrt(5)))/4    = 0.951056516
# b = sqrt(3) / 2                         = 0.866025404
# t = (1 + sqrt(5)) / 2             = 1.61803399 
# ti = 1/t                                        = 0.618033989
# t*b =         1.40125854        
# t*a =         1.53884177    
# ti*a =        0.587785252 
# t/2 =         0.809016995 
# ti/2 =         0.309016994


"""
Defines a base class from which to derive each child class, and contains methods applicable to all Danzer prototiles
"""
# golden ratio (0.618033989)
tau = 2 / (1 + math.sqrt(5))
# powers of golden ratio, used for scaling tiles
tau_pow = [tau**n for n in range(15)]

class DzTile(object):
        
    def __init__(self,**kargs):
        #lineage, tracks tile types of ancestors
        self.lineage = kargs["lineage"] if "lineage" in kargs else "RT" 
        #recursion level, sets the scale of tiles
        self.rlvl = kargs["rlvl"] if "rlvl" in kargs else 0 
        #the spatial transformation of this tile
        self.xf = kargs["xf"] if "xf" in kargs else Xform() 
        #determines if this tile is mirrored
        self.flip = kargs["flip"] if "flip" in kargs else False
        
    """
    Retrieves vertices of Danzer tiles in world coordinates
    """
    @property
    def tile_pts(self):
        # a scaling factor based upon this tile's recursion level
        factor = tau_pow[self.rlvl]
        xf_scale = Xform.scale(factor)
        # return an world-space copy of each base_pt 
        return [(pt*xf_scale)*self.xf for pt in self._base_pts]
        
    """
    Constructs a child tile of the specified type, positioned by matching a CS on this tile with a CS on the desired child tile
    """        
    def child_by_explicit(self,name,cs_chld,cs_self,flip):
        # construct a world-space cs of the desired child tile
        cs_tile = CS()*Xform.change_basis(cs_chld,cs_self)*self.xf
        # the transformation from world origin to this cs
        xf = cs_tile.xform
        if flip : xf = xf * Xform.mirror()
        # set the recursion level to one more than this tile
        rl = self.rlvl + 1
        # construct the lineage string
        l = self.lineage+","+name
        f = flip
        
        # return a child tile of the desired type
        if name.startswith("A"): return DzTileA(xf=xf,rlvl=rl,lineage=l,flip=f)
        if name.startswith("B"): return DzTileB(xf=xf,rlvl=rl,lineage=l,flip=f)
        if name.startswith("C"): return DzTileC(xf=xf,rlvl=rl,lineage=l,flip=f)
        if name.startswith("K"): return DzTileK(xf=xf,rlvl=rl,lineage=l,flip=f)

    """
    Constructs a child tile of the specified type, positioned by matching a CS on this tile with the base CS of the desired child tile
    """
    def child_by_base(self,tile_chld,cs_self,flip):
        return self.child_by_explicit(tile_chld,CS(),cs_self,flip)
    
    """
    Constructs a sibling tile of the specified type, positioned by mirroring this tile about a given CS
    [pseudo]
    """
    def sibling_by_mirror(self,name,cs_mir):
        # construct the transformation of the desired child tile by mirroring
        xf = Xform.mirror(cs_mir) * self.xf
        # prepare other required arguments by modifying this tile's properties
        rl = self.rlvl
        l = self.lineage[:-2]+name
        f = not self.flip
        
        # return a child tile of the desired type
        if name.startswith("A"): return DzTileA(xf=xf,rlvl=rl,lineage=l,flip=f)
        if name.startswith("B"): return DzTileB(xf=xf,rlvl=rl,lineage=l,flip=f)
        if name.startswith("C"): return DzTileC(xf=xf,rlvl=rl,lineage=l,flip=f)
        if name.startswith("K"): return DzTileK(xf=xf,rlvl=rl,lineage=l,flip=f)
        raise
        
    """
    Methods for constructing and orienting local- and world-space CS given the indices of three base points
    """
    @classmethod
    def cs_by_base_pts(cls,rlvl,pt_o,pt_x,pt_y,flip=False):
        # scale the base points to the proper size for this rlvl
        factor = tau_pow[rlvl]
        pts = [pt*factor for pt in cls._base_pts]
        
        # to orient to flipped tiles, simply invert the apex point
        if flip : pts[3] = Point(pts[3].x,pts[3].y,-pts[3].z)
        # construct and return the desired coordinate system
        return CS(pts[pt_o],pts[pt_x]-pts[pt_o],pts[pt_y]-pts[pt_o])

    def cs_by_tile_pts(self,pt_o,pt_x,pt_y):
        # construct and return the desired coordinate system
        pts = self.tile_pts
        return CS(pts[pt_o],pts[pt_x]-pts[pt_o],pts[pt_y]-pts[pt_o])

    """
    [noprint]
    """
    @property
    def to_mesh(self):
        msh = Mesh()
        for v in self.tile_pts : msh.append(v)
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
        
"""
Extends DzTile, and adds methods specific to a Danzer Tile A
"""        
class DzTileA(DzTile):
    _base_pts= ( \
            Point(0.0, 0.0, 0.0),\
            Point(0.9510565, 0.0, 0.0),\
            Point(0.6881910 , 1.3763819 , 0.0),\
            Point(0.5257311 , 0.6881910, 0.5)\
            )
    """
    Inflation routine for Tile A
    [pseudo]
    """
    def inflate(self):
        #create a child TileB by mapping child pts[2,1,0] to parent pts[0,1,3]
        cs_chld = DzTileB().cs_by_base_pts(self.rlvl+1,2,1,0 )
        cs_prnt = DzTileA().cs_by_base_pts(self.rlvl,0,1,3 )
        tileB0 = self.child_by_explicit("B0",cs_chld,cs_prnt,self.flip) # same handedness as parent
        #create a child TileC by mapping child pts[1,2,0] to parent pts[3,2,1]
        cs_chld = DzTileC().cs_by_base_pts(self.rlvl+1,1,2,0 )
        cs_prnt = DzTileA().cs_by_base_pts(self.rlvl,3,2,1 )
        tileC0 = self.child_by_explicit("C0",cs_chld,cs_prnt,self.flip) # same handedness as parent
        #create a child TileC by mapping child pts[2,3,1] to parent pts[2,0,1]
        cs_chld = DzTileC().cs_by_base_pts(self.rlvl+1,2,3,1, True )
        cs_prnt = DzTileA().cs_by_base_pts(self.rlvl,2,0,1 )
        tileC1 = self.child_by_explicit("C1",cs_chld,cs_prnt,not self.flip) # opposite handedness as parent
        #create a child TileK by mapping child pts[2,0,3] to parent pts[3,1,0]
        cs_chld = DzTileK().cs_by_base_pts(self.rlvl+1,2,0,3, True)
        cs_prnt = DzTileA().cs_by_base_pts(self.rlvl,3,1,0 )
        tileK0 = self.child_by_explicit("K0",cs_chld,cs_prnt,not self.flip) # opposite handedness as parent
        #create a child TileK by mirroring the previous tile
        cs_mir = tileK0.cs_by_tile_pts(0,1,3)
        tileK1 = tileK0.sibling_by_mirror("K1",cs_mir)
        
        #create a child TileB by mapping child pts[2,3,1] to parent pts[0,3,2]
        cs_chld = DzTileB().cs_by_base_pts(self.rlvl+1,2,3,1 )
        cs_prnt = DzTileA().cs_by_base_pts(self.rlvl,0,3,2 )
        tileB1 = self.child_by_explicit("B1",cs_chld,cs_prnt,self.flip) # same handedness as parent
        tileB2 = self.child_by_explicit("B2",cs_chld,cs_prnt,not self.flip) # opposite handedness as parent
        #create a child TileK by mapping child pts[1,0,2] to parent pts[1,3,2]
        cs_chld = DzTileK().cs_by_base_pts(self.rlvl+1,1,0,2, True)
        cs_prnt = DzTileA().cs_by_base_pts(self.rlvl,1,3,2 )
        tileK2 = self.child_by_explicit("K2",cs_chld,cs_prnt,not self.flip) # opposite handedness as parent
        #create a child TileK by mirroring the previous tile
        cs_mir = tileK2.cs_by_tile_pts(0,1,3)
        tileK3 = tileK2.sibling_by_mirror("K3",cs_mir)
        
        #create two child TileK by mirroring the previous two tiles
        cs_mir = tileK2.cs_by_tile_pts(0,2,3)
        tileK4 = tileK2.sibling_by_mirror("K4",cs_mir)##
        tileK5 = tileK3.sibling_by_mirror("K5",cs_mir)
        
        #return all children
        return [tileB0,tileC0,tileC1,tileK0,tileK1,tileB1,tileB2,tileK2,tileK3,tileK4,tileK5]

"""
Extends DzTile, and adds methods specific to a Danzer Tile B
"""    
class DzTileB(DzTile):
    _base_pts= ( \
            Point(0.0, 0.0, 0.0),\
            Point(0.9510565, 0.0, 0.0),\
            Point(0.2628656 , 1.3763819, 0.0),\
            Point(0.2628656 , 0.4253254 , 0.3090170)\
        )
    """
    Inflation routine for Tile B
    [pseudo]
    """
    def inflate(self):
        #create a child TileA by mapping child base to parent pts[3,0,1]
        cs_prnt = DzTileB().cs_by_base_pts(self.rlvl,    3,0,1 )
        tileB0 = self.child_by_base("B0",cs_prnt,not self.flip)    # opposite handdeness as parent
        #create a child TileA by mapping child base to parent pts[3,0,2]
        cs_prnt = DzTileB().cs_by_base_pts(self.rlvl,    3,0,2 )
        tileK0 = self.child_by_base("K0",cs_prnt,self.flip)# same handedness as parent
        #create a child TileK by mapping child pts[1,0,3] to parent pts[0,3,1]
        cs_chld = DzTileK().cs_by_base_pts(self.rlvl+1,    1,0,3 )
        cs_prnt = DzTileB().cs_by_base_pts(self.rlvl,    0,3,1 )
        tileK1 = self.child_by_explicit("K2",cs_chld,cs_prnt,not self.flip) # opposite handedness as parent
        #create two child TileK by mirroring the previous two tiles
        cs_mir = tileK0.cs_by_tile_pts(0,2,3)
        tileK2 = tileK0.sibling_by_mirror("K2",cs_mir)
        tileK3 = tileK1.sibling_by_mirror("K3",cs_mir)
        
        #create a child TileB by mapping child pts[2,0.1] to parent pts[1,3,2]
        cs_chld = DzTileB().cs_by_base_pts(self.rlvl+1,    2,0,1 )
        cs_prnt = DzTileB().cs_by_base_pts(self.rlvl,    1,3,2 )
        tileB1 = self.child_by_explicit("B1",cs_chld,cs_prnt,self.flip) # same handedness as parent
        #create a child TileC by mapping child pts[2,1,3] to parent pts[2,0,1]
        cs_chld = DzTileC().cs_by_base_pts(self.rlvl+1,    2,1,3 )
        cs_prnt = DzTileB().cs_by_base_pts(self.rlvl,    2,0,1 )
        tileC0 = self.child_by_explicit("C0",cs_chld,cs_prnt,self.flip) # same handedness as parent
        
        #return all children
        return [tileB0,tileK0,tileK1,tileK2,tileK3,tileB1,tileC0]

"""
Extends DzTile, and adds methods specific to a Danzer Tile C
"""    
class DzTileC(DzTile):
    _base_pts= (\
            Point(0.0, 0.0, 0.0),\
            Point(0.5877853, 0.0, 0.0),\
            Point(0.8506509 , 1.3763819, 0.0),\
            Point(0.4253254 , 0.6881910 , 0.50 )\
        )
    """
    Inflation routine for Tile C
    [pseudo]
    """
    def inflate(self):
        #create a child TileA by mapping child base to parent pts[0,1,3]
        cs_prnt = DzTileA().cs_by_base_pts(self.rlvl,    0,1,3 )
        tileA0 = self.child_by_base("A0",cs_prnt,not self.flip)    # opposite handdeness as parent
        #create a child TileK by mapping child pts[1,0,2] to parent pts[2,3,1]
        cs_chld = DzTileK().cs_by_base_pts(self.rlvl+1,    1,0,2)
        cs_prnt = DzTileC().cs_by_base_pts(self.rlvl,    2,3,1 )
        tileK0 = self.child_by_explicit("K0",cs_chld,cs_prnt,self.flip) # same handedness as parent
        #create a child TileK by mirroring the previous tile
        cs_mir = tileK0.cs_by_tile_pts(0,2,3)
        tileK1 = tileK0.sibling_by_mirror("K1",cs_mir)        
        
        #create a child TileC by mapping child pts[1,2,0] to parent pts[3,1,2]
        cs_chld = DzTileC().cs_by_base_pts(self.rlvl+1,    1,2,0)
        cs_prnt = DzTileC().cs_by_base_pts(self.rlvl,    3,1,2 )
        tileC0 = self.child_by_explicit("C0",cs_chld,cs_prnt,not self.flip) # opposite handedness as parent
        #create a child TileC by mirroring the previous tile
        cs_mir = tileC0.cs_by_tile_pts(0,2,3)
        tileC1 = tileC0.sibling_by_mirror("C1",cs_mir)   
        
        #return all children
        return [tileA0,tileK0,tileK1,tileC0,tileC1]

        
"""
Extends DzTile, and adds methods specific to a Danzer Tile K
""" 
class DzTileK(DzTile):
    _base_pts= ( \
        Point(0.0, 0.0, 0.0),\
        Point(0.9510565, 0.0, 0.0),\
        Point(0.2628656 , 0.5257311 , 0.0),\
        Point(0.2628656 , 0.3440955 , 0.250)\
        )
    """
    Inflation routine for Tile K
    """
    def inflate(self):
        #a cs at pts[3,1,0] on child tile
        cs_chld = DzTileK().cs_by_base_pts(self.rlvl+1,3,1,0)
        #a cs at pts[3,1,0] on parent tile
        cs_prnt = DzTileK().cs_by_base_pts(self.rlvl,3,0,2)
        #create a child TileK by mapping cs on child to cs on parent
        tileK0 = self.child_by_explicit("K0",cs_chld,cs_prnt,self.flip)
        
        #a cs at pts[2,0,1] on parent tile
        cs_prnt = DzTileK().cs_by_base_pts(self.rlvl,2,0,1)
        #create a child TileK by mapping child base to cs on parent
        tileB0 = self.child_by_base("B0",cs_prnt,self.flip)
        
        #return both children
        return [tileK0,tileB0]
        


# Here we check the integrity of inflations for each tile type
# This section may be deleted when file distributed

def DanzerAxiom():
    outie = dc.make_out(dc.outies.Rhino, "axiom")
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
        out_0 = dc.make_out(dc.outies.Rhino, "0")
        out_0.set_color(0,0,0)
        out_0.iconscale = 0.2
        
        out_1 = dc.make_out(dc.outies.Rhino, "1")
        out_1.set_color(0.5,0.5,1.0)
        out_1.iconscale = 0.1
    
        out_2 = dc.make_out(dc.outies.Rhino, "2")
        out_2.set_color(1.0,0.5,1.0)
        out_2.iconscale = 0.05    
        
        DanzerAxiom()
        inflationA(out_0,out_1,out_2)
        inflationB(out_0,out_1,out_2)
        inflationC(out_0,out_1,out_2)
        inflationK(out_0,out_1,out_2)
        
        for outie in [out_0,out_1,out_2] : outie.draw()

