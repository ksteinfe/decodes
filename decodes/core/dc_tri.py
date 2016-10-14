from decodes.core import *
from . import dc_base, dc_vec, dc_point, dc_line, dc_plane #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print("tri.py loaded")

class Tri(Geometry):
    
    def __init__(self, pt_a, pt_b, pt_c):
        self.pa = pt_a
        self.pb = pt_b
        self.pc = pt_c
        if Vec(self.pa, self.pb).is_parallel(Vec(self.pa, self.pc)):
            raise GeometricError("points are colinear")
        
    @property
    def edges(self): return [self.edge(0),self.edge(1),self.edge(2)]
    
    @property
    def pts(self): return [self.pa,self.pb,self.pc]
    
    @property
    def centroid(self): return Point.centroid(self.pts)
        
    @property
    def plane(self): 
        vec = self.edges[0].vec.cross(Vec(self.pa,self.pc))
        return Plane(self.centroid,vec)
        
    @property
    def perimeter(self): return sum([e.length for e in self.edges])
        
    @property
    def area(self):
        #http://www.mathopenref.com/heronsformula.html
        p = self.perimeter/2.0
        a = self.edge(0).length
        b = self.edge(1).length
        c = self.edge(2).length
        return (p*(p-a)*(p-b)*(p-c))**0.5
        
        
    @property
    def circumcenter(self):
        #http://www.mathopenref.com/trianglecircumcenter.html
        from  dc_intersection import Intersector
        xsec = Intersector()
        bsec_ab = self.edge_bisector(0)
        bsec_bc = self.edge_bisector(1)
        if xsec.of(bsec_ab,bsec_bc):
            return xsec[0]
        return False
        
    @property
    def circumcircle(self):
        #http://www.mathopenref.com/trianglecircumcircle.html
        pt = self.circumcenter
        vec = self.edges[0].vec.cross(Vec(self.pa,self.pc))
        pln = Plane(pt,vec)
        return Circle(pln,pt.distance(self.pa))
        
    @property
    def incenter(self):
        #http://www.mathopenref.com/triangleincenter.html
        from  dc_intersection import Intersector
        xsec = Intersector()
        bsec_ab = self.angle_bisector(0)
        bsec_bc = self.angle_bisector(1)
        if xsec.of(bsec_ab,bsec_bc):
            return xsec[0]
        return False
        
    @property
    def incircle(self):
        #http://www.mathopenref.com/triangleincircle.html
        pt = self.incenter
        vec = self.edges[0].vec.cross(Vec(self.pa,self.pc))
        pln = Plane(pt,vec)
        rad = 2.0*self.area/self.perimeter
        return Circle(pln,rad)
        
    def rotate(self):
        self.pa, self.pb, self.pc = self.pb, self.pc, self.pa
        
    def flip(self, keep_a=False,keep_b=False):
        if keep_a: self.pb, self.pc = self.pc, self.pb
        elif keep_b: self.pa, self.pc = self.pc, self.pa
        else: self.pa, self.pb = self.pb, self.pa
        
    def edge(self,index):
        if index == 0 : return Segment(self.pa,self.pb)
        elif index == 1 : return Segment(self.pb,self.pc)
        elif index == 2 : return Segment(self.pc,self.pa)
        else: return False
        
    def altitude(self,base_index):
        #http://www.mathopenref.com/altitude.html
        edge = self.edges[base_index]
        if base_index == 0 : pt = self.pc
        elif base_index == 1 : pt = self.pa
        elif base_index == 2 : pt = self.pb
        else: return False
        
        npt,t,dist = Line(edge.spt,edge.ept).near(pt) #returns a near point, its t-val, and the dist
        return dist, Segment(npt,pt)
        
    def edge_bisector(self,index):
        edge = self.edge(index)
        pt = edge.midpoint
        vec = edge.vec.cross(self.plane.normal)
        return Line(pt,vec.inverted())
        
    def angle_bisector(self,index):
        if index == 0 : 
            va,vb = Vec(self.pa,self.pb),Vec(self.pa,self.pc)
        elif index == 1 : 
            va,vb = Vec(self.pb,self.pc),Vec(self.pb,self.pa)
        elif index == 2 : 
            va,vb = Vec(self.pc,self.pa),Vec(self.pc,self.pb)
        else: return False
        
        vec = Vec.bisector(va,vb)
        return Line(self.pts[index],vec)
        
    def pedal_tri(self,pt):
        pts = [e.near_pt(pt) for e in self.edges]
        return Tri(pts[0],pts[1],pts[2])
        
    def to_pgon(self):
        from .dc_pgon import PGon
        return PGon(self.pts)
    
    def to_msh(self):
        from .dc_mesh import Mesh
        msh = Mesh(self.pts)
        msh.add_face(0,1,2)
        return msh

