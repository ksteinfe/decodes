from decodes.core import *
if VERBOSE_FS: print "base.py loaded"
import copy,exceptions, collections




class GeometricError(StandardError):
    pass

class BasisError(GeometricError):
    pass

class DomainError(GeometricError):
    pass

class IsBasis(object):
    """
    A base class for anything that wants to call itself a basis. Bases must impliment the folloiwng methods:
    """
    
    def eval(self,other):
        """Other should be any object with either "x,y,z" attributes, "x,y" attributes, or a single "t" attribute which may be interpreted by the basis in order to generate a valid baseless point in R3
            
            :param other: Object with "x,y,z" attributes, "x,y" attributes, or a single "t". 
            :type other: Basis
            :result: Basis object.
            :rtype: Basis
        """
        raise NotImplementedError("Evalutate not implimented.    I am a BAD basis!")

class Geometry(object):
    """
    A base geometry class for all other geometry to inherit.
    """
    
    def __mul__(self, other):
        """Overloads the multiplication **(*)** operator.

            :param other: Geometry to be multiplied.
            :type other: Geometry
            :result: New geometry.
            :rtype: Geometry
        """
        from .dc_xform import Xform
        if isinstance(other, Xform) :
            return other*self
    
    def copy_props(self,other):
        """ Transfers the properties of the other geometry to this geometry, overwriting any properties this object currently has"""
        new_props = {}
        if hasattr(other, 'props') : new_props = other.props
        self.props = new_props
        return new_props


    def set_color(self,a,b=None,c=None):
        """Sets the geometry's color

            :param a: Color object to set the geometry's color, or number value (between 0 and 1) to create a new color. If only a is passed as a float, the color will be greyscale.
            :type a: Color or float
            :param b: If no color object is passed, the G value in an RGB scale.
            :type b: float
            :param c: If no color object is passed, the B value in an RGB scale.
            :type c: float
            :result: Sets the geometry's color.
            :rtype: Geometry
        """
        from .dc_color import Color
        if not hasattr(self, 'props') : self.props = {}
        if isinstance(a, (Color) ) : self.props['color'] = a
        else : self.props['color'] = Color(a,b,c)
        
    def get_color(self):
        # TODO: test if object has props
        # TODO: test if props dict contains entry for color
        if hasattr(self, 'props') : return self.props['color']
        return False
        
    def set_name(self,str):
        """Sets the geometry's name

            :param str: A str with the new geometry's name.
            :type str: str
            :result: Sets the geometry's name.
            :rtype: Geometry
        """
        if not hasattr(self, 'props') : self.props = {}
        self.props['name'] = str
        
    def set_weight(self,num):
        """Sets the geometry's weight

            :param num: A number with the new geometry's weight.
            :type num: float
            :result: Sets the geometry's name.
            :rtype: Geometry
        """
        if not hasattr(self, 'props') : self.props = {}
        self.props['weight'] = num

    def set_fill(self,a,b=None,c=None):
        """Sets the geometry's fill

            :param a: Color object to set the geometry's fill, or number value (between 0 and 1) to create a new color. If only a is passed as a float, the color will be greyscale.
            :type a: Color or float
            :param b: If no color object is passed, the G value in an RGB scale.
            :type b: float
            :param c: If no color object is passed, the B value in an RGB scale.
            :type c: float
            :result: Sets the geometry's fill.
            :rtype: Geometry
        """
        from .dc_color import Color
        if not hasattr(self, 'props') : self.props = {}
        if isinstance(a, (Color) ) : self.props['fill'] = a
        else : self.props['fill'] = Color(a,b,c)
        
        
    @property
    def do_translate(self):
        """
        if this property is set to false, outies will not translate this geometry into external formats, and pass along the class as-is.
        """
        return True

    @property
    def xform(self): 
        #TODO: i think these are obsolete
        return self.objCS.xform
        
    @property
    def ixform(self): 
        #TODO: i think these are obsolete
        return self.objCS.ixform
 

class HasBasis(Geometry):
    """
    A base class for anything that wants to define a basis for itself. Bases must impliment the following methods:
    """
    
    @property
    def is_baseless(self):
        """Tells us if a basis has been defined
        """
        return (not hasattr(self, 'basis')) or self.basis is None


    def basis_applied(self, copy_children=True):
        """Returns a new object with basis applied. Copies of are created of any child objects by default. Take care to copy over props if appropriate.
            
            :result: Object with basis applied.
            :rtype: Basis
        """
        raise NotImplementedError("basis_applied not implimented.    I am a BAD HasBasis!")
    
    def basis_stripped(self, copy_children=True): 
        """Returns a new object stripped of any basis. Copies of are created of any child objects by default. Take care to copy over props if appropriate.
            
            :result: Object with basis applied.
            :rtype: Basis
        """ 
        raise NotImplementedError("basis_stripped not implimented.    I am a BAD HasBasis!")



