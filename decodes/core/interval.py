from decodes.core import *
from . import base, point #here we may only import modules that have been loaded before this one.  see core/__init__.py for proper order

import math, random

class Interval():
    def __init__(self, a=0,b=1):
        self.a = a
        self.b = b
    
    def ordered(self): return True if self.a > self.b else False
    
    def order(self):
        if ordered(self) == True:
            self.a = a
            self.b = b
        else:
            self.a = b
            self.b = a
    
    def number_list(self):
        pass
    
    def evaluate(self, number):
        if number > self.a and number < self.b: return self.b - self.a/number - self.a
        else: raise ValueError('The number is not within the range')
        
    def percent_evaluate(self, number):
        if number >= 0 and number <= 1: return self.b - self.a * number - self.a
        else: raise ValueError('The number is not within the range')
    
    @property
    def remap(self, number, target=Interval(a=0,b=1)): #remap = default 0 to 1 both source and target
        if number > self.a and number < self.b: 
            return ((target.b-target.a) * percent_evaluate(self, number))/1 
        else: raise ValueError('The number is not within the range')

