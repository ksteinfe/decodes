from .. import *
from ..core import *
from ..core import base, vec, point, cs, line, mesh, pgon
from . import outie
if VERBOSE_FS: print "svg_out loaded"

import os, sys
import pysvg
from pysvg.structure import *
from pysvg.shape import *
from pysvg.builders import *

class SVGOut(outie.Outie):
    """outie for writing stuff to a SVG file"""
    
    default_color = Color(0)

    def __init__(self, filename, path=False):
        super(SVGOut,self).__init__()
        #if not path : self.filepath = __file__.rpartition(os.sep)[0] + os.sep + filename + ".svg"
        if not path : self.filepath = os.path.expanduser("~") + os.sep + filename + ".svg"
        else : self.filepath = path
        
    def _startDraw(self):
        print "drawing svn to "+self.filepath
        self.svg = svg()
    
    def _endDraw(self):
        self.svg.save(self.filepath)
        
    def _drawGeom(self, g):
        # here we sort out what type of geometry we're dealing with, and call the proper draw functions
        # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)
        
        if isinstance(g, Point) : 
            return self._drawPoint(g)
        if isinstance(g, PGon) : 
            return self._drawPolygon(g)
        
        return False

    def _drawPoint(self, pt):
        svg_pt = circle(pt.x, pt.y, 2)
        svg_pt.set_style(self._extract_props(pt,force_fill=True)) # circles are always filled
        self.svg.addElement(svg_pt)
        return True
        
    def _drawPolygon(self, pgon):
        oh=ShapeBuilder()
        pointsAsTuples=[(v.x,v.y) for v in pgon.verts]
        svg_rect=oh.createPolygon(points=oh.convertTupleArrayToPoints(pointsAsTuples),strokewidth=10, stroke='blue', fill='red')
        
        svg_rect.set_style(self._extract_props(pgon,force_fill=True)) # polygons are always filled
        self.svg.addElement(svg_rect)
        return True


    

    def _extract_props(self,object,force_fill=False):
        '''
        extracts props from a given object, filling in default values where needed
        '''

        if not hasattr(object, 'props'): 
            if force_fill or fill_by_default :  return self._props_to_style({'stroke_color': False, 'stroke_width': 0.0, 'fill_color': self.default_color})
            else : return self._props_to_style({'stroke_color': self.default_color, 'stroke_width': 0.5, 'fill_color': False})
        
        props = {}
        if force_fill:
            props['stroke_color'] = False
            if (not 'color' in object.props) and (not 'fill' in object.props) : props['fill_color'] = self.default_color
            if 'color' in object.props : props['fill_color'] = object.props['color']
            if 'fill' in object.props : props['fill_color'] = object.props['fill']
        else:
            if (not 'color' in object.props) and (not 'weight' in object.props): props['stroke_color'] = False
            if (not 'color' in object.props) and ('weight' in object.props): 
                props['stroke_color'] = self.default_color
                props['stroke_width'] = object.props['weight']
            if ('color' in object.props) and (not 'weight' in object.props): 
                props['stroke_color'] = object.props['color']
                props['stroke_width'] = 0.5
        
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
        fill_color = 'none' if not props['fill_color'] else 'rgb(%s,%s,%s)' % (props['fill_color'].r*255,props['fill_color'].g*255,props['fill_color'].b*255)
        # TODO: fill opacity may be set, but would require an alpha color representation

        stroke_width = 0 if not props['stroke_color'] else props['stroke_width']
        stroke_color = 'none' if not props['stroke_color'] else 'rgb(%s,%s,%s)' % (props['stroke_color'].r*255,props['stroke_color'].g*255,props['stroke_color'].b*255)
        
        
        style = 'fill:%s;stroke-width:%s; stroke:%s' % (fill_color, stroke_width, stroke_color)
        return style
