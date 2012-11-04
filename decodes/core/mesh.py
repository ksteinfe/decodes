import decodes.core as dc
from decodes.core import *
if dc.VERBOSE_FS: print "mesh.py loaded"

import copy, collections

class Mesh(dc.Geometry, dc.HasBasis):
  """a very simple mesh class"""
  ## TODO: make mesh only triangles
  
  def __init__(self, verts=None, faces=None, basis=None):
    super(Mesh,self).__init__()
    self._verts = [] if (verts is None) else verts
    self._faces = [] if (faces is None) else faces
    if (basis is not None) : self.basis = basis
    
  def basis_applied(self, copy_children=True): 
    if copy_children : msh = Mesh([v.basis_applied() for v in self.verts],copy.copy(self._faces))
    else : msh = Mesh([v.basis_applied() for v in self.verts],self._faces)
    if hasattr(self, 'props') : msh.props = self.props
    return msh
  def basis_stripped(self, copy_children=True): 
    if copy_children : msh = Mesh(copy.copy(self._verts),copy.copy(self._faces))
    else : msh = Mesh(self._verts,self._faces)
    if hasattr(self, 'props') : msh.props = self.props
    return msh
    
  @property
  def faces(self): return self._faces
   
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
        # we assume here that the user is describing the point within the mesh's basis
        # they may, however, be trying to add a "world" point to a mesh with a defined basis
        # if this is the case, they should call mesh.basis_stripped()
        self._verts.append(other)
      else : raise BasisError("The basis for this Mesh and the point you're adding do not match.  Try applying or stripping the point of its basis, or describing the point in terms of the Mesh's basis")
    
  def add_face(self,a,b,c,d=-1):
    #TODO: add lists of faces just the same
    if (d>=0) : self._faces.append([a,b,c,d])
    else: self._faces.append([a,b,c])
  
  def face_verts(self,index):
    return [self.verts[i] for i in self.faces[index]]
  
  def face_centroid(self,index):
    return Point.centroid(self.face_verts(index))
    
  def face_normal(self,index):
    verts = self.face_verts(index)
    if len(verts) == 3 : return Vec(verts[0],verts[1]).cross(Vec(verts[0],verts[2])).normalized()
    else :
      v0 = Vec(verts[0],verts[1]).cross(Vec(verts[0],verts[3])).normalized()
      v1 = Vec(verts[2],verts[3]).cross(Vec(verts[2],verts[1])).normalized()
      return Vec.bisector(v0,v1).normalized()
  
  
  def __repr__(self):
    return "msh[{0}v,{1}f]".format(len(self._verts),len(self._faces))
