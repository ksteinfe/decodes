from decodes.core import *
from . import dc_base, dc_vec, dc_point, dc_cs, dc_line, dc_mesh, dc_pgon


if VERBOSE_FS: print("xform.py loaded")

class Xform(object):
    """
        A transformation matrix class.
    """
    def __init__(self,matrix=None):
        """XForm Constructor
            
            :param matrix: Matrix
            :type matrix: list
            :result: XForm object.
            :rtype: XForm
        """
        if matrix is not None :
            self._m = matrix
        else :
            self._m = [0.0]*16
            self.c11 = 1.0
            self.c22 = 1.0
            self.c33 = 1.0
            self.c44 = 1.0
            
    def __repr__(self):
        return ( "xform\t[{},{},{},{}]".format(self.c11,self.c12,self.c13,self.c14) +
        "\n\t\t[{},{},{},{}]".format(self.c21,self.c22,self.c23,self.c24) +
        "\n\t\t[{},{},{},{}]".format(self.c31,self.c32,self.c33,self.c34) +
        "\n\t\t[{},{},{},{}]".format(self.c41,self.c42,self.c43,self.c44) )
    
    def strip_translation(self):
        m = list(self._m)
        xf = Xform(matrix = m)
        xf.c14 = 0
        xf.c24 = 0
        xf.c34 = 0
        return xf
    
    @staticmethod
    def translation(vec):
        """Translates an object by a given Vector.

            :param vec: Vector to apply a translation.
            :type vec: Vec
            :result: Translates an object.
            :rtype: Geometry
        """
        xf = Xform()
        xf.c14 = vec.x
        xf.c24 = vec.y
        xf.c34 = vec.z
        return xf

    @staticmethod
    def scale(factor, origin=None):
        """Scales an object by a given factor.

            :param factor: Factor to scale by.
            :type factor: float
            :result: Scaled object.
            :rtype: Geometry
        """
        if not origin:
            xf = Xform()
            xf.c11 = factor
            xf.c22 = factor
            xf.c33 = factor
            return xf
        else:
            xf = Xform()
            xf.c11 = factor
            xf.c22 = factor
            xf.c33 = factor

            xf.c14 = (1-factor)*origin.x
            xf.c24 = (1-factor)*origin.y
            xf.c34 = (1-factor)*origin.z
            return xf

    @staticmethod
    def mirror(plane="world_xy"):
        """Produces mirror transform. Can pass in "world_xy", "world_yz", or "world_xz". Or, pass in an arbitrary cs (produces mirror about XYplane of CS).
        
            :param plane: Plane to mirror the object with. Defaults to world XY plane.
            :type plane: Plane
            :result: Mirrored object.
            :rtype: Geometry
            
            .. warning:: When mirroring about an arbitrary plane, this method currently relies on access to the Rhinocommon Kernel.  It will not work in other contexts.
            .. todo:: Re-implement this method without using the Rhinocommon Kernel.
            
        """
        #TODO: Re-implement this method without using the Rhinocommon Kernel
        
        xf = Xform()
        
        if isinstance(plane, str):
            if plane=="world_xy" : xf.c33 *= -1
            elif plane=="world_xz" : xf.c22 *= -1
            elif plane=="world_yz" : xf.c11 *= -1
            else: 
                raise NotImplementedError("Xform.mirror accepts only the following string values for 'plane':/n'world_xy','world_xz','world_yz'")
            return xf
        
        nx,ny,nz = plane._vec.x, plane._vec.y, plane._vec.z
        origin = plane.origin
        xf_plane = Xform()
        xf_plane.m00 = 1-2*nx*nx
        xf_plane.m01 = -2*nx*ny
        xf_plane.m02 = -2*nx*nz
        xf_plane.m10 = -2*nx*ny
        xf_plane.m11 = 1-2*ny*ny
        xf_plane.m12 = -2*ny*nz
        xf_plane.m20 = -2*nx*nz
        xf_plane.m21 = -2*ny*nz
        xf_plane.m22 = 1-2*nz*nz
        xf_o = Xform.translation(Vec(origin))
        xf_minuso = Xform.translation(-Vec(origin))
        return xf_o*xf_plane*xf_minuso           
        
        """
            if isinstance(plane, CS) : 
                #TODO: do this ourselves instead
                import Rhino
                from ..io.rhino_out import to_rgvec, to_rgpt
                from ..io.rhino_in import from_rgtransform
                rh_xform = Rhino.Geometry.Transform.Mirror(to_rgpt(plane.origin),to_rgvec(plane.zAxis))       
                return from_rgtransform(rh_xform)
        
        raise NotImplementedError("Xform.mirror currently accepts the following values for 'plane':/n'world_xy','world_xz','world_yz'")
        """
        
    @staticmethod
    def rotation(**kargs):
        """ Rotates an object around by a center and a rotation angle OR by a center, an axis and a rotation angle. 
            
            :param \**kargs: Function that accepts multiple parameters to be passed. Parameters include center and axis of rotation and a rotation angle. 
            :type \**kargs: Point, Vec, float
            :result: Rotated object.
            :rtype: Geometry

            .. warning:: This method currently relies on access to the Rhinocommon Kernel. It will not work in other contexts.            
            
        """
       # TODO:: Re-implement this method without using the Rhinocommon Kernel.

       # TODO:: Rotation about an axis ought to take in a linear entity, not a vector.
        
        try:
            try:
                axis = kargs["axis"].normalized()
            except:
                axis = Vec(0,0,1)

            if "angle" in kargs and not "center" in kargs :
                xf = Xform()
                u,v,w = axis.x,axis.y,axis.z
                uv,uw,vw = u*v,u*w,v*w
                u2,v2,w2 = u**2,v**2,w**2
                cost = math.cos(kargs["angle"])
                sint = math.sin(kargs["angle"])

                xf.c11 = u2+(1-u2)*cost
                xf.c12 = uv*(1-cost)- w * sint
                xf.c13 = uw*(1-cost)+ v * sint

                xf.c21 = uv*(1-cost)+ w * sint
                xf.c22 = v2+(1-v2) * cost
                xf.c23 = vw*(1-cost)- u * sint

                xf.c31 = uw*(1-cost)- v * sint
                xf.c32 = vw*(1-cost)+ u * sint
                xf.c33 = w2+(1-w2)*cost
                return xf
            else:
                raise
        except:
            if all (k in kargs for k in ("angle","axis","center")) :
                # rotation by center, rotation angle, and rotation axis
                import Rhino
                from ..io.rhino_out import to_rgvec, to_rgpt
                from ..io.rhino_in import from_rgtransform
                center = to_rgpt(kargs["center"]) if "center" in kargs else to_rgpt(Point(0,0,0))
                rh_xform = Rhino.Geometry.Transform.Rotation(kargs["angle"],to_rgvec(kargs["axis"]),center)
            elif all (k in kargs for k in ("center","angle")) :
                # rotation by center and rotation angle
                import Rhino
                from ..io.rhino_out import to_rgvec, to_rgpt
                from ..io.rhino_in import from_rgtransform
                rh_xform = Rhino.Geometry.Transform.Rotation(kargs["angle"],to_rgpt(kargs["center"]))
            else :
                raise AttributeError("Could not construct a rotation transfer with these arguments")
            return from_rgtransform(rh_xform)
            
    @staticmethod
    def change_basis(cs_src,cs_tar):
        """ Changes the plane basis of an object.            
            
            :param cs_src: CS source of the object.
            :type cs_src: CS
            :param cs_tar: CS plane of the object.
            :type cs_tar: CS
            :result: Transformation Matrix.
            :rtype: Xform
            
        """
        xg, yg, zg = Vec(1,0,0), Vec(0,1,0), Vec(0,0,1) # global coordinate basis vectors
        xs, ys, zs = cs_src.x_axis, cs_src.y_axis, cs_src.z_axis
        xt, yt, zt = cs_tar.x_axis, cs_tar.y_axis, cs_tar.z_axis
        xf_gs = Xform(matrix=[xs.dot(xg),xs.dot(yg),xs.dot(zg),0,ys.dot(xg),ys.dot(yg),ys.dot(zg),0,zs.dot(xg),zs.dot(yg),zs.dot(zg),0,0,0,0,1])
        xf_gs *= Xform.translation(-cs_src.origin) 
        xf_st = Xform(matrix=[xg.dot(xt),xg.dot(yt),xg.dot(zt),0,yg.dot(xt),yg.dot(yt),yg.dot(zt),0,zg.dot(xt),zg.dot(yt),zg.dot(zt),0,0,0,0,1])
        return Xform.translation(cs_tar.origin)* (xf_st * xf_gs )
    
    def __mul__(self, other):
        """| Multiplies this Geometry by another Matrix, or by any piece of geometry.
           | This function must be kept up to date with every new class of DC geom.
            
           :param other: Matrix to multiply or Geometry to transform.
           :type other: object
           :result: multiplied object
           :rtype: object
        """
        if isinstance(other, Xform) : 
            xf = Xform()
            xf._m = [
                self.c11 * other.c11 + self.c12 * other.c21 + self.c13 * other.c31 + self.c14 * other.c41,
                self.c11 * other.c12 + self.c12 * other.c22 + self.c13 * other.c32 + self.c14 * other.c42,
                self.c11 * other.c13 + self.c12 * other.c23 + self.c13 * other.c33 + self.c14 * other.c43,
                self.c11 * other.c14 + self.c12 * other.c24 + self.c13 * other.c34 + self.c14 * other.c44,
                self.c21 * other.c11 + self.c22 * other.c21 + self.c23 * other.c31 + self.c24 * other.c41,
                self.c21 * other.c12 + self.c22 * other.c22 + self.c23 * other.c32 + self.c24 * other.c42,
                self.c21 * other.c13 + self.c22 * other.c23 + self.c23 * other.c33 + self.c24 * other.c43,
                self.c21 * other.c14 + self.c22 * other.c24 + self.c23 * other.c34 + self.c24 * other.c44,
                self.c31 * other.c11 + self.c32 * other.c21 + self.c33 * other.c31 + self.c34 * other.c41,
                self.c31 * other.c12 + self.c32 * other.c22 + self.c33 * other.c32 + self.c34 * other.c42,
                self.c31 * other.c13 + self.c32 * other.c23 + self.c33 * other.c33 + self.c34 * other.c43,
                self.c31 * other.c14 + self.c32 * other.c24 + self.c33 * other.c34 + self.c34 * other.c44,
                self.c41 * other.c11 + self.c42 * other.c21 + self.c43 * other.c31 + self.c44 * other.c41,
                self.c41 * other.c12 + self.c42 * other.c22 + self.c43 * other.c32 + self.c44 * other.c42,
                self.c41 * other.c13 + self.c42 * other.c23 + self.c43 * other.c33 + self.c44 * other.c43,
                self.c41 * other.c14 + self.c42 * other.c24 + self.c43 * other.c34 + self.c44 * other.c44,
            ]
            return xf
        
        return self.transform(other)
        

    def transform(self,other):
        """| Multiplies any appropriate piece of geometry by this XForm
           | This function must be kept up to date with every new class of DC geom.
            
           :param other: geometry to transform.
           :type other: Geometry
           :result: multiplied object
           :rtype: Geometry
        """
        # HASPTS GEOMETRY
        # applies transformation to the verts, leaving the basis intact
        if isinstance(other, HasPts) : 
            #raise NotImplementedError("can't xform a haspts")
            other._verts = [v*self for v in other._verts]
            return other
            # TODO: deal with applying transformations to haspts geometry
            

        # BASED GEOMETRY
        # all objects that are not HASPTS but are HASBASIS and have a basis defined and are capable of applying their basis... must do so before transforming points
        # this condition only applies to Based Points at the moment, may apply to Tetrahedron class
        # TODO: move this functionality down to Based Points
        if isinstance(other, HasBasis) and (not other.is_baseless): 
            try:
                o = other.basis_applied()
                o.copy_props(other)
                other = o
            except:
                pass
        
        if isinstance(other, LinearEntity) : 
            pt = other._pt*self
            xf = self.strip_translation()
            vec = other._vec*xf
            if isinstance(other, Line) : return Line(pt,vec)
            if isinstance(other, Ray) : return Ray(pt,vec)
            if isinstance(other, Segment) : return Segment(pt,vec)
            
        if isinstance(other, CS) : 
            cs = other
            tup = self._xform_tuple(cs.origin.to_tuple())
            origin = Point(tup[0],tup[1],tup[2])
            
            xf = self.strip_translation()
            tup = xf._xform_tuple(cs.x_axis.to_tuple())
            x_axis = Vec(tup[0],tup[1],tup[2])
            tup = xf._xform_tuple(cs.y_axis.to_tuple())
            y_axis = Vec(tup[0],tup[1],tup[2])
            
            
            ret = CS(origin, x_axis, y_axis)
            ret.copy_props(other)
            return ret
        
        if isinstance(other, Arc) : 
        
            cs = other._basis
            tup = self._xform_tuple(cs.origin.to_tuple())
            origin = Point(tup[0],tup[1],tup[2])
            xf = self.strip_translation()
            tup = xf._xform_tuple(cs.x_axis.to_tuple())
            x_axis = Vec(tup[0],tup[1],tup[2])
            tup = xf._xform_tuple(cs.y_axis.to_tuple())
            y_axis = Vec(tup[0],tup[1],tup[2])
            
            
            ret = Arc(CS(origin, x_axis, y_axis),other.rad,other.angle)
            ret.copy_props(other)
            return ret
        
        if isinstance(other, Point) : 
            tup = self._xform_tuple(other.to_tuple())
            pt = Point(tup[0],tup[1],tup[2])
            pt.copy_props(other)
            return pt
        
        if isinstance(other, Vec) : 
            tup = self._xform_tuple(other.to_tuple())
            vec = Vec(tup[0],tup[1],tup[2])
            vec.copy_props(other)
            return vec
        
        if isinstance(other, Circle) :
            pln = other.plane * self
            cir = Circle(pln,other.rad)
            cir.copy_props(other)
            return cir 
        
        if isinstance(other, Plane) : 
            pln = other
            tup = self._xform_tuple(pln.origin.to_tuple())
            origin = Point(tup[0],tup[1],tup[2])
            
            xf = self.strip_translation()
            tup = xf._xform_tuple(pln.normal.to_tuple())
            normal = Vec(tup[0],tup[1],tup[2]).normalized()
            
            pln = Plane(origin, normal)
            pln.copy_props(other)
            return pln

        
        raise NotImplementedError("can't xform an object of type {}".format(type(other)))
        
        
        
    def _xform_tuple(self,tup):

        return (
            tup[0] * self._m[0] + tup[1] * self._m[1] + tup[2] * self._m[2]     + self._m[3],
            tup[0] * self._m[4] + tup[1] * self._m[5] + tup[2] * self._m[6]     + self._m[7],
            tup[0] * self._m[8] + tup[1] * self._m[9] + tup[2] * self._m[10]    + self._m[11]
            )
    
    @property 
    def c11(self): return self._m[0]
    @c11.setter
    def c11(self,value): self._m[0] = value
    @property
    def c12(self): return self._m[1]
    @c12.setter
    def c12(self,value): self._m[1] = value
    @property
    def c13(self): return self._m[2]
    @c13.setter
    def c13(self,value): self._m[2] = value
    @property
    def c14(self):  return self._m[3]
    @c14.setter
    def c14(self,value): self._m[3] = value
    
    @property
    def c21(self):  return self._m[4]
    @c21.setter
    def c21(self,value): self._m[4] = value
    @property
    def c22(self): return self._m[5]
    @c22.setter
    def c22(self,value): self._m[5] = value
    @property
    def c23(self): return self._m[6]
    @c23.setter
    def c23(self,value): self._m[6] = value
    @property
    def c24(self): return self._m[7]
    @c24.setter
    def c24(self,value): self._m[7] = value
    
    @property
    def c31(self): return self._m[8]
    @c31.setter
    def c31(self,value): self._m[8] = value
    @property
    def c32(self): return self._m[9]
    @c32.setter
    def c32(self,value):  self._m[9] = value
    @property
    def c33(self):  return self._m[10]
    @c33.setter
    def c33(self,value): self._m[10] = value
    @property
    def c34(self): return self._m[11]
    @c34.setter
    def c34(self,value):  self._m[11] = value
    
    @property
    def c41(self): return self._m[12]
    @c41.setter
    def c41(self,value): self._m[12] = value
    @property
    def c42(self): return self._m[13]
    @c42.setter
    def c42(self,value): self._m[13] = value
    @property
    def c43(self): return self._m[14]
    @c43.setter
    def c43(self,value): self._m[14] = value
    @property
    def c44(self): return self._m[15]
    @c44.setter
    def c44(self,value): self._m[15] = value        
    
    
    
    
    
    @property 
    def m00(self): return self._m[0]
    @m00.setter
    def m00(self,value): self._m[0] = value
    @property
    def m01(self): return self._m[1]
    @m01.setter
    def m01(self,value): self._m[1] = value
    @property
    def m02(self): return self._m[2]
    @m02.setter
    def m02(self,value): self._m[2] = value
    @property
    def m03(self):  return self._m[3]
    @m03.setter
    def m03(self,value): self._m[3] = value
    
    @property
    def m10(self):  return self._m[4]
    @m10.setter
    def m10(self,value): self._m[4] = value
    @property
    def m11(self): return self._m[5]
    @m11.setter
    def m11(self,value): self._m[5] = value
    @property
    def m12(self): return self._m[6]
    @m12.setter
    def m12(self,value): self._m[6] = value
    @property
    def m13(self): return self._m[7]
    @m13.setter
    def m13(self,value): self._m[7] = value
    
    @property
    def m20(self): return self._m[8]
    @m20.setter
    def m20(self,value): self._m[8] = value
    @property
    def m21(self): return self._m[9]
    @m21.setter
    def m21(self,value):  self._m[9] = value
    @property
    def m22(self):  return self._m[10]
    @m22.setter
    def m22(self,value): self._m[10] = value
    @property
    def m23(self): return self._m[11]
    @m23.setter
    def m23(self,value):  self._m[11] = value
    
    @property
    def m30(self): return self._m[12]
    @m30.setter
    def m30(self,value): self._m[12] = value
    @property
    def m31(self): return self._m[13]
    @m31.setter
    def m31(self,value): self._m[13] = value
    @property
    def m32(self): return self._m[14]
    @m32.setter
    def m32(self,value): self._m[14] = value
    @property
    def m33(self): return self._m[15]
    @m33.setter
    def m33(self,value): self._m[15] = value    
    



