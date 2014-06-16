from .. import *
from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon
from . import outie
if VERBOSE_FS: print "json_out loaded"

import os, sys, math
import cStringIO
import jsonpickle

class JsonOut(outie.Outie):
    """outie for writing stuff to a ThreeJS scene file"""

    default_color = Color(0)
    point_size = 2
    min_point_size = 0.001
    default_curve_resolution = 50

    def __init__(self, filename, path=False, save_file=True):
        super(JsonOut,self).__init__()
        if filename[-4:].lower() == ".js" : filename = filename[:-4]
        if path==False : 
            self.filepath = os.path.expanduser("~") + os.sep + filename + ".js"
        else : 
            if path[-4:].lower() == ".js" : self.filepath = path
            else : self.filepath = path + os.sep + filename + ".js"

        self._save_file = save_file

        
        class PointHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                data['xyz'] = (obj._x,obj._y,obj._z)
                return data
        jsonpickle.handlers.registry.register(Point, PointHandler)
        
        class PLineHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                #data['pts'] = [PointHandler(None).flatten(pt,{}) for pt in obj.pts]
                data['pts'] = [(pt.x,pt.y,pt.z)for pt in obj.pts]
                return data
        jsonpickle.handlers.registry.register(PLine, PLineHandler)
        
        class CircleHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                #data['pts'] = [PointHandler(None).flatten(pt,{}) for pt in obj.pts]
                data['center'] = (obj.x,obj.y,obj.z)
                data['normal'] = (obj._vec.x,obj._vec.y,obj._vec.z)
                data['rad'] = obj.rad
                return data
        jsonpickle.handlers.registry.register(Circle, CircleHandler)
        
        class CurveHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                #data['pts'] = [PointHandler(None).flatten(pt,{}) for pt in obj.pts]
                data['pts'] = [(pt.x,pt.y,pt.z)for pt in obj.surrogate.pts]
                return data
        jsonpickle.handlers.registry.register(Curve, CurveHandler)
        
    def draw(self):
        print "drawing"        
        pickled = jsonpickle.encode(self.geom)
        
        if self._save_file: 
            print "drawing js to "+self.filepath
            # write buffer to file
            fo = open(self.filepath, "wb")
            fo.write( pickled )
            fo.close()
        
        return True




