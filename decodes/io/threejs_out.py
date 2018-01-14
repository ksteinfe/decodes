from .. import *
from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon
from . import outie
if VERBOSE_FS: print("threejs_out loaded")

import os, sys, math
import io

class ThreeJSOut(outie.Outie):
    """outie for writing stuff to a ThreeJS scene file"""

    default_color = Color(0)
    point_size = 2
    min_point_size = 0.001
    default_curve_resolution = 50

    def __init__(self, filename, path=False, save_file=True):
        super(ThreeJSOut,self).__init__()
        if filename[-4:].lower() == ".js" : filename = filename[:-4]
        if path==False : 
            self.filepath = os.path.expanduser("~") + os.sep + filename + ".js"
        else : 
            if path[-4:].lower() == ".js" : self.filepath = path
            else : self.filepath = path + os.sep + filename + ".js"

        self._save_file = save_file
        self.jsonstr = False

    def _startDraw(self):
        print("building 3js string")
        self.jsonstr = False
        
        self.buffer = io.StringIO()
        self.buffer.write('{\n"metadata":{},\n')
    
    def _endDraw(self):
        self.buffer.write('\n}')
        self.jsonstr = self.buffer.getvalue()
        
        if self._save_file: 
            print("drawing 3js to "+self.filepath)
            # write buffer to file
            fo = open(self.filepath, "wb")
            fo.write( self.jsonstr )
            fo.close()
                
        self.buffer.close()

        
    def _drawGeom(self, g):
        # here we sort out what type of geometry we're dealing with, and call the proper draw functions
        # MUST LOOK FOR CHILD CLASSES BEFORE PARENT CLASSES (points before vecs)

        if isinstance(g, Point) : return self._drawPoint(g)
        if isinstance(g, LinearEntity) : 
            if isinstance(g, Line) : return self._drawLine(g)
            if isinstance(g, Ray) : return self._drawRay(g)
            if isinstance(g, Segment) : return self._drawSegment(g)

        return False

    def _drawPoint(self, pt):
        self.buffer.write('a point at location %s, %s, %s \n' % (pt.x, pt.y,pt.z))
        return True
        
    def _drawSegment(self, seg):
        self.buffer.write('a line from x1="%s" y1="%s" x2="%s" y2="%s \n"' % (seg.spt.x, seg.spt.y, seg.ept.x, seg.ept.y))
        return True

    def _drawRay(self, ray):
        return False

    def _drawLine(self, line):
        return False


