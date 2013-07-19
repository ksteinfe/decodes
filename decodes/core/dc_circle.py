from decodes.core import *
from . import dc_base, dc_interval, dc_vec, dc_point, dc_plane, dc_cs #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "dc_circle.py loaded"

import copy, collections
import math

class Circle(Plane):
    """
    a circle class
    inherits all properties of the Plane class
    """
    
    def __init__(self,plane,radius):
        self.x = plane.x
        self.y = plane.y
        self.z = plane.z
        self._vec = plane._vec
        self.rad = radius
        
    @property
    def plane(self):
        return Plane(Point(self.x,self.y,self.z),self._vec)

        
    def __repr__(self): return "circ[{0},{1},{2},{3},{4},{5} r:{6}]".format(self.x,self.y,self.z,self._vec.x,self._vec.y,self._vec.z,self.rad)

    def intersections(self,other):
        '''
        returns intersections with another circle
        '''
        warnings.warn("circle.intersections depreciated. please intersection instead")
        results = XSec()
        if intersect(self,other,results):
            return results._geom
        return False

      
class Arc(HasBasis):
    """
    a circle class
    """
    
    def __init__(self,cs,radius,sweep_angle):
        self._basis = cs
        self.rad = radius
        self.angle = sweep_angle
        
    def eval(self,t):
        """ Evaluates this Arc and returns a Point.
            :param t: Normalized value between 0 and 1
            :type t: float
            :result: a Point on the Arc.
            :rtype: Point
        """
        x = self.rad * math.cos(t*self.angle)
        y = self.rad * math.sin(t*self.angle)
        return self._basis.eval(x,y)

    def eval_pln(self,t):
        """ Evaluates this Arc and returns a Plane.
            :param t: Normalized value between 0 and 1
            :type t: float
            :result: a Plane on the Arc.
            :rtype: Plane
        """
        pt = self.eval(t)
        return Plane(pt,Vec(self.origin,pt).cross(self._basis.z_axis))
        
    def deval(self,t):
        # only here so that we may use arcs as curves
        return self.eval(t)

    def deval_pln(self,t):
        # only here so that we may use arcs as curves
        return self.eval_pln(t)
        
    @property
    def length(self):
        return self.rad * self.angle
        
    @property
    def epts(self):
        return self.eval(0), self.eval(1) 
        
    @property
    def spt(self):
        return self.eval(0)
        
    @property
    def ept(self):
        return self.eval(1) 

    @property
    def origin(self):
        return self._basis.origin
        
    def __repr__(self): return "arc[{0},r:{1},sweep angle{2}]".format(self.origin,self.radius,self.sweep_angle)

    #Returns a best fit arc using the modified least squares method
    @staticmethod
    def arc_from_pts(pts_in):
        # Get the number of input points
        cnt = len(pts_in)
        # An Arc needs at least 3 points
        if len(pts_in) < 2 :
            raise GeometricError("Please provide more points") 
        x, y, x, xsq, ysq, xy, xysq, xsqy, xcube, ycube = [0]*10
        
        # Get new point values for the center point of the arc
        for pt in pts_in :
            x += pt.x 
            y += pt.y
            xsq += pt.x*pt.x
            ysq += pt.y*pt.y
            xy += pt.x*pt.y
            xysq += pt.x*pt.y*pt.y
            xsqy += pt.x*pt.x*pt.y
            xcube += pt.x*pt.x*pt.x
            ycube += pt.y*pt.y*pt.y
        
        # Get the center point for the arc
        A = cnt*xsq - x*x
        B = cnt*xy - x*y
        C = cnt*ysq - y*y
        D = 0.5*(cnt*xysq - x*ysq + cnt*xcube - x*xsq)
        E = 0.5*(cnt*xsqy - y*xsq + cnt*ycube - y*ysq)
        
        denom = A*C - B*B
        if (denom != 0):
            center = Point((D*C - B*E)/denom, (A*E - B*D)/denom)
        else: 
             raise GeometricError("A*C == B*B ... I Cannot find center of this Arc") 
        
        # Get the radius of the arc by getting the average distance from the points to the center
        rad = sum([pt._distance(center) for pt in pts_in])/cnt
        
        # Create segments between all the points and the center
        segs = [Segment(center,pt) for pt in pts_in]
        # The reference segment will be the first segment
        ref_vec = segs[0].vec
        for seg in segs:
            # Get the angle between all the segments and the reference segment
            seg.angle = ref_vec.angle(seg.vec)
            # Make sure the ange is not negative
            if ref_vec.cross(seg.vec).z < 0 : seg.angle = - seg.angle
            
        # Sort the segments by angle
        segs = sorted(segs, key=lambda seg: seg.angle)
        # Get the sweep angle
        sweep = segs[-1].angle - segs[0].angle
        
        # Orient the CS with the segment with the smallest angle
        cs = CS(center,segs[0].vec,segs[1].vec)
        return Arc(cs,rad,sweep)


