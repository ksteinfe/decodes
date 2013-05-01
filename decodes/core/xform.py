from decodes.core import *
from . import base, vec, point, cs, line, mesh, pgon


if VERBOSE_FS: print "xform.py loaded"

class Xform(object):
    """
        A transformation matrix class.
    """
    def __init__(self,value=1.0,matrix=None):
        """XForm Constructor

            :param value: Transformation value (defaults to 1.0).
            :type value: float
            :param matrix: Matrix
            :type matrix: list
            :result: XForm object.
            :rtype: XForm
        """
        if matrix :
            self._m = matrix
        else :
            self._m = [0.0]*16
            self.m00 = value
            self.m11 = value
            self.m22 = value
            self.m33 = 1.0
            
    def __repr__(self):
        return ( "xform\t[{},{},{},{}]".format(self.m00,self.m01,self.m02,self.m03) +
        "\n\t\t[{},{},{},{}]".format(self.m10,self.m11,self.m12,self.m13) +
        "\n\t\t[{},{},{},{}]".format(self.m20,self.m21,self.m22,self.m23) +
        "\n\t\t[{},{},{},{}]".format(self.m30,self.m31,self.m32,self.m33) )
    
    """an Xform can act as a basis for a point"""
    def eval(self,other):
        try:
            x = other.x
            y = other.y
            z = other.z
        except TypeError:
            print("mallard can't quack()")
        tup = self._xform_tuple(other.to_tuple())
        return Point(tup[0],tup[1],tup[2])
        
    
    def strip_translation(self):
        m = list(self._m)
        xf = Xform(matrix = m)
        xf.m03 = 0
        xf.m13 = 0
        xf.m23 = 0
        return xf
    
    @staticmethod
    def translation(vec):
        """Translates a geometry by a given Vector.

            :param vec: Vector to apply a translation
            :type vec: Vec
            :result: Translates an object
            :rtype: Geometry
        """
        xf = Xform()
        xf.m03 = vec.x
        xf.m13 = vec.y
        xf.m23 = vec.z
        return xf

    @staticmethod
    def scale(factor):
        """Scales an object by a given factor.

            :param factor: Factor to scale by
            :type factor: float
            :result: Scaled object.
            :rtype: Geometry
        """
        #TODO: add scaling about a given point
        xf = Xform()
        xf.m00 = factor
        xf.m11 = factor
        xf.m22 = factor
        return xf
        
    @staticmethod
    def mirror(plane="world_xy"):
        """Produces mirror transform. Can pass in "world_xy", "world_yz", or "world_xz". Or, pass in an arbitrary cs (produces mirror about XYplane of CS)
        
        .. warning:: When mirroring about an arbitrary plane, this method currently relies on access to the Rhinocommon Kernel.  It will not work in other contexts.
        .. todo:: Re-implement this method without using the Rhinocommon Kernel.
        
            :param plane: Plane to mirror the object with. Defaults to world XY plane.
            :type plane: Plane
            :result: Mirrored object.
            :rtype: Geometry
        """
        xf = Xform()
        if plane=="world_xy" :
            xf.m22 *= -1
            return xf
        elif plane=="world_xz" :
            xf.m11 *= -1
            return xf
        elif plane=="world_yz" :
            xf.m00 *= -1
            return xf
        else:
            if isinstance(plane, CS) : 
                #TODO: do this ourselves instead
                import Rhino
                from ..io.rhino_out import to_rgvec, to_rgpt
                from ..io.rhino_in import from_rgtransform
                rh_xform = Rhino.Geometry.Transform.Mirror(to_rgpt(plane.origin),to_rgvec(plane.zAxis))       
                return from_rgtransform(rh_xform)
        
        raise NotImplementedError("Xform.mirror currently accepts the following values for 'plane':/n'world_xy','world_xz','world_yz'")

    @staticmethod
    def rotation(**kargs):
        """Rotates an object around by center and rotation angle, or by a center, an axis and a rotation angle. 
        .. warning:: This method currently relies on access to the Rhinocommon Kernel.    It will not work in other contexts.
        .. todo:: Re-implement this method without using the Rhinocommon Kernel.
        .. todo:: Rotation about an axis ought to take in a linear entitiy, not a vector
            :param **kargs: Function that accepts multiple parameters to be passed. Parameters include center and axis of rotation and a rotation angle. 
            :type **kargs: Point, Vec, float
            :result: Rotated object.
            :rtype: Geometry
        """
        import Rhino
        from ..io.rhino_out import to_rgvec, to_rgpt
        from ..io.rhino_in import from_rgtransform
        if all (k in kargs for k in ("angle","axis")) :
            # rotation by center, rotation angle, and rotation axis
            center = to_rgpt(kargs["center"]) if "center" in kargs else to_rgpt(Point(0,0,0))
            rh_xform = Rhino.Geometry.Transform.Rotation(kargs["angle"],to_rgvec(kargs["axis"]),center)
        elif all (k in kargs for k in ("center","angle")) :
            # rotation by center and rotation angle
            rh_xform = Rhino.Geometry.Transform.Rotation(kargs["angle"],to_rgpt(kargs["center"]))
        else :
            return False
        return from_rgtransform(rh_xform)
            
    @staticmethod
    def change_basis(csSource,csTarget):
        """Changes the plane basis of an object.
        .. warning:: This method currently relies on access to the Rhinocommon Kernel.    It will not work in other contexts.
        .. todo:: Re-implement this method without using the Rhinocommon Kernel.
            :param csSource: Plane source of the object.
            :type csSource: Plane
            :param csTarget: Target plane of the object.
            :type csTarget: Plane
            :result: Object with new Plane basis.
            :rtype: Geometry
        """
        import Rhino
        from ..io.rhino_out import to_rgvec, to_rgpt, to_rgplane
        from ..io.rhino_in import from_rgtransform
        rh_source_plane = to_rgplane(csSource)
        rh_target_plane = to_rgplane(csTarget)
        rh_xform = Rhino.Geometry.Transform.PlaneToPlane(rh_source_plane, rh_target_plane)
        return from_rgtransform(rh_xform)
    
    def __mul__(self, other):
        '''
        Multiply by another Matrix, or by any piece of fieldpack geometry
        This function must be kept up to date with every new class of DC geom
        '''
        if isinstance(other, Xform) : 
            xf = Xform()
            xf._m = [
                self.m00 * other.m00 + self.m01 * other.m10 + self.m02 * other.m20 + self.m03 * other.m30,
                self.m00 * other.m01 + self.m01 * other.m11 + self.m02 * other.m21 + self.m03 * other.m31,
                self.m00 * other.m02 + self.m01 * other.m12 + self.m02 * other.m22 + self.m03 * other.m32,
                self.m00 * other.m03 + self.m01 * other.m13 + self.m02 * other.m23 + self.m03 * other.m33,
                self.m10 * other.m00 + self.m11 * other.m10 + self.m12 * other.m20 + self.m13 * other.m30,
                self.m10 * other.m01 + self.m11 * other.m11 + self.m12 * other.m21 + self.m13 * other.m31,
                self.m10 * other.m02 + self.m11 * other.m12 + self.m12 * other.m22 + self.m13 * other.m32,
                self.m10 * other.m03 + self.m11 * other.m13 + self.m12 * other.m23 + self.m13 * other.m33,
                self.m20 * other.m00 + self.m21 * other.m10 + self.m22 * other.m20 + self.m23 * other.m30,
                self.m20 * other.m01 + self.m21 * other.m11 + self.m22 * other.m21 + self.m23 * other.m31,
                self.m20 * other.m02 + self.m21 * other.m12 + self.m22 * other.m22 + self.m23 * other.m32,
                self.m20 * other.m03 + self.m21 * other.m13 + self.m22 * other.m23 + self.m23 * other.m33,
                self.m30 * other.m00 + self.m31 * other.m10 + self.m32 * other.m20 + self.m33 * other.m30,
                self.m30 * other.m01 + self.m31 * other.m11 + self.m32 * other.m21 + self.m33 * other.m31,
                self.m30 * other.m02 + self.m31 * other.m12 + self.m32 * other.m22 + self.m33 * other.m32,
                self.m30 * other.m03 + self.m31 * other.m13 + self.m32 * other.m23 + self.m33 * other.m33,
            ]
            return xf
        
        # BASED GEOMETRY
        # all objects that have a basis defined must apply their basis before transforming points
        if isinstance(other, HasBasis) and (not other.is_baseless): 
            o = other.basis_applied()
            o.copy_props(other)
            other = o

        if isinstance(other, HasPts) : 
            verts = [Vec(pt*self) for pt in other.pts]
            other.clear()
            other._verts = verts
            return other
               
        if isinstance(other, LinearEntity) : 
            other._pt = other._pt*self
            xf = self.strip_translation()
            other._vec = other._vec*xf
            return other

        if isinstance(other, CS) : 
            cs = other
            tup = self._xform_tuple(cs.origin.to_tuple())
            origin = Point(tup[0],tup[1],tup[2])
            
            xf = self.strip_translation()
            tup = xf._xform_tuple(cs.xAxis.to_tuple())
            xAxis = Vec(tup[0],tup[1],tup[2])
            tup = xf._xform_tuple(cs.yAxis.to_tuple())
            yAxis = Vec(tup[0],tup[1],tup[2])
            
            cs = CS(origin, xAxis, yAxis)
            cs.copy_props(other)
            return cs
            
        if isinstance(other, Point) : 
            tup = self._xform_tuple(other.to_tuple())
            pt = Point(tup[0],tup[1],tup[2])
            pt.copy_props(other)
            return pt
            '''
            if other.is_baseless : 
                tup = self._xform_tuple(other.to_tuple())
                pt = Point(tup[0],tup[1],tup[2])
                pt.copy_props(other)
                return pt
            else :
                tup = self._xform_tuple(other.basis_stripped().to_tuple())
                pt = Point(tup[0],tup[1],tup[2],basis=other.basis)
                pt.copy_props(other)
                return pt
            '''

        if isinstance(other, Vec) : 
            tup = self._xform_tuple(other.to_tuple())
            vec = Vec(tup[0],tup[1],tup[2])
            vec.copy_props(other)
            return vec
        
        raise Exception("can't xform that thing")

    def _xform_tuple(self,tup):
        return (
            tup[0] * self._m[0] + tup[1] * self._m[1] + tup[2] * self._m[2]     + self._m[3],
            tup[0] * self._m[4] + tup[1] * self._m[5] + tup[2] * self._m[6]     + self._m[7],
            tup[0] * self._m[8] + tup[1] * self._m[9] + tup[2] * self._m[10]    + self._m[11]
            )
    
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
    def m03(self): return self._m[3]
    @m03.setter
    def m03(self,value): self._m[3] = value
    
    @property
    def m10(self): return self._m[4]
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
    def m21(self,value): self._m[9] = value
    @property
    def m22(self): return self._m[10]
    @m22.setter
    def m22(self,value): self._m[10] = value
    @property
    def m23(self): return self._m[11]
    @m23.setter
    def m23(self,value): self._m[11] = value
    
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

    



