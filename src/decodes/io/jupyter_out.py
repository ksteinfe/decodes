from .. import *
from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon
from . import outie
from . import svg_out
if VERBOSE_FS: print("jupyter_out loaded")

import os, sys, math
import io

class JupyterOut(svg_out.SVGOut):
    """outie for writing stuff to a Jupyter notebook"""
    
    point_size = 4
    default_canvas_dimensions = Interval(560,360)
    html_template = '<div style="width:{}px; height:{}px; box-shadow: 2px 2px 8px 4px #ddd; margin: 8px;">{}</div>'
    default_scale = 10.0
    default_grid_color = Color(0.98,0.98,0.98)
        
    def __init__(self, scale=False, grid_bnds=False, grid_color=False):
        if not scale: scale = JupyterOut.default_scale
        super(JupyterOut,self).__init__(
            "",
            canvas_dimensions = JupyterOut.default_canvas_dimensions, 
            flip_y = True,
            center_on_origin = True,
            scale = scale,
            save_file = False,
            verbose = False
        )
        
        self.grid_bnds = grid_bnds
        self.grid_color = grid_color
        if not self.grid_color: self.grid_color = JupyterOut.default_grid_color
        self.put_reference_geom()

    def put_reference_geom(self):
        # grid set to 1-unit cells
        # grid extents set by y-dimension
        
        if self.grid_bnds:
            for bnd in self.grid_bnds:
                pl = bnd.to_pline()
                pl.set_fill(self.grid_color)
                pl.set_color(1,1,1)
                pl.set_weight(1)
                self.put( pl )
        
            pt = Point()
            pt.set_weight(min(self.grid_bnds[0].dim_x, self.grid_bnds[0].dim_y ) * 0.5 * self._scale )
            pt.set_color(1,1,1)
            self.put(pt)
        
        '''
        ext = self._canvas_dim.b / 2 / self._scale
        cnt = int(ext/self.cell_size - 1) * 2
        ext = cnt * self.cell_size
        
        for ival_y in Interval(-ext/2,ext/2)//cnt:
            for ival_x in Interval(-ext/2,ext/2)//cnt:
                pt = Point(ival_x.a,ival_y.a) + Vec(0.5,0.5)
                pg = PGon.rectangle(pt,1,1)
                pg.set_fill(0.95,0.95,0.95)
                pg.set_color(1,1,1)
                pg.set_weight(1)
                self.put( pg )
                '''
        
    def draw(self):
        from IPython.core.display import display, HTML
        
        super(JupyterOut,self).draw()
        
        display(HTML(JupyterOut.html_template.format(
            self._canvas_dim.a, 
            self._canvas_dim.b, 
            self.svg
            )))
            
    def clear(self):
        super(JupyterOut,self).clear()
        self.put_reference_geom()

    
    @staticmethod
    def origin_centered(scale=10, half_cell_count=16):
        # fits well to a canvas dimension of 560,360
        ext = half_cell_count 
        bnds = Bounds(ival_x = Interval(-ext,ext), ival_y = Interval(-ext,ext) )
        bnds = bnds // half_cell_count * 2
        return JupyterOut(scale=scale, grid_bnds=bnds)
        
    @staticmethod
    def two_pi(scale=40, grid_color=False):
        # fits well to a canvas dimension of 560,360
        ext_x = math.pi*2
        ext_y = 4.0
        bnds = Bounds(ival_x = Interval(-ext_x,ext_x), ival_y = Interval(-ext_y,ext_y) )
        bnds = bnds // 8
        return JupyterOut(scale=scale, grid_bnds=bnds, grid_color=grid_color)        

    @staticmethod
    def unit_square(scale=300, grid_color=False):
        # fits well to a canvas dimension of 560,360
        
        bnds = Bounds(ival_x = Interval(), ival_y = Interval() )
        bnds = bnds // 4
        
        out = JupyterOut(scale=scale, grid_bnds=bnds, grid_color=grid_color)
        out._xf *= Xform.translation(Vec(-0.5,-0.5))
        return out
