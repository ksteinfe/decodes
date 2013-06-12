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
        self.a = a
        self.b = b
    
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
        calls Interval.subinterval(other)
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
        
    def eval(self, t):
        """ Evaluates a given parameter within this interval.
            For example, given an Interval(0->2*math.pi): eval(0.5) == math.pi
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
        return self.delta * t + self.a
    

    
    def __repr__(self): return "ival[{0},{1}]".format(self.a,self.b)



    @staticmethod
    def remap(val, source_interval, target_interval=None): 
        """ Translates a number from its position within the source interval to its relative position in the target interval.
        
            :param val: Number to remap.
            :type val: float
            :returns: The given number remapped to the target interval.
            :rtype: float
        """  
        if target_interval is None: target_interval = Interval(0,1)

        t = source_interval.deval(val)
        return target_interval.eval(t)

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

class Bounds(Geometry):
    """
    A 2d or 3d boudary class
    """
    def __init__ (self, **kargs):
        """
        a Bounds may be constructed two ways: By setting "center", "dim_x", "dim_y", and optionally "dim_z" OR by setting "ival_x", "ival_y", and optionally "ival_z"
        """
        try:
            self.cpt = center
            self.w2 = width/2.0
            self.h2 = height/2.0
        except:
            try:
                print kargs['ival_x']

            except:
                raise AttributeError

    @property
    def ival_x(self):
        return Interval(self.cpt.x-(self.w2),self.cpt.x+(self.w2))
    @property
    def ival_y(self):
        return Interval(self.cpt.y-(self.h2),self.cpt.y+(self.h2))

    @property
    def cpt(): 
        return Point()


    @property
    def corners(self):
        """
        starts at bottom left and moves clockwise
        """
        cpts = []
        cpts.append(Point(self.cpt.x-(self.w2),self.cpt.y-(self.h2)))
        cpts.append(Point(self.cpt.x-(self.w2),self.cpt.y+(self.h2)))
        cpts.append(Point(self.cpt.x+(self.w2),self.cpt.y+(self.h2)))
        cpts.append(Point(self.cpt.x+(self.w2),self.cpt.y-(self.h2)))
        return cpts
        
    def contains(self, pt):
        lbx = self.cpt.x - self.w2
        ubx = self.cpt.x + self.w2
        lby = self.cpt.y - self.h2
        uby = self.cpt.y + self.h2
        if lbx <= pt.x < ubx and lby <= pt.y < uby : return True
        else:return False
    
    def overlaps(self, other) :
        for p in other.corners :
            if self.contains(p) : return True
        for p in self.corners :
            if other.contains(p) : return True
        return False
        