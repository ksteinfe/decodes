from decodes.core import *
from . import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon
if VERBOSE_FS: print "intersection.py loaded"



class Intersector(object):
    """
    intersection results class
    """
    def __init__(self):
        self._geom = []
        self.log = None

    def __getitem__(self,slice):
        return self._geom[slice]

    def append(self,item):
        self._geom.append(item)

    def clear(self):
        del self._geom[:]
        self.log = None

    def __len__(self): return len(self._geom)

    def of(self,a,b,**kargs):
        return self.intersect(a,b,**kargs)

    def intersect(self,a,b,**kargs):
        """
        pass in two pieces of decodes geometry (a & b), and i'll have a go at intersecting them.
        results will be stored in this xsec object
        extras (such as distance to intersection points) will be assigned as attributes to this xsec object
        function returns success, True or False
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

            # if intersecting with a linear entity, first intersect with this pgon's basis
            xsec = Intersector()
            basis_success = xsec.of(pgon.basis.xy_plane,other,ignore_backface = ignore_backface)
            if not basis_success : 
                self.log = xsec.log + " of Pgon"
                return False
            
            if pgon.contains_pt(xsec._geom[0]):
                self._geom = xsec._geom
                self.dist = xsec.dist
                return True
            else:
                self.log = "Intersection of PGon.basis and LinearEntity does not lie within PGon."
                return False


        # INTERSECTIONS WITH A LINE
        # last resort for Line-Line intersections
        if all(item == Line for item in [type_a,type_b]) : 
            return self._line_line(a,b)


        raise NotImplementedError("I don't know how to intersect a %s with a %s"%(type_a.__name__,type_b.__name__))


    def _pgon_plane(self,line,plane,ignore_backface=False):
        """
        upon success, the Intersector.dist property will be set to the distance between line.spt and the point of intersection
        """
        
        return False


    def _line_plane(self,line,plane,ignore_backface=False):
        """
        upon success, the Intersector.dist property will be set to the distance between line.spt and the point of intersection
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

    def _plane_plane(self,pln_a,pln_b):
        if pln_a.normal.is_parallel(pln_b.normal) :
            self.log = "Planes are parallel, no intersection found."
            return False
        vec = pln_a.normal.cross(pln_b.normal)

        a1,b1,c1 = pln_a.normal.x,pln_a.normal.y,pln_a.normal.z
        a2,b2,c2 = pln_b.normal.x,pln_b.normal.y,pln_b.normal.z

        x = 0
        y = (-c1 -pln_a.d) / b1
        z = ((b2/b1)*pln_a.d -pln_b.d)/(c2 - c1*b2/b1)
        
        self.append( Line(Point(x,y,z),vec) )
        return True

    def _line_line(self,ln_a,ln_b):
        if ln_a.is_parallel(ln_b) :
            self.log = "Lines are parallel, no intersection found."
            return False
        
        p1 = Vec(float(ln_a.spt.x),float(ln_a.spt.y),float(ln_a.spt.z))
        p2 = Vec(float(ln_a.ept.x),float(ln_a.ept.y),float(ln_a.ept.z))
        p3 = Vec(float(ln_b.spt.x),float(ln_b.spt.y),float(ln_b.spt.z))
        p4 = Vec(float(ln_b.ept.x),float(ln_b.ept.y),float(ln_b.ept.z))
        p13 = p1 - p3
        p43 = p4 - p3
        tol = 0.00001

        if (p43.length2 < tol): return False
        p21 = p2 - p1
        if (p21.length2 < tol): return False
        
        d1343 = p13.x * p43.x + p13.y * p43.y + p13.z * p43.z
        d4321 = p43.x * p21.x + p43.y * p21.y + p43.z * p21.z
        d1321 = p13.x * p21.x + p13.y * p21.y + p13.z * p21.z
        d4343 = p43.x * p43.x + p43.y * p43.y + p43.z * p43.z
        d2121 = p21.x * p21.x + p21.y * p21.y + p21.z * p21.z

        denom = d2121 * d4343 - d4321 * d4321
        numer = d1343 * d4321 - d1321 * d4343

        mua = numer / denom
        mub = (d1343 + d4321 * (mua)) / d4343
        self.ta, self.tb = mua,mub

        pa = Point(p1.x + mua * p21.x,p1.y + mua * p21.y,p1.z + mua * p21.z)
        pb = Point(p3.x + mub * p43.x,p3.y + mub * p43.y,p3.z + mub * p43.z)
        if pa == pb : 
            self.log = "3d intersection found."
            self.append(pa)
            return True
        else: 
            self.log = "No intersection found in 3d, recording shortest Segment between these two lines."
            self.append(Segment(pa,pb))
            return False

        


    def _circle_circle(self,cir_a,cir_b):
        '''
        upon success, the Intersector.dist property will be set to the distance between the pair of points of intersection
        dist of zero when circles intersect at just one point
        '''
        # TODO: this func currently only works on co-planar circles
        # TODO: move this functionality to the intersections class
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

