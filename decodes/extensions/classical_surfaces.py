import decodes.core as dc
from decodes.core import *
import math


class ClassicalSurface(Surface):
    def __init__(self, function, dom_u=Interval(0,1), dom_v=Interval(0,1), tol_u=None, tol_v=None):
        
        if function is not None : self._func = function
        self._dom = dom_u, dom_v
        self._tol = self.tol_max
        if tol_u is not None : self.tol_u = tol_u
        if tol_v is not None : self.tol_v = tol_v

        for u,v in [(self.u0,self.v0),(self.u0,self.v1),(self.u1,self.v1),(self.u1,self.v0)]:
            try:
                pt = self.func(u,v)
                pt.x
                pt.y
                pt.z
            except:
                raise GeometricError("Surface not valid: The given function does not return a point at parameter %s, %s"%(u,v))


    def deval_pln(self,u,v):
        raise NotImplementedError("deval_pln not implemented. I am a BAD ClassicalSurface!")

    def deval_crv(self,u,v):
        raise NotImplementedError("deval_crv not implemented. I am a BAD ClassicalSurface!")

    def isocurve(self, u_val=None, v_val=None):
        raise NotImplementedError("isocurve not implemented. I am a BAD ClassicalSurface!")



class RotationalSurface(ClassicalSurface):
    # rotational surfaces are constrained to rotational axis that pass thru the world origin
    
    def __init__(self, generator, axis=Ray(Point(), Vec(0,0,1)), dom_u=Interval.twopi(), tol_u=None):
        '''
        the given generator curve will be rotated about an axis through the center and defined by given vector
        '''
        self.genx = generator
        self.center = axis._pt
        self.axis = axis._vec

        def func(u,v):
            pt = self.genx.eval(v)
            xf = Xform.rotation(angle = dom_u.eval(u), center = self.center, axis = self.axis)        
            return pt*xf

        try:
            dom_v = self.genx.domain
            tol_v = self.genx.tol
        except:
            dom_v = Interval()
            tol_v = 1.0/10.0

        super(RotationalSurface,self).__init__(func,Interval(),Interval(),tol_u,tol_v)

    def deval_pln(self,u,v,flip_ang_tol=0.0001):
        xf = Xform.rotation(angle=u,axis=self.axis)
        pln_crv = self.genx.deval_pln(v) * xf
        axis_pt = Point(self.axis.to_line().near_pt(pln_crv.origin))

        try:
            pln = Plane(pln_crv.origin, pln_crv.normal.cross(axis_pt).cross(pln_crv.normal))
            # doesn't work in all situations
            # if self.axis.angle(axis_pt) < flip_ang_tol : pln.normal = pln.normal.inverted()
        except:
            # seems to only happen when evaluated point lies at (0,0), but may happen when evaluated pt lies on axis
            return super(ClassicalSurface,self).deval_pln(u,v)

        return pln

    def deval_crv(self,u,v):
        # we could re-implement deval_crv here in the context of this classical surface type, or we could pass the buck to our general Surface class
        return super(ClassicalSurface,self).deval_crv(u,v)

    def isocurve(self, u_val=None, v_val=None):
        if u_val is None and v_val is None: raise AttributeError("Surface.isocurve requires either u_val OR v_val to be set")
        if u_val is not None and v_val is not None: raise AttributeError("u_val AND v_val cannot both be set when generating a Surface.isocurve")
        
        # if plotting a u-iso, return an Arc
        if u_val is None:
            pt_0 = self.func(0,v_val)
            pt_1 = self.func(0.5,v_val)
            pt_2 = self.func(1,v_val)
            return Arc.thru_pts(pt_0, pt_1,pt_2)
        # else if plotting a v-iso, return rotated Curve
        else :            
             iso = copy.copy(self.genx)
             if iso.is_baseless:
                iso.basis = CS()*Xform.rotation(angle=u_val,axis=self.axis)
             else:
                 iso.basis = iso.basis*Xform.rotation(angle=u_val,axis=self.axis)

             try:
                 iso._rebuild_surrogate()
             except:
                 pass
             return iso


class TranslationalSurface(ClassicalSurface):
    
    def __init__(self, generator, directrix, origin, tol_v=None):
        '''
        the given generator curve will be translated along the given directrix curve
        '''
        self.genx = generator
        self.dirx = directrix
        self.origin = origin #intersection of the generator and directrix curves

        def func(u,v):                 
            vec = self.dirx.eval(u) - origin
            return self.genx.eval(v) + vec
            
        try:
            tol_u = self.dirx.tol
            tol_v = self.genx.tol
        except:
            tol_u = 1.0/10.0
            tol_v = 1.0/10.0

        super(TranslationalSurface,self).__init__(func,Interval(), Interval(),tol_u,tol_v)

    def deval_pln(self,u,v):
        pln_crv = self.genx.deval_pln(u)

        pt = self._func(u,v)
        return Plane(pt, pln_crv.normal.cross(self.vec)) ### this will break, no longer uses self.vec


    def deval_crv(self,u,v):
        # we could re-implement deval_crv here in the context of this classical surface type, or we could pass the buck to our general Surface class
        return super(ClassicalSurface,self).deval_crv(u,v)

    def isocurve(self, u_val=None, v_val=None):
        # TODO: implement
        # we could re-implement deval_crv here in the context of this classical surface type, or we could pass the buck to our general Surface class
        if v_val is None:
            # we're plotting a u-iso, return the tranlated directrix
            pass
        else :
             # we're plotting a v-iso, return the translated generator
             pass

        return super(ClassicalSurface,self).isocurve(u_val,v_val)



class Torus(ClassicalSurface):
    pi = math.pi
    
    def __init__(self, cs, major_radius, minor_radius, dom_u, dom_v, tol_u=None, tol_v=None,param_type=None):
        self.cs = cs
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.param_type = param_type
        def func(u,v):
            if self.param_type == 1 or self.param_type == 2:
                #Set v to phi which determines 2 V-circles.  Choose one and let
                #u traverse pts on that circle
                phi = v
                cos_gamma = -self.minor_radius*math.sin(phi)/(self.major_radius*self.sin_alpha)
                if (phi > 0.5*math.pi) and (phi < 1.5*math.pi):
                    psi_v1 = math.atan2(-self.major_radius*math.sqrt(1-cos_gamma*cos_gamma) + self.minor_radius, self.major_radius*self.cos_alpha*cos_gamma)
                else:
                    psi_v1 = math.atan2(self.major_radius*math.sqrt(1-cos_gamma*cos_gamma) + self.minor_radius, self.major_radius*self.cos_alpha*cos_gamma)
                #Villarceau #1  (t = "gamma")
                if self.param_type == 1: return self.func_v1(u, psi_v1)
                #Villarceau #2  (t = "gamma")
                else:return self.func_v2(u, psi_v1)
                
            else:
                rho = self.major_radius + self.minor_radius*math.cos(v)
                pt_out = self.cs.eval(Point(rho*math.cos(u), rho*math.sin(u), self.minor_radius*math.sin(v)))
                return pt_out
        super(Torus,self).__init__(func,dom_u,dom_v,tol_u,tol_v)
        
    @property
    def alpha(self): return math.asin(self.minor_radius/self.major_radius)
        
    @property
    def cos_alpha(self): return math.cos(self.alpha)
        
    @property
    def sin_alpha(self): return math.sin(self.alpha)
        
    #Villarceau #1  (t = "gamma")
    def func_v1(self, t, psi):
        x1 = self.major_radius*self.cos_alpha*math.cos(t)
        y1 = self.major_radius*math.sin(t) + self.minor_radius
        z1 = -self.major_radius*self.sin_alpha*math.cos(t)
        rot_psi = Xform.rotation(axis = Vec(0,0,1), angle = -psi)
        pt_out = self.cs.eval(Point(x1,y1,z1)*rot_psi)
        return pt_out
    
    #Villarceau #2  (t = "gamma")
    def func_v2(self, t, psi):
        x = self.major_radius*self.cos_alpha*math.cos(t)
        y = self.major_radius*math.sin(t) - self.minor_radius
        z = -self.major_radius*self.sin_alpha*math.cos(t)
        rot_psi = Xform.rotation(axis = Vec(0,0,1), angle = -psi)
        pt_out = self.cs.eval(Point(x,y,z)*rot_psi)
        return pt_out
    
