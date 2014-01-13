from decodes.core import *
from . import dc_base, dc_interval, dc_vec, dc_point  #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
import math


class Bounds(Geometry):
    """
    A 2d rectangular or 3d cubic boundary class
    axis are oriented to world axis
    """
    def __init__ (self, **kargs):
        """A Bounds may be constructed two ways: By setting "center", "dim_x", "dim_y", and optionally "dim_z" OR by setting "ival_x", "ival_y", and optionally "ival_z"
        
            :param **kargs: Function that accepts multiple parameters to be passed. Parameters include center, x, y and z dimension OR x, y and z intervals.
            :type **kargs: (float, float), float, float OR Interval, Interval
            :result: Bounds
            :rtype: Bounds
        
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
        """Returns the center Point of the Bounds.
            
            :result: Center Point of Bounds.
            :rtype: Point
        
        """
        try:
            return Point(self.ival_x.mid,self.ival_y.mid,self.ival_z.mid)
        except:
            return Point(self.ival_x.mid,self.ival_y.mid)
            
    @property
    def dim_x(self):
        """Returns x dimension of Bounds.
        """
        
        return self.ival_x.delta

    @property
    def dim_y(self):
        """Returns y dimension of Bounds.
        """
        
        return self.ival_y.delta

    @property
    def dim_z(self):
        """Returns z dimension of Bounds.
        """
        
        try:
            return self.ival_z.delta
        except:
            return 0.0

    @property
    def is_2d(self):
        """Returns True if Bounds is 2-dimensional (no z component). Otherwise returns False.
        """
        return not hasattr(self, 'ival_z')

    @property
    def is_3d(self): 
        """Returns True if Bounds is 3-dimensional (x, y and z components). Otherwise returns False.
        """
        return hasattr(self, 'ival_z')

    @property
    def corners(self):
        """Moves counter clockwise, like so:
        
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
        Overloads the containment **(in)** operator.
        
        Note: less-than or equal-to logic applied, points that lie on any edge of the bounds will be considered to be contained within it.
        
            :param pt: Point whose containment must be determined.
            :type pt: Point
            :result: Boolean value
            :rtype: bool
        
        """
        if not (pt.x in self.ival_x) : return False
        if not (pt.y in self.ival_y) : return False
        try:
            if not (pt.z in self.ival_z) : return False
            return True
        except:
            return True
    
    def __floordiv__(self, other): 
        """Overloads the integer division **(//)** operator. Calls Bounds.subbounds(other).
        
            :param other: Number of sub-boundaries.
            :type other: int
            :result: a Bounds divided into sub-bounds.
            :rtype: Bounds
        """
        return self.subbounds(other)

    def eval(self,u,v,w=0):
        """Returns a point at normalized coordinates (u,v,w). If all coordinates are within a range of [0,1] then the point is in the Bounds. Otherwise the point is outside the Bounds.
        
            :param u: u-coordinate of a Point.
            :type u: float
            :param v: v-coordinate of a Point.
            :type v: float
            :param w: w-coordinate of a Point.
            :type w: float
            :result: A Point with normalized coordinates in the Bounds.
            :rtype: Point
        """
        if self.is_2d:
            return Point(self.ival_x.eval(u),self.ival_y.eval(v))
        return Point(self.ival_x.eval(u),self.ival_y.eval(v),self.ival_z.eval(w))

    def overlaps(self, other) :
        """Returns True if this Bounds overlaps the given Bounds.
        
            :param other: Given Bounds to be compared with this Bounds.
            :type other: Bounds
            :result: Boolean value
            :rtype: bool
            
        """
        return any([pt in self for pt in other.corners] + [pt in other for pt in self.corners])

    def subbounds(self,divs):
        """Produces sub-boundaries. Starts at bottom left, moves from left to right and then bottom to top.
        
            :param divs: Number of sub-boundaries.
            :type divs: int
            :result: A Bounds divided into sub-bounds.
            :rtype: Bounds
        
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
        """Returns the closest point within this Bounds.  If the point is already within the bounds, simply returns the point.
        
            :param p: Point.
            :type p: Point
            :result: A Point within this Bounds.
            :rtype: Point
            
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
        """Returns a PLine along the perimeter of a Bounds.
        
            :result: PLine around the Bounds.
            :rtype: PLine
            
        """
        from .dc_pline import *
        return PLine(self.corners+[self.corners[0]])


    @staticmethod
    def encompass(pts = [Point()]):
        """Constructs a Bounds that encompasses all Points in pts.
        
            :param pts: A list of Points.
            :type pts: [Point]
            :result: A Bounds that includes all Points in pts.
            :rtype: Bounds
        
        """
        ix = Interval.encompass([p.x for p in pts])
        iy = Interval.encompass([p.y for p in pts])
        try:
            iz = Interval.encompass([p.z for p in pts])
            return Bounds(ival_x = ix, ival_y = iy, ival_z = iz)
        except:
            return Bounds(ival_x = ix, ival_y = iy)
                    
        
    @staticmethod
    def unit_square():
        """Returns a unit square Bounds (2D) in the xy plane.
        
            :result: Unit square Bounds.
            :rtype: Bounds
            
        """
        return Bounds(ival_x=Interval(),ival_y=Interval())

    @staticmethod
    def unit_cube():
        """Returns a unit cube Bounds (3D).
            
            :result: Unit cube Bounds.
            :rtype: Bounds
        
        """
    
        return Bounds(ival_x=Interval(),ival_y=Interval(),ival_z=Interval())

class QuadTree():
    def __init__ (self, capacity, bounds):
        """Description
        
            :param capacity: Total number of points to contain.
            :type capacity: int
            :param bounds: Bounds.
            :type bounds: Bounds
            :result: QuadTree object.
            :rtype: QuadTree
        
        """
    
        self.cap = capacity
        self.bnd = bounds
        self._pts = []
        
    @property
    def has_children(self):
        """Description
        
            :result: Boolean value.
            :rtype: bool
        
        """
    
        if hasattr(self,'children'):return True 
        return False
        
    @property
    def pts(self):
        """Recursively returns all the points in this QuadTree.
        
            :result: List of Points.
            :rtype: [Point]
        """
        ret_pts = []
        if not self.has_children :
            ret_pts = [Point(pt) for pt in self._pts]
        else :
            for child in self.children: ret_pts.extend(child.pts)
        return ret_pts

    def append(self, pt) :
        """Appends the given point to the points in this QuadTree.
        
            :param pt: Point
            :type pt: Point
            :result: Boolean Value
            :rtype: bool
        
        """
    
        if not self.contains(pt) : return False
        if not self.has_children :
            if len(Point.cull_duplicates(self._pts)) < self.cap:
                self._pts.append(pt)
                return True
            else :
                self._divide()
        
        if self.has_children :
            for child in self.children:
                if child.append(pt) : return True
            return False
        else:
            raise("quadtree.append()... how did i get here?")
        
    def _divide(self) :
        """Divides self into sub regions. Starts at bottom left and moves clockwise.
        
            :result: Boolean Value
            :rtype: bool
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
        """Returns true if given point is in this QuadTree.
        
            :param pt: Point to test for containment.
            :type pt: Point
            :result: Boolean Value.
            :rtype: bool
            
        """
        if self.has_children:
            return any([child.contains(pt) for child in self.children])
        else:
            return pt in self.bnd
            
    def pts_in_bounds(self,bounds):
        """Finds all points that fall within a given bounds.
        
            :param bounds: bounds
            :type bounds: Bounds
            :result: List of Points in Bounds.
            :rtype: [Point]
            
        """
        if not self.bnd.overlaps(bounds) : return []
        ret_pts = []
        if not self.has_children :
            for pt in self._pts :
                if pt in bounds :  ret_pts.append(pt)
        else :
            for child in self.children: ret_pts.extend(child.pts_in_bounds(bounds))
        return ret_pts
        
    @staticmethod
    def encompass(capacity = 4, pts = [Point()]):
        """Returns a Bounds that encompasses the given points.
        
            :param capacity: Capacity of points within the Bounds.
            :type capacity: int
            :param pts: List of Points.
            :type pts: [Point]
            :result: Bounds encompassing the given points.
            :rtype: Bounds
        
        """
    
        q = QuadTree(capacity, Bounds.encompass(pts))
        for p in pts : q.append(p)
        return q
        
