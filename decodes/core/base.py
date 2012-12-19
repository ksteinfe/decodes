import decodes.core as dc
from decodes.core import *

#this also seemed to work
#from .. import core as dc
#from core import *

if dc.VERBOSE_FS: print "base.py loaded"

import copy,exceptions



#TODO: do these better elsewhere
# perhaps in a domain / range class?  
def frange(start, stop, step):
  r = start
  while r < stop:
    yield r
    r += step

def drange(start, stop, divs):
  r = start
  while r < stop:
    yield r
    r += (stop-start)/divs



class GeometricError(StandardError):
    pass

class BasisError(GeometricError):
    pass

class Basis(object):
  """a base class for anything that wants to call itself a basis"""
  """bases must impliment the folloiwng methods:"""
  
  def eval(self,other):
    # other should be any object with either "x,y,z" attributes, "x,y" attributes, or a single "t" attribute
    # which may be interpreted by the basis in order to generate a valid baseless point in R3
    raise NotImplementedError("Evalutate not implimented.  I am a BAD basis!")

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
    raise NotImplementedError("basis_applied not implimented.  I am a BAD HasBasis!")
  
  '''
  returns a new object stripped of any basis.
  copies of are created of any child objects by default.
  take care to copy over props if appropriate
  '''
  def basis_stripped(self, copy_children=True): 
    raise NotImplementedError("basis_stripped not implimented.  I am a BAD HasBasis!")








class Geometry(object):
  """a base geometry class for all other geometry to inherit"""
  
  def __mul__(self, other):
    if isinstance(other, dc.Xform) :
      return other*self
  
  def set_color(self,a,b=None,c=None):
    if not hasattr(self, 'props') : self.props = {}
    if isinstance(a, (dc.Color) ) : self.props['color'] = a
    else : self.props['color'] = dc.Color(a,b,c)

  @property
  def xform(self): 
    return self.objCS.xform
    
  @property
  def ixform(self): 
    return self.objCS.ixform