import decodes.core as dc
from decodes.core import *
import math as m
import random

class Poisson_Sampler():
    
    def __init__(self, bds, r):
        
        self.r = r
        self.r_sqr = r*r
        self.cell_size = r/m.sqrt(2)
        self.dom_x, self.dom_y = bds.ival_x, bds.ival_y
        self.len_row = int(m.ceil(self.dom_x.b/self.cell_size))
        self.len_col = int(m.ceil(self.dom_y.b/self.cell_size))
        self.cells = {}
        self.graph = Graph()
        
        for xi in range(self.len_row):
            for yi in range(self.len_col):
                self.cells[(xi,yi)] = []
        
        for cell in self.cells:
            if cell[0]<self.len_row and cell[1]<self.len_col:
                self.graph.add_edge(cell, (cell[0], cell[1]+1))
                self.graph.add_edge(cell, (cell[0]+1, cell[1]+1))
                self.graph.add_edge(cell, (cell[0]+1, cell[1]))
            if 0<cell[0]: self.graph.add_edge(cell, (cell[0]-1, cell[1]+1))
    
    
    def grid_coord(self, p):
        return (int(m.floor(p.x/self.cell_size)), int(m.floor(p.y/self.cell_size)))
    
    
    def in_bds(self, p):
        return p.x in self.dom_x and p.y in self.dom_y
    
    
    def in_nbd(self, p):
        index = self.grid_coord(p)
        if len(self.cells[index]):return True
        for ci in self.graph.edges[index]:
            if ci in self.cells:
                for pt in self.cells[ci]:
                    if p.distance2(pt) <= self.r_sqr:
                        return True
        return False
    
    
    def run(self, max_cycles=5000, k=30):
        
        def put_point(p):
            process_list.append(p)
            sample_points.append(p)
            self.cells[self.grid_coord(p)].append(p)
        
        def gen_random(p, r):
            rr = random.uniform(r, 2*r)
            rt = random.uniform(0, 2*m.pi)
            return Point(p.x+rr*m.sin(rt), p.y+rr*m.cos(rt))
        
        process_list = []
        sample_points = []
        
        x0 = Point(self.dom_x.eval(random.random()), self.dom_y.eval(random.random()))
        put_point(x0)
        
        cycles = 0
        while len(process_list):
            
            process_pt =random.choice(process_list)
            process_list.remove(process_pt)
            coord = self.grid_coord(process_pt)
            
            for i in range(k):
                check_pt = gen_random(process_pt, self.r)
                if self.in_bds(check_pt) and not self.in_nbd(check_pt) :
                    put_point(check_pt)
                
            cycles+=1
            if cycles > max_cycles:
                print('stopped after {} cycles'.format(max_cycles))
                break
        
        return sample_points