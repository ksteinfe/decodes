import unittest, math
import decodes.core 
from decodes.core import *


class Tests(unittest.TestCase):
    interval = Interval()
    def test_empty_constructor(self):
        inter_test = Interval(0,1)
        self.assertEqual(self.interval,inter_test,"intervals with empty constructors are from 0 to 1")
        self.assertEqual(self.interval.a,inter_test.a)
        self.assertEqual(self.interval.b,inter_test.b)

    def test_properties(self):
        self.assertEqual(self.interval.list,[0,1])
        self.assertEqual(self.interval.is_ordered,True)
        self.assertEqual(self.interval.length,1)
        self.assertEqual(self.interval.delta,1)
        self.assertEqual(self.interval.is_ordered,True)
        
    def test_operations(self):
        inter_test = Interval(5,2)
        self.assertEqual(inter_test.order,Interval(2,5))
        self.assertEqual(inter_test.invert,Interval(2,5))
        self.assertEqual(inter_test.divide,range(5,2,.3))
        self.assertEqual(inter_test.divide(include_last=True),range(5,2.3,.3))
        self.assertEqual(inter_test.subinterval(2),[Interval(5,3.5),Interval(3.5,2)])
        
    def test_operations(self):
        inter_test = Interval(0,math.pi*2)
        self.assertEqual(inter_test.eval(0.5),math.pi)
        self.assertEqual(inter_test.deval(math.pi),0.5)
        self.assertEqual(Interval.remap(.5, Interval(), Interval(0,10)),5)
        


