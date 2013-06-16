from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_xform
import math

# according to Radin, the pinwheel tiling contains one prototyle 
# a triangle with the following edge lenghts: 1, 2, sqrt(5)
# (http://www.ma.utexas.edu/users/radin/papers/pinwheel.pdf)
# (http://www.michaelwhittaker.ca/fractalpinwheel.pdf)
# some nice variation (color) here: http://tilings.math.uni-bielefeld.de/substitution_rules/pinwheel_1_2_0

class PinwheelTile(object):    
      

    def __init__(self,xf=Xform(), lineage="RT",**kargs):
        self.lineage = lineage
        self.xf = xf

        self._xf_scale = Xform.scale(1/math.sqrt(5)) #the amount to scale down at each inflation = 0.447213595
        
        # the idealized base points for all pinwheel tiles
        self._base_pts= [
            Point(),
            Point(2.0, 0.0),
            Point(0.0, 1.0),
            Point(0.2, 0.4),
            Point(1.2, 0.4),
            Point(0.4, 0.8),
            Point(1.0, 0.0),
        ]

        # sets base colors for pinwheeel tiles
        self._colors=[
                      Color(0.41,0.34,0.13),
                      Color(0.76,0.63,0.24),
                      Color(0.11,0.22,0.41),
                      Color(0.25,0.43,0.71),
                      Color(1.00,0.25,0.25),
                      ]
        
    @property
    def base_pts(self):
        '''
        world base points for this tile
        returns the ideal Pinwheel Tile's base points transformed by this tile's xform
        '''
        return [p*self.xf for p in self._base_pts]

            
    def _cs_from_base_pts(self,pt_o=0,pt_x=1,pt_y=2):
        '''
        Returns a CS oriented to an idealized tile's base points.  
        Multiply result by this_tile.xf and you'll get a coordinate system oriented to the postition of this tile in the world
        pt_0: index of origin point
        pt_x: index of a point on the desired x-axis
        pt_y: index of a point on the desired y-axis
        '''
        return CS(self._base_pts[pt_o],self._base_pts[pt_x]-self._base_pts[pt_o],self._base_pts[pt_y]-self._base_pts[pt_o])
            
    def to_mesh(self, color=None, parent_color_inheritance=0.5):
        if color is None : 
            clr_list = self._lineage_to_colors()
            try:
                clr_list.reverse()
                color = clr_list[0]
                for parent_color in clr_list[1:]:
                    color = Color.interpolate(color,parent_color,parent_color_inheritance)
            except:
                color = clr_list

        msh = Mesh()
        msh.append(self._base_pts[0] * self.xf)
        msh.append(self._base_pts[1] * self.xf)
        msh.append(self._base_pts[2] * self.xf)
        msh.add_face(0,1,2)
        msh.set_name(self.lineage)
        msh.set_color(color)
        return msh
    
    def _lineage_to_colors(self):
        lin = self.lineage.split(',')
        if len(lin)==0 : return Color()
        return [self._colors[int(str)] for str in lin[1:]]

    @property
    def centroid(self): return Point.centroid(self.base_pts)
    
    def inflate(self):
        cs = self._cs_from_base_pts(3,6,5)
        tile0 = PinwheelTile(self.xf * cs.xform * self._xf_scale,self.lineage+",0")
                                                                                                                                                                                     
        cs = self._cs_from_base_pts(4,5,6)                                                                                                                
        tile1 = PinwheelTile(self.xf * cs.xform * self._xf_scale,self.lineage+",1")
                                                                                                                                                                                     
        cs = self._cs_from_base_pts(3,6,0)                                                                                                                
        tile2 = PinwheelTile(self.xf * cs.xform * self._xf_scale,self.lineage+",2" )
                                                                                                                                                                                     
        cs = self._cs_from_base_pts(5,0,2)                                                                                                                
        tile3 = PinwheelTile(self.xf * cs.xform * self._xf_scale,self.lineage+",3")
        
        cs = self._cs_from_base_pts(4,1,6)
        tile4 = PinwheelTile(self.xf * cs.xform * self._xf_scale , self.lineage+",4")
        
        return [tile0,tile1,tile2,tile3,tile4]



class AmmannA3Tile(object):
    '''
    Ammann A3
    http://tilings.math.uni-bielefeld.de/substitution_rules/ammann_a3
    '''

