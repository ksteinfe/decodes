import decodes.core as dc
from decodes.core import *
if dc.VERBOSE_FS: print "polygon.py loaded"

import copy, collections

def rect(cpt, w, h):
  w2 = w/2
  h2 = h/2
  basis = dc.CS(cpt)
  return PGon([Point(-w2,-h2),Point(w2,-h2),Point(w2,h2),Point(-w2,h2)],basis)



class PGon(dc.Geometry, dc.HasBasis):
  """a very simple polygon class"""
  """Polygons limit their vertices to x and y dimensions, and enforce that they employ a basis.  Transformations of a polygon should generally be applied to the basis.  Any tranfromations of the underlying vertices should ensure that the returned vectors are limited to x and y dimensions"""
  
  def __init__(self, verts=None, basis=None):
    super(PGon,self).__init__()
    self.basis = dc.CS() if (basis is None) else basis
    self._verts = []
    if (verts is not None) : 
      for v in verts: self.add_vert(v)
    
  def basis_applied(self, copy_children=True): 
    return self
	#TODO: copy this functionality from Mesh class
	
  def basis_stripped(self, copy_children=True): 
    return self
	#TODO: copy this functionality from Mesh class
    
  @property
  def verts(self):
    if not self.is_baseless: return [ v.set_basis(self.basis) for v in self._verts]
    else : return self._verts
    
  @verts.setter
  def verts(self, verts): 
    self._verts = []
    self.add_vert(verts)
   
  def add_vert(self,other) : 
    if isinstance(other, collections.Iterable) : 
      for v in other : self.add_vert(v)
    else : 
      if self.is_baseless : self._verts.append(other.basis_applied())
      elif self.basis is other.basis : 
        self._verts.append(other.basis_stripped())
      elif other.is_baseless : 
        # we assume here that the user is describing the point within the pgon's basis
        # they may, however, be trying to add a "world" point to a mesh with a defined basis
        # if this is the case, they should call pgon.basis_stripped()
        #TODO: shouldn't we apply the basis to this point?
        self._verts.append(other)
      else : raise BasisError("The basis for this PGon and the point you're adding do not match.  Try applying or stripping the point of its basis, or describing the point in terms of the PGon's basis")
    
    
  def __repr__(self):
    return "pgon[{0}v]".format(len(self._verts))
