from decodes.core import *
from . import dc_base, dc_interval, dc_vec, dc_point, dc_cs, dc_has_pts #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print("polygon.py loaded")

import copy, collections
import math

class PGon(HasPts):
    """A very simple 2d polygon class
       
       Polygons limit their vertices to x and y dimensions, and enforce that they employ a basis.    Transformations of a polygon should generally be applied to the basis.    Any tranfromations of the underlying vertices should ensure that the returned vectors are limited to x and y dimensions
    """
    subclass_attr = ['_edges'] # this list of props is unset anytime this HasPts object changes

    def __init__(self, vertices=None, basis=None):
        """ PGon Constructor.
        
            :param vertices: List of vertices to build the polygon.
            :type vertices: list
            :param basis: Plane basis for the PGon.
            :type basis: Basis
            :returns: PGon object. 
            :rtype: PGon
            
            ::
            
                pts=[
                    Point(0,0,0),
                    Point(0,1,0),
                    Point(1,1,0),
                    Point(1,0,0)
                    ]
                    
                my_pgon=PGon(pts)
        """ 
        if basis is None and vertices is None : raise GeometricError("You must define either a basis or a list of vertices (or both) to construct a PGon")
        
        if basis is None:
            #if i pass in vertices but no basis, try and figure out what the CS should be and project all points to the proper plane
            def appx_eq(a, b): return abs(a-b) < EPSILON

            x_vals,y_vals,z_vals = [v.x for v in vertices],[v.y for v in vertices],[v.z for v in vertices]
            x_avg,y_avg,z_avg = sum(x_vals)/float(len(x_vals)) , sum(y_vals)/float(len(y_vals)) , sum(z_vals)/float(len(z_vals))
            cen = Point(x_avg,y_avg,z_avg)
            if all(appx_eq(x,x_avg) for x in x_vals) or all(appx_eq(y,y_avg) for y in y_vals) or all(appx_eq(z,z_avg) for z in z_vals) :
                cs = CS(vertices[0],Vec(vertices[0],vertices[1]),Vec(vertices[0],cen))
                verts = [cs.deval(v) for v in vertices]
                super(PGon,self).__init__([Vec(v.x,v.y) for v in verts],cs)
            else:
                plane = Plane.from_pts(vertices[0],vertices[1],vertices[2])
                if all([plane.near(v)[2] < EPSILON for v in vertices]):
                    cs = CS(vertices[0],Vec(vertices[0],vertices[1]),Vec(vertices[0],Point.centroid(vertices)))
                    verts = [cs.deval(v) for v in vertices]
                    super(PGon,self).__init__([Vec(v.x,v.y) for v in verts],cs)
                else:
                    raise GeometricError("Cannot create a polygon from a non-planar set of points")
        else:
            super(PGon,self).__init__([Vec(v.x,v.y) for v in vertices],basis) #HasPts constructor handles initialization of verts and basis
            self.basis = basis # set the basis after appending the points

        
    def append(self,pts):
        """| Appends the given Point to the PGon.
           | Each Point is processed to ensure planarity.

           :param pts: Point(s) to append.
           :type pts: Point or [Point]
           :result: Modifies this geometry by adding items to the stored list of points.
           :rtype: None
        """
        super(PGon,self).append(pts)
        try:
            for n in range(len(pts)): self._verts[-(n+1)].z = 0
        except:
            self._verts[-1].z = 0
        
    def seg(self,idx):
        """| Returns a segment of this Polygon as a Segment
           | The returned line segment will contain a copy of the Points stored in the segment.
        
           :param index: Index of the desired segment.
           :type index: Int
           :returns: Segment object. 
           :rtype: Segment
           
           
        """
        idx_a, idx_b = idx%(len(self)), (idx+1)%(len(self))
        return Segment(self.pts[idx_a],self.pts[idx_b])

        
    def cnr(self,index):
        """| Returns a corner of this Polygon as a pair of Rays
        
           :param index: Index of the desired corner.
           :type index: Int
           :returns: A Pair of Rays. 
           :rtype: (Ray)
        """
        if index >= len(self) : raise IndexError()
        i0, i1 = index - 1, index + 1
        if i0<0 : i0 = len(self)-1
        if i1> len(self)-1 : i1 = 0
        
        return Ray(self.pts[index],Vec(self.pts[index],self.pts[i0])) , Ray(self.pts[index],Vec(self.pts[index],self.pts[i1]))
        
        
    def __contains__(self, pt):
        """ Overloads the containment **(in)** operator.
        
            :param pts: Point to determine containment in this PGon.
            :type pts: Point
            :result: Boolean Value.
            :rtype: bool
            
        """
        return self.contains_pt(pt)

    @property
    def edges(self):
        """ Returns the edges of a PGon.
       
            :result: List of edges of a PGon
            :rtype: [Segment]
            
            ::
            
                my_pgon.edges
            
        """
        return [self.seg(n) for n in range(len(self))]
        
    @property
    def area(self):
        """ Returns the area of this PGon.
        
            :result: Area of PGon.
            :rtype: float
            
            ::
            
                my_pgon.area
            
        """
        a = 0
        for n in range(len(self._verts)): a += (self._verts[n-1].x + self._verts[n].x) * (self._verts[n-1].y - self._verts[n].y)
        return abs(a / 2.0)
        
    @property
    def is_clockwise(self):
        """ Determines if the verts of this PGon are more-or-less ordered clockwise or counter-clockwise relative to its basis.
        
            :result: The clockwiseness of this PGon.
            :rtype: bool
            
            ::
            
                my_pgon.area
            
        """
        a = 0
        for n in range(len(self._verts)): a += (self._verts[n-1].x - self._verts[n].x) * (self._verts[n-1].y + self._verts[n].y)
        return a > 0.0
        

    @property
    def bounds(self):
        """ Returns the bounding box of this polygon, aligned to the basis of this polygon.
        
            :result: Bounding box of polygon.
            :rtype: Bounds
            
            ::
            
                my_pgon.bounds
            
        """

        xx = [vec.x for vec in self._verts]
        yy = [vec.y for vec in self._verts]
        ivx = Interval(min(xx),max(xx))
        ivy = Interval(min(yy),max(yy))

        return Bounds(ival_x = ivx, ival_y = ivy)

        
    def angle_bisector(self,index):
        """ Returns the bisector of one angle in a Polygon
        
            :result: The Vector that bisects that angle, and the angle of the bisector
            :rtype: (Vec, float)

            
        """
        v0 = self.edges[index-1].vec
        v1 = self.edges[index].vec
        bisec =  Vec.bisector(v0,v1).cross(self._basis.z_axis)
        return (bisec, bisec.angle(v1))
        
       
        
    def rotated_to_min_bounds(self, divs = 4 , levels = 2, min_a = 0, max_a =.5 * math.pi ):
        """ Creates a copy of a polygon rotated to its best-fit bounding box.
        
            :param divs: Number of divisions of rotation per level.
            :type divs: int
            :param levels: Number of iterations.
            :type levels: int
            :param min_a: Minimum angle of rotation.
            :type min_a: float
            :param max_a: Maximum angle of rotation
            :type max_a: float
            :result: Polygon rotated to minimum bounds.
            :rtype: PGon
            
            
        """
        from .dc_xform import Xform
    
        delta_a = (max_a - min_a) / divs

        t_list = []

        # make a copy and rotate into initial position
        t = copy.deepcopy(self)
        xf = Xform.rotation(angle = (min_a - delta_a))
        t._verts = [v * xf for v in t._verts]


        # make transform for incremental rotations
        xf = Xform.rotation(angle = delta_a)

        for i in range(divs+1):
            t._verts = [v * xf for v in t._verts]
            b_area = t.bounds.dim_x * t.bounds.dim_y
            t_list.append([min_a + i*delta_a,b_area])

        min_vals = min(t_list, key=lambda s: (s[1]))
#        print "Iteration :", levels
#        print t_list
#        print "Minimum values : ",min_vals

        if levels == 0 :
            t = copy.deepcopy(self)
            xf = Xform.rotation(angle = min_vals[0])
            t._verts = [v * xf for v in t._verts]
            return t
        else:
            min_a = min_vals[0] - delta_a
            max_a = min_vals[0] + delta_a
            levels -= 1
            return self.rotated_to_min_bounds(divs, levels, min_a, max_a)



    def eval(self,t):
        """| Evaluates this polygon at the specified parameter t.
           | A t-value of 0 will result in a point coincident with PGon.pts[0].
           | A t-value of 1 will result in a point coincident with PGon.pts[-1].
           
           
           :param t: A decimal number between [0:1].
           :type t: float
           :result: Point on PGon.
           :rtype: Point
           
           ::
           
                my_pgon.eval(0.5)
                
        """
        if t > 1 : t = t%1.0
        if t < 0 : t = 1.0 - abs(t)%1.0
        if t == 0.0 or t == 1.0 : return self.pts[0]
        for n, ival in enumerate(Interval()//len(self)):
            if t in ival:
                pa = self.pts[n]
                try:
                    pb = self.pts[n+1]
                except:
                    pb = self.pts[0]
                return Point.interpolate(pa,pb,ival.deval(t))


    def near(self, p):
        """ Returns a tuple of the closest point to a given PGon, the index of the closest segment and the distance from the Point to the near Point.
       
            :param p: Point to look for a near Point on the PGon.
            :type p: Point
            :result: Nearest point on the PGon, index of the segment of this PGon on which this Point lies, the t-value along this segment, and the distance from the given Point.
            :rtype: (Point, integer, float, float)
            
            ::
            
                my_pgon.near(Point(0,0,0))
        """
        npts = [seg.near(p) for seg in self.edges]
        npts = [(tup[0],tup[1],tup[2],n) for n,tup in enumerate(npts)] # add index
        npts.sort(key=lambda tup: tup[2])
        return (npts[0][0],npts[0][3],npts[0][1],npts[0][2])

    def near_pt(self, p):
        """ Returns the closest point to a given PGon.
       
            :param p: Point to look for a near Point on the PGon.
            :type p: Point
            :result: Near point on PGon.
            :rtype: Point
            
            ::
            
                my_pgon.near_pt(Point(0,0,0))
        """
        return self.near(p)[0]

    def __repr__(self): return "pgon[{0}v]".format(len(self._verts))
    
    def basis_applied(self):
        """ Returns a new PGon with basis applied.
        
            :result: PGon with basis applied.
            :rtype: PGon
            
        """
        
        clone = super(PGon,self).basis_applied()
        clone.basis = CS()
        return clone

    def basis_stripped(self):
        """ Returns a new PGon with basis stripped.
        
            :result: PGon with basis stripped.
            :rtype: PGon
            
        """
        
        clone = super(PGon,self).basis_stripped()
        clone.basis = CS()
        return clone


    def inflate(self, t=0.5):
        """| Returns a polygon inscribed inside this one.
           | Each vertex of the returned polygon will lie on the midpoint of one of this polygon's edges.
           | Optionally, you may set the t 0->1
           
           :param t: A decimal number between [0:1].
           :type t: float
           :result: A polygon inscribed of this one.
           :rtype: PGon
           
           ::
           
                my_pgon.inflate()
        """
        
        ipts = [Vec.interpolate(self._verts[n],self._verts[n-1],t) for n in range(len(self._verts))]
        return PGon(ipts,self._basis)
    
    
    def offset(self, dist, flip=False):
        """| Returns a polygon offset from this one.
           
           :param dist: A distance to offset the polygon.
           :type dist: float
           :result: A polygon offset from this one.
           :rtype: PGon
           
           ::
           
                my_pgon.offset()
        """
        from .dc_intersection import Intersector
        
        segs = []
        for i in range(len(self.pts)):
        
            bisec, theta  = self.angle_bisector(i)
            if theta < math.pi/2: off_len = dist/math.sin(theta)
            else: off_len = dist/math.cos(theta-math.pi/2)

            if not flip: segs.append(Segment(self.pts[i], self.pts[i] + bisec.normalized(off_len)))
            else: segs.append(Segment(self.pts[i], self.pts[i] - bisec.normalized(off_len)))
        
        xsec = Intersector()
        for n in range(len(segs)):
            if xsec.intersect(segs[n-1],segs[n]):
                raise GeometricError("The offset value is to high")
                
        return PGon([self._basis.deval(seg.ept) for seg in segs],self._basis)
    
    

    def contains_pt(self, pt,tolerance=EPSILON):
        """ Tests if this polygon contains the given point. The given point must lie on the plane of this polygon.
        
            :param pt: Point to test containment in PGon.
            :type pt: Point
            :param tolerance: A decimal number.
            :type tolerance: float
            :result: Boolean Value.
            :rtype: bool
            
            ::
            
                my_pgon.constains_pt(Point(0,0,0))
            
        """
        
        pt = Point(self._basis.deval(pt))
        if abs(pt.z) > tolerance : 
            warnings.warn("Given point does not lie on the same plane as this polygon.")
            return False
        pt.z = 0
        if not pt in self.bounds : return False

        #TODO: maybe move this intersection routine to intersection class
        
        for seg in self.edges:
            ln = Segment(seg.spt,pt)
            if ln.vec.length2 < tolerance: return True
            if ln.vec.is_coincident(seg.vec) and ln.vec.length2 <= seg.vec.length2 : return True
        
        icnt = 0
        ray = Ray(pt,Vec(0,1))
        for n in range(len(self._verts)):
            try:
                seg = Segment(Point(self._verts[n]),Point(self._verts[n+1]))
            except:
                seg = Segment(Point(self._verts[n]),Point(self._verts[0]))

            if seg.is_parallel(ray) : continue
            try:
                slope = (seg.ept.y - seg.spt.y) / (seg.ept.x - seg.spt.x)
                cond1 = (seg.spt.x <= pt.x) and (pt.x <= seg.ept.x)
                cond2 = (seg.ept.x <= pt.x) and (pt.x <= seg.spt.x)
                above = (pt.y < slope * (pt.x - seg.spt.x) + seg.spt.y)
                if ((cond1 or cond2) and above ) : icnt += 1
            except:
                pass

        return icnt%2!=0

    def overlaps(self, other) :
        """ Tests for overlap with another polygon. Returns true if these two polygons share a common plane, and if they overlap or if one is completely contained within another.
        
            :param other: Another polygon,
            :type other: PGon
            :result: Boolean Value.
            :rtype: bool
            
            ::
            
                my_pgon2=PGon([Point(1,1,0), Point(1,2,0), Point(2,2,0), Point(2,1,0)])
                
                my_pgon.overlaps(my_pgon2)
            
        """
        if not self._basis.xy_plane.is_coplanar(other.basis.xy_plane): return False

        for pt in other.pts: 
            if self.contains_pt(pt) : return True

        for pt in self.pts: 
            if other.contains_pt(pt) : return True

        return False

    @staticmethod
    def triangle(pt_a,pt_b,pt_c):
        """ Constructs a triangular polygon from three points. Resulting PGon will have a basis at the centroid of the three points, with the x_axis pointing toward pt_a.
        
            :param pt_a: First Point.
            :type pt_a: Point
            :param pt_b: Second Point.
            :type pt_b: Point
            :param pt_c: Third Point.
            :type pt_c: Point
            :result: Triangular polygon.
            :rtype: PGon
            
            ::
            
                PGon.triangle(Point(0,0,0), Point(1,2,3), Point(4,5,6))
        
        """
        cen = Point.centroid([pt_a,pt_b,pt_c])
        cs = CS(cen,Vec(cen,pt_a),Vec(cen,pt_b))
        pts = [cs.deval(pt) for pt in [pt_a,pt_b,pt_c]]
        return PGon(pts,cs)
        #pln = Plane.from_pts(pt_a,pt_b,pt_c)
        

    @staticmethod
    def rectangle(cpt, w, h):
        """ Constructs a rectangle based on a center point, a width, and a height.
        
            :param cpt: Center point of a rectangle.
            :type cpt: Point
            :param w: Width of a rectangle.
            :type w: float
            :param h: Height of a rectangle.
            :type h: float
            :returns: Rectangle (PGon object). 
            :rtype: PGon
            
            ::
            
                PGon.rectangle(Point(0,0,0), 5, 10)
        """ 
        w2 = w/2.0
        h2 = h/2.0
        basis = CS(cpt)
        return PGon([Point(-w2,-h2),Point(w2,-h2),Point(w2,h2),Point(-w2,h2)],basis)

    @staticmethod
    def doughnut(cs,radius_interval,angle_interval=Interval(0,math.pi*2),res=20):
        """ Constructs a doughnut based on a center point, two radii, and optionally a start angle, sweep angle, and resolution.
        
            :param cpt: Center point of a rectangle.
            :type cpt: Point
            :param radius_interval: Radii interval.
            :type radius_interval: Interval
            :param angle_interval: Angle interval.
            :type angle_interval: Interval
            :param res: Doughnut resolution.
            :type res: float
            :returns: Doughnut object. 
            :rtype: PGon
            
        """ 
        try:
            cs.eval(0,0)
        except:
            cs = CS(cs)
        pts = []
        rad_a = radius_interval.a
        rad_b = radius_interval.b
        if rad_a == 0 : rad_a = EPSILON
        if rad_b == 0 : rad_b = EPSILON
        if rad_a == rad_b : rad_b += EPSILON
        for t in angle_interval.divide(res,True):pts.append(cs.eval_cyl(rad_a,t))
        for t in angle_interval.invert().divide(res,True):pts.append(cs.eval_cyl(rad_b,t))
        return PGon(pts)

class RGon(PGon):
    """
    A Regular Polygon Class
    """
    subclass_attr = ['_edges'] # this list of props is unset any time this HasPts object changes

    def __init__(self, num_of_sides, radius=None, basis=None, edge_length=None, apothem=None):
        """ RGon Constructor.
            
            :param num_of_sides: Number of sides of polygon.
            :type num_of_sides: int
            :param radius: Distance from center to vertices.
            :type radius: float
            :param basis: Basis.
            :type basis: Basis.
            :param edge_length: Length of polygon edge.
            :type edge_length: float
            :param apothem: Distance from center to midpoint of sides.
            :type apothem: float
            :result: Polygon.
            :rtype: RGon
            
            ::
            
                my_rgon=RGon(num_of_sides=5, radius=2.0, edge_length=3.5)
                
                OR
                
                my_rgon2=RGon(num_of_sides=4, radius=3, apothem=4.5)
        
        """ 
        self._in_init = True
        if num_of_sides < 3 : raise GeometricError("Cannot create a regular polygon with fewer than three sides.")
        if radius is None and edge_length is None and apothem is None : raise GeometricError("You must specify one and only one of the following: radius, edge length, apothem")
        if radius is not None and edge_length is not None  and apothem is not None : raise GeometricError("You must specify one and only one of the following: radius, edge length, apothem")
        #TOOD: test that one and only one have been set
        self._nos = num_of_sides
        
        if basis is None : basis = CS()
        
        if edge_length is not None: 
            if edge_length <= 0 : raise GeometricError("edge_length must be greater than zero")
            self._edge_length = edge_length
            self._radius = edge_length / (2.0 * math.sin(math.pi/self._nos))
        elif apothem is not None: 
            if apothem <= 0 : raise GeometricError("apothem must be greater than zero")
            self._apothem = apothem
            self._radius = apothem / math.cos(math.pi/self._nos)
        elif radius is not None: 
            if radius <= 0 : raise GeometricError("radius must be greater than zero")
            self._radius = radius
        else:
            raise GeometricError("You must specify one and only one of the following: radius, edge length, apothem")

        step = math.pi*2.0/num_of_sides
        verts = [Point( self.radius * math.cos(step*n), self.radius * math.sin(step*n))  for n in range(num_of_sides) ]

        super(RGon,self).__init__(verts, basis)
        self._in_init = False


    @property
    def radius(self):
        """ Returns radius of RGon.
        
            :result: Radius of polygon.
            :rtype: float
            
        """
        return self._radius

    @property
    def num_of_sides(self):
        """ Returns number of sides of the RGon.
        
            :result: Number of sides of polygon.
            :rtype: int
        
        """
        return self._nos

    @property
    def area(self):
        """ Returns the area of the polygon.
        
            :result: Area of the polygon.
            :rtype: float
            
            ::
            
                my_rgon.area
                
        """
        try:
            return self._area
        except:
            self._area = 0.5 * self._nos * math.sin(math.pi*2.0/self._nos) * (self.radius ** 2)
            return self._area

    @property
    def apothem(self):
        """ The distance from the center to the midpoint of any side.
        
            :result: Apothem of the polygon.
            :rtype: float
            
            ::
            
                my_rgon.apothem
                
        """
        try:
            return self._apothem
        except:
            mpt = Point.interpolate(self.pts[0],self.pts[1])
            self._apothem = mpt.distance(self.centroid)
            #self._apothem = Vec.interpolate(self._verts[0],self._verts[1]).length
            return self._apothem

    @property
    def edge_length(self):
        """ The length of any edge.
            
            :result: The length of any edge.
            :rtype: float
            
            ::
            
                my_rgon.edge_length
                
        """
        try:
            return self._edge_length
        except:
            self._edge_length = 2 * self.radius * math.sin(math.pi/self._nos)
            return self._edge_length

    @property
    def circle_inscr(self):
        """ Returns the inscribed circle of this RGon.
        
            :result: Inscribed circle.
            :rtype: Circle
            
            ::
            
                my_rgon.circle_inscr
            
        """
        return Circle(self._basis.xy_plane, self.radius)
 
    @property
    def circle_cirscr(self):
        """ Returns the circumscribed circle of this RGon.
        
            :result: Circumscribed circle.
            :rtype: Circle
            
        """
        return Circle(self._basis.xy_plane, self.apothem)
 
    @property
    def interior_angle(self):
        """ Returns the interior angle of this RGon.
        
            :result: Interior angle in radians.
            :rtype: float
            
            ::
            
                my_rgon.interior_angle
        """
        try:
            return self._iangle
        except:
            self._iangle = (self._nos-2) * math.pi/self._nos
            return self._iangle
        
    def append(self,pts):
        raise GeometricError("I can't even. You can't append vertices to a RGon!")
        
        
    def __repr__(self): return "rgon[{0}]".format(self.num_of_sides)

    def inflate(self, t=0.5):
        """ Returns a regular polygon inscribed inside this one while maintaining the same number of sides.
            Optionally, you may set parameter t 0->1
           
            :param t: A decimal number between [0:1].
            :type t: float
            :result: An regular inscribed polygon.
            :rtype: RGon
            
            ::
            
                my_rgon.inflate(t)
            
        """
        pt = Point.interpolate(self.pts[0],self.pts[1],t)
        o = self._basis.origin
        x = Vec(o,pt)
        y = self._basis.z_axis.cross(x)
        return RGon(self._nos, basis = CS(o,x,y), radius = o.dist(pt))

    def deflate(self, t=0.5):
        """ Returns a regular polygon that circumscribes this one while maintaining the same number of sides.
            Optionally, you may set parameter t 0->1
           
            :param t: A decimal number between [0:1].
            :type t: float       
            :result: a regular polygon circumscribing this one.
            :rtype: RGon
            
            ::
            
                my_rgon.deflate(t)
            
        """        
        pt_a = Point.interpolate(self.pts[0],self.pts[1],t)
        pt_b = Point.interpolate(self.pts[-1],self.pts[0],t)
        o = self._basis.origin
        x = Vec(o,pt_a)
        y = self._basis.z_axis.cross(x) 
        if (t == 0.5):
            return RGon(self._nos, basis = CS(o,x,y), apothem = self.radius) 
        vec_perp = (Vec(pt_b, pt_a).cross(self._basis.z_axis)).normalized()
        return RGon(self._nos, basis = CS(o,x,y), apothem = Vec(o,self.pts[0]).dot(vec_perp))
  

    def to_pgon(self):
        """ Returns the PGon equivalent of this RGon.
        
            :result: A polygon.
            :rtype: PGon
            
            ::
            
                my_rgon.to_pgon()
        """
        return PGon(self._verts,self._basis)

    def _vertices_changed(self):
        if not self._in_init : raise GeometricError("I cannot manipulate the vertices of this PGon.  Convert to PGon using RGon.to_pgon()")

    @staticmethod
    def from_edge(segment,num_of_sides,normal=Vec(0,0,1)):
        """ Constructs a regular polygon given a line segment describing one edge. The side of the edge that the center of the resulting polygon falls is determined by taking the cross product of the given edge vector and the given normal vector.
            
            :param segment: Edge of polygon.
            :type segment: Segment
            :param num_of_sides: Number of sides of polygon.
            :type num_of_sides: int
            :param normal: Vector normal to edge.
            :type normal: Vec
            :result: Regular polygon.
            :rtype: RGon
            
            ::
            
                new_rgon=RGon.from_edge(Segment.by_coords2d(0,0,0,5),5, Vec(0,1,0))
            
        """
        apothem = segment.length / (2.0 * math.tan(math.pi/num_of_sides))
        cpt = segment.midpoint + segment.vec.cross(normal).normalized(apothem)
        cs = CS(cpt,Vec(cpt,segment.spt),segment.vec.cross(normal))
        return RGon(num_of_sides,apothem=apothem, basis=cs)