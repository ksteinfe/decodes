from decodes.core import *

   
class Grid(Raster):
    """
    an abstract class for storing information in a spatialized raster grid format.
    once a Grid.bnds is initialized it should not be changed, as collections of spatial intervals are calculated to speed addressing and near pts calculations
    """
    
    def __init__(self,pixel_dim=None,bnds=None,**kwargs):
        """ Grid constructor.

            :param pixel_dim: Resolution of Grid.
            :type pixel_dim: Interval or Tuple of two Integers
            :param bnds: 2d spatial boundary of Grid.
            :type pixel_dim: Bounds         
            :param include_corners: Boolean value.
            :type include_corners: bool
            :param wrap: Boolean value.
            :type wrap: bool
            :result: Raster object
            :rtype: Raster
            
        """
        super(Grid,self).__init__(pixel_dim,**kwargs)
        if bnds is None: self._bnds = Bounds.unit_square()
        else: self._bnds = Bounds(ival_x=bnds.ival_x,ival_y=bnds.ival_y ) # enforces 2d Bounds
        self._recalculate_base_pts()

        
    @property
    def bnds(self):
        """ Returns Grid bounds.
            
            :result: Grid bounds.
            :rtype: Bounds
            
        """
        return self._bnds
        
    def get_cpt(self,x,y):
        """ Returns the center point of the cell associated with the given address.
        
            :param x: x-coordinate
            :type x: float
            :param y: y-coordinate
            :type y: float
            :result: Center point of cell.
            :rtype: Point
        
        """
        return self._base_pts[y*self.px_width+x]
       
    def cpt_near(self,a,b=None):
        """ Returns center point of cell nearest to given location. May be passed either a point or an x,y coordinate.
        
            :param a: x-coordinate or Point.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: Center point of near cell.
            :rtype: Point
            
            
        """
        x,y = self.address_near(a,b)
        return self.get_cpt(x,y)       

    def cpts_near(self,a,b=None):
        """ Returns center points of cells near the given location. May be passed either a point or an x,y coordinate.
        
            :param a: x-coordinate or Point.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: List of center points near given location.
            rtype: [Point]
            
        """
        
        tups = self.addresses_near(a,b)
        return [self.get_cpt(tup[0],tup[1]) for tup in tups]

    def address_near(self,a,b=None):
        """ Returns address of the grid cell nearest to the given location. May be passed either a point or an x,y coordinate.
        
            :param a: x-coordinate or Point.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: Location of vector.
            :rtype: int, int
            
        """
        pt = Point(a,b)
        
        if pt.x <= self.bnds.ival_x.a : idx_x = 0
        elif pt.x >= self.bnds.ival_x.b : idx_x = self.px_width - 1
        else: idx_x = [pt.x in ival for ival in self._ivals_x].index(True)
        
        if pt.y <= self.bnds.ival_y.a : idx_y = 0
        elif pt.y >= self.bnds.ival_y.b : idx_y = self.px_height - 1
        else: idx_y = [pt.y in ival for ival in self._ivals_y].index(True)
        
        return idx_x, idx_y

    def addresses_near(self,a,b=None):
        """ Returns addresses of grid cells near the given location. May be passed either a point or an x,y coordinate.
        
            :param a: x-coordinate or Point.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: List of locations.
            :rtype: [tup]
            
        """
        pt = Point(a,b)
        add = self.address_near(pt)
        dx = 1 if pt.x > self._ivals_x[add[0]].mid else -1
        dy = 1 if pt.y > self._ivals_y[add[1]].mid else -1
        adds = [add,(add[0]+dx,add[1]),(add[0]+dx,add[1]+dy),(add[0],add[1]+dy)]
        adds = [add for add in adds if add[0]>=0 and add[0]<self.px_width]
        adds = [add for add in adds if add[1]>=0 and add[1]<self.px_height]
        return sorted(adds)
        
    def _recalculate_base_pts(self):
        """
        If the bounds changes or the res changes, the values defined here must be recalculated
        
        """
        #sp_org = self._bnds.cpt
        #sp_dim = spatial_dim
        #self._sp_ival_x = Interval(self._sp_org.x - self._sp_dim.a/2, self._sp_org.x + self._sp_dim.a/2) # spatial interval x
        #self._sp_ival_y = Interval(self._sp_org.y - self._sp_dim.b/2, self._sp_org.y + self._sp_dim.b/2) # spatial interval y
        self._base_pts = []
        self._ivals_x = self.bnds.ival_x//self.px_width
        self._ivals_y = self.bnds.ival_y//self.px_height
        for ival_y in self._ivals_y:
            for ival_x in self._ivals_x:
                self._base_pts.append(Point(ival_x.mid, ival_y.mid))
     
    @property
    def cell_pgons(self):
        from .dc_pgon import PGon
        pgons = []
        for ival_y in self._ivals_y:
            for ival_x in self._ivals_x:
                pts = Point(ival_x.a, ival_y.a),Point(ival_x.b, ival_y.a),Point(ival_x.b, ival_y.b),Point(ival_x.a, ival_y.b)
                pgons.append(PGon(pts))
        return pgons

    @property
    def lattice_segs(self):
        x_segs = []
        x_segs.append(Segment( Point(self._ivals_x[0].a,self.bnds.ival_y.a), Point(self._ivals_x[0].a,self.bnds.ival_y.b) ))
        for ival_x in self._ivals_x:
            x_segs.append(Segment( Point(ival_x.b,self.bnds.ival_y.a), Point(ival_x.b,self.bnds.ival_y.b) ))
            
        y_segs = []
        y_segs.append(Segment( Point(self.bnds.ival_x.a,self._ivals_y[0].a), Point(self.bnds.ival_x.b,self._ivals_y[0].a) ))
        for ival_y in self._ivals_y:
            y_segs.append(Segment( Point(self.bnds.ival_x.a,ival_y.b), Point(self.bnds.ival_x.b,ival_y.b) ))            
                
        return x_segs, y_segs
        
class VecField(Grid):
    """| A raster grid of vectors.
       | Each pixel contains a positioned 3d vector (a Ray).

    """   
       
    #TODO: allow to set vectors as "bidirectional" tensors, which would affect the behavior of average vectors, and would produce lines rather than rays. or, Make a TensorField class
    
    def __init__(self,pixel_dim=None,bnds=None,initial_value = Vec(),**kwargs):
    
        """ Vector field constructor.
            
            TODO: UPDATE DOCUMENTATION 
            
            :param pixel_dim: Resolution of vector grid.
            :type pixel_dim: Interval
            :param spatial_origin: Center of vector field.
            :type spatial_origin: Point
            :param spatial_dim: Dimension of vector field.
            :type spatial_dim: Interval
            :param initial_value: Start value for vector field.
            :type initial_value: Vec
            :param include_corners: Boolean Value.
            :type include_corners: bool
            :param wrap: Boolean Value.
            :type wrap: bool
            :result: A vector field.
            :rtype: VecField
            
        """
        super(VecField,self).__init__(pixel_dim,bnds,**kwargs)
        self.populate(initial_value,True)

    def to_rays(self):
        """ Returns a list of Rays that correspond to the Vecs from the Vector Field.
        
            :result: A list of Rays.
            :rtype: [Ray]
        """
        return [Ray(pt,vec) for vec,pt in zip(self._pixels, self._base_pts )]

    def vec_near(self,a,b=None):
        """ Returns closest vector to the given location. May be passed either a point or an x,y coordinate.
        
            :param a: x-coordinate or Point.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: Nearest Vec.
            :rtype: Vec
            
        """
        return self.get(*self.address_near(a,b))

    def vecs_near(self,a,b=None):
        """ Returns locations of vectors near the given location. May be passed either a point or an x,y coordinate.
        
            :param a: x-coordinate or Point.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: List of locations of near vectors.
            :rtype: [tup]
            
        """
        return [self.get(*add) for add in self.addresses_near(a,b)]

    def avg_vec_near(self,a,b=None):
        """ Returns an average vector from the near vectors around the given location. May be passed a point or an x,y coordinate.
        
            :param a: x-coordinate or Point.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: An average vector.
            :rtype: Vec
            
        """
        
        try:
            sample_pt = Point(a.x,a.y)
        except:
            sample_pt = Point(a,b)
            
        vecs = self.vecs_near(sample_pt)
        cpts = self.cpts_near(sample_pt)
        try:
            dists = [1.0/sample_pt.distance2(cpt) for cpt in cpts]
            tot = sum(dists)
            weights = [dist/tot for dist in dists]
            vec = Vec()
            for n in range(len(vecs)):
                vec = vec + vecs[n]* weights[n]
            return vec
        except:
            # sample point is coincident with one of the near cpts
            for n in range(len(cpts)):
                if cpts[n] == sample_pt : return vecs[n]
            raise GeometricError("sample point coincident with center point: %s"%(sample_pt))
            
    def spin_pt(self,a,b=None):
        """ Rotates vectors in a VecField around a given point. May be passed a point or an x,y coordinate.
        
            :param a: x-coordinate or Point to rotate around.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: Modifies this Vector Field in place.
            :rtype: None
                        
        """
        try:
            spin_pt = Point(a.x,a.y)
        except:
            spin_pt = Point(a,b)
            
        import math as m # import math library
        # for every x value in the vector field:
        for x in range(self.px_width):
            # for every y value in the vector field
            for y in range(self.px_height):
                # create a new spin vector
                v_x = y*(m.sin(spin_pt.y) + m.cos(spin_pt.x)) # vector x-component
                v_y = x*(m.sin(spin_pt.x) - m.cos(spin_pt.y)) # vector y-component
                new_vec = Vec(v_x, v_y) # construct new spin vector
                # set vector at x,y to new spin vector
                self.set(x,y,new_vec)
            
