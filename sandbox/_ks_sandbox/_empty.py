import decodes as dc
from decodes.core import *
#import decodes.unit_tests


cs = CS.on_xy(1,1,x_vec=Vec(0,1))
cs = CS()
pt_a = cs.eval_cyl(1,math.pi,0)
pt_b = cs.eval_cyl(1,math.pi/2,0)
pt_c = cs.eval_cyl(1,math.pi*3/2,0)

pt_d = cs.eval_cyl(1,math.pi+0.1,0)
pt_e = cs.eval_cyl(1,math.pi-0.1,0)

print pt_a
print cs.deval_cyl(pt_a)

print pt_b
print cs.deval_cyl(pt_b)

print pt_c
print cs.deval_cyl(pt_c)

print cs.deval_cyl(pt_d)
print cs.deval_cyl(pt_e)

raw_input("press enter...")