from .. import *
from ..core import *
from ..core import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon
from . import outie
if VERBOSE_FS: print("json_out loaded")

import os, sys, math
import io
from . import jsonpickle

class JsonOut(outie.Outie):
    """outie for writing stuff to a ThreeJS scene file"""

    default_color = Color(0)
    point_size = 2
    min_point_size = 0.001
    default_curve_resolution = 50

    @property
    def json(self):
        try:
            return self._json
        except:
            self.draw()
            return self._json
    
    
    def __init__(self, filename, path=False, save_file=True):
        super(JsonOut,self).__init__()
        if filename[-4:].lower() == ".js" : filename = filename[:-4]
        if path==False : 
            self.filepath = os.path.expanduser("~") + os.sep + filename + ".js"
        else : 
            if path[-4:].lower() == ".js" : self.filepath = path
            else : self.filepath = path + os.sep + filename + ".js"

        self._save_file = save_file

        
        def props_to_data(obj,data):
            try:
                data['props'] = obj.props
                data['props']['color'] = (data['props']['color'].r*255,data['props']['color'].g*255,data['props']['color'].b*255)
                data['props']['fill'] = (data['props']['fill'].r*255,data['props']['fill'].g*255,data['props']['fill'].b*255)
                return data
            except:
                return data
        
        def cs_to_arr(cs):
            return (cs.origin.x,cs.origin.y,cs.origin.z,cs.x_axis.x,cs.x_axis.y,cs.x_axis.z,cs.y_axis.x,cs.y_axis.y,cs.y_axis.z)
            #return (cs.origin.x,cs.origin.y,cs.origin.z,cs.x_axis.x,cs.x_axis.y,cs.x_axis.z,cs.y_axis.x,cs.y_axis.y,cs.y_axis.z,cs.z_axis.x,cs.z_axis.y,cs.z_axis.z)
            
        def pln_to_arr(pln):
            return (pln.x,pln.y,pln.z,pln.normal.x,pln.normal.y,pln.normal.z)
            #return (cs.origin.x,cs.origin.y,cs.origin.z,cs.x_axis.x,cs.x_axis.y,cs.x_axis.z,cs.y_axis.x,cs.y_axis.y,cs.y_axis.z,cs.z_axis.x,cs.z_axis.y,cs.z_axis.z)
        
        class PointHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                data['xyz'] = (obj._x,obj._y,obj._z)
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(Point, PointHandler)
        jsonpickle.handlers.registry.register(Vec, PointHandler)
        
        class VecHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                data['xyz'] = (obj._x,obj._y,obj._z)
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(Point, PointHandler)
        
        class PlaneHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                #data['pts'] = [PointHandler(None).flatten(pt,{}) for pt in obj.pts] 
                data['center'] = (obj.x,obj.y,obj.z)
                data['normal'] = (obj.normal.x,obj.normal.y,obj.normal.z)
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(Plane, PlaneHandler)
        
        class CSHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                data['origin'] = (obj.origin.x,obj.origin.y,obj.origin.z)
                data['x_axis'] = (obj.x_axis.x,obj.x_axis.y,obj.x_axis.z)
                data['y_axis'] = (obj.y_axis.x,obj.y_axis.y,obj.y_axis.z)
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(CS, CSHandler)
        
        class SegmentHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                data['spt'] = (obj.spt.x,obj.spt.y,obj.spt.z)
                data['ept'] = (obj.ept.x,obj.ept.y,obj.ept.z)
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(Segment, SegmentHandler)
        
        
        class LineHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                data['pt'] = (obj.spt.x,obj.spt.y,obj.spt.z)
                data['vec'] = (obj.vec.x,obj.vec.y,obj.vec.z)
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(Line, LineHandler)
        jsonpickle.handlers.registry.register(Ray, LineHandler)
        
        class PLineHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                #data['pts'] = [PointHandler(None).flatten(pt,{}) for pt in obj.pts]
                data['pts'] = [(pt.x,pt.y,pt.z)for pt in obj.pts]
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(PLine, PLineHandler)
        
        class PGonHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                #data['pts'] = [PointHandler(None).flatten(pt,{}) for pt in obj.pts]
                data['pts'] = [(pt.x,pt.y,pt.z)for pt in obj.pts]
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(PGon, PGonHandler)
        jsonpickle.handlers.registry.register(RGon, PGonHandler)
        
        class CircleHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                #data['pts'] = [PointHandler(None).flatten(pt,{}) for pt in obj.pts]
                data['plane'] = pln_to_arr(obj)
                data['rad'] = obj.rad
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(Circle, CircleHandler)
        
        class ArcHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                #data['pts'] = [PointHandler(None).flatten(pt,{}) for pt in obj.pts] 
                data['cs'] = cs_to_arr(obj.basis)
                data['rad'] = obj.rad
                data['angle'] = obj.angle
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(Arc, ArcHandler)
        
        class CurveHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                #data['pts'] = [PointHandler(None).flatten(pt,{}) for pt in obj.pts]
                data['pts'] = [(pt.x,pt.y,pt.z)for pt in obj.surrogate.pts]
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(Curve, CurveHandler)
        
        class SurfaceHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                data['pts'] = [(pt.x,pt.y,pt.z)for pt in obj.surrogate.pts]
                data['faces'] = [f for f in obj.surrogate.faces]
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(Surface, SurfaceHandler)
        
        class MeshHandler(jsonpickle.handlers.BaseHandler):    
            def flatten(self, obj, data):
                data['pts'] = [(pt.x,pt.y,pt.z)for pt in obj.pts]
                data['faces'] = [f for f in obj.faces]
                data = props_to_data(obj,data)
                return data
        jsonpickle.handlers.registry.register(Mesh, MeshHandler)
        
        
        
    def draw(self):
        self._json = jsonpickle.encode(self.geom)
        
        if self._save_file: 
            print("drawing js to "+self.filepath)
            # write buffer to file
            fo = open(self.filepath, "wb")
            fo.write( self.json )
            fo.close()
        
        return True




