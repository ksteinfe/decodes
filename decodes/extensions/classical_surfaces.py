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
    
    def __init__(self, generatrix, axis=Vec(0,0,1), dom_v=Interval(0,math.pi), tol_v=None):
        '''
        the given generatrix curve will be rotated about an axis through the origin and defined by given vector
        '''
        self.genx = generatrix
        self.axis = axis

        def func(u,v):
            pt = self.genx.deval(u)
            xf = Xform.rotation(angle=v,axis=self.axis)
            return pt*xf

        try:
            dom_u = self.genx.domain
            tol_u = self.genx.tol
        except:
            # we may have been passed a non-curve genx, such as an arc
            # todo, make a way to set the tolerence of this arc
            dom_u = Interval()
            tol_u = 1.0/10.0

        super(RotationalSurface,self).__init__(func,dom_u,dom_v,tol_u,tol_v)

    def deval_pln(self,u,v,flip_ang_tol=0.0001):
        xf = Xform.rotation(angle=v,axis=self.axis)
        pln_crv = self.genx.deval_pln(u) * xf
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

        if v_val is None:
            # we're plotting a u-iso, return an Arc
            pt_0 = self.genx.deval(u_val)
            pt_1 = self.axis.to_line().near_pt(pt_0)
            rad = pt_0.distance(pt_1)
            cs = CS(pt_1,Vec(pt_1,pt_0),Vec(pt_0,pt_1).cross(self.axis))

            return Arc(cs,rad,self.domain_v.delta)
        else :
             # we're plotting a v-iso, return our curve
             iso = copy.copy(self.genx)
             if iso.is_baseless:
                iso.basis = CS()*Xform.rotation(angle=v_val,axis=self.axis)
             else:
                 iso.basis = iso.basis*Xform.rotation(angle=v_val,axis=self.axis)

             try:
                 iso._rebuild_surrogate()
             except:
                 pass
             return iso

        
class TranslationalSurface(ClassicalSurface):
    
    def __init__(self, generatrix, axis=Vec(1,0), dom_v=Interval(0,1), tol_v=None):
        '''
        the given generatrix curve will be translated along the given axis
        '''
        self.genx = generatrix
        self.axis = axis

        def func(u,v):
            pt = self.genx.deval(u)
            vec = Vec(axis)*v
            return pt+vec

        try:
            dom_u = self.genx.domain
            tol_u = self.genx.tol
        except:
            # we may have been passed a non-curve genx, such as an arc
            # todo, make a way to set the tolerence of this arc
            dom_u = Interval()
            tol_u = 1.0/10.0

        super(TranslationalSurface,self).__init__(func,dom_u,dom_v,tol_u,tol_v)

    def deval_pln(self,u,v):
        pln_crv = self.genx.deval_pln(u)

        pt = self._func(u,v)
        return Plane(pt, pln_crv.normal.cross(self.axis))


    def deval_crv(self,u,v):
        # we could re-implement deval_crv here in the context of this classical surface type, or we could pass the buck to our general Surface class
        return super(ClassicalSurface,self).deval_crv(u,v)

    def isocurve(self, u_val=None, v_val=None):
        # TODO: implement
        # we could re-implement deval_crv here in the context of this classical surface type, or we could pass the buck to our general Surface class
        if v_val is None:
            # we're plotting a u-iso, return a line
            pass
        else :
             # we're plotting a v-iso, return our curve translated
             pass

        return super(ClassicalSurface,self).isocurve(u_val,v_val)
