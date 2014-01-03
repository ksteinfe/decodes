from decodes.core import *
import math, random


class Interval():
    """
    an interval class
    """

    def __init__(self, a=0,b=1):
        """Interval Constructor.
        
            :param a: First number of the interval.
            :type a: float
            :param b: Second number of the interval.
            :type a: float
            :returns: Interval Object.
            :rtype: Interval.
        """
        self.a = float(a)
        self.b = float(b)
    
    def __truediv__(self,divs): return self.__div__(divs)
    def __div__(self, divs): 
        """overloads the division **(/)** operator
        calls Interval.divide(divs)
        
            :returns: List of numbers in which a list is divided. 
            :rtype: list
        """
        return self.divide(divs)

    def __floordiv__(self, other): 
        """overloads the integer division **(//)** operator
        calls Interval.subinterval(other)
        """
        return self.subinterval(other)

    def __add__(self, val):
        """Overloads the addition **(+)** operator. 
        """    
        return Interval(self.a + val, self.b + val)
    def __sub__(self, val): 
        """Overloads the addition **(-)** operator. 
        """    
        return Interval(self.a - val, self.b - val)

    def __contains__(self, number):
        """
        overloads the containment **(in)** operator
        """
        ival = self.order()
        return (ival.a <= number) and (ival.b >= number)

    def __eq__(self, other): 
        """Overloads the equal **(==)** operator.
        
            :param other: Interval to be compared.
            :type other: Interval
            :result: Boolean result of comparison
            :rtype: bool
        """
        return all([self.a==other.a,self.b==other.b])

    @property
    def list(self): 
        """Returns a list of the interval's start and end values.
        
            :returns: List of interval's components
            :rtype: list
        """
        return [self.a, self.b]
        
    @property
    def is_ordered(self): 
        """Returns True if the start value of the interval is smaller than the end value.
        
            :returns: Boolean value
            :rtype: bool
        """
        return True if self.a < self.b else False

    @property
    def length(self):
        """Returns the absolute value of length of the interval.
        
        For a signed representation, use delta
        
            :returns: Absolute value of length of an interval.
            :rtype: int 
        """
        length = self.b - self.a 
        if length > 0: return length
        else: return length *-1
    
    @property
    def delta(self): 
        """Returns the signed delta of the interval, calculated as b-a
        
        For an unsigned representation, use length

            :returns: Delta of an interval.
            :rtype: float 
        """
        return float(self.b - self.a)

    @property
    def mid(self):
        """
        """
        return self.eval(0.5)

    def order(self):
        """Returns a copy of this interval with ordered values, such that a < b
        
            :returns: Ordered copy of Interval object.
            :rtype: Interval 
        """
        if self.is_ordered: return Interval(self.a, self.b)
        else: return Interval(self.b, self.a)

    def invert(self):
        """Returns a copy of this interval with swapped values.
        Such that this.a = new.b and this.b = new.a
        
            :returns: Interval object with swapped values.
            :rtype: Interval 
        """
        return Interval(self.b, self.a)
    
    def divide(self, divs=10, include_last=False):
        """Divides this interval into a list of values equally spaced between a and b.
        Unless include_last is set to True, returned list will not include Interval.b: the first value returned is Interval.a and the last is Interval.b-(Interval.delta/divs)
        
            :param divs: Number of interval divisions.
            :type divs: int
            :returns: List of numbers in which a list is divided. 
            :rtype: list
        """
        step = self.delta/float(divs)
        if include_last : divs += 1
        return [self.a+step*n for n in range(divs)]
    
    def subinterval(self, divs):
        """Divides an interval into a list of equal size subintervals(interval objects).
        
            :param divs: Number of subintervals.
            :type divs: int
            :returns: List of subintervals (interval objects). 
            :rtype: list
        """
        return [Interval(n,n+self.delta/float(divs)) for n in self.divide(divs)]

    def rand_interval(self, divs):
        """ Divides an interval into a list of randomly sized subintervals(interval objects).
        
            :param divs: Number of subintervals.
            :type divs: int
            :returns: List of subintervals (interval objects). 
            :rtype: list
        """
        if divs < 1 : return ival
        result = []
        r_list = [self.a,self.b]
        r_list.extend(self.eval(random.random()) for k in range(divs-1)) 
        r_list.sort()

        return [Interval(r_list[n],r_list[n+1]) for n in range(divs)]
           
    def deval(self, number): 
        """ 
        Returns a parameter cooresponding to the position of the given number within this Interval.
        Effectively, the opposite of eval()

            :param number: Number to find the parameter of.
            :type number: float
            :returns: Parameter.
            :rtype: float

        ::
            
            print Interval(10,20).deval(12)
            >>0.2
            print Interval(10,20).deval(25)
            >>1.5

        """ 
        if self.delta == 0 : raise ZeroDivisionError("This interval cannot be devaluated because the delta is zero")
        return (number-self.a) / self.delta
        
    def eval(self, t,limited=False):
        """ Evaluates a given parameter within this interval.
            For example, given an Interval(0->2*math.pi): eval(0.5) == math.pi
             Optionally, you may limit the resulting output to this interval
            :param t: Number to evaluate.
            :type t: float
            :returns: Evalauted number. 
            :rtype: float

        ::
            
            print Interval(10,20).eval(0.2)
            >>12.0
            print Interval(10,20).deval(1.5)
            >>25.0

        """  
        ret = self.delta * t + self.a
        if not limited : return ret
        return self.limit_val(ret)

    def limit_val(self, n):
        """
        Limits a given value to the min and max of this Interval
        """
        if n < self.a : return self.a
        if n > self.b : return self.b
        return n
    
    def __repr__(self): return "ival[{0},{1}]".format(self.a,self.b)

    @staticmethod
    def encompass(values):
        pass
        return Interval()

    @staticmethod
    def remap(val, source_interval, target_interval=None, limited=False): 
        """ Translates a number from its position within the source interval to its relative position in the target interval.  Optionally, you may limit the resulting output to the target interval
        
            :param val: Number to remap.
            :type val: float
            :returns: The given number remapped to the target interval.
            :rtype: float
        """  
        if target_interval is None: target_interval = Interval(0,1)

        t = source_interval.deval(val)
        return target_interval.eval(t,limited)

    @staticmethod
    def twopi():
        """Creates an interval from 0->2PI
        
            :rtype: Interval
        """
        return Interval(0,math.pi*2)

    @staticmethod
    def pi():
        """Creates an interval from 0->PI
        
            :rtype: Interval
        """
        return Interval(0,math.pi)
