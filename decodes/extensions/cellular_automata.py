from ..core import *
from ..core import dc_color, dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_xform
import copy
print "cellular_automata.py loaded"

class CA (object):

    def __init__(self,pixel_res=Interval(20,20),include_corners=False,wrap=False):
        self.width = pixel_res.a
        self.height = pixel_res.b
        self.include_corners = include_corners
        self.wrap = wrap
        self.clear()
    
    def set_u(self,x,y,val):
        x,y = self._reframe(x,y)
        self._uvals.set(x,y,val)

# pass a function to be used for each iteration of the automata
# assumes that function takes the status of the home cell, and a list of the statuses of the neighbors
# function returns the new value for the home cell
    def set_rule(self,func=False):
        self.rule = func

    def get_u(self,x,y): return self._uvals.get(x,y)

    def _reframe(self,x,y):
        while x > self.width -1 : x = x - self.width
        while y > self.height -1: y = y - self.height
        while x < 0 : x = self.width + x
        while y < 0 : y = self.height + y
        return x,y

    def clear(self):
        self._uvals = BoolField(Interval(self.width,self.height),False,self.include_corners)
        self.step_count = 0
        self.hist_u = []

    def record(self):
        self.hist_u.append(self._uvals)

# makes a new generation by calling the function stored in self.rule

    def step(self, t=1.0):
        nxt_uvals = BoolField(Interval(self.width,self.height),False,self.include_corners)
        t = max(min(1.0,t),0.0)
        for x in range(0,self.width):
            for y in range(0,self.height):
                cur_u = self._uvals.get(x,y)
                neighbors_u = self._uvals.neighbors_of(x,y)
                nxt_u = self.rule(cur_u, neighbors_u)
                nxt_uvals.set(x,y,nxt_u)
 #               self.log_u(nxt_u)
 #       self.hist_u.append(self._uvals)
        self._uvals = nxt_uvals
        self.step_count += 1

# sets the initial condition for the CA. Expects a list of booleans
    def start(self, initial_uvals=False):
        for n, bool in enumerate(initial_uvals):
            self._uvals._pixels[n] = bool


        
