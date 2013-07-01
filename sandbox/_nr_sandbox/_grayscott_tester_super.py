import decodes as dc
from decodes.core import *
from decodes.extensions.reaction_diffusion import GrayScott
import random
from time import time

import os
path = os.path.expanduser("~") + os.sep + "_decodes_export"
f_prefix = "gs"
random.seed(0.1)

size = Interval(40,40)

x_interval = Interval(0,size.a)
y_interval = Interval(0,size.b)
gen = 10
stepsize = 5
attempts = 2
max_rects = 10




# define corner colors for double interpolation
u0v0 = Color(1,1,1)
u0v1= Color(0,0,0)
u1v0 = Color(1,1,1)
u1v1 = Color(1,0,0)

# 
def rand_interval(ival = Interval(0.0,1.0), divs = 1):
    if divs < 1 : return ival
    result = []
    r_list = [ival.a,ival.b]
    for k in range(divs-1):
        r_list.append(ival.eval(random.random()))  
    r_list.sort()

    return [Interval(r_list[n],r_list[n+1]) for n in range(divs)]


print rand_interval(ival = Interval(0.0,10.0), divs = 2)

for n in range(attempts):
    print "Iteration "+str(n)

    f_name = f_prefix+'_%02d_'% n

    scott = GrayScott(size)

    x_segments = random.choice(range(1,max_rects))
    y_segments = random.choice(range(1,max_rects))

    x_ints = rand_interval(x_interval,x_segments)
    y_ints = rand_interval(y_interval,y_segments)
    
    for x_i in x_ints:
        for y_j in y_ints:
            test = True

            x_list = range(int(x_i.a-.5), int(x_i.b+1.5))
            y_list = range(int(y_j.a-.5), int(y_j.b+1.5))
            if len(x_list) == 1: x_list.append(1+x_list[0])
            if len(y_list) == 1: y_list.append(1+y_list[0])

            x = int(random.choice(x_list))
            y = int(random.choice(y_list))
            x_list.remove(x)
            y_list.remove(y)
            x2 = int(random.choice(x_list))
            y2 = int(random.choice(y_list))

            scott.set_rect(min(x,x2),min(y,y2),abs(x2-x),abs(y2-y))



    #uv_imgs = export_uv(scott)

    t1 = time()
    print "performing "+str(gen)+" generations ",
    for n in range(gen):
        print ".",
        scott.step()
        if gen%stepsize == 0:
            scott.record()
    print
    t2 = time()
    print " took: %f" %(t2-t1)

    print "writing uv images ",
    imgs = scott.to_image_sequence(u0v1,u1v0,u0v0,0.5)
    
    for i,img in enumerate(imgs):
        print ".",
        img.save(f_name+"_uv_%03d"%i, path)
    print

    print "writing u images ",
    imgs = scott.to_image_sequence(v_color = Color(0.0), u_color = Color(0.0), base_color = Color(1.0), power = False, uv_flag = 'u')
    
    for i,img in enumerate(imgs):
        print ".",
        img.save(f_name+"_u_%03d"%i, path)
    print


    print "writing v images ",
    imgs = scott.to_image_sequence(v_color = Color(0.0), u_color = Color(0.0), base_color = Color(1.0), power = False, uv_flag = 'v')
    
    for i,img in enumerate(imgs):
        print ".",
        img.save(f_name+"_v_%03d"%i, path)
    print














raw_input("press enter...")