from ..core import *
from ..core import dc_color, dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_xform
import copy
print "lsystem.py loaded"



class LEngine(object):

    def __init__(axiom):
        self.axiom = axiom
        self.rules = []
        self.clear()

    def add_rule(self,rulething):
        # check on structure of rulething and convert to proper format
        rule = rulething
        self.rules.append(rule)

    def clear(self):
        self.hist = [axiom]

    @property
    def cur_gen(): return self.hist[-1]
    
    def step(self):
        # grab the latest generation
        # self.cur_gen

        # apply the rules to construct a string
        nxt_gen = ""
        #apply_rule()

        # add this string to our history
        self.hist.append(nxt_gen)

    def apply_rule(rule, char):
        # if the rule matches char, return rule replacement
        # otherwise return false
        return False


class LTurtle(object):

    def __init__():
        pass