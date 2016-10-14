from decodes.core import *
from . import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon
if VERBOSE_FS: print("intersection.py loaded")



class Intersector(object):
    """
    Intersection results class.
    """
    def __init__(self):
        """Intersection Constructor.
        
            :result: Intersection Object.
            :rtype: None
            
        """
        self._geom = []
        self.log = None
        self.tol = EPSILON

    def __getitem__(self,slice):
        """Returns intersection geometry at given index.
        
            :param slice: Index of intersection geometry.
            :type slice: int
            :result: Intersection geometry.
            :rtype: Intersector
            
        """
        return self._geom[slice]

    @property
    def results(self):
        """Returns list of intersection geometries. 
        
            :result: List of intersection geometries.
            :rtype: [Intersector]
            
        """
        return self._geom

    def append(self,item):
        """ Appends item to list of intersection geometries.
        
            :result: Appended item to list of intersection geometries.
            :rtype: None
            
        """
        
        #ATTENTION! This function doesn't really make sense for intersections.
        
        self._geom.append(item)

    def clear(self):
        """Clears all intersection geometries from results list.
        
            :result: Empty list of intersections.
            :rtype: None
            
        """
    
        del self._geom[:]
        self.log = None

    def __len__(self): 
        """Returns the length of the list of intersection geometries.
        
            :result: Length of list.
            :rtype: int
            
        """
        
        return len(self._geom)

    def of(self,a,b,**kargs):
        """| Pass in two pieces of decodes geometry (a & b), and i'll have a go at intersecting them.
           | Results will be stored in this xsec object.
           | Extras (such as distance to intersection points) will be assigned as attributes to this xsec object.
           | Function returns success, True or False        
           
           :param a: First geometry to intersect. May be any decodes geometry.
           :type a: Geometry
           :param b: Second geometry to intersect. May be any decodes geometry.
           :type b: Geometry
           :param \**kargs: Two geometries to intersect.
           :type \**kargs: Geometry, Geometry
           :result: Boolean Value
           :rtype: bool
            
        """
        
        return self.intersect(a,b,**kargs)

    def intersect(self,a,b,**kargs):
        """| Pass in two pieces of decodes geometry (a & b), and I'll have a go at intersecting them.
           | Results will be stored in this xsec object.
           | Extras (such as distance to intersection points) will be assigned as attributes to this xsec object.
           | Function returns success, True or False.
        
           :param a: First geometry to intersect. May be any decodes geometry.
           :type a: Geometry
           :param b: Second geometry to intersect. May be any decodes geometry.
           :type b: Geometry
           :param \**kargs: Two geometries to intersect.
           :type \**kargs: Geometry, Geometry
           :result: Boolean Value.
           :rtype: bool
        
        """
        self.clear()
        
        # a whitelist of types we support
        good_types = [Plane, Circle, PGon, RGon, Line, Ray, Segment, PLine, Arc]
        bad_types = [Bounds,Color,Interval,Point,Xform]
        if any([type(obj) in bad_types for obj in [a,b]]) : raise NotImplementedError("It isn't possible to intersect the following types: %s"%([typ.__name__ for typ in bad_types]))
        if any([type(obj) not in good_types for obj in [a,b]]) : raise NotImplementedError("I can only intersect the following types: %s"%([typ.__name__ for typ in good_types]))
        # sort by order found in whitelist collection
        a,b = sorted( [a,b], key = lambda obj: good_types.index(type(obj)) )
        type_a, type_b = type(a), type(b)
                
        # INTERSECTIONS WITH A PLANE
        if type_a == Plane:
            plane, other = a,b

            if type_b == Vec : return self._ray_plane(Ray(Point(),other),plane,**kargs)
            if type_b == Line : return self._line_plane(other,plane,**kargs)
            if type_b == Ray : return self._ray_plane(other,plane,**kargs)
            if type_b == Segment : return self._seg_plane(other,plane)
            if type_b == PLine : return self._pline_plane(other,plane)
            if type_b == Circle : return self._circle_plane(other,plane)
            if type_b == Arc : return self._arc_plane(other,plane)
            if type_b == Plane : return self._plane_plane(other,plane)
            
            raise NotImplementedError("I don't know how to intersect a Plane with a %s"%(type_other.__name__))

        # INTERSECTIONS WITH A CIRCLE
        if type_a == Circle:
            circ, other = a,b
            if type_b == Circle : return self._circle_circle(other,circ)
            if isinstance(other, LinearEntity) : return self._line_circle(other, circ)

        # INTERSECTIONS WITH A PGON
        if type_a == RGon or type_a == PGon:
            pgon, other = a,b
            if isinstance(other,LinearEntity) : return self._line_pgon(other,pgon,**kargs)

        # INTERSECTIONS WITH A LINE
        # last resort for Line-Line intersections
        if all(isinstance(item,LinearEntity) for item in [a,b]) : 
            return self._line_line(a,b)

        raise NotImplementedError("I don't know how to intersect a %s with a %s"%(type_a.__name__,type_b.__name__))


    def _pgon_plane(self,pgon,plane,**kargs):
        """ Intersects a Polygon with a Plane. Upon success, the Intersector.dist property will be set to the distance between line.spt and the point of intersection.
        
            :param line: Line to intersect.
            :type line: Line
            :param plane: Plane to intersect.
            :type plane: Plane
            :param ignore_backface: Boolean Value.
            :type ignore_backface: bool
            :result: Boolean Value.
            :rtype: bool
        
        
        
            .. warning:: This method has not been implemented.
        
        """
        # TODO
        return False

    def _line_pgon(self,line,pgon,**kargs):
        """ Intersects a  LinearEntity with a PGon. If the LinearEntity lies in the Plane of PGon, all Segments of intersection will be returned and Intersector.dist property will be set to 0. If the line and plane of PGon intersect at a Point, the Intersector.dist property to the distance between line.spt and the point of intersection. 
        TODO - once line_line_collinear is incorporated, this will be able to handle the case when the LinearEntity overlaps any of the PGon edges
    
        :param line: Line to intersect.
        :type line: Line
        :param pgon: Polygon to intersect.
        :type pgon: PGon
        :param ignore_backface: Boolean Value.
        :type ignore_backface: bool
        :result: Boolean Value.
        :rtype: bool
            
        """
        ignore_backface = False
        if "ignore_backface" in kargs: ignore_backface = kargs['ignore_backface']
    
        #first find intersection between LinearEntity and Plane of PGon
        xsec = Intersector()
        basis_success = xsec.of(pgon.basis.xy_plane,line,ignore_backface = ignore_backface)

        #if LinearEntity and Plane do not intersect
        if not basis_success:
            self.log = "LinearEntity does not intersect PGon.basis."
            return False

        #if LinearEntity lies in the Plane of PGon
        if pgon.basis.xy_plane.contains(line.spt) and pgon.basis.xy_plane.contains(line.spt+line.vec):
            self.log = "LinearEntity in Plane of PGon"
            self.dist = 0
            success = False
            results = [] #stores tuples (t-value, point) used to find intersecting segments
            if pgon.contains_pt(line.spt): 
                results.append((0,line.spt))
            #for each edge of PGon
            for edge in pgon.edges:
                #find intersection between LinearEntity and edge 
                xsec = Intersector()
                edge_success = xsec.of(line,edge)
                #if Line-Line intersection is successful
                if edge_success:
                    #add intersection to results
                    results.append((xsec.ta, xsec[0]))
            if type(line)==Segment and pgon.contains_pt(line.ept): 
                results.append((1,line.ept))
            #sort points by t-value along LinearEntity
            results = sorted(results)
            #find all segments between ordered pairs of points that lie in PGon
            for i in range(len(results)-1):
                seg = Segment(results[i][1],results[i+1][1])
                if pgon.contains_pt(seg.midpoint):
                    self.append(seg)
                    #return True if there is any segment that lies in the PGon
                    success = True
            return success
        
        #if LinearEntity intersects Plane of PGon at a Point
        self.log = "LinearEntity intersects Plane of PGon at a Point"
        #if Point is contained in the PGon
        if pgon.contains_pt(xsec[0]):
            #add point of intersection to results
            self.append(xsec[0])
            self.dist = xsec.dist
            return True
            
            
    def _line_plane(self,line,plane,**kargs):
        """ Intersects a Line with a Plane. Upon success, the Intersector.dist property will be set to the distance between line.spt and the point of intersection.
        
            :param line: Line to intersect.
            :type line: Line
            :param plane: Plane to intersect.
            :type plane: Plane
            :param ignore_backface: Boolean Value.
            :type ignore_backface: bool
            :result: Boolean Value
            :rtype: bool
            
        """
        ignore_backface = False
        if "ignore_backface" in kargs: ignore_backface = kargs['ignore_backface']
        
        if plane.contains(line.spt) and plane.contains(line.spt+line.vec):
            self.log = "LinearEntity lies in the Plane"
            self.dist = 0.0
            self.append(line)
            return True
        pln_norm = plane.normal
        line_vec = line.vec
        denom = pln_norm.dot(line_vec) # note, plane normal faces outward in the direction of the 'front' of the plane.  this may not be standard. 
        # pos denom indicates ray behind plane
        if ignore_backface and denom >= 0 : 
            self.log = "Backfaces ignored. LinearEntity lies behind Plane"
            return False 
        # denom of zero indicates no intersection
        if denom == 0 : 
            self.log = "No intersection"
            return False
        t = pln_norm.dot(plane.origin-line.spt) / denom
        self.dist = t # t < 0 indicates plane behind ray
        self.append(line.eval(t))
        self.log = "Intersection found."
        return True

        
    def _ray_plane(self,ray,plane,**kargs):
        """ Intersects a Ray with a Plane. Upon success the Intersector.dist property will be set to the distance between the ray.spt and the point of intersection.
        
            :param ray: Ray to intersect.
            :type ray: Ray
            :param plane: Plane to intersect.
            :type plane: Plane
            :param ignore_backface: Boolean Value.
            :type ignore_backface: bool
            :result: Boolean Value.
            :rtype: bool
            
        """
        ignore_backface = False
        if "ignore_backface" in kargs: ignore_backface = kargs['ignore_backface']
    
        xsec = Intersector()
        line_success = xsec._line_plane(ray,plane,ignore_backface = ignore_backface)
        if not line_success : 
            self.log = xsec.log
            return False
        if xsec.dist < 0 : 
            self.log = "Ray is directed away from Plane"
            return False
        self._geom = xsec._geom
        self.dist = xsec.dist
        self.log = "Intersection found."
        return True

        
    def _seg_plane(self,seg,plane):
        """ Intersects a Segment with a Plane. Upon success the Intersector.dist property will be set to the distance between the seg.spt and the point of intersection.
            
            :param seg: Segment to intersect.
            :type seg: Segment
            :param plane: Plane to intersect.
            :type plane: PLane
            :result: Boolean Value
            :rtype: bool
            
        """
    
        xsec = Intersector()
        line_success = xsec._line_plane(seg,plane,ignore_backface = False)
        if not line_success : 
            self.log = xsec.log
            return False
        if xsec.dist < 0 : 
            self.log = "While pointing in the right direction, this Segment does cross Plane"
            return False
        if xsec.dist > seg.length : 
            self.log = "Segment points in the wrong direction, and does not cross Plane"
            return False
        self._geom = xsec._geom
        self.dist = xsec.dist
        self.log = "Intersection found."
        return True

        
    def _pline_plane(self,pline,plane):
        """ Intersects a Polyline with a Plane. 
        
            :param pline: Polyline to intersect.
            :type pline: PLine
            :param plane: Plane to intersect.
            :type plane: Plane
            :result: Boolean value.
            :rtype: bool
            
        """
        self.edges = []
        self.verts = []
        xsec = Intersector()
        pts = pline.pts
        for pt in pts:
            pt.side = 0
            line = Line(plane.origin, plane.normal)
            t = line.near(pt)[1]
            if t < 0 : pt.side = -1
            if t > 0 : pt.side = 1

        ret = False
        for n in range(len(pts)):
            if n< len(pts)-1 and pts[n].side != pts[n+1].side and pts[n].side !=0 and pts[n+1].side !=0:
                if xsec.of(pline.edges[n],plane):
                    self.append(xsec[0])
                    self.edges.append(n)
                    self.verts.append(False)
                    ret = True
            if pts[n].side == 0 :
                #if self.log is None: self.log = ""
                #self.log += "Found an intersection at a polyline vertex %s\n"%(n)
                self.append(pts[n])
                self.edges.append(False)
                self.verts.append(n)
                ret = True

        return ret

    def _plane_plane(self,pln_a,pln_b):
        """ Intersects two planes.
        
            :param pln_a: First plane to intersect.
            :type pln_a: Plane
            :param pln_b: Second plane to intersect.
            :type pln_b: Plane
            :result: Boolean value.
            :rtype: bool
            
        """
        #TODO - return plane if coincident or coplanar
        if pln_a.normal.is_parallel(pln_b.normal) :
            self.log = "Planes are parallel, no intersection found."
            return False
        n1, n2 = pln_a.normal, pln_b.normal
        n1dotn2, r1, r2 = n1.dot(n2), n1.dot(pln_a.origin), n2.dot(pln_b.origin)
        vec = n1.cross(pln_b.normal)
        denom = 1-n1dotn2*n1dotn2
        c1 = (r1 - n1dotn2*r2)/denom
        c2 = (r2 - n1dotn2*r1)/denom
        p0 = n1*c1 + n2*c2
        self.append(Line(p0, vec))    
        return True
        """
        vec = pln_a.normal.cross(pln_b.normal)    
        ldir = pln_b.normal.cross(vec)
        denom = pln_a.normal.dot(ldir)
        tvec = pln_a.origin - pln_b.origin
        t = pln_a.normal.dot(tvec) / denom
        pt = pln_b.origin + ldir * t   
        self.append( Line(pt,vec) )
        return True
        """

    def _circle_plane(self,circ,plane):
        """ Intersects a circle and a plane.
        
            :param circ: circle to intersect.
            :type circ: Circle
            :param pln: plane to intersect.
            :type pln: Plane
            :result: Boolean value.
            :rtype: bool
            
        """
        xsec = Intersector()
        plane_success = xsec._plane_plane(circ,plane)
        if not plane_success : 
            self.log = xsec.log
            return False
        
        self.line = xsec[0] # add plane-plane intersection line
        npt, t, dist = self.line.near(circ.origin)       
        R = circ.rad
        # dist == R within set tolerance
        if (abs(dist-R) < self.tol):
            self.log = "One intersection point found"
            self.append(npt)
            return True   
        if dist > R:
            self.log = "No intersection found"
            return False   
        if dist < R:
            self.log = "Two intersection points found"
            factor = math.sqrt(R**2-dist**2)/self.line.vec.length
            self.append(npt-self.line.vec*factor)
            self.append(npt+self.line.vec*factor)
            return True
        """
        x_vec = Vec(circ.origin,npt)
        if x_vec.length < self.tol : x_vec = Vec(circ.origin,self.line.pt+self.line.vec)
        if x_vec.length < self.tol : x_vec = Vec(circ.origin,self.line.pt)

        cs = CS(circ.origin,x_vec,circ.normal.cross(x_vec))
        p0 = cs.deval(self.line.spt)
        p1 = cs.deval(self.line.spt+self.line.vec)

        # circle-line intersection
        # TODO: move this to its own method
        dx = p1.x - p0.x
        dy = p1.y - p0.y
        dr = math.sqrt(dx**2+dy**2)
        d = (p0.x*p1.y) - (p1.x*p0.y)

        discr = circ.rad**2 * dr**2 - d**2
        if discr < 0 :
            self.log = "Circle does not intersect with given Plane"
            return False
        elif discr == 0:
            self.log = "Circle intersects Plane at a tangent Point"
            self.append(npt)
            return True
        elif discr > 0:
            self.log = "Circle intersects Plane at two Points"
            discr2 = math.sqrt(discr)
            dr2 = dr**2
            def sgn(x):
                if x > 0 : return -1
                return 1

            x0 = (d * dy + sgn(dy) * dx * discr2) / dr2
            x1 = (d * dy - sgn(dy) * dx * discr2) / dr2
            y0 =(-d * dx + abs(dy) * discr2) / dr2
            y1 =(-d * dx - abs(dy) * discr2) / dr2

            self.append(cs.eval(x0,y0))
            self.append(cs.eval(x1,y1))
            return True
        return False
        """
        
    def _arc_plane(self,arc,plane):
        xsec = Intersector()
        circ = Circle(arc.basis.xy_plane,arc.rad)
        circle_success = xsec._circle_plane(circ,plane)
        if not circle_success : 
            self.log = xsec.log
            self.log = "Plane failed to intersect with Circle derived from given Arc: "+xsec.log
            return False
        else:
            self.angs = []
            for pt in xsec.results:
                ang = arc.basis.deval_cyl(pt)[1]
                '''
                n+=1
                vec = Vec(arc.origin,pt)
                ang = vec.angle(arc.basis.x_axis)
                if ang == 0:
                    self.append(pt)
                    continue
                if not CS(arc.origin,arc.basis.x_axis,vec).z_axis.is_coincident(arc.basis.z_axis):
                    # look here!
                    pass
                    ang = math.pi*2 - ang
                '''

                if ang <= arc.angle:             
                    self.append(pt)
                    self.angs.append(ang)
                else:
                    self.log = "One of the intersection Points do not fall within sweep angle of this Arc: pt_angle={0} arc_angle={1}".format(ang,arc.angle)
        
        if len(self)==0:
            self.log = "Intersection Points do not fall within sweep angle of this Arc"

        return len(self)>0 

        
    def _line_circle(self, line, circ): 
        """ Intersects a LinearEntity with a Circle. 
        
            :param circ: circle to intersect.
            :type circ: Circle
            :param pln: LinearEntity to intersect.
            :type pln: Line, Seg or Ray
            :result: Boolean value.
            :rtype: bool
            
        """
        xsec = Intersector()
        if not xsec.of(line, circ.plane): 
            self.log = "Line and Plane of Circle don't intersect"
            return False
        if type(xsec[0])==Point:
            self.log = "Line and Plane of Circle intersect at one point"
            pt, self.t = xsec[0], xsec.dist
            if not circ.contains(pt) and not (circ.origin.distance(pt) == R):
                return False
            if type(line) == Ray and self.t < 0.0: return False
            if type(line) == Segment and ((self.t < 0.0) or (self.t > 1.0)): return False
            self.log = "Intersection found"
            self.append(pt)
            return True
        self.log = "Line lies in Plane of Circle"
        R, center = circ.rad, circ.origin
        npt, t, dist = Line(line.spt, line.vec).near(center) #projection onto the extended line
        #if dist is "equal" to R
        if (abs(dist-R) < self.tol):
            self.log = "Case of one possible intersection point"
            self.t = t
            if type(line) == Ray and self.t < 0.0: return False
            if type(line) == Segment and ((self.t < 0.0) or (self.t > 1.0)): return False
            self.append(npt)
            return True
        if dist > R:
            self.log = "Case of no intersection point"
            return False
        if dist < R:
            self.log = "Case of two possible intersection points"
            factor = math.sqrt(circ.rad**2-dist**2)/line.vec.length
            self.ta, self.tb = t - factor, t + factor
            pa, pb = npt-line.vec*factor, npt+line.vec*factor 
            if type(line) == Ray:
                if self.ta >= 0.0: self.append(pa)
                if self.tb >= 0.0: self.append(pb)
                if len(self) == 0: return False 
                return True
            if type(line) == Segment:
                if (self.ta >= 0.0 and self.ta <= 1.0): self.append(pa)
                if (self.tb >= 0.0 and self.tb <= 1.0): self.append(pb)
                if len(self) == 0: return False
                return True

                
    def _line_line(self,ln_a,ln_b):
        """Intersects two lines, returning False for non-intersecting lines but 
        calculates/records the shortest segment between the two lines if that exists
            
            :param ln_a: First line to intersect.
            :type ln_a: Line
            :param ln_b: Second line to intersect.
            :type ln_b: Line
            :result: Boolean value
            :rtype: bool            
        """    
        if ln_a.is_collinear(ln_b):
            self.log = "Lines are collinear, attempting to find intersection"
            return False
            #return self._line_line_collinear(ln_a,ln_b) #TODO
        if ln_a.is_parallel(ln_b, self.tol):
            self.log = "Lines are parallel, no intersection found."
            return False   
        p0, v1 = ln_a.spt, ln_a.vec
        q0, v2 = ln_b.spt, ln_b.vec       
        if v1.length2 < self.tol or v2.length2 < self.tol: 
            self.log("Length of one of the lines is below the tolerance")
            return False
        v_q0p0 = Vec(p0-q0)
        v1dotv2 = v1.dot(v2)
        denom = - v1.length2*v2.length2 + v1dotv2*v1dotv2
        self.ta = (v2.length2*(v1.dot(v_q0p0)) - v1dotv2*(v2.dot(v_q0p0)))/denom
        self.tb = (v1dotv2*(v1.dot(v_q0p0)) - v1.length2*(v2.dot(v_q0p0)))/denom
        pa = ln_a.eval(self.ta)
        pb = ln_b.eval(self.tb)   
        
        if pa.is_equal(pb, self.tol) :
            if type(ln_a) == Ray and self.ta < 0.0 : return False
            if type(ln_b) == Ray and self.tb < 0.0 : return False  
            if type(ln_a) == Segment and (self.ta < 0.0 or self.ta > 1.0) : return False
            if type(ln_b) == Segment and (self.tb < 0.0 or self.tb > 1.0) : return False
            self.log = "Intersection found."
            self.append(pa)
            return True
        else: 
            self.log = "No intersection found, recording shortest Segment between these two lines."
            self.append(Segment(pa,pb))
            return False
 
 
    def _line_line_SAVE(self,ln_a,ln_b):
        """Intersects two lines, returning False for any pair of non-intersecting lines
            
            :param ln_a: First line to intersect.
            :type ln_a: Line
            :param ln_b: Second line to intersect.
            :type ln_b: Line
            :result: Boolean value
            :rtype: bool
            
        """
        #first three if blocks deal with special cases (lines are coplanar, collinear, parallel)
        if not ln_a.is_coplanar(ln_b, self.tol):
            self.log = "Lines don't lie on same plane, no intersection found."
            return False       
        if ln_a.is_collinear(ln_b):
            self.log = "Lines are collinear, attempting to find intersection"
            return False
            #return self._line_line_collinear(ln_a,ln_b) #TODO
        if ln_a.is_parallel(ln_b, self.tol):
            self.log = "Lines are parallel, no intersection found."
            return False
        
        #Everything that follows deals with the case where the intersection, if there is any, is a point
        p0, v1 = ln_a.spt, ln_a.vec
        q0, v2 = ln_b.spt, ln_b.vec    
        if v1.length2 < self.tol or v2.length2 < self.tol: 
            self.log("Length of one of the lines is below the tolerance")
            return False
        n_vec = v1.cross(v2)
        v2_perp = v2.cross(n_vec)
        v_q0p0 = Vec(p0-q0)
        #parameter of intersection along ln_a
        self.ta = -v2_perp.dot(v_q0p0)/(v2_perp.dot(v1))
        v1_perp = v1.cross(n_vec)
        #parameter of intersection along ln_b
        self.tb = v1_perp.dot(v_q0p0)/(v1_perp.dot(v2))
        if type(ln_a) == Ray and self.ta < 0.0 : return False
        if type(ln_b) == Ray and self.tb < 0.0 : return False  
        if type(ln_a) == Segment and (self.ta < 0.0 or self.ta > 1.0) : return False
        if type(ln_b) == Segment and (self.tb < 0.0 or self.tb > 1.0) : return False
        self.log = "Intersection found."
        self.append(ln_a.eval(self.ta))
        return True
 
    
    def _line_line_collinear(self,ln_a,ln_b):
        """Intersects two lines that are collinear
            
            :param ln_a: First line to intersect.
            :type ln_a: Line
            :param ln_b: Second line to intersect.
            :type ln_b: Line
            :result: Boolean value
            :rtype: bool
            
            
            TODO - implemented, not yet incorporated
        """
 
        if not ln_a.is_collinear(ln_b):
            self.log = "Lines are not collinear"
            return False
        if type(ln_a) == Line:
            self.append(ln_b)
            return True
        if type(ln_b) == Line:
            self.append(ln_a)
            return True
        if type(ln_a) == Ray and type(ln_b) == Ray:
            #if rays overlap
            if ln_a.contains(ln_b.spt) or ln_b.contains(ln_a.spt):
                #if rays have same direction
                if ln_a.vec.is_coincident(ln_b.vec):
                    if ln_a.near(ln_b.spt)[1] > 0: self.append(Ray(ln_b.spt, ln_b.vec))
                    if ln_b.near(ln_a.spt)[1] >= 0: self.append(Ray(ln_a.spt, ln_a.vec))
                else:
                    return Segment(ln_a.spt, ln_b.spt)
                return True
            else:
                self.log = "Rays don't overlap"
                return False    
        if type(ln_a) == Ray and type(ln_b) == Segment:
            if ln_a.contains(ln_b.spt) and ln_a.contains(ln_b.ept):
                self.append(ln_b)
                return True
            if ln_a.contains(ln_b.spt): 
                self.append(Segment(ln_b.spt, ln_a.spt))
                return True
            if ln_a.contains(ln_b.ept): 
                self.append(Segment(ln_a.spt, ln_b.ept))
                return True
            self.log = "Ray and Segment don't overlap"    
            return False
        if type(ln_a) == Segment and type(ln_b) == Ray:
            if ln_b.contains(ln_a.spt) and ln_b.contains(ln_a.ept): 
                self.append(ln_a)
                return True
            if ln_b.contains(ln_a.spt):
                self.append(Segment(ln_a.spt, ln_b.spt))
                return True
            if ln_b.contains(ln_a.ept): 
                self.append(Segment(ln_b.spt, ln_a.ept))
                return True
            self.log = "Segment and Ray don't overlap" 
            return False
        if type(ln_a) == Segment and type(ln_b) == Segment:
            if not ln_a.is_overlapping(ln_b):
                self.log = "Segments don't overlap"
                return False
            ln_ext = ln_a.to_line()
            pts = [ln_a.spt, ln_a.ept, ln_b.spt, ln_b.ept]
            t_vals = sorted([ln_ext.near(p)[1] for p in pts])
            self.append(Segment(ln_ext.eval(t_vals[1]), ln_ext.eval(t_vals[2])))
            return True
        return False

        
    def _circle_circle(self,cir_a,cir_b):
        """| Intersects two circles.
           | Upon success, the Intersector.dist property will be set to the distance between the pair of points of intersection.
           | Dist of zero when circles intersect at just one point.
            
           :param cir_a: First circle to intersect.
           :type cir_a: Circle
           :param cir_b: Second circle to intersect.
           :type cir_b: Circle
           :result: Boolean value.
           :rtype: bool
            
        """
        # TODO: this func currently only works on co-planar circles

        if not cir_a.plane.is_coplanar( cir_b.plane ) : 
            self.log = "Circles are not coplanar. Try checking the normal direction of the circle base planes, as these must align in order to be coplanar."
            return False
        d = cir_a.origin.distance(cir_b.origin)
        if d == 0 : 
            self.log = "Coplanar circles share a center point - no intersections possible."
            return False
        a = (cir_a.rad**2 - cir_b.rad**2 + d**2)/(2*d)
        h2 = cir_a.rad**2 - a**2
        if h2 < 0 : 
            self.log = "Coplanar circles do not intersect."
            return False
        self.dist = math.sqrt(h2)
        pt = ( cir_b.origin - cir_a.origin ) * (a/d) + cir_a.origin
        if self.dist == 0 : self.append(pt)
        else:
            vec = Vec(cir_a.origin,pt).cross(cir_a.plane.normal).normalized(self.dist)
            self.append(pt - vec)
            self.append(pt + vec)
        return True

