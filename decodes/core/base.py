from decodes.core import *
if VERBOSE_FS: print "base.py loaded"
import copy,exceptions, collections




class GeometricError(StandardError):
        pass

class BasisError(GeometricError):
        pass

class Basis(object):
    """
    a base class for anything that wants to call itself a basis
    bases must impliment the folloiwng methods:
    """
    
    def eval(self,other):
        """
        other should be any object with either "x,y,z" attributes, "x,y" attributes, or a single "t" attribute
        which may be interpreted by the basis in order to generate a valid baseless point in R3
        """
        raise NotImplementedError("Evalutate not implimented.    I am a BAD basis!")

class HasBasis(object):
    """a base class for anything that wants to define a basis for itself"""
    """bases must impliment the folloiwng methods:"""
    
    '''
    tells us if a basis has been defined
    '''
    @property
    def is_baseless(self): return (not hasattr(self, 'basis')) or self.basis is None

    '''
    returns a new object with basis applied. 
    copies of are created of any child objects by default.
    take care to copy over props if appropriate
    '''
    def basis_applied(self, copy_children=True): 
        raise NotImplementedError("basis_applied not implimented.    I am a BAD HasBasis!")
    
    '''
    returns a new object stripped of any basis.
    copies of are created of any child objects by default.
    take care to copy over props if appropriate
    '''
    def basis_stripped(self, copy_children=True): 
        raise NotImplementedError("basis_stripped not implimented.    I am a BAD HasBasis!")

class Geometry(object):
    """a base geometry class for all other geometry to inherit"""
    
    def __mul__(self, other):
        from .xform import Xform
        if isinstance(other, Xform) :
            return other*self
    
    def set_color(self,a,b=None,c=None):
        from .color import Color
        if not hasattr(self, 'props') : self.props = {}
        if isinstance(a, (Color) ) : self.props['color'] = a
        else : self.props['color'] = Color(a,b,c)

    def set_name(self,str):
        if not hasattr(self, 'props') : self.props = {}
        self.props['name'] = str
        
    def set_weight(self,num):
        if not hasattr(self, 'props') : self.props = {}
        self.props['weight'] = num

    def set_fill(self,a,b=None,c=None):
        from .color import Color
        if not hasattr(self, 'props') : self.props = {}
        if isinstance(a, (Color) ) : self.props['fill'] = a
        else : self.props['fill'] = Color(a,b,c)
        
        
    @property
    def xform(self): 
        #TODO: i think these are obsolete
        return self.objCS.xform
        
    @property
    def ixform(self): 
        #TODO: i think these are obsolete
        return self.objCS.ixform
 
class HasVerts(object):
    def __getitem__(self,index):
        return self._verts[index]
    
    def __setitem__(self,index,vert):
        self._verts[index] = vert
    
    @property
    def verts(self): return self._verts
    
    @verts.setter
    def verts(self, verts): 
        self._verts = []
        self.append(verts)
        
    def append(self,other) : 
        if isinstance(other, collections.Iterable) : 
            for v in other : self.append(v)
        else : 
            self._verts.append(other)

            
