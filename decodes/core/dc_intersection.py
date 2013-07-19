from decodes.core import *
from . import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon
if VERBOSE_FS: print "intersection.py loaded"



class XSec(object):
    """
    intersection results class
    """
    def __init__(self):
        self._geom = []

    def __getitem__(self,slice):
        return self._geom[slice]

    def append(self,item):
        self._geom.append(item)

    def __len__(self): return len(self._geom)
'''
TODO: move interseect function into XSec class, such that
intersection = XSec() # this could be secretly pre-loaded when module loads
if intersection.of(a,b):
    b.put(intersection.geom)
else:
    print "no intersections"
'''

def intersect(a,b,xsec,**kargs):
    """
    pass in two pieces of decodes geometry (a & b), and i'll have a go at intersecting them.
    results will be stored in given xsects list
    extras (such as distance to intersection points) will be stored in optional extras variable
    function returns success, True or False
    """
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

        if type_other == Ray : return _xsect_ray_plane(other,plane,xsec,ignore_backface)
        if type_other == Line : return _xsect_line_plane(other,plane,xsec,ignore_backface)
        raise NotImplementedError("I don't know how to intersect a Plane with a %s"%(type_other.__name__))

    # INTERSECTIONS WITH A CIRCLE
    if any(item == Circle for item in [type_a,type_b]) : 
        if type_a == Circle : circ,other,type_other = a,b,type_b
        else: circ,other,type_other = b,a,type_a

        if type_other == Circle : return _xsect_circle_circle(other,circ,xsec)

    
    raise NotImplementedError("I don't know how to intersect a %s with a %s"%(type_a.__name__,type_b.__name__))



def _xsect_ray_plane(ray,plane,xsec,ignore_backface=False):
    line_xsec = XSec()
    line_success = _xsect_line_plane(ray,plane,line_xsec,ignore_backface = ignore_backface)
    if not line_success : return False
    if line_xsec.dist < 0 : return False
    xsec._geom = line_xsec._geom
    xsec.dist = line_xsec.dist
    return True

def _xsect_line_plane(line,plane,xsec,ignore_backface=False):
    """
    upon success, the xsec.dist property will be set to the distance between line.spt and the point of intersection
    """
    pln_norm = plane.normal.normalized()
    line_vec = line.vec.normalized()
    denom = pln_norm.dot(line_vec) # note, plane normal faces outward in the direction of the 'front' of the plane.  this may not be standard. 
    if ignore_backface and denom >= 0 : return False # pos denom indicates ray behind plane
    if denom == 0 : return False # denom of zero indicates no intersection
    xsec.dist = (plane.origin - line.spt).dot(pln_norm) / denom # t < 0 indicates plane behind ray
    
    xsec.append(line.spt + line_vec.normalized(xsec.dist))
    return True



def _xsect_circle_circle(cir_a,cir_b,xsec):
    '''
    upon success, the xsec.dist property will be set to the distance between the pair of points of intersection
    dist of zero when circles intersect at just one point
    '''
    # TODO: this func currently only works on co-planar circles
    # TODO: move this functionality to the intersections class
    if not cir_a.plane.is_coplanar( cir_b.plane ) : 
        warnings.warn("Circles are not coplanar. Try checking the normal direction of the circle base planes, as these must align in order to be coplanar.")
        return False
    d = cir_a.origin.distance(cir_b.origin)
    if d == 0 : 
        warnings.warn("Coplanar circles share a center point - no intersections possible.")
        return False
    a = (cir_a.rad**2 - cir_b.rad**2 + d**2)/(2*d)
    h2 = cir_a.rad**2 - a**2
    if h2 < 0 : 
        #warnings.warn("Coplanar circles do not intersect.")
        return False
    xsec.dist = math.sqrt(h2)
    pt = ( cir_b.origin - cir_a.origin ) * (a/d) + cir_a.origin
    if xsec.dist == 0 : xsec.append(pt)
    else:
        vec = Vec(cir_a.origin,pt).cross(cir_a.plane.normal).normalized(xsec.dist)
        xsec.append(pt - vec)
        xsec.append(pt + vec)
    return True