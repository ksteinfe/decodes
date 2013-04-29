import decodes as dc
from decodes.core import *
from decodes.io import *
from decodes.io.pyautocad import *

acad = Autocad(False,  True)

outie = dc.makeOut(dc.Outies.ACAD, "wayout")

# Surface Parameters
rad_0 = 0.4
rad_1 = 0.22
ipt = Point(1.0,1.0,0.0)

# u_val Parameters
count_u = 15
skew_u = 0.5
ival_u = Interval(0, math.pi)

# v_val Parameters
count_v = 15
skew_v = 0.9
ival_v = Interval(0, math.pi)

# Surface Function
tvec = Vec(0,-3,0) # to move the thing away from origin
def func(u,v):
    x = (rad_0+rad_1*math.cos(v))*math.cos(u)
    y = (rad_0+rad_1*math.cos(v))*math.sin(u)
    z = rad_1 * math.sin(v)
    
    vec = Vec(ipt,Point(x,y,z))
    vec.length = 1/vec.length
    return ipt + vec + tvec

# Sqrt Distribution U_Vals
s = Interval(0.00001,4.0).eval(skew_u) # 0 < s < 4.0
def f(x):
    x = x - 0.5
    y = 0.0
    if x < 0 :
        y = -math.sqrt(-x) ** s
    if x > 0:
        y = math.sqrt(x) ** s
    return y

def u_vals(count, skew, ival):
    vals = []
    ival_y = Interval(f(0),f(1))
    for x in Interval().divide(count,include_last = True):
        y = f(x)
        vals.append(ival.eval(ival_y.deval(y)))
    return vals

# Sqrt Distribution V_Vals
def v_vals(count, skew, ival):
    vals = []
    for x in Interval().divide(count,include_last = True):
        s = Interval(0.5,1.5).eval(skew) # 0.5 < s < 1.5
        y = x**(s**10)# 0 < y < 1
        vals.append(ival.eval(y))
    return vals
        
u_vals = u_vals(count_u, skew_u, ival_u)
v_vals = v_vals(count_v, skew_v, ival_v)

msh = Mesh()
for v in v_vals:
    for u in u_vals:
        msh.append(func(u,v))

res_u = len(u_vals)

# simple triangulation style
for v in range(len(v_vals)-1):
    row = v*res_u
    for u in range(len(u_vals)-1):
        pi_0 = row+u
        pi_1 = row+u+1
        pi_2 = row+u+res_u+1
        pi_3 = row+u+res_u
        msh.add_face(pi_0,pi_1,pi_3,pi_2)

outie.put(msh)
outie.draw()
