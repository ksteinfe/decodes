from .. import *
from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon
from . import outie
if VERBOSE_FS: print("svg_out loaded")

import os, sys, math
import io

class SVGOut(outie.Outie):
    """outie for writing stuff to a SVG file"""
    
    default_color = Color(0)
    point_size = 2
    min_point_size = 0.001
    default_curve_resolution = 50

    def __init__(self, filename, path=False, canvas_dimensions=False, flip_y=False, save_file=True,verbose=True):
        super(SVGOut,self).__init__()
        #if not path : self.filepath = __file__.rpartition(os.sep)[0] + os.sep + filename + ".svg"
        if filename[-4:].lower() == ".svg" : filename = filename[:-4]
        if path==False : 
            self.filepath = os.path.expanduser("~") + os.sep + filename + ".svg"
        else : 
            if path[-4:].lower() == ".svg" : self.filepath = path
            else : self.filepath = path + os.sep + filename + ".svg"
        
        self._canvas_dim = canvas_dimensions
        self._flip = flip_y
        self._save_file = save_file
        self._verbose = verbose
        self.svg = False

    def _startDraw(self):
        if self._verbose: print("building svg string")
        self.svg = False
        
        self.buffer = io.StringIO()
        svg_size = ""
        if self._canvas_dim is not False: svg_size = 'width="'+str(self._canvas_dim.a)+'" height="'+str(self._canvas_dim.b)+'"'
        self.buffer.write('<svg '+svg_size+' xmlns="http://www.w3.org/2000/svg" version="1.1">\n')
    
    def _endDraw(self):
        self.buffer.write('</svg>')
        self.svg = self.buffer.getvalue()
        
        if self._save_file: 
            if self._verbose: print("drawing svg to "+self.filepath)
            # write buffer to file
            fo = open(self.filepath, "wb")
            fo.write( self.svg )
            fo.close()
                
        self.buffer.close()

        
    def _drawGeom(self, g):
        # here we sort out what type of geometry we're dealing with, and call the proper draw functions
        # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)
        if isinstance(g,Curve): g = g.surrogate

        # treat Tris as PGons
        if isinstance(g, Tri):  g = PGon([g.pa,g.pb,g.pc])
        
        
        g = self._flip_geom(g)

        if isinstance(g, Point) : return self._drawPoint(g)
        if isinstance(g, PGon) :  return self._drawPolygon(g)
        if isinstance(g, PLine) :  return self._drawPolyline(g)
        if isinstance(g, LinearEntity) : 
            if isinstance(g, Line) : return self._drawLine(g)
            if isinstance(g, Ray) : return self._drawRay(g)
            if isinstance(g, Segment) : return self._drawSegment(g)
        if isinstance(g, Circle) : return self._drawCircle(g)
            
        return False

    def _buffer_append(self,type,atts,style):
        self.buffer.write('<'+type+' '+atts+' style="'+style+'"/>\n')

    def _flip_geom(self,geom):
        if self._flip and self._canvas_dim is not False:
            xf = Xform.mirror(plane="world_xz")
            ngeom = geom*xf
            xf = Xform.translation(Vec(0,self._canvas_dim.b))
            ngeom = ngeom*xf
            if hasattr(geom, 'props'): ngeom.props = geom.props
            return ngeom
        return geom

    def _drawPoint(self, pt):
        type = 'circle'
        style = self._extract_props(pt,force_fill=True) # force filled
        size = self.point_size/2.0
        if (hasattr(pt, 'props')) and ('weight' in pt.props) : size = pt.props['weight']
        if size < self.min_point_size : size = self.min_point_size
        atts = 'cx="%s" cy="%s" r="%s"' % (pt.x, pt.y,size)
        self._buffer_append(type,atts,style)
        return True
        
    def _drawCircle(self, cir):
        type = 'circle'
        style = self._extract_props(cir)
        atts = 'cx="%s" cy="%s" r="%s"' % (cir.x, cir.y, cir.rad)
        self._buffer_append(type,atts,style)
        return True        
        
    def _drawPolygon(self, pgon):
        type = 'polygon'
        style = self._extract_props(pgon,force_fill=True) # force filled
        point_string = " ".join([str(v.x)+","+str(v.y) for v in pgon.pts])
        atts = 'points="'+point_string+'"'
        self._buffer_append(type,atts,style)
        return True

    def _drawPolyline(self, pline):
        type = 'polyline'
        style = self._extract_props(pline)
        point_string = " ".join([str(v.x)+","+str(v.y) for v in pline.pts])
        atts = 'points="'+point_string+'"'
        self._buffer_append(type,atts,style)
        return True

    def _drawSegment(self, seg):
        type = 'line'
        style = self._extract_props(seg)
        atts = 'x1="%s" y1="%s" x2="%s" y2="%s"' % (seg.spt.x, seg.spt.y, seg.ept.x, seg.ept.y)
        self._buffer_append(type,atts,style)
        return True

    def _drawRay(self, ray):
        return False

    def _drawLine(self, line):
        return False



    def _extract_props(self,object,force_fill=False):
        '''
        extracts props from a given object, filling in default values where needed
        '''

        if not hasattr(object, 'props'): 
            if force_fill :  return self._props_to_style({'stroke_color': False, 'stroke_width': 0.0, 'fill_color': self.default_color})
            else : return self._props_to_style({'stroke_color': self.default_color, 'stroke_width': 0.5, 'fill_color': False})
        
        props = {}
        if force_fill:
            props['stroke_color'] = False
            if (not 'color' in object.props) and (not 'fill' in object.props) : props['fill_color'] = self.default_color
            if 'color' in object.props : props['fill_color'] = object.props['color']
            if 'fill' in object.props : props['fill_color'] = object.props['fill']
        else:
            if (not 'color' in object.props) and (not 'weight' in object.props): props['stroke_color'] = False
            elif (not 'color' in object.props) and ('weight' in object.props): 
                props['stroke_color'] = self.default_color
                props['stroke_width'] = object.props['weight']
            elif ('color' in object.props) and (not 'weight' in object.props): 
                props['stroke_color'] = object.props['color']
                props['stroke_width'] = 0.5
            elif ('color' in object.props) and ('weight' in object.props): 
                props['stroke_color'] = object.props['color']
                props['stroke_width'] = object.props['weight']
        
            if not 'fill' in object.props: props['fill_color'] = False
            else : props['fill_color'] = object.props['fill']
        
        return self._props_to_style(props)

    def _props_to_style(self,props):
        '''
        converts object properties to SVG style.
        expects the following fields to be filled in: fill_color, stroke_color, stroke_width

        to turn off fills, set props['fill_color'] = False
        to turn off strokes, set props['stroke_color'] = False
        '''
        fill_color = 'none' if not props['fill_color'] else 'rgb(%s,%s,%s)' % (int(props['fill_color'].r*255),int(props['fill_color'].g*255),int(props['fill_color'].b*255))
        # TODO: fill opacity may be set, but would require an alpha color representation

        stroke_width = 0 if not props['stroke_color'] else props['stroke_width']
        stroke_color = 'none' if not props['stroke_color'] else 'rgb(%s,%s,%s)' % (int(props['stroke_color'].r*255),int(props['stroke_color'].g*255),int(props['stroke_color'].b*255))
        
        
        style = 'fill:%s;stroke-width:%s;stroke:%s' % (fill_color, stroke_width, stroke_color)
        return style
