from decodes.core import *
from . import base, vec, point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "mesh.py loaded"

import copy, collections

class Mesh(HasVerts):
    """
    a very simple mesh class
    """
    ## TODO: make mesh only triangles
    
    def __init__(self, verts=None, faces=None, basis=None):
        """Mesh Constructor

            :param verts: New vertice or vertices to be added to the mesh.
            :type verts: Point
            :param faces: List of ordered faces.
            :type faces: list
            :param basis: Plane basis of the mesh.
            :type basis: Point
            :result: Mesh object.
            :rtype: Mesh
        """
        super(Mesh,self).__init__()
        self._verts = [] if (verts is None) else verts
        self._faces = [] if (faces is None) else faces
        if (basis is not None) : self.basis = basis
    '''    
    def basis_applied(self, copy_children=True): 
        """
            :param copy_children: If True, creates a new Mesh object with 'world' coordinates.
            :type verts: bool
            :result: Mesh object with basis applied.
            :rtype: Mesh
        """
        if copy_children : msh = Mesh([v.basis_applied() for v in self.verts],copy.copy(self._faces))
        else : msh = Mesh([v.basis_applied() for v in self.verts],self._faces)
        if hasattr(self, 'props') : msh.props = self.props
        return msh
    def basis_stripped(self, copy_children=True):
        """Returns a mesh based on its local location.

            :param copy_children: If True, creates a new Mesh object with the 'local' coordinates.
            :type verts: bool
            :result: Mesh object with basis stripped.
            :rtype: Mesh
        """    
        if copy_children : msh = Mesh(copy.copy(self._verts),copy.copy(self._faces))
        else : msh = Mesh(self._verts,self._faces)
        if hasattr(self, 'props') : msh.props = self.props
        return msh
    '''
        
    @property
    def faces(self): 
        """Returns a list of mesh faces.
        
            :returns: List of mesh faces.
            :rtype: list
        """
        return self._faces
    '''
    @property
    def verts(self):
        """Returns a list of mesh vertices.
        
            :returns: List of mesh vertices.
            :rtype: list
        """
        if not self.is_baseless: return [ v.set_basis(self.basis) for v in self._verts]
        else : return self._verts
        
    @verts.setter
    def verts(self, verts):
        """
        Sets vertices for a mesh.
        """    
        self._verts = []
        self.add_vert(verts)
     
    @property
    def centroid(self):
        """Returns a list of mesh centroids (points).
        
            :returns: List of centroids.
            :rtype: list
        """
        return Point.centroid(self.verts)
     
    def add_vert(self,other) :
        """Adds a vertice to the mesh.
        
            :param other: New vertice or vertices to be added to the mesh.
            :type other: Point.
            :returns: Modifies list of vertices.
        """
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
            else : raise BasisError("The basis for this Mesh and the point you're adding do not match.    Try applying or stripping the point of its basis, or describing the point in terms of the Mesh's basis")
    '''    
    def add_face(self,a,b,c,d=-1):
        """Adds a face to the mesh.
        
            :param a,b,c,d: Face to be added to the list of faces.
            :type a,b,c,d: int.
            :returns: Modifies list of faces.
        """
        #TODO: add lists of faces just the same
        if (d>=0) : self._faces.append([a,b,c,d])
        else: self._faces.append([a,b,c])
    
    def face_verts(self,index):
        """Returns the vertice of a given face.
        
            :param index: Face's index
            :type index: int
            :returns: Vertice.
            :rtype: Point
        """
        return [self.verts[i] for i in self.faces[index]]
    
    def face_centroid(self,index):
        """Returns the centroids of individual mesh faces.
        
            :param index: Index of a face.
            :type index: int
            :returns: Vertice.
            :rtype: Point
        """
        return Point.centroid(self.face_verts(index))
        
    def face_normal(self,index):
        """Returns the normal vector to a face.
        
            :param index: Index of a face.
            :type index: int
            :returns: Normal vector.
            :rtype: Vec
        """
        verts = self.face_verts(index)
        if len(verts) == 3 : return Vec(verts[0],verts[1]).cross(Vec(verts[0],verts[2])).normalized()
        else :
            v0 = Vec(verts[0],verts[1]).cross(Vec(verts[0],verts[3])).normalized()
            v1 = Vec(verts[2],verts[3]).cross(Vec(verts[2],verts[1])).normalized()
            return Vec.bisector(v0,v1).normalized()
    
    
    def __repr__(self):
        return "msh[{0}v,{1}f]".format(len(self._verts),len(self._faces))
    
    
    @staticmethod
    def explode(msh):
        """Explodes a mesh into individual faces.
        
            :param msh: Mesh to explode.
            :type msh: Mesh
            :returns: List of meshes.
            :type: list
        """
        exploded_meshes = []
        for face in msh.faces:
            pts = [msh.verts[v] for v in face]
            nface = [0,1,2] if len(face)==3 else [0,1,2,3]
            exploded_meshes.append(Mesh(pts,[nface]))
        return exploded_meshes
    
    
    