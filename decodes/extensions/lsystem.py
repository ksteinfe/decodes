from ..core import *
from math import *
from ..core import dc_color, dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_xform
import copy
print("lsystem.py loaded")


class LEngine(object):

    def __init__(self,axiom):
        self.axiom = axiom
        self.rules = []
        self.clear()

    def add_rule(self,rulething):
        # check on structure of rulething and convert to tuple
        rule = rulething
        try:
            rule.strip()
            rule = [str.strip() for str in rulething.split("->")]
        except:
            try:
                rule = rulething[0],rulething[1]
            except:
                raise TypeError("oh snap")
        self.rules.append(rule)
    
    def clear(self):
        self.hist = [self.axiom]
        self.rules = []

    @property
    def cur_gen(self): return self.hist[-1]
            
    def apply_rules(self, char):
        # check the rules for the appropriate one to apply
        for rule in self.rules:
            if char == rule[0]:
                return rule[1]
                break
        return char
        
    def step(self):
        nxt_gen = ""
        for chr in self.cur_gen: nxt_gen += str(self.apply_rules(chr))
        self.hist.append(nxt_gen) # add this string to our history


class LTurtle(object):
    
    def __init__(self,instructions):
        self.inst = instructions
        self.pts = [Point()]
        self.css = [CS()]
        self.angle = math.pi/4
        self.step_size = 1.0

    def go(self):
        lines = []
        while len(self.inst)>0:
            chr = self.inst[0]
            # move the turtle based on the current string character
            if chr == '-': #yaw right
                self.do_xform(self.css[-1].zAxis,self.angle)
            elif chr == '+': #yaw left
                self.do_xform(self.css[-1].zAxis,-self.angle)
            elif chr == '^': #pitch up
                self.do_xform(self.css[-1].xAxis,-self.angle)
            elif chr == '&': #pitch down
                self.do_xform(self.css[-1].xAxis,self.angle)
            elif chr == '}': #roll right
                self.do_xform(self.css[-1].yAxis,self.angle)
            elif chr == '{': # roll left
                self.do_xform(self.css[-1].yAxis,-self.angle)
            elif chr == 'F': # draw line
                nxt_pt = self.pts[-1] + (self.css[-1].yAxis * self.step_size)
                lines.append(Segment(self.pts[-1],nxt_pt))
                self.pts[-1] = nxt_pt
            elif chr == '[': #push the stack
                self.push(self.pts[-1], self.css[-1])
            elif chr == ']': #pop the stack
                self.pop() 
            self.inst = self.inst[1:]
        return lines

    def do_xform(self,axis,angle):
        xf = Xform.rotation(axis=axis,angle=angle)
        self.css[-1] = self.css[-1] * xf
        pass

    def push(self,pt,cs):
        self.pts.append(pt)
        self.css.append(cs)

    def pop(self):
        self.pts = self.pts[:-1]
        self.css = self.css[:-1]


        