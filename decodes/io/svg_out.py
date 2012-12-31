from .. import *
from ..core import *
from ..core import base, vec, point, cs, line, mesh, pgon
from . import outie
if VERBOSE_FS: print "svgOut loaded"

import os, sys
import pysvg
from pysvg.structure import *
from pysvg.shape import *
from pysvg.builders import *

class SVGOut(outie.Outie):
  """outie for writing stuff to a SVG file"""
  
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
    if hasattr(pt, 'props') and 'color' in pt.props : 
      style = self._props_to_style(fill_color=pt.props['color'])
    else :
      style = self._props_to_style(fill_color=Color(0))
    svg_pt = circle(pt.x, pt.y, 2)
    svg_pt.set_style(style)
    self.svg.addElement(svg_pt)
    return True
    
  def _drawPolygon(self, pgon):
    if hasattr(pgon, 'props') and 'color' in pgon.props : 
      style = self._props_to_style(fill_color=pgon.props['color'])
    else :
      style = self._props_to_style(fill_color=Color(0))
    
    oh=ShapeBuilder()
    pointsAsTuples=[(v.x,v.y) for v in pgon.verts]
    svg_rect=oh.createPolygon(points=oh.convertTupleArrayToPoints(pointsAsTuples),strokewidth=10, stroke='blue', fill='red')
    
    svg_rect.set_style(style)
    self.svg.addElement(svg_rect)
    return True
  
  def _props_to_style(self, fill_color=False, stroke_color=False, stroke_width=False):
    fill_color = 'none' if not fill_color else 'rgb(%s,%s,%s)' % (fill_color.r*255,fill_color.g*255,fill_color.b*255)
    if not stroke_width : stroke_width = 1
    stroke_color = 'none' if not stroke_color else 'rgb(%s,%s,%s)' % (stroke_color.r*255,stroke_color.g*255,stroke_color.b*255)
    style = 'fill:%s;stroke-width:%s; stroke:%s' % (fill_color, stroke_width, stroke_color)
    return style
    
  
    