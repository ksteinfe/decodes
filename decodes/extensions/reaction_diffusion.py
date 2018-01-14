from ..core import *
from ..core import dc_color, dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon, dc_xform
import copy
print("reaction_diffusion.py loaded")

class GrayScott (object):

    def __init__(self, dimensions=Interval(20,20)):
        self.width = dimensions.a
        self.height = dimensions.b

        # set default coefficients
        self.f, self.k = 0.023, 0.077
        self.du, self.dv = 0.095, 0.03

        self.clear()

    def k_at(self,x,y):
        return self.k

    def f_at(self,x,y):
        return self.f
    
    def set_u(self,x,y,val):
        x,y = self._reframe(x,y)
        self._uvals.set(x,y,val)

    def set_v(self,x,y,val):
        x,y = self._reframe(x,y)
        self._vvals.set(x,y,val)

    def get_u(self,x,y): return self._uvals.get(x,y)
    def get_v(self,x,y): return self._vvals.get(x,y)

    def set_rect(self,x,y,w,h):
        x,y,w,h = int(x),int(y),int(w),int(h)
        for xi in range(x,x+w):
            for yi in range(y,y+h):
                self.set_u(xi,yi,0.5)
                self.set_v(xi,yi,0.25)

    def _reframe(self,x,y):
        while x > self.width -1 : x = x - self.width
        while y > self.height -1: y = y - self.height
        while x < 0 : x = self.width + x
        while y < 0 : y = self.height + y
        return x,y

    def clear(self):
        self._uvals = ValueField(Interval(self.width,self.height),1.0)
        self._vvals = ValueField(Interval(self.width,self.height))
        self.step_count = 0
        self.hist_u = []
        self.hist_v = []
        
        self.max_recorded_u = 0.0
        self.min_recorded_u = 1.0
        self.max_recorded_v = 0.0
        self.min_recorded_v = 1.0

    def record(self):
        self.hist_u.append(self._uvals)
        self.hist_v.append(self._vvals)

    def to_image(self, v_color = Color(0.0), u_color = Color(1.0), base_color = Color(1.0), power = False, uv_flag = 'uv', gen = 0):
        ival_u = Interval(self.min_recorded_u,self.max_recorded_u)
        ival_v = Interval(self.min_recorded_v,self.max_recorded_v)
        uv_color = Color.interpolate(u_color,v_color)        
        imgs = []

        img = Image(Interval(self.width,self.height),base_color)

        for px in range(len(img._pixels)):
            ut = ival_u.deval(self.hist_u[gen]._pixels[px])
            vt = ival_v.deval(self.hist_v[gen]._pixels[px])
            if power:
                if uv_flag == 'uv':
                    c0 = Color.interpolate(base_color,u_color,ut**power)
                    c1 = Color.interpolate(v_color,uv_color,ut**power)
                    c = Color.interpolate(c0,c1,vt**power)
                elif uv_flag == 'u':
                    c = Color.interpolate(base_color,u_color,ut**power)
                elif uv_flag == 'v':
                    c = Color.interpolate(base_color,v_color,vt**power)
            else:
                if uv_flag == 'uv':
                    c0 = Color.interpolate(base_color,u_color,ut)
                    c1 = Color.interpolate(v_color,uv_color,ut)
                    c = Color.interpolate(c0,c1,vt)
                elif uv_flag == 'u':
                    c = Color.interpolate(base_color,u_color,ut)
                elif uv_flag == 'v':
                    c = Color.interpolate(base_color,v_color,vt)
            img._pixels[px]= c

        return img

    def to_image_sequence(self, v_color = Color(0.0), u_color = Color(1.0), base_color = Color(1.0), power = False, uv_flag = 'uv'):
    
        imgs = []
        for n in range(len(self.hist_u)):
            img = self.to_image(v_color, u_color, base_color, power, uv_flag, n)

            imgs.append(img)
        return imgs

    def log_uv(self,u,v):
        if u > self.max_recorded_u : self.max_recorded_u = u
        if u < self.min_recorded_u : self.min_recorded_u = u
        if v > self.max_recorded_v : self.max_recorded_v = v
        if v < self.min_recorded_v : self.min_recorded_v = v

    def step(self, t=1.0):
        nxt_uvals = ValueField(Interval(self.width,self.height),0.0)
        nxt_vvals = ValueField(Interval(self.width,self.height),0.0)
        t = max(min(1.0,t),0.0)
        for x in range(0,self.width):
            for y in range(0,self.height):
                cur_f = self.f_at(x,y)
                cur_k = self.k_at(x,y)
                cur_u = self._uvals.get(x,y)
                cur_v = self._vvals.get(x,y)
                d2 = cur_u * cur_v * cur_v
                neighbors_u = self._uvals.neighbors_of(x,y)
                neighbors_v = self._vvals.neighbors_of(x,y)

                nxt_u = cur_u + t * ((self.du * ( sum(neighbors_u) - 4.0 * cur_u) - d2) + cur_f * (1.0 - cur_u))
                nxt_v = cur_v + t * ((self.dv * ( sum(neighbors_v) - 4.0 * cur_v) + d2) - cur_k * cur_v)

                nxt_uvals.set(x,y,max(0.0,nxt_u))
                nxt_vvals.set(x,y,max(0.0,nxt_v))
                self.log_uv(nxt_u,nxt_v)
        
        self._uvals = nxt_uvals
        self._vvals = nxt_vvals
        self.step_count += 1

        
