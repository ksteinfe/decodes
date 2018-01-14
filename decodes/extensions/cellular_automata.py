from ..core import *
from ..core import dc_color, dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_xform
import copy
print("cellular_automata.py loaded")

class CA (object):

    def __init__(self,pixel_res=Interval(20,20),include_corners=False,wrap=False):
        self.width = int(pixel_res.a)
        self.height = int(pixel_res.b)
        self.clear(include_corners,wrap)
    
    def set_cell(self,x,y,val):
        x,y = self._reframe(x,y)
        self.cells.set(x,y,val)

# sets the entire field. Expects a list of booleans
    def set_cells(self, initial_cell=False):
        for n, bool in enumerate(initial_cell):
            self.cells._pixels[n] = bool

# pass a function to be used for each iteration of the automata
# assumes that function takes the status of the home cell, and a list of the statuses of the neighbors
# function returns the new value for the home cell
    def set_rule(self,func=False):
        self.rule = func

    def get_cell(self,x,y): return self.cells.get(x,y)

    def get_cells(self) : return self.cells

    def _reframe(self,x,y):
        while x > self.width -1 : x = x - self.width
        while y > self.height -1: y = y - self.height
        while x < 0 : x = self.width + x
        while y < 0 : y = self.height + y
        return x,y

    def clear(self,include_corners,wrap):
        self.cells = BoolField(Interval(self.width,self.height),wrap,include_corners)
        self.step_count = 0
        self.hist = []

    def record(self):
        self.hist.append(self.cells)

# makes a new generation by calling the function stored in self.rule

    def step(self, t=1.0):
        nxt_cells = BoolField(Interval(self.width,self.height),self.cells.wrap,self.cells.include_corners)
        t = max(min(1.0,t),0.0)
        for x in range(0,self.width):
            for y in range(0,self.height):
                cur_cell = self.cells.get(x,y)
                neighbor_cells = self.cells.neighbors_of(x,y)
                nxt_cell = self.rule(cur_cell, neighbor_cells)
                nxt_cells.set(x,y,nxt_cell)
        self.cells = nxt_cells
        self.step_count += 1




        
