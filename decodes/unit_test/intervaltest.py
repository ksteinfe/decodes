import decodes.core 
from decodes.core import *

print 'Constructors'
interval = Interval(2,0)
a = interval.a
b = interval.b

print 'Interval List'
list = interval.list_int()
division = interval.division(3)
subdomain = interval.subdomain(3)

print 'Interval Order' 
order = interval.order()
interval_2 = Interval(5,2)
order_interval = interval_2.order(copy=True)
interval_2.order() # mutate_interval

print 'Evaluators'
eval_int = Interval(2,0)
length = eval_int.length()
delta = eval_int.delta()
deval = eval_int.deval(1.25)
eval = eval_int.eval(.5)
remap = eval_int.remap(1,Interval(0,4))