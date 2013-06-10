from ..core import *
from ..core import dc_color, dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_xform
import copy
print "cellular_automata.py loaded"

class CA (object):

    def __init__(self, dimensions=Interval(20,20)):
        self.width = dimensions.a
        self.height = dimensions.b

        self.clear()
    
    def set_u(self,x,y,val):
        x,y = self._reframe(x,y)
        self._uvals.set(x,y,val)


    def get_u(self,x,y): return self._uvals.get(x,y)

    def set_rect(self,x,y,w,h):
        x,y,w,h = int(x),int(y),int(w),int(h)
        for xi in range(x,x+w):
            for yi in range(y,y+h):
                self.set_u(xi,yi,0.5)
                self.set_v(xi,yi,0.25)

    def _reframe(self,x,y):
        while x > self.width -1 : x = x - self.width
        while y > self.height -1: y = y - self.height
        while x < 0 : x = self.width + x
        while y < 0 : y = self.height + y
        return x,y

    def clear(self):
        self._uvals = BoolField(Interval(self.width,self.height))
        self.step_count = 0
        self.hist_u = []
        
        self.max_recorded_u = 0.0
        self.min_recorded_u = 1.0

    def record(self):
        self.hist_u.append(self._uvals)

    def to_image_sequence(self, f_color = Color(0.0), t_color = Color(1.0)):    
        imgs = []
        for n in range(len(self.hist_u)):
            img = Image(Interval(self.width,self.height),f_color)

            for px in range(len(img._pixels)):
                if self.hist_u[n]._pixels[px] : img._pixels[px] = t_color
            imgs.append(img)
        return imgs



    def log_u(self,u):
        if u > self.max_recorded_u : self.max_recorded_u = u
        if u < self.min_recorded_u : self.min_recorded_u = u

    def step(self, t=1.0):
        nxt_uvals = BoolField(Interval(self.width,self.height))
        t = max(min(1.0,t),0.0)
        for x in range(0,self.width):
            for y in range(0,self.height):
                cur_u = self._uvals.get(x,y)
                #neighbors_u = self._uvals.neighbors_of(x,y)
                nxt_u = cur_u
                nxt_uvals.set(x,y,nxt_u)
 #               self.log_u(nxt_u)
        
        self._uvals = nxt_uvals
        self.step_count += 1

        
