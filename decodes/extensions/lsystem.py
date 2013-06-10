from ..core import *
from math import *
from ..core import dc_color, dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_xform
import copy
print "lsystem.py loaded"



class LEngine(object):

    def __init__(self,axiom):
        self.axiom = axiom
        self.rules = []
        self.clear()

    def add_rule(self,rulething):
        # check on structure of rulething and convert
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
        for chr in self.cur_gen(): nxt_gen += str(self.apply_rules(chr))
        self.hist.append(nxt_gen) # add this string to our history



class LTurtle(object):

    def __init__(self, production):
        self.production = production
        self.angle = radians(15) # default for now
        
        turtle_matrix = [0,0,0] #[yaw,pitch,roll]
        turtleCS = CS(Point(0,0,0), Vec(

            
    def step(self):
        for char in self.production:
            turtled = self.move(char)
            if turtled[0] == True: # push the stack
            if turtled[1] == True # pop the stack
            
            
    def move(self, chr):
        push = False
        pop = False
        
        # move the turtle based on the current string character
        if chr == '-': #yaw right
            self.yaw += angle
        if chr == '+': #yaw left
            self.yaw -= angle
        if chr == '^': #pitch up
            self.pitch += angle
        if chr == '&': #pitch down
            self.pitch -= angle
        if chr == '>': #roll right
            self.roll += angle
        if chr == '<': # roll left
            self.roll -= angle
        
        # update the CS
        
        # add a new turtle
        
        # handle branching
        if chr == '[': #branch
            push == True
        if chr == ']': #endbranch
            pop == True
        return push,pop
        
        
        
            
        
        
        
        