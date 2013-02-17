from decodes.core import *
#from . import base, point #here we may only import modules that have been loaded before this one.  see core/__init__.py for proper order

import math, random

class Interval():
    def __init__(self, a=0,b=1):
        self.a = a
        self.b = b

    def list_int(self): return [self.a, self.b]
        """Returns a list of the interval's start and end values.
        
            :rtype: List of interval's components
        """
        
    def ordered(self): return True if self.a < self.b else False
        """Returns True if the start value of the interval is smaller than the end value.
        
            :rtype: Boolean value
        """
        
    def order(self, copy=False):
    #def makeOut(outtype, name="untitled", path=False):
        """Returns a list of interval components ordered from smaller to larger.
        
            :param copy: Specify whether you want to modify the original interval or create a new ordered one.
            :type copy: True or False
            :rtype: Ordered list of domain components.
        """
        if self.ordered() == True: return [self.a, self.b]
        else:
            if copy == True:
                a, b = self.b, self.a
                return [a,b]
            else:
                self.a, self.b = self.b, self.a
                return [self.a, self.b]
            
    def division(self, number):
        """Divides an interval into a list of values with equal size.
        
            :param number: Number of interval divisions.
            :type number: integer
            :rtype: List of numbers in which a list is divided. 
        """
        step = float(self.delta())/float(number-1)
        r = self.a
        division = [self.a]
        if self.delta() < 0: r, step = r*-1,  step*-1
        while r < (self.b): 
            r += step
            division.append(r)
        return division
    
    def subdomain(self, number):
        """Divides an interval into a list of equal size subdomains(interval objects).
        
            :param number: Number of interval subdomains.
            :type number: integer
            :rtype: List of subdomains (interval objects). 
        """
        step = float(self.delta())/float(number-1)
        r = self.a
        division = [Interval(self.a,step)]
        if self.delta() < 0: r, step = r*-1,  step*-1
        while r < (self.b): 
            start = step
            r += step
            division.append(Interval(start, r))
        return division
    
    def length(self):
        """Returns the absolut length of the interval
        
            :rtype: Number 
        """
        length = self.b - self.a 
        if length > 0: return length
        else: return length *-1
    
    def delta(self): return self.b - self.a
        """Returns the length of the interval
        
            :rtype: Number 
        """
        #
    def deval(self, number): # Return the number a percentage refers to
        """ Reparameterizes between zero and one the value of a number, within an interval.
        
            :param number: Number to reparameterize.
            :type number: float
            :rtype: Reparameterized number. 
        """ 
        if number > self.a and number < self.b: return float(number-self.a)/float(self.delta())
        elif self.delta() < 0 and number < self.a and number > self.b: return float(number-self.a)/float(self.delta())
        else: raise ValueError('The number is not within the range')
        
    def eval(self, number):
        """ Evaluates a number between zero and one in a range.
        
            :param number: Number to evaluate.
            :type number: float
            :rtype: Evalauted number. 
        """  
        if number >= 0 and number <= 1: return (self.delta() * number) + self.a
        else: raise ValueError('The number is not within the range')
    
    def remap(self, number, target=None): 
        """ Translates a number in an interval into a new interval.
        
            :param number: Number to remap.
            :type number: float
            :rtype: Translated number. 
        """  
        if target==None: target =Interval(0,1)
        if number > self.a and number < self.b: 
            return target.eval(self.deval(number))
        elif self.delta() < 0 and number < self.a and number > self.b:
            return target.eval(self.deval(number))
        else: raise ValueError('The number is not within the range')

