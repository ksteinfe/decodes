from decodes import core as dc
from decodes.core import *

if dc.VERBOSE_FS: print "svgOut loaded"

import os, sys
import outie
import pysvg
from pysvg.structure import *
from pysvg.shape import *


class SVGOut(outie.Outie):
  """outie for writing stuff to a SVG file"""
  
  def __init__(self, filename, path=False):
    super(SVGOut,self).__init__()
    if not path : self.filepath = path + os.sep + filename + ".svg"
    else : self.filepath = path
    
  def _startDraw(self):
    print "drawing svn to "+self.filepath
    self.svg = svg()
  
  def _endDraw(self):
    self.svg.save(self.filepath)
    
  def _drawGeom(self, g):
    # here we sort out what type of geometry we're dealing with, and call the proper draw functions
    # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)
    
    if isinstance(g, dc.Point) : 
      return self._drawPoint(g)
    
    return False

  def _drawPoint(self, pt):
    if hasattr(pt, 'props') and 'color' in pt.props : 
      style = self._props_to_style(fill_color=pt.props['color'])
    else :
      style = self._props_to_style(fill_color=dc.Color(0))
    svg_pt = circle(pt.x, pt.y, 2)
    svg_pt.set_style(style)
    self.svg.addElement(svg_pt)
    return True
  
  def _props_to_style(self, fill_color=False, stroke_color=False, stroke_width=False):
    fill_color = 'none' if not fill_color else 'rgb(%s,%s,%s)' % (fill_color.r*255,fill_color.g*255,fill_color.b*255)
    if not stroke_width : stroke_width = 1
    stroke_color = 'none' if not stroke_color else 'rgb(%s,%s,%s)' % (stroke_color.r*255,stroke_color.g*255,stroke_color.b*255)
    style = 'fill:%s;stroke-width:%s; stroke:%s' % (fill_color, stroke_width, stroke_color)
    return style
    
  
    