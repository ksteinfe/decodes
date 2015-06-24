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
        
            :param \**kargs: Function that accepts multiple parameters to be passed. Parameters include center, x, y and z dimension OR x, y and z intervals.
            :type \**kargs: (float, float), float, float OR Interval, Interval
            :result: Bounds
            :rtype: Bounds
        
        """
        if len(kargs)==0:
            self.ival_x = Interval()
            self.ival_y = Interval()
        else:
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
        """ Returns the center Point of the Bounds.
            
            :result: Center Point of Bounds.
            :rtype: Point
        
        """
        try:
            return Point(self.ival_x.mid,self.ival_y.mid,self.ival_z.mid)
        except:
            return Point(self.ival_x.mid,self.ival_y.mid)
            
    @property
    def dim_x(self):
        """ Returns x dimension of Bounds.
        """
        
        return self.ival_x.delta

    @property
    def dim_y(self):
        """ Returns y dimension of Bounds.
        """
        
        return self.ival_y.delta

    @property
    def dim_z(self):
        """ Returns z dimension of Bounds.
        """
        
        try:
            return self.ival_z.delta
        except:
            return 0.0

    @property
    def is_2d(self):
        """ Returns True if Bounds is 2-dimensional (no z component). Otherwise returns False.
        """
        return not hasattr(self, 'ival_z')

    @property
    def is_3d(self): 
        """ Returns True if Bounds is 3-dimensional (x, y and z components). Otherwise returns False.
        """
        return hasattr(self, 'ival_z')

    @property
    def corners(self):
        """ Moves counter clockwise, like so:
        
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
    
    @property
    def edges(self):
        from .dc_line import Segment
        cnrs = self.corners
        if self.is_2d:
            return [
                Segment(cnrs[0],cnrs[1]),
                Segment(cnrs[1],cnrs[2]),
                Segment(cnrs[2],cnrs[3]),
                Segment(cnrs[3],cnrs[0])
                ]
        else:
            return [
                Segment(cnrs[0],cnrs[1]),
                Segment(cnrs[1],cnrs[2]),
                Segment(cnrs[2],cnrs[3]),
                Segment(cnrs[3],cnrs[0]),
                
                Segment(cnrs[4],cnrs[5]),
                Segment(cnrs[5],cnrs[6]),
                Segment(cnrs[6],cnrs[7]),
                Segment(cnrs[7],cnrs[4]),
                
                Segment(cnrs[0],cnrs[4]),
                Segment(cnrs[1],cnrs[5]),
                Segment(cnrs[2],cnrs[6]),
                Segment(cnrs[3],cnrs[7])
                ]
        
    
    
    
    def __contains__(self, pt):
        """| Overloads the containment **(in)** operator.

           .. note:: Less-than or equal-to logic applied, points that lie on any edge of the bounds will be considered to be contained within it.
        
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
        """ Overloads the integer division **(//)** operator. Calls Bounds.subbounds(other).
        
            :param other: Number of sub-boundaries.
            :type other: int
            :result: a Bounds divided into sub-bounds.
            :rtype: Bounds
        """
        return self.subbounds(other)

    def eval(self,u,v,w=0):
        """ Returns a point at normalized coordinates (u,v,w). If all coordinates are within a range of [0,1] then the point is in the Bounds. Otherwise the point is outside the Bounds.
        
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
        
    def scaled(self, factor):
        f2 = (factor-1.0)/2.0
        pts = [self.eval(0-f2,0-f2,0-f2),self.eval(1+f2,1+f2,1+f2)]
        ix = Interval.encompass([p.x for p in pts])
        iy = Interval.encompass([p.y for p in pts])
        if self.is_2d:  return Bounds(ival_x = ix, ival_y = iy)
        iz = Interval.encompass([p.z for p in pts])
        return Bounds(ival_x = ix, ival_y = iy, ival_z = iz)
        

    def overlaps(self, other) :
        """ Returns True if this Bounds overlaps the given Bounds.
        
            :param other: Given Bounds to be compared with this Bounds.
            :type other: Bounds
            :result: Boolean value
            :rtype: bool
            
        """
        #if any([pt in self for pt in other.corners] + [pt in other for pt in self.corners]): return True
        #if self.is_2d: return ((self.ival_x in other.ival_x and other.ival_y in self.ival_y) or (other.ival_x in self.ival_x and self.ival_y in other.ival_y))
        #return ((self.ival_x in other.ival_x or other.ival_x in self.ival_x) and (self.ival_y in other.ival_y or other.ival_y in self.ival_y) and (self.ival_z in other.ival_z or other.ival_z in self.ival_z) )
        #return False
        if self.is_2d: 
            return(
                (other.ival_x.overlaps(self.ival_x) or self.ival_x.overlaps(other.ival_x)) and 
                (other.ival_y.overlaps(self.ival_y) or self.ival_y.overlaps(other.ival_y)) 
            )
        else: 
            return(
                (other.ival_x.overlaps(self.ival_x) or self.ival_x.overlaps(other.ival_x)) and 
                (other.ival_y.overlaps(self.ival_y) or self.ival_y.overlaps(other.ival_y)) and 
                (other.ival_z.overlaps(self.ival_z) or self.ival_z.overlaps(other.ival_z))
            )

    def subbounds(self,divs,equalize=False):
        """ Produces sub-boundaries. Starts at bottom left, moves from left to right and then bottom to top.
        
            :param divs: Number of sub-boundaries.
            :type divs: int
            :result: A Bounds divided into sub-bounds.
            :rtype: Bounds
        
        """
        if equalize:
            divdim = min(self.ival_x.delta / divs, self.ival_y.delta / divs)
            if self.is_3d: divdim = min(divdim, self.ival_z.delta / divs)
            divs_x = int(round(self.ival_x.delta/divdim))
            divs_y = int(round(self.ival_y.delta/divdim))
            subival_x = self.ival_x // divs_x
            subival_y = self.ival_y // divs_y
            if self.is_3d: 
                divs_z = int(round(self.ival_z.delta/divdim))
                subival_z = self.ival_z // divs_z
        else:
            subival_x = self.ival_x//divs
            subival_y = self.ival_y//divs
            if self.is_3d: subival_z = self.ival_z//divs
        ret = []
        if self.is_3d:
            for iz in subival_z:
                for iy in subival_y:
                    for ix in subival_x:
                        ret.append(Bounds(ival_x=ix,ival_y=iy,ival_z=iz))
        else:
            for iy in subival_y:
                for ix in subival_x:
                    ret.append(Bounds(ival_x=ix,ival_y=iy))

        return ret

    def near_pt(self, p, force_project=False):
        """ Returns the closest point within this Bounds.  If the point is already within the bounds and force_project is False, simply returns the point; if force_project is True, the point is projected to the edge of this bounds.
        
            :param p: Point.
            :type p: Point
            :result: A Point within this Bounds.
            :rtype: Point
            
        """
        p = Point(p.x,p.y,p.z)
        if p in self : 
            if force_project:
                dx = self.ival_x.a - p.x if p.x - self.ival_x.a < self.ival_x.b - p.x else self.ival_x.b - p.x
                dy = self.ival_y.a - p.y if p.y - self.ival_y.a < self.ival_y.b - p.y else self.ival_y.b - p.y
                dz = self.ival_z.a - p.z if p.z - self.ival_z.a < self.ival_z.b - p.z else self.ival_z.b - p.z
                
                deltas = (abs(dx),abs(dy),abs(dz))
                mn = deltas.index(min(deltas))
                if mn == 0: p.x += dx
                elif mn == 1: p.y += dy
                else : p.z += dz
            
        else:
            if p.x < self.ival_x.a : p.x = self.ival_x.a
            if p.x > self.ival_x.b : p.x = self.ival_x.b
            if p.y < self.ival_y.a : p.y = self.ival_y.a
            if p.y > self.ival_y.b : p.y = self.ival_y.b
        
            if self.is_2d: p.z = 0
            else:
                if p.z < self.ival_z.a : p.z = self.ival_z.a
                if p.z > self.ival_z.b : p.z = self.ival_z.b
        
        return p


    def to_pline(self):
        """ Returns a PLine along the perimeter of a Bounds.
        
            :result: PLine around the Bounds.
            :rtype: PLine
            
        """
        from .dc_pline import PLine
        if self.is_2d: return PLine(self.corners+[self.corners[0]])
        else: 
            pp = self.corners
            return PLine([pp[0],pp[1],pp[2],pp[3],pp[0],pp[4],pp[5],pp[6],pp[7],pp[4]])


    @staticmethod
    def encompass(pts = [Point()]):
        """ Constructs a Bounds that encompasses all Points in pts.
        
            :param pts: A list of Points.
            :type pts: [Point]
            :result: A Bounds that includes all Points in pts.
            :rtype: Bounds
        
        """
        ix = Interval.encompass([p.x for p in pts],nudge=True)
        iy = Interval.encompass([p.y for p in pts],nudge=True)
        try:
            iz = Interval.encompass([p.z for p in pts])
            if not iz: raise
            return Bounds(ival_x = ix, ival_y = iy, ival_z = iz)
        except:
            return Bounds(ival_x = ix, ival_y = iy)
                    
        
    @staticmethod
    def unit_square(dimension = 1.0):
        """ Returns a unit square Bounds (2D) in the xy plane.
        
            :result: Unit square Bounds.
            :rtype: Bounds
            
        """
        return Bounds(ival_x=Interval(-dimension/2,dimension/2),ival_y=Interval(-dimension/2,dimension/2))

    @staticmethod
    def unit_cube():
        """ Returns a unit cube Bounds (3D).
            
            :result: Unit cube Bounds.
            :rtype: Bounds
        
        """
    
        return Bounds(ival_x=Interval(),ival_y=Interval(),ival_z=Interval())

        
        
        
        
        
class QuadTree():
    def __init__ (self, capacity, bounds):
        """ QuadTree constructor.
        
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
        """ Returns True if QuadTree has children.
        
            :result: Boolean value.
            :rtype: bool
        
        """
    
        if hasattr(self,'children'):return True 
        return False
        
    @property
    def pts(self):
        """ Recursively returns all the points in this QuadTree.
        
            :result: List of Points.
            :rtype: [Point]
        """
        ret_pts = []
        if not self.has_children :
            ret_pts = list(self._pts)
        else :
            for child in self.children: ret_pts.extend(child.pts)
        return ret_pts

    def append(self, pt) :
        """ Appends the given point to the points in this QuadTree.
        
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
        
    def _divide(self,equalize_bounds=False) :
        """ Divides self into sub regions. Starts at bottom left and moves clockwise.
        
            :result: Boolean Value
            :rtype: bool
        """
        if self.has_children: return False
        
        if equalize_bounds: 
            sub_bnds = self.bnd.subbounds(1,equalize=True)
        else:
            sub_bnds = self.bnd//2
            
        self.children = [QuadTree(self.cap,sub_bnd) for sub_bnd in sub_bnds]
        for child in self.children: child.parent = self
        
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
        """ Returns true if given point is in this QuadTree.
        
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
        """ Finds all points that fall within a given bounds.
        
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
        
        
    def flatten(self,return_empty_containers=False):
        if self.has_children:
            ret = []
            if return_empty_containers: ret = [self]
            for child in self.children: ret.extend(child.flatten(return_empty_containers))
            return ret
        else:
            return [self]

    def container_of(self,pt):
        if not pt in self.bnd: raise Exception("point does not lie within the bounds of this QTree")
        if not self.has_children: return self
        for child in self.children:
            if pt in child.bnd: return child.container_of(pt)
            
            
    def pts_neighboring(self,pt):
        return self.container_of(pt).pts
        
    def containers_neighboring(self,pt):
        container = self.container_of(pt)
        bnd = container.bnd.scaled(1.10)
        others = self.flatten()
        ret = []
        for other in others:
            if other.bnd.overlaps(bnd): ret.append(other)
        return ret
        
    def pts_nearby(self,src_pt):
        if not src_pt in self.bnd : src_pt = self.bnd.near_pt(src_pt)
        container = self.container_of(src_pt)
        #a.put(container.bnd.to_pline())
        near_pts = container.pts
        
        proj_pts = [Point(container.bnd.ival_x.a,src_pt.y,src_pt.z), Point(container.bnd.ival_x.b,src_pt.y,src_pt.z),Point(src_pt.x,container.bnd.ival_y.a,src_pt.z), Point(src_pt.x,container.bnd.ival_y.b,src_pt.z)]
        if container.bnd.is_3d: proj_pts.extend([Point(src_pt.x,src_pt.y,container.bnd.ival_z.a), Point(src_pt.x,src_pt.y,container.bnd.ival_z.b)])
        for edge in container.bnd.edges: proj_pts.append(edge.near_pt(src_pt))
        
        for p in proj_pts:
            p += Vec(src_pt,p)*EPSILON
            #a.put(Segment(src_pt,p))
            try:
                adj_container = self.container_of(p)
                a.put(adj_container.bnd.to_pline())
                for adj_pt in adj_container.pts:
                    if adj_pt not in near_pts: near_pts.append(adj_pt)
            except:
                # no adjacent container
                pass
        near_pts.sort(key = lambda p: p.distance2(src_pt))
        return near_pts
        
        
    @staticmethod
    def encompass(capacity = 4, pts = [Point()]):
        """ Returns a QuadTree that encompasses the given points.
        
            :param capacity: Capacity of points within the Bounds.
            :type capacity: int
            :param pts: List of Points.
            :type pts: [Point]
            :result: QuadTree encompassing the given points.
            :rtype: QuadTree
        
        """
    
        q = QuadTree(capacity, Bounds.encompass(pts))
        q._divide(equalize_bounds=True)
        for p in pts : q.append(p)
        return q
        
