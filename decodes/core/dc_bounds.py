from decodes.core import *
from . import dc_base, dc_interval, dc_vec, dc_point  #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
import math


class Bounds(Geometry):
    """
    A 2d retangular or 3d cubic boudary class
    axis are oriented to world axes
    """
    def __init__ (self, **kargs):
        """
        a Bounds may be constructed two ways: By setting "center", "dim_x", "dim_y", and optionally "dim_z" OR by setting "ival_x", "ival_y", and optionally "ival_z"
        """
        try:
            x2 = abs(kargs['dim_x']/2.0)
            y2 = abs(kargs['dim_y']/2.0)
            self.ival_x = Interval(kargs['center'].x-x2,kargs['center'].x+x2)
            self.ival_y = Interval(kargs['center'].y-y2,kargs['center'].y+y2)
            if "dim_z" in kargs:
                z2 = abs(kargs['dim_z']/2.0)
                self.ival_z = Interval(kargs['center'].z-z2,kargs['center'].z+z2)
        except:
            try:
                self.ival_x = kargs['ival_x']
                self.ival_y = kargs['ival_y']
                if "ival_z" in kargs:
                    self.ival_z = kargs['ival_z']
            except:
                raise ValueError('Bounds require either "center", "dim_x", "dim_y" OR "ival_x", "ival_y"')

    @property
    def cpt(self):
        try:
            return Point(self.ival_x.mid,self.ival_y.mid,self.ival_z.mid)
        except:
            return Point(self.ival_x.mid,self.ival_y.mid)
    @property
    def dim_x(self):
        return self.ival_x.delta

    @property
    def dim_y(self):
        return self.ival_y.delta

    @property
    def dim_z(self):
        try:
            return self.ival_z.delta
        except:
            return 0.0

    @property
    def is_2d(self): return not hasattr(self, 'ival_z')

    @property
    def is_3d(self): return hasattr(self, 'ival_z')

    @property
    def corners(self):
        """
        moves counter clockwise, like so:
        (-,-)(+,-)(+,+)(-,+)
        """
        cpts = []
        try:
            cpts.append(Point(self.ival_x.a,self.ival_y.a,self.ival_z.a))
            cpts.append(Point(self.ival_x.b,self.ival_y.a,self.ival_z.a))
            cpts.append(Point(self.ival_x.b,self.ival_y.b,self.ival_z.a))
            cpts.append(Point(self.ival_x.a,self.ival_y.b,self.ival_z.a))

            cpts.append(Point(self.ival_x.a,self.ival_y.a,self.ival_z.b))
            cpts.append(Point(self.ival_x.b,self.ival_y.a,self.ival_z.b))
            cpts.append(Point(self.ival_x.b,self.ival_y.b,self.ival_z.b))
            cpts.append(Point(self.ival_x.a,self.ival_y.b,self.ival_z.b))
        except:
            cpts.append(Point(self.ival_x.a,self.ival_y.a))
            cpts.append(Point(self.ival_x.b,self.ival_y.a))
            cpts.append(Point(self.ival_x.b,self.ival_y.b))
            cpts.append(Point(self.ival_x.a,self.ival_y.b))
        return cpts
    
    def __contains__(self, pt):
        """
        overloads the containment **(in)** operator
        note: less-than or equal-to logic applied, points that lie on any edge of the bounds will be considered to be contained within it
        """
        if not (pt.x in self.ival_x) : return False
        if not (pt.y in self.ival_y) : return False
        try:
            if not (pt.z in self.ival_z) : return False
            return True
        except:
            return True
    
    def __floordiv__(self, other): 
        """overloads the integer division **(//)** operator
        calls Bounds.subbounds(other)
        """
        return self.subbounds(other)

    def eval(self,x,y,z=0):
        if self.is_2d:
            return Point(self.ival_x.eval(x),self.ival_y.eval(y))
        return Point(self.ival_x.eval(x),self.ival_y.eval(y),self.ival_z.eval(z))

    def overlaps(self, other) :
        return any([pt in self for pt in other.corners] + [pt in other for pt in self.corners])

    def subbounds(self,divs):
        """
        produces subboundaries.
        starts at bottom left, moves from left to right and then bottom to top.
        """
        ret = []
        
        subival_x = self.ival_x//divs
        subival_y = self.ival_y//divs
        if self.is_3d:
            subival_z = self.ival_z//divs
            for iz in subival_z:
                for iy in subival_y:
                    for ix in subival_x:
                        ret.append(Bounds(ival_x=ix,ival_y=iy,ival_z=iz))
        else:
            for iy in subival_y:
                for ix in subival_x:
                    ret.append(Bounds(ival_x=ix,ival_y=iy))

        return ret

    def near_pt(self, p):
        """Returns the closest point to this Bounds.  If the point in within the bounds, simply returns the point
        """
        if p in self : return p
        if p.x < self.ival_x.a : p.x = self.ival_x.a
        if p.x > self.ival_x.b : p.x = self.ival_x.b
        if p.y < self.ival_y.a : p.y = self.ival_y.a
        if p.y > self.ival_y.b : p.y = self.ival_y.b

        if self.is_2d:
            p.z = 0
        else:
            if p.z < self.ival_z.a : p.z = self.ival_z.a
            if p.z > self.ival_z.b : p.z = self.ival_z.b

        return p


    def to_polyline(self):
        from .dc_pline import *
        return PLine(self.corners+[self.corners[0]])


    @staticmethod
    def encompass(pts = [Point()]):
        ix = Interval.encompass([p.x for p in pts])
        iy = Interval.encompass([p.y for p in pts])
        return Bounds(ival_x = ix,ival_y = iy)
        
        
    @staticmethod
    def unit_square():
        return Bounds(ival_x=Interval(),ival_y=Interval())

    @staticmethod
    def unit_cube():
        return Bounds(ival_x=Interval(),ival_y=Interval(),ival_z=Interval())

class QuadTree():
    def __init__ (self, capacity, bounds):
        self.cap = capacity
        self.bnd = bounds
        self._pts = []
        
    @property
    def has_children(self):
        if hasattr(self,'children'):return True 
        return False
        
    @property
    def pts(self):
        """
        recursively returns all the points in this quadtree
        """
        ret_pts = []
        if not self.has_children :
            ret_pts = [Point(pt) for pt in self._pts]
        else :
            for child in self.children: ret_pts.extend(child.pts)
        return ret_pts

    def append(self, pt) :
        if not self.contains(pt) : return False
        if not self.has_children and len(self._pts) < self.cap:
            self._pts.append(pt)
            return True
        else :
            if not self.has_children : self._divide()
            for child in self.children:
                if child.append(pt) : return True
            return False
        
    def _divide(self) :
        """
        divides self into sub regions.
        starts at bottom left and moves clockwise
        """
        if self.has_children: return False
        
        sub_bnds = self.bnd//2
        self.children = [QuadTree(self.cap,sub_bnd) for sub_bnd in sub_bnds]

        for pt in self._pts : 
            accepted = False
            for child in self.children:
                if child.append(pt) : 
                    accepted = True
                    break
            if not accepted : "no child accepted this point!"
            
        self._pts = None
        return True
    
    def contains(self,pt):
        if self.has_children:
            return any([child.contains(pt) for child in self.children])
        else:
            return pt in self.bnd
            
    def pts_in_bounds(self,bounds):
        """
        finds all points that fall within a given bounds
        """
        if not self.bnd.overlaps(bounds) : return []
        ret_pts = []
        if not self.has_children :
            for pt in self._pts :
                if pt in bounds :  ret_pts.append(pt)
        else :
            for child in self.children: ret_pts.extend(child.pts_in_bounds(bounds))
        return ret_pts
