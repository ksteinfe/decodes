from decodes.core import *


class ValueField(Grid):
    """
    a raster grid of floating point values
    each pixel contains a floating point number
    """
    def __init__(self, pixel_res=Interval(20,20), initial_value = 0.0,include_corners=False,wrap=True):
        """ ValueField constructor.
        
            :param pixel_res: Resolution of ValueField.
            :type pixel_res: Interval
            :param initial_value: Start value of ValueField.
            :type initial_value: float
            :param include_corners: Boolean Value.
            :type include_corners: bool
            :param wrap: Boolean Value.
            :type wrap: bool
            :result: ValueField Object
            :rtype: ValueField
            
        """
        try:
            self._res = (int(pixel_res.a),int(pixel_res.b))
        except:
            self._res = pixel_res
        self._pixels = [initial_value]*(self.px_width*self.px_height)
        super(ValueField,self).__init__(include_corners, wrap)

    @property
    def max_value(self):
        """ Returns max value of ValueField.
        
            :result: Maximum value.
            :rtype: float
        """
    
        return max(self._pixels)

    @property
    def min_value(self):
        """ Returns min value of ValueField.
        
            :result: Minimum value.
            :rtype: float
        """
        return min(self._pixels)

    def to_image(self,min_color,max_color,value_range=None):
        """ Constructs image from ValueField.
        
            :param min_color: Minimum color in image.
            :type min_color: Color
            :param max_color: Maximum color in image.
            :type max_color: Color
            :param value_range: Range of values.
            :type value_range: Interval
            :result: Image.
            :rtype: Image.
            
        """
        from .dc_interval import Interval
        if value_range is None : value_range = Interval(self.min_value,self.max_value)
        img = Image(self.dimensions)
        for n, val in enumerate(self._pixels):
            try: 
                t = value_range.deval(val)
            except :
                t = 0.0
            img._pixels[n] = Color.interpolate(min_color,max_color,t)
        return img

class BoolField(Grid):
    """
    a raster grid of boolean values
    each pixel contains a True or a False
    """
    def __init__(self, pixel_res=Interval(20,20), initial_value = False,ic=False,wrap=True):
        """ BoolField constructor.
        
            :param pixel_res: Resolution of BoolField.
            :type pixel_res: Interval
            :param initial_value: Start value of BoolField
            :type initial_value: bool
            :param ic: Include corners parameter.
            :type ic: bool
            :param wrap: Boolean value.
            :type wrap: bool
            :result: BoolField object.
            :rtype: BoolField
            
        """
        try:
            self._res = (int(pixel_res.a),int(pixel_res.b))
        except:
            self._res = pixel_res
        self._pixels = [initial_value]*(self.px_width*self.px_height)
        super(BoolField,self).__init__(ic)

    def to_image(self,false_color=Color(1.0),true_color=Color(0.0)):
        """ Constructs and image from the BoolField.
            
            :param false_color: Color for False values.
            :type false_color: Color
            :param true_color: Color for True values.
            :type true_color: Color
            :result: Image
            :rtype: Image
            
        """
        img = Image(self._res,false_color)
        for n, bool in enumerate(self._pixels):
            if bool : img._pixels[n] = true_color

        return img

class VecField(Grid):
    """| A raster grid of vectors.
       | Each pixel contains a positioned 3d vector (a Ray).

    """   
       
    #TODO: allow to set vectors as "bidirectional", which would affect the behavior of average vectors, and would produce lines rather than rays
    
    def __init__(self, pixel_res=Interval(8,8), spatial_origin=Point(), spatial_dim=Interval(4,4), initial_value = Vec(),include_corners=False,wrap=True):
    
        """ Vector field constructor.
        
            :param pixel_res: Resolution of vector grid.
            :type pixel_res: Interval
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
        try:
            self._res = (int(pixel_res.a),int(pixel_res.b))
        except:
            self._res = pixel_res
        self._pixels = [initial_value]*(self.px_width*self.px_height)
        self._sp_org = spatial_origin
        self._sp_dim = spatial_dim
        super(VecField,self).__init__(include_corners)

        self._sp_ival_x = Interval(self._sp_org.x - self._sp_dim.a/2, self._sp_org.x + self._sp_dim.a/2) # spatial interval x
        self._sp_ival_y = Interval(self._sp_org.y - self._sp_dim.b/2, self._sp_org.y + self._sp_dim.b/2) # spatial interval y
        self._base_pts = []
        for ival_y in self._sp_ival_y//self._res[1]:
            for ival_x in self._sp_ival_x//self._res[0]:
                self._base_pts.append(Point(ival_x.mid, ival_y.mid)) 

    def to_rays(self):
        """ Returns a list of Rays that correspond to the Vecs from the Vector Field.
        
            :result: A list of Rays.
            :rtype: [Ray]
        """
        return [Ray(pt,vec) for vec,pt in zip(self._pixels, self._base_pts )]

    def get_cpt(self,x,y):
        """ Returns the center point of the cell associated with the given address.
        
            :param x: x-coordinate
            :type x: float
            :param y: y-coordinate
            :type y: float
            :result: Center point of cell.
            :rtype: Point
        
        """
        return self._base_pts[y*self._res[0]+x]

    def vec_near(self,a,b=None):
        """ Returns closest vector to the given location. May be passed either a point or an x,y coordinate.
        
            :param a: x-coordinate or Point.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: Nearest Vec.
            :rtype: Vec
            
        """
        x,y = self.address_near(a,b)
        return self.get(x,y)

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

    def vecs_near(self,a,b=None):
        """ Returns locations of vectors near the given location. May be passed either a point or an x,y coordinate.
        
            :param a: x-coordinate or Point.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: List of locations of near vectors.
            :rtype: [tup]
            
        """
        tups = self.addresses_near(a,b)
        return [self.get(tup[0],tup[1]) for tup in tups]

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
        """ Returns location of vector near the given location. May be passed either a point or an x,y coordinate.
        
            :param a: x-coordinate or Point.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: Location of vector.
            :rtype: int, int
            
        """
        try:
            sample_pt = Point(a.x,a.y)
        except:
            sample_pt = Point(a,b)

        x = min(1.0,max(0.0,self._sp_ival_x.deval(sample_pt.x)))
        y = min(1.0,max(0.0,self._sp_ival_y.deval(sample_pt.y)))

        x = int(math.floor(Interval(0,self.px_width).eval(x)))
        y = int(math.floor(Interval(0,self.px_height).eval(y)))
        if x == self.px_width : x = self.px_width-1
        if y == self.px_height : y = self.px_height-1
        return x,y

    def addresses_near(self,a,b=None):
        """ Returns locations of vectors near the given location. May be passed either a point or an x,y coordinate.
        
            :param a: x-coordinate or Point.
            :type a: float or Point
            :param b: y-coordinate or None.
            :type b: float or None
            :result: List of locations.
            :rtype: [tup]
            
        """
        
        try:
            sample_pt = Point(a.x,a.y)
        except:
            sample_pt = Point(a,b)
    
        dx2 = self._sp_ival_x.delta / self.px_width / 2
        dy2 = self._sp_ival_y.delta / self.px_height / 2
    
        x = self._sp_ival_x.deval(sample_pt.x)
        y = self._sp_ival_y.deval(sample_pt.y)
    
        x = Interval.remap(x,Interval(dx2,1-dx2),Interval(0,self.px_width-1))
        y = Interval.remap(y,Interval(dy2,1-dy2),Interval(0,self.px_height-1))
    
        x_flr,y_flr = math.floor(x),math.floor(y)
        x_cei,y_cei = math.ceil(x), math.ceil(y)
    
        x_flr = int(Interval(0,self.px_width-1).limit_val(x_flr))
        y_flr = int(Interval(0,self.px_height-1).limit_val(y_flr))
        x_cei = int(Interval(0,self.px_width-1).limit_val(x_cei))
        y_cei = int(Interval(0,self.px_height-1).limit_val(y_cei))
    
        adds = []
        for tup in [(x_flr,y_flr),(x_cei, y_flr),(x_cei, y_cei),(x_flr, y_cei)]:
            if tup not in adds:
                adds.append(tup)
        return adds

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
            
