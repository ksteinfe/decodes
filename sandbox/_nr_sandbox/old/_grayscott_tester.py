import decodes as dc
from decodes.core import *
from decodes.extensions.reaction_diffusion import GrayScott
import random
from time import time

import os
path = os.path.expanduser("~") + os.sep + "_decodes_export"
f_prefix = "gs_04"
random.seed(0.1)



def export_uv(scott=GrayScott(), v_color = Color(0.0), u_color = Color(0.0), base_color = Color(1.0), power = False):
#    ival_u = Interval(scott.min_recorded_u,scott.max_recorded_u)
#    ival_v = Interval(scott.min_recorded_v,scott.max_recorded_v)
    ival_u = Interval(0.0,1.0)
    ival_v = Interval(0.0,1.0)

#    uv_color = Color.interpolate(u_color,v_color)        
    imgs = []

    img_u = Image(Interval(scott.width,scott.height),base_color)

    for px in range(len(scott.hist_u[0]._pixels)):
        ut = ival_u.deval(scott.hist_u[0]._pixels[px])
        if power:
            c = Color.interpolate(base_color,u_color,ut**power)
        else:
            c = Color.interpolate(base_color,u_color,ut)

        img_u._pixels[px]= c

    imgs.append(img_u)

    img_v = Image(Interval(scott.width,scott.height),base_color)


    for px in range(len(scott.hist_v[0]._pixels)):
        vt = ival_v.deval(scott.hist_v[0]._pixels[px])
        if power:
            c = Color.interpolate(base_color,v_color,vt**power)
        else:
            c = Color.interpolate(base_color,v_color,vt)

        img_v._pixels[px]= c

    imgs.append(img_v)


    return imgs


# define corner colors for double interpolation
u0v0 = Color(1,1,1)
u0v1= Color(0,0,0)
u1v0 = Color(1,1,1)
u1v1 = Color(1,0,0)



scott = GrayScott(Interval(100,100))
'''
scott.set_rect(3,3,3,3)
scott.set_rect(13,13,3,2)
scott.set_rect(18,4,3,8)
'''
scott.set_rect(60,60,60,60)
scott.set_rect(65,65,15,10)
scott.set_rect(90,20,15,40)
scott.record()
#scott.log_uv()

#uv_imgs = export_uv(scott)


gen = 50
stepsize = 5
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
'''
uv_imgs = []
uv_imgs.append(scott.to_image(v_color = Color(0.0), u_color = Color(0.0), base_color = Color(1.0), power = False, uv_flag = 'u', gen = 0))
uv_imgs.append(scott.to_image(v_color = Color(0.0), u_color = Color(0.0), base_color = Color(1.0), power = False, uv_flag = 'v', gen = 0))
uv_imgs[0].save(f_prefix+"_u", path)
uv_imgs[1].save(f_prefix+"_v", path)
'''
print "writing uv images ",
imgs = scott.to_image_sequence(u0v1,u1v0,u0v0,0.5)
    
for i,img in enumerate(imgs):
    print ".",
    img.save(f_prefix+"_uv_%03d"%i, path)
print

print "writing u images ",
imgs = scott.to_image_sequence(v_color = Color(0.0), u_color = Color(0.0), base_color = Color(1.0), power = False, uv_flag = 'u')
    
for i,img in enumerate(imgs):
    print ".",
    img.save(f_prefix+"_u_%03d"%i, path)
print


print "writing v images ",
imgs = scott.to_image_sequence(v_color = Color(0.0), u_color = Color(0.0), base_color = Color(1.0), power = False, uv_flag = 'v')
    
for i,img in enumerate(imgs):
    print ".",
    img.save(f_prefix+"_v_%03d"%i, path)
print

# gs.put(scott)












raw_input("press enter...")