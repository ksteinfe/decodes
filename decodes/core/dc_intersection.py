from decodes.core import *
from . import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon
if VERBOSE_FS: print "intersection.py loaded"



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
        self.tol = 0.000001

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
        bad_types = [Bounds,Color,Interval,Point,Xform]
        type_a = type(a)
        type_b = type(b)
        if any(type_a == type for type in bad_types) : raise NotImplementedError("It isn't possible to intersect a %s with anything!"%(type_a.__name__))
        if any(type_b == type for type in bad_types) : raise NotImplementedError("It isn't possible to intersect a %s with anything!"%(type_b.__name__))

        # INTERSECTIONS WITH A PLANE
        if any(item == Plane for item in [type_a,type_b]) : 
            if type_a == Plane : plane,other,type_other = a,b,type_b
            else: plane,other,type_other = b,a,type_a

            ignore_backface = False
            if "ignore_backface" in kargs: ignore_backface = kargs['ignore_backface']

            if type_other == Vec : return self._ray_plane(Ray(Point(),other),plane,ignore_backface)
            if type_other == Line : return self._line_plane(other,plane,ignore_backface)
            if type_other == Ray : return self._ray_plane(other,plane,ignore_backface)
            if type_other == Segment : return self._seg_plane(other,plane)

            if type_other == PLine : return self._pline_plane(other,plane)

            if type_other == Circle : return self._circle_plane(other,plane)

            if type_other == Arc : return self._arc_plane(other,plane)

            if type_other == Plane : return self._plane_plane(other,plane)



            raise NotImplementedError("I don't know how to intersect a Plane with a %s"%(type_other.__name__))

        # INTERSECTIONS WITH A CIRCLE
        if any(item == Circle for item in [type_a,type_b]) : 
            if type_a == Circle : circ,other,type_other = a,b,type_b
            else: circ,other,type_other = b,a,type_a

            if type_other == Circle : return self._circle_circle(other,circ)


            
        # INTERSECTIONS WITH A PGON
        if any(item == RGon for item in [type_a,type_b]) : 
            if type_a == RGon : type_a = PGon
            else: type_b = PGon

        if any(item == PGon for item in [type_a,type_b]) : 
            if type_a == PGon : pgon,other,type_other = a,b,type_b
            else: pgon,other,type_other = b,a,type_a

            ignore_backface = False
            if "ignore_backface" in kargs: ignore_backface = kargs['ignore_backface']

            if isinstance(other,LinearEntity) : return self._line_pgon(other,pgon,ignore_backface)


        # INTERSECTIONS WITH A LINE
        # last resort for Line-Line intersections
        if all(isinstance(item,LinearEntity) for item in [a,b]) : 
            return self._line_line(a,b)


        raise NotImplementedError("I don't know how to intersect a %s with a %s"%(type_a.__name__,type_b.__name__))


    def _pgon_plane(self,pgon,plane,ignore_backface=False):
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


    def _line_pgon(self,line,pgon,ignore_backface=False):
        """ Intersects a  Line with a Polygon. Upon success, the Intersector.dist property will be set to the distance between line.spt and the point of intersection.
        
            :param line: Line to intersect.
            :type line: Line
            :param pgon: Polygon to intersect.
            :type pgon: PGon
            :param ignore_backface: Boolean Value.
            :type ignore_backface: bool
            :result: Boolean Value.
            :rtype: bool
            
        """

        # first intersect LinearEntity with this pgon's basis
        xsec = Intersector()
        basis_success = xsec.of(pgon.basis.xy_plane,line,ignore_backface = ignore_backface)
        if not basis_success : 
            # if no intersection found, test to see if LinearEntity lies within the plane of the pgon
            pln = Plane.from_pts(line.spt,line.ept,line.spt+line.vec.cross(pgon.basis.z_axis))
            if pln.is_coplanar(pgon.basis.xy_plane):
                self.log = "LinearEntity in Plane of Pgon"
                success = False
                for edge in pgon.edges:
                    xsec = Intersector()
                    edge_success = xsec.of(edge,line)
                    if edge_success:
                        # we've found an intersection between this segment and our LinearEntity, check if point lies on edge
                        t = Line(edge.spt,edge.vec).near(xsec.results[0])[1]
                        if t>=0.0 and t<=1.0:
                            # now check that intersection lies on our LinearEntity
                            is_on = True
                            t = Line(line.spt,line.vec).near(xsec.results[0])[1]
                            #print type(line), t
                            if type(line) == Segment:
                                if t<0.0: is_on = False
                                if t>1.0: is_on = False
                            elif type(line) == Ray and t<0.0: is_on = False

                            if is_on:
                                self._geom.extend(xsec.results)
                                success = True
                return success
            else:
                self.log = xsec.log + " of Pgon"
                return False
            
        if pgon.contains_pt(xsec._geom[0]):
            self._geom = xsec._geom
            self.dist = xsec.dist
            return True
        else:
            self.log = "Intersection of PGon.basis and LinearEntity does not lie within PGon."
            return False


    def _line_plane(self,line,plane,ignore_backface=False):
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
        pln_norm = plane.normal.normalized()
        line_vec = line.vec.normalized()
        denom = pln_norm.dot(line_vec) # note, plane normal faces outward in the direction of the 'front' of the plane.  this may not be standard. 
        if ignore_backface and denom >= 0 : 
            self.log = "Backfaces ingored. LinearEntity lies behind Plane"
            return False # pos denom indicates ray behind plane
        if denom == 0 : 
            self.log = "LinearEntity does not intersect Plane"
            return False # denom of zero indicates no intersection
        self.dist = (plane.origin - line.spt).dot(pln_norm) / denom # t < 0 indicates plane behind ray
    
        self.append(line.spt + line_vec.normalized(self.dist))
        return True

    def _ray_plane(self,ray,plane,ignore_backface=False):
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
            self.log = "While pointing in the right direction, this Segment does not span across Plane"
            return False
        if xsec.dist > seg.length : 
            self.log = "Segment points in the wrong direction, and does not span across Plane"
            return False
        self._geom = xsec._geom
        self.dist = xsec.dist
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
        

        if pln_a.normal.is_parallel(pln_b.normal) :
            self.log = "Planes are parallel, no intersection found."
            return False
        vec = pln_a.normal.cross(pln_b.normal)
    
        ldir = pln_b.normal.cross(vec)
        denom = pln_a.normal.dot(ldir)
        tvec = pln_a.origin - pln_b.origin
        t = pln_a.normal.dot(tvec) / denom
        pt = pln_b.origin + ldir * t
    
        self.append( Line(pt,vec) )
        return True
        """
        a1,b1,c1 = pln_a.normal.x,pln_a.normal.y,pln_a.normal.z
        a2,b2,c2 = pln_b.normal.x,pln_b.normal.y,pln_b.normal.z

        x = 0
        y = (-c1 -pln_a.d) / b1
        z = ((b2/b1)*pln_a.d -pln_b.d)/(c2 - c1*b2/b1)
        
        self.append( Line(Point(x,y,z),vec) )
        return True
        """

    def _circle_plane(self,circ,plane):
        xsec = Intersector()
        plane_success = xsec._plane_plane(circ,plane)
        if not plane_success : 
            self.log = xsec.log
            return False
        
        self.line = xsec._geom[0] # add plane-plane intersection line
        npt, t, dist = self.line.near(circ.origin)
        x_vec = Vec(circ.origin,npt)
        if x_vec.length < self.tol : x_vec = Vec(circ.origin,self.line.ept)
        if x_vec.length < self.tol : x_vec = Vec(circ.origin,self.line.spt)

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

    def _arc_plane(self,arc,plane):
        xsec = Intersector()
        circ = Circle(arc.basis.xy_plane,arc.rad)
        circle_success = xsec._circle_plane(circ,plane)
        if not circle_success : 
            self.log = xsec.log
            self.log = "Plane failed to intersect with Circle derived from given Arc: "+xsec.log
            return False
        else:
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
                else:
                    self.log = "One of the intersection Points do not fall within sweep angle of this Arc: pt_angle={0} arc_angle={1}".format(ang,arc.angle)
        
        if len(self)==0:
            self.log = "Intersection Points do not fall within sweep angle of this Arc"

        return len(self)>0 


    def _line_line(self,ln_a,ln_b):
        """Intersects two lines.
            
            :param ln_a: First line to intersect.
            :type ln_a: Line
            :param ln_b: Second line to intersect.
            :type ln_b: Line
            :result: Boolean value
            :rtype: bool
            
        """
        #TODO: test for lines on the xy plane, and do simpler intersection
        #TODO: differentiate Lines from Rays and Segs 
        if Line.is_parallel(ln_a,ln_b) :
            self.log = "Lines are parallel, no intersection found."
            return False
        ept_a = ln_a.spt+ln_a.vec
        ept_b = ln_b.spt+ln_b.vec
        p1 = Vec(float(ln_a.spt.x),float(ln_a.spt.y),float(ln_a.spt.z))
        p2 = Vec(float(ept_a.x),float(ept_a.y),float(ept_a.z))
        p3 = Vec(float(ln_b.spt.x),float(ln_b.spt.y),float(ln_b.spt.z))
        p4 = Vec(float(ept_b.x),float(ept_b.y),float(ept_b.z))
        p13 = p1 - p3
        p43 = p4 - p3

        if (p43.length2 < self.tol): return False
        p21 = p2 - p1
        if (p21.length2 < self.tol): return False
        
        d1343 = p13.x * p43.x + p13.y * p43.y + p13.z * p43.z
        d4321 = p43.x * p21.x + p43.y * p21.y + p43.z * p21.z
        d1321 = p13.x * p21.x + p13.y * p21.y + p13.z * p21.z
        d4343 = p43.x * p43.x + p43.y * p43.y + p43.z * p43.z
        d2121 = p21.x * p21.x + p21.y * p21.y + p21.z * p21.z

        denom = d2121 * d4343 - d4321 * d4321
        numer = d1343 * d4321 - d1321 * d4343
        if denom == 0.0 :
            self.log = "Division by Zero, no intersection found."
            return False

        mua = numer / denom
        mub = (d1343 + d4321 * (mua)) / d4343
        self.ta, self.tb = mua,mub

        pa = Point(p1.x + mua * p21.x,p1.y + mua * p21.y,p1.z + mua * p21.z)
        pb = Point(p3.x + mub * p43.x,p3.y + mub * p43.y,p3.z + mub * p43.z)
        if pa.is_identical(pb,self.tol) : 
            self.log = "3d intersection found."
            self.append(pa)
            
            if type(ln_a) == Ray and self.ta < 0.0 : return False
            if type(ln_b) == Ray and self.tb < 0.0 : return False  
            if type(ln_a) == Segment and (self.ta < 0.0 or self.ta > 1.0) : return False
            if type(ln_b) == Segment and (self.tb < 0.0 or self.tb > 1.0)  : return False  
            
            return True
        else: 
            self.log = "No intersection found in 3d, recording shortest Segment between these two lines."
            self.append(Segment(pa,pb))
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

