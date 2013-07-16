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
    # rotational surfaces are currently constrained to rotational axis that pass thru the world origin
    
    def __init__(self, curve, axis=Vec(0,0,1), dom_v=Interval(0,math.pi), tol_v=None):
        '''
        the given curve will be rotated about an axis through the origin and defined by given vector
        '''
        self.curve = curve
        self.axis = axis

        def func(u,v):
            pt = self.curve.deval(u)
            xf = Xform.rotation(angle=v,axis=self.axis)
            return pt*xf

        dom_u = curve.domain
        tol_u = curve.tol
        super(RotationalSurface,self).__init__(func,dom_u,dom_v,tol_u,tol_v)

    def deval_pln(self,u,v):
        xf = Xform.rotation(angle=v,axis=self.axis)
        pln_crv = self.curve.deval_pln(u) * xf
        pt = Point(self.axis.to_line().near_pt(pln_crv.origin))
        return Plane(pln_crv.origin, pln_crv.normal.cross(pt).cross(pln_crv.normal))

    def deval_crv(self,u,v):
        # we could re-implement deval_crv here in the context of this classical surface type, or we could pass the buck to our general Surface class
        # don't forget that rotational surfaces are BASED... points need to be processed through self.basis as we go
        return super(ClassicalSurface,self).deval_crv(u,v)

    def isocurve(self, u_val=None, v_val=None):
        if u_val is None and v_val is None: raise AttributeError("Surface.isocurve requires either u_val OR v_val to be set")
        if u_val is not None and v_val is not None: raise AttributeError("u_val AND v_val cannot both be set when generating a Surface.isocurve")

        if v_val is None:
            # we're plotting a u-iso, return an Arc
            pt_0 = self.curve.deval(u_val)
            pt_1 = self.axis.to_line().near_pt(pt_0)
            rad = pt_0.distance(pt_1)
            cs = CS(pt_1,Vec(pt_0,pt_1),Vec(pt_0,pt_1).cross(self.axis))

            return Arc(cs,rad,self.domain_v.delta)
        else :
             # we're plotting a v-iso, return our curve
             iso = copy.copy(self.curve)
             iso.basis = CS()*Xform.rotation(angle=v_val,axis=self.axis)
             iso._rebuild_surrogate()
             return iso
        



class RotationalSurface_Depreciated(ClassicalSurface):
    # rotational surfaces are currently constrained to rotational axis that pass thru the world origin
    
    def __init__(self, cs, curve, dom_v=Interval(0,math.pi), tol_v=None):
        '''
        the given curve will be evaluated using the given cs as a basis
        and then rotated about a the x_axis of this cs
        '''

        self.curve = curve
        self.basis = cs

        self.axis = Vec(1,0)

        def func(u,v):
            pt = self.curve.deval(u)
            xf = Xform.rotation(angle=v,axis=self.axis)
            return self.basis.eval(pt*xf)

        dom_u = curve.domain
        tol_u = curve.tol
        super(RotationalSurface,self).__init__(func,dom_u,dom_v,tol_u,tol_v)

    def deval_pln(self,u,v):
        # don't forget that rotational surfaces are BASED... points need to be processed through self.basis as we go
        xf = Xform.rotation(angle=v,axis=self.axis)
        pln_crv = self.curve.deval_pln(u) * xf
        pt = self.basis.eval(pln_crv.origin)
        crv_vec = Vec(pt,self.basis.eval(pln_crv.origin + pln_crv.normal))
        
        vec = Vec(pt,self.basis.origin)
        if vec.length == 0 : vec = Vec(pt,self.basis.origin+self.axis)
        vec = vec.cross(crv_vec)
        vec = vec.cross(crv_vec)

        return Plane(pt,vec)

    def deval_crv(self,u,v):
        # we could re-implement deval_crv here in the context of this classical surface type, or we could pass the buck to our general Surface class
        # don't forget that rotational surfaces are BASED... points need to be processed through self.basis as we go
        return super(ClassicalSurface,self).deval_crv(u,v)

    def isocurve(self, u_val=None, v_val=None):
        if u_val is None and v_val is None: raise AttributeError("Surface.isocurve requires either u_val OR v_val to be set")
        if u_val is not None and v_val is not None: raise AttributeError("u_val AND v_val cannot both be set when generating a Surface.isocurve")

        if v_val is None:
            # we're plotting a u-iso, return an Arc
            pt_0 = self.curve.deval(u_val)
            pt_1 = Point(pt_0.x)
            rad = pt_0.distance(pt_1)
            cs = CS(self.basis.eval(pt_0.x,0,0),Vec(pt_1,pt_0),self.basis.z_axis)

            return Arc(cs,rad,math.pi)
        else :
             # we're plotting a v-iso, return our curve
             xf = Xform.rotation(angle=v_val,axis=self.axis)
             iso = self.curve
             y_pt = self.basis.eval(0,1)*xf
             cs = CS(self.basis.origin,self.basis.x_axis,y_pt)
             iso.basis = cs
             iso._rebuild_surrogate()
             return iso
        