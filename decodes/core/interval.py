from decodes.core import *
#from . import base, point #here we may only import modules that have been loaded before this one.  see core/__init__.py for proper order

import math, random

class Interval():
    """
    an interval class
    """

    def __init__(self, a=0,b=1):
        """Interval Constructor

        .. todo:: Document this method
        """
        self.a = a
        self.b = b

    def list_int(self): 
        """Returns a list of the interval's start and end values.
        
            :rtype: List of interval's components
        """
        return [self.a, self.b]
        
    def ordered(self): 
        """Returns True if the start value of the interval is smaller than the end value.
        
            :rtype: Boolean value
        """
        return True if self.a < self.b else False
        
    def order(self, copy=False):
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
            :type number: int
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
            :type number: int
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
        """Returns the absolute value of length of the interval.
        
        For a signed representation, use delta
        
            :rtype: int 
        """
        length = self.b - self.a 
        if length > 0: return length
        else: return length *-1
    
    def delta(self): 
        """Returns the signed delta of the interval, calculated as b-a
        
        For an unsigned representation, use length

            :rtype: Number 
        """
        return self.b - self.a
        
    def deval(self, number): 
        """ Reparameterizes between zero and one the value of a number, within an interval.
        
            :param number: Number to reparameterize.
            :type number: float
            :rtype: Reparameterized number. 
        """ 
        if number >= self.a and number <= self.b: return float(number-self.a)/float(self.delta())
        elif self.delta() <= 0 and number <= self.a and number >= self.b: return float(number-self.a)/float(self.delta())
        else: raise ValueError('The number is not within the range')
        
    def eval(self, number):
        """ Evaluates a number between zero and one in a range.
        
            :param number: Number to evaluate.
            :type number: float
            :rtype: Evalauted number. 
        """  
        if number >= 0 and number <= 1: return (self.delta() * number) + self.a
        else: raise ValueError('The number is not within the range')
    
    @staticmethod
    def remap(val, source_interval, target_interval=None): 
        """ Translates a number from its position within the source interval to its relative position in the target interval.
        
            :param val: Number to remap.
            :type val: float
            :rtype: Translated number. 
        """  
        if target_interval==None: target_interval = Interval(0,1)

        t = source_interval.deval(val)
        return target_interval.eval(t)

