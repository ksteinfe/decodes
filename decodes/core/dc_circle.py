from decodes.core import *
from . import dc_base, dc_interval, dc_vec, dc_point, dc_plane, dc_cs #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print("dc_circle.py loaded")

import copy, collections
import math

class Circle(Plane):
    """
    a circle class
    inherits all properties of the Plane class
    """
    
    def __init__(self,plane,radius):
        """ Circle constructor.
        
            :param plane: Plane the Circle is centered on.
            :type plane: Plane
            :param radius: Radius of the circle.
            :type radius: float
            :result: Circle object.
            :rtype: Circle
            
            
        """
        self.x = plane.x
        self.y = plane.y
        self.z = plane.z
        self._vec = plane._vec
        self.rad = radius
        
    @property
    def plane(self):
        """ Returns the plane this circles lies on.
            
            :result: Plane.
            :rtype: Plane
        """
        return Plane(Point(self.x,self.y,self.z),self._vec)

        
    def __repr__(self): return "circ[{0},{1},{2},{3},{4},{5} r:{6}]".format(self.x,self.y,self.z,self._vec.x,self._vec.y,self._vec.z,self.rad)

    def intersections(self,other):
        """ Returns intersections with another circle.
        
            :param other: Other circle to intersect.
            :type other: Circle
            :result: Boolean value.
            :rtype: bool
            
            .. warning:: Please use Intersector() instead.
        """
        warnings.warn("circle.intersections depreciated. please Intersector() instead")
        xsec = Intersector()
        if xsec.of(self,other):
            return xsec._geom
        return False
    
    @staticmethod
    def mutually_tangent(cir_a,cir_b,tangent_offset=0.0,calc_extras=False):
        """| given two circles, returns a circle that is tangent to both of them.
           | by default, returns the smallest possible circle (where the points of tangency on each given circle lies along a single line), 
           | however, if the tan_offset parameter is set to a value other than zero, then the point of tangency may be explicitly set as a rotation from this smallest tangency point
           | the two given circles must be co-planar
           | calc_extras = True returns the points of tangency as well
           
           :param cir_a: First Circle.
           :type cir_a: Circle.
           :param cir_b: Second Circle.
           :type cir_b: Circle
           :param tangent_offset: Rotation from the smallest tangency point.
           :type tangent_offset: float
           :param calc_extras: Boolean Value.
           :type calc_extras: bool
           :result: Mutually tangent Circle.
           :rtype: Circle
           
        """
        if not cir_a.plane.is_coplanar(cir_b.plane):
            raise GeometricError("Circles must be co-planar.")  
        z_axis = cir_a.plane.normal

        vec_rad = Vec(cir_a.origin,cir_b.origin).normalized(cir_a.rad)
        pt_tan = cir_a.origin + vec_rad
        if tangent_offset != 0.0:
            cs = CS(cir_a.origin,vec_rad,vec_rad.cross(z_axis))
            pt_tan = cs.eval(cir_a.rad * math.cos(tangent_offset),cir_a.rad * math.sin(tangent_offset))

        pt_ff = pt_tan + Vec(pt_tan,cir_a.origin).normalized(cir_b.rad)
        ln_f = Line(pt_ff,Vec(pt_ff,pt_tan))

        pt_gg = Point.centroid([pt_ff,cir_b.plane.origin])
        ln_g = Line(pt_gg , Vec(pt_ff,cir_b.plane.origin).cross(z_axis))

        from .dc_intersection import Intersector 
        xsec = Intersector()
        if xsec.of(ln_g,ln_f):
            rad = xsec[0].distance(pt_tan)
            cir = Circle(Plane(xsec[0],z_axis),rad)
            if calc_extras:
                pt_tan_b = cir.plane.origin + Vec(cir.plane.origin,cir_b.plane.origin).normalized(cir.rad)
                return cir,pt_tan,pt_tan_b
            return cir
        else:
            raise GeometricError("Circle.mutually_tangent encountered a problem performing an intersection operation.") 
            
    @staticmethod
    def thru_pts(start_pt, mid_pt, end_pt):
        """ Returns an Circle that goes through a startpoint, midpoint and endpoint
                
            :param start_pt: First Point on Circle
            :type start_pt: Point
            :param mid_pt: Second Point on Circle.
            :type mid_pt: Point
            :param end_pt: Third Point on Circle
            :type end_pt: Point
            :result: circ_out
            :rtype: Circle
            
        """
        v1 = Vec(end_pt - mid_pt)
        v2 = Vec(start_pt - mid_pt)
        v3 = Vec(end_pt - start_pt)
        
        try:
            rad_osc = 0.5*v1.length*v2.length*v3.length/(v1*v3).length
            denom = 2*(v1.cross(v3).length)*(v1.cross(v3).length)
            a1 = v3.length*v3.length*v1.dot(v2)/denom
            a2 = v2.length*v2.length*v1.dot(v3)/denom
            a3 = v1.length*v1.length*(-v2.dot(v3))/denom
            center_osc = mid_pt*a1 + end_pt*a2 + start_pt*a3
            
            pln_out = Plane(center_osc, v1.cross(v2))
            circ_out = Circle(pln_out,rad_osc)
            
            return circ_out
        
        except: 
            raise GeometricError("points are either co-linear or at least two are coincident") 

      
class Arc(HasBasis):
    """
    a circle class
    """
    
    def __init__(self,cs,radius,sweep_angle):
        """Arc Constructor
        
            :param cs: Coordinate system.
            :type cs: CS
            :param radius: Radius of arc.
            :type radius: float
            :param sweep_angle: Angle of arc.
            :type swee_angle: float
            :result: Arc object
            :rtype: Arc
            
            ::
            
                my_arc=Arc(CS(Point(0,0,0)), 6.0, 1.5) 
            
        """
        self._basis = cs
        self.rad = radius
        self.angle = sweep_angle
        
    def eval(self,t):
        """ Evaluates this Arc and returns a Point.
        
            :param t: Normalized value between 0 and 1.
            :type t: float
            :result: a Point on the Arc.
            :rtype: Point
            
            ::
            
                my_arc.eval(0.5)
        """
        x = self.rad * math.cos(t*self.angle)
        y = self.rad * math.sin(t*self.angle)
        return self._basis.eval(x,y)

    def eval_pln(self,t):
        """ Evaluates this Arc and returns a Plane.
        
            :param t: Normalized value between 0 and 1.
            :type t: float
            :result: a Plane on the Arc.
            :rtype: Plane
            
            ::
            
                my_arc.eval_pln(0.5)
        """
        pt = self.eval(t)
        return Plane(pt,Vec(self.origin,pt).cross(self._basis.z_axis))
        
    def deval(self,t):
        """ Evaluates this Arc and returns a Point. Equivalent to eval.
            
            :param t: Normalized value between 0 and 1.
            :type t: float
            :result: a Point on the Arc.
            :rtype: Point
            
        """
        # only here so that we may use arcs as curves
        return self.eval(t)

    def deval_pln(self,t):
        """ Evaluates this Arc and returns a Plane. Equivalent to eval_pln.
        
            :param t: Normalized value between 0 and 1.
            :type t: float
            :result: a Plane on the Arc.
            :rtype: Plane
        """    
        # only here so that we may use arcs as curves
        return self.eval_pln(t)
        
    @property
    def length(self):
        """ Returns length of this Arc.
        
            :result: Length of arc.
            :rtype: float
            
            ::
            
                my_arc.length
        """
        return self.rad * self.angle
        
    @property
    def epts(self):
        """ Returns the end points of this Arc.
            
            :result: End points of this arc.
            :rtype: Point, Point
            
            ::
            
                my_arc.epts
        
        """
        return self.eval(0), self.eval(1) 
        
    @property
    def spt(self):
        """ Returns the start Point of this Arc.
        
            :result: Start Point of this arc.
            :rtype: Point
            
            ::
            
                my_arc.spt
            
        """
        return self.eval(0)
        
    @property
    def ept(self):
        """ Returns the end Point of this Arc.
            
            :result: End Point of this arc.
            :rtype: Point
            
            ::
            
                my_arc.ept
            
        """
        return self.eval(1) 

    @property
    def origin(self):
        """ Returns the origin of the basis of this Arc.
        
            :result: Origin of this Arc's basis.
            :rtype: Point
            
            ::
            
                my_arc.origin
        """
        return self._basis.origin
        
    @property
    def is_major(self):
        return self.angle > math.pi

    @property
    def is_minor(self):
        return self.angle < math.pi

    @property
    def is_semicircle(self):
        return self.angle == math.pi          
      
    
    # Returns the distance between an Arc and a point
    def near(self, p):
        """ Returns the distance between an Arc and a Point.
        
            :param p: Point to look for a near Point on the LinearEntity.
            :type p: Point
            :result: Tuple of near point on Arc, and distance from point to near point
            :rtype: (Point, float)
            
        """
    
        #find the normal vector to the plane of the arc
        if self.spt != self.ept:
            pln_normal = (Vec(self.origin, self.spt).cross(Vec(self.origin, self.ept))).normalized()
        else:
            pln_normal = (Vec(self.origin, self.ept).cross(Vec(self.origin, self.eval(0.25)))).normalized()
        
        # if normal vector points to same side of plane as curve point
        if Vec(self.origin, p).dot(pln_normal) > 0:
            pt_proj = p - pln_normal*(Vec(self.origin, p).dot(pln_normal))
        else:
            pt_proj = p + pln_normal*(Vec(self.origin, p).dot(-pln_normal))
        dist_1 = p.distance(pt_proj) 

        #find intersection of the projected point with full circle (both lying on same plane)
        vec_u = Vec(self.origin, pt_proj).normalized()
        pt_int = self.origin + vec_u*self.rad  

        #set up quantities to test whether the intersection point is on the arc
        v_perp = Vec(self.spt, self.ept).cross(pln_normal)
        if (self.angle > math.pi): v_perp = -v_perp

        #if intersection point is on the arc
        if (Vec(self.spt, pt_int).dot(v_perp) > 0):     
            dist_2 = pt_proj.distance(pt_int)
        #if pt_int is not on the arc
        else:
            dist_2 = min(pt_proj.distance(self.spt), pt_proj.distance(self.ept))
   
        angle = Vec(self.origin, self.spt).angle(Vec(self.origin, pt_int))
        
        if self.basis.deval(self._basis.xAxis.cross(Vec(self.origin, pt_int))).z < 0:
            angle = math.pi * 2 - angle
        t = angle/self.angle
        near = (pt_int, t, math.sqrt(dist_1**2 + dist_2**2))
        
        if near[1] < 0 or near[1] > 1:
            if p.distance(self.spt) < p.distance(self.ept):
                near = (self.spt,0.0,p.distance(self.spt))
            else: near = (self.ept,1.0,p.distance(self.ept))
        
        return near
    
    
    def near_pt(self, p):
        """ Returns the closest point to a given Arc
       
            :param p: Point to look for a near Point on the Arc.
            :type p: Point
            :result: Near point on Arc.
            :rtype: Point
        """
        return self.near(p)[0]
    
     
    def reciprocal(self):
        vx = Vec(self.origin,self.ept)
        vy = Vec(self.origin,self.eval(1.0+EPSILON))
        cs = CS(self.origin,vx,vy)
        return Arc(cs,self.rad,math.pi*2-self.angle)

    
    def split_by(self,plane):
        """ Splits this arc by a given Plane
        
            :result: Origin of this Arc's basis.
            :rtype: Point
            
            ::
            
                my_arc.origin
        """    
        from .dc_intersection import Intersector 
        xsec = Intersector()
        if not xsec.of(self, plane): return False
        
        pts = xsec.results + [self.ept]
        delts = [j-i for i, j in zip([0]+xsec.angs, xsec.angs+[self.angle])]
        angs = xsec.angs + [self.angle]
        
        split_arcs = []
        cs = self.basis
        for pt, delt, ang in zip(pts,delts,angs):
            split_arcs.append(Arc(cs,self.rad,delt))
            vx = Vec(cs.origin,pt)
            vy = Vec(cs.origin,self.eval(ang/self.angle+EPSILON))
            cs = CS(cs.origin,vx,vy)
            
        return split_arcs    
    
      
        
    def __repr__(self): return "arc[{0},r:{1},sweep angle{2}]".format(self.origin,self.rad,self.angle)
    

    
    # Returns an arc using a start point, a sweep point and a tangent to the arc at the start point
    @staticmethod
    def from_tan(start_pt,sweep_pt,tan):
        """Returns an arc using a start point, a sweep point and a tangent to the arc at the start point.
            
            :param start_pt: Arc start Point.
            :type start_pt: Point
            :param sweep_pt: Arc sweep Point.
            :type sweep_pt: Point
            :param tan: Tangent vector at start point.
            :type tan: Vec
            :result: Arc
            :rtype: Arc
            
        """
        
        vec_ab = Vec(start_pt, sweep_pt)
        try:
            vec_rad = tan.cross(tan.cross(vec_ab))
            ang = vec_ab.angle(vec_rad)
            rad = vec_ab.length/math.cos(ang)/2.0
            center = Point(start_pt+vec_rad.normalized(rad))
        
            if (vec_ab.dot(tan) > 0):
                arc_out = Arc.from_pts(center,start_pt,sweep_pt)
            else:
                arc_out = Arc.from_pts(center,start_pt, sweep_pt, True)    
            return arc_out
        
        except: 
            raise GeometricError("points are either co-linear or at least two are coincident") 
        
    
    # Returns an arc using a center, a start point and a sweep point
    @staticmethod
    def from_pts(center,start_pt,sweep_pt,is_major=False):
        """ Returns an arc using a center, a start point and a sweep point.
            
            :param center: Center Point of Arc.
            :type center: Point
            :param start_pt: Start Point of Arc.
            :type start_pt: Point
            :param sweep_pt: Sweep Point of Arc.
            :type sweep_pt: Point
            :param is_major: Boolean Value.
            :type is_major: bool
            :result: Arc
            :rtype: Arc
            
        """
        
        radius = center.distance(start_pt)
        angle = Vec(center, start_pt).angle(Vec(center, sweep_pt))
        
        if is_major:
            angle = 2*math.pi - angle
            cs = CS(center, Vec(center, start_pt), Vec(center, sweep_pt).inverted())
        else:
            cs = CS(center, Vec(center, start_pt), Vec(center, sweep_pt))    
        return Arc(cs, radius, angle)
    
    
    # Make an arc that goes through a startpoint, midpoint and endpoint
    @staticmethod
    def thru_pts(start_pt, mid_pt, end_pt):
        """ Returns an arc that goes through a startpoint, midpoint and endpoint
                
            :param start_pt: Start Point of Arc.
            :type start_pt: Point
            :param mid_pt: Mid Point of Arc.
            :type mid_pt: Point
            :param end_pt: End Point of Arc.
            :type end_pt: Point
            :result: Arc
            :rtype: Arc
            
        """
    
    
        v1 = Vec(start_pt, mid_pt)
        v2 = Vec(start_pt, end_pt)
        v3 = Vec(end_pt, mid_pt)
        
        try:
            xl = v1.cross(v3).length
            if xl == 0 : return False
                
            rad = 0.5*v1.length*v2.length*v3.length/xl        
            denom = 2*xl*xl
            
            a1 = v3.length*v3.length*v1.dot(v2)/denom
            a2 = v2.length*v2.length*v1.dot(v3)/denom
            a3 = v1.length*v1.length*(-v2.dot(v3))/denom
            center = start_pt*a1 + mid_pt*a2 + end_pt*a3
            
            #test to see which arc between start_pt and end_pt contains mid_pt
            #condition given by the angle between v1 and the perpendicular vector to v2 being acute
            pln_normal = Vec(center, start_pt).cross(Vec(center, end_pt))
            if pln_normal.length == 0:
                pln_normal = v1.cross(v2)
            v_perp = v2.cross(pln_normal)
            
            try:
                arc_out = Arc.from_pts(center,start_pt,end_pt, not v1.dot(v_perp))
            except:
                angle = Vec(center,start_pt).angle(Vec(center, end_pt))
                radius = center.distance(start_pt)
                cs = CS(center, Vec(center, start_pt), Vec(center, mid_pt))
                arc_out = Arc(cs, radius, angle)
            return arc_out   
            
        except: 
            raise GeometricError("points are either co-linear or at least two are coincident") 

        
    #Returns a best fit arc using the modified least squares method
    @staticmethod
    def best_fit(pts_in):
        """ Returns a best fit arc using the modified least squares method.
        
            :param pts_in: Points to fit Arc to.
            :type pts_in: [Point]
            :result: Best fit Arc
            :rtype: Arc
            
        """
        
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
        rad = sum([pt.distance(center) for pt in pts_in])/cnt
        
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
        
    


