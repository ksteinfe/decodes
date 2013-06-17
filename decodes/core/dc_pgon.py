from decodes.core import *
from . import dc_base, dc_interval, dc_vec, dc_point, dc_cs #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "polygon.py loaded"

import copy, collections
import math

class PGon(HasPts):
    """
    a very simple 2d polygon class
    Polygons limit their vertices to x and y dimensions, and enforce that they employ a basis.    Transformations of a polygon should generally be applied to the basis.    Any tranfromations of the underlying vertices should ensure that the returned vectors are limited to x and y dimensions
    """
    
    def __init__(self, vertices=None, basis=None):
        """ PGon Constructor.
        
            :param vertices: List of vertices to build the polygon.
            :type vertices: list
            :param basis: Plane basis for the PGon.
            :type basis: Basis
            :returns: PGon object. 
            :rtype: PGon
        """ 
        #TODO: if i pass in verices but no basis, try and figure out what the CS should be and project all points to the proper plane

        super(PGon,self).__init__() #HasPts constructor initializes list of verts and an empty basis
        self.basis = CS() if (basis is None) else basis
        if (vertices is not None) : 
            for v in vertices: self.append(v)
    
        
    def seg(self,index):
        """ Returns a segment of this Polygon
        The returned line segment will contain a copy of the Points stored in the segment.
        
            :param index: Index of the desired segment.
            :type index: Int
            :returns: Segment object. 
            :rtype: Segment
        """
        if index >= len(self) : raise IndexError()
        if index == len(self)-1 : return Segment(self.pts[index],self.pts[0])
        #TODO: handle negative indices
        return Segment(self.pts[index],self.pts[index+1])
        

    @property
    def edges(self):
        """Returns the edges of a PGon.
       
            :result: List of edges of a PGon
            :rtype: [Segment]
        """
        edges = []
        for n in range(len(self)):
            edges.append(self.seg(n))
        return edges
        
    def near(self, p):
        """Returns a tuple of the closest point to a given PGon, the index of the closest segment and the distance from the Point to the near Point.
       
            :param p: Point to look for a near Point on the PGon.
            :type p: Point
            :result: Tuple of near point on PGon, index of near segment and distance from point to near point.
            :rtype: (Point, integer, float)
        """
        #KS: this does not function as advertised, after narrowing down to the nearest segment we need to project the given point
        return False
        npts = [seg.near(p) for seg in self.edges]
        ni = Point.near_index(p,[npt[0] for npt in npts])
        return (npts[ni][0],ni,npts[ni][2])

    def near_pt(self, p):
        """Returns the closest point to a given PGon
       
            :param p: Point to look for a near Point on the PGon.
            :type p: Point
            :result: Near point on PGon.
            :rtype: Point
        """
        return self.near(p)[0]

    def __repr__(self): return "pgon[{0}v]".format(len(self._verts))
    
    def basis_applied(self):
        clone = super(PGon,self).basis_applied()
        clone.basis = CS()
        return clone

    def basis_stripped(self):
        clone = super(PGon,self).basis_stripped()
        clone.basis = CS()
        return clone

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
        """ 
        w2 = w/2.0
        h2 = h/2.0
        basis = CS(cpt)
        return PGon([Point(-w2,-h2),Point(w2,-h2),Point(w2,h2),Point(-w2,h2)],basis)

    @staticmethod
    def doughnut(cpt,radius_interval,angle_interval=Interval(0,math.pi*2),res=20):
        """ Constructs a doughnut based on a center point, two radii, and optionally a start angle, sweep angle, and resolution.
        
            :param cpt: Center point of a rectangle.
            :type cpt: Point
            :param angle_interval: Radii interval.
            :type angle_interval: Interval
            :param res: doughnut resolution.
            :type res: float
            :returns: Doughnut object. 
            :rtype: PGon
        """ 
        cs = CylCS(cpt)
        pts = []
        
        def cyl_pt(rad,ang): return Point(rad,ang,basis=cs).basis_applied()

        for t in angle_interval.divide(res,True):pts.append(cyl_pt(radius_interval.a,t))
        for t in angle_interval.invert().divide(res,True):pts.append(cyl_pt(radius_interval.b,t))
        return PGon(pts)

class RGon(PGon):
    '''
    A Regular Polygon Class
    '''
    def __init__(self, num_of_sides, radius=None, basis=None, edge_length=None, apothem=None):
        """ RGon Constructor.
        
        """ 
        if num_of_sides < 3 : raise GeometricError("Cannot create a regular polygon with fewer than three sides.")
        if radius is None and edge_length is None and apothem is None : raise GeometricError("You must specify one and only one of the following: radius, edge length, apothem")
        if radius is not None and edge_length is not None  and apothem is not None : raise GeometricError("You must specify one and only one of the following: radius, edge length, apothem")
        self._nos = num_of_sides

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
            raise GeometricError("You must specify one and only one of the following: radius, edge length, in_radius")

        step = math.pi*2.0/num_of_sides
        verts = [Point( self.radius * math.cos(step*n), self.radius * math.sin(step*n))  for n in range(num_of_sides) ]

        super(RGon,self).__init__(verts, basis)

    @property
    def radius(self):
        return self._radius

    @property
    def num_of_sides(self):
        return self._nos

    @property
    def area(self):
        try:
            return self._area
        except:
            self._area = 0.5 * self._nos * math.sin(math.pi*2.0/self._nos) * (self.radius ** 2)
            return self._inradius

    @property
    def apothem(self):
        '''
        the distance from the center to the midpoint of any side
        '''
        try:
            return self._apothem
        except:
            self._apothem = Vec.interpolate(self._verts[0],self._verts[1]).length
            return self._apothem

    @property
    def edge_length(self):
        '''
        the length of any edge
        '''
        try:
            return self._edge_length
        except:
            self._edge_length = 2 * self.radius * math.sin(math.pi/self._nos)
            return self._edge_length

    @property
    def circle_inscr(self):
        '''
        returns the inscribed circle of this RGon
        '''
        return Circle(self.basis.xy_plane,self.radius)

    @property
    def circle_cirscr(self):
        '''
        returns the circumscribed circle of this RGon
        '''
        return Circle(self.basis.xy_plane,self.apothem)

    @property
    def interior_angle(self):
        try:
            return self._iangle
        except:
            self._iangle = (self._nos-2) * math.pi/self._nos
            return self._iangle
        


    def inflate(self):
        '''
        returns a regular polygon inscribed inside this one while maintaining the same number of sides
        '''
        o = self.basis.origin
        x = Vec(o,Point.interpolate(self.pts[0],self.pts[1]))
        y = self.basis.zAxis.cross(x)
        basis = CS(o,x,y)
        return RGon(self._nos,self.apothem,basis)

    def deflate(self):
        '''
        returns a regular polygon that circumscribes this one while maintaining the same number of sides
        '''
        o = self.basis.origin
        x = Vec(o,Point.interpolate(self.pts[0],self.pts[1]))
        y = self.basis.zAxis.cross(x)
        basis = CS(o,x,y)
        return RGon(self._nos,basis=basis,apothem=self.radius)

    @staticmethod
    def from_edge(segment,num_of_sides,normal=Vec(0,0,1)):
        """
        constructs a regular polygon given a line segment describing one edge.
        the side of the edge that the center of the resulting polygon falls is determined by taking the cross product of the given edge vector and the given normal vector
        """
        apothem = segment.length / (2.0 * math.tan(math.pi/num_of_sides))
        cpt = segment.midpoint + segment.vec.cross(normal).normalized(apothem)
        cs = CS(cpt,Vec(cpt,segment.spt),segment.vec.cross(normal))
        return RGon(num_of_sides,apothem=apothem, basis=cs)