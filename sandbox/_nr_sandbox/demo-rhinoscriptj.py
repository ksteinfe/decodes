import decodes as dc
from decodes.core import *
from decodes.io import *

outie = dc.make_out(dc.Outies.Rhino, "wayout")

u= 10
v = 10
x = .8
y = 1.2
"""
Define a two parametric surfaces
"""
def func_a(u,v): 
    u1 = u*x
    v1 = v*y
    return Point(u,v,(u1**3-3*u1*(v1**2))/4)
    
# eval function for a handkerchief surface
def func_b(u,v): 
    u1 = u*x
    v1 = v*y
    return Point(u,v,((1/3)*u1**3+u1*v1**2+2*(u1**2-v1**2))/4 )

func = func_a

# create surface over domain -1 to 1
surf = Surface(func,Interval(-1,1),Interval(-1,1))

meshes = surf.to_mesh(divs_u=u,divs_v=v)

outie.put(meshes)
outie.draw()