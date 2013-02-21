from decodes.core import *

import math, random

class Interval():
    """
    an interval class
    """

    def __init__(self, a=0,b=1):
        """Interval Constructor.
        
            :param a: First number of the interval.
            :type a: Number.
            :param b: Second number of the interval.
            :type a: Number.
            :rtype: Interval object.
        """
        self.a = a
        self.b = b
    
    def __div__(self, other): 
        """
        overloads the division **(/)** operator
        calls Interval.divide(other)
        """
        return self.divide(other)

    def __floordiv__(self, other): 
        """
        overloads the integer division **(//)** operator
        calls Interval.subinterval(other)
        """
        return self.subinterval(other)

    def __contains__(self, number):
        """
        overloads the containment **(in)** operator
        calls Interval.subinterval(other)
        """
        ival = self.order()
        return (ival.a <= number) and (ival.b >= number)

    @property
    def list(self): 
        """Returns a list of the interval's start and end values.
        
            :rtype: List of interval's components
        """
        return [self.a, self.b]
        
    @property
    def is_ordered(self): 
        """Returns True if the start value of the interval is smaller than the end value.
        
            :rtype: Boolean value
        """
        return True if self.a < self.b else False

    @property
    def length(self):
        """Returns the absolute value of length of the interval.
        
        For a signed representation, use delta
        
            :rtype: int 
        """
        length = self.b - self.a 
        if length > 0: return length
        else: return length *-1
    
    @property
    def delta(self): 
        """Returns the signed delta of the interval, calculated as b-a
        
        For an unsigned representation, use length

            :rtype: Number 
        """
        return float(self.b - self.a)

    def order(self):
        """Returns a copy of this interval with ordered values, such that a < b
        
        """
        if self.is_ordered: return Interval(self.a, self.b)
        else: return Interval(self.b, self.a)

    def invert(self):
        """Returns a copy of this interval with swapped values.
        Such that this.a = new.b and this.b = new.a
        
        """
        return Interval(self.b, self.a)
    
    def divide(self, divs=10, include_last=False):
        """Divides this interval into a list of values equally spaced between a and b.
        Unless include_last is set to True, returned list will not include Interval.b: the first value returned is Interval.a and the last is Interval.b-(Interval.delta/divs)
        
            :param divs: Number of interval divisions.
            :type divs: int
            :rtype: List of numbers in which a list is divided. 
        """
        step = self.delta/float(divs)
        if include_last : divs += 1
        return [self.a+step*n for n in range(divs)]
    
    def subinterval(self, divs):
        """Divides an interval into a list of equal size subintervals(interval objects).
        
            :param divs: Number of subintervals.
            :type divs: int
            :rtype: List of subintervals (interval objects). 
        """
        return [Interval(n,n+self.delta/float(divs)) for n in self.divide(divs)]
    
        
    def deval(self, number): 
        """ 
        Returns a parameter cooresponding to the position of the given number within this Interval.
        Effectively, the opposite of eval()

            :param number: Number to find the parameter of.
            :type number: float
            :rtype: parameter

        ::
            
            print Interval(10,20).deval(12)
            >>0.2
            print Interval(10,20).deval(25)
            >>1.5

        """ 
        return (number-self.a) / self.delta
        
    def eval(self, t):
        """ Evaluates a given parameter within this interval.
        
            :param t: Number to evaluate.
            :type t: float
            :rtype: Evalauted number. 

        ::
            
            print Interval(10,20).eval(0.2)
            >>12
            print Interval(10,20).deval(1.5)
            >>25

        """  
        return self.delta * t + self.a
    
    def __repr__(self): return "ival[{0},{1}]".format(self.a,self.b)



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

