from decodes.core import *
from . import dc_base, dc_vec, dc_point, dc_has_pts #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "mesh.py loaded"

import copy, collections

class Mesh(HasPts):
    """
    a very simple mesh class
    """
    subclass_attr = [] # this list of props is unset any time this HasPts object changes
    
    def __init__(self, vertices=None, faces=None, basis=None):
        """Mesh Constructor

            :param vertices: The vertices of the mesh.
            :type vertices: [Point]
            :param faces: List of ordered faces.
            :type faces: [int]
            :param basis: The (optional) basis of the mesh.
            :type basis: Basis
            :result: Mesh object.
            :rtype: Mesh
        """
        super(Mesh,self).__init__(vertices,basis) #HasPts constructor handles initalization of verts and basis
        self._faces = [] if (faces is None) else faces

        
    @property
    def faces(self): 
        """Returns a list of mesh faces.
        
            :result: List of mesh faces.
            :rtype: list
        """
        return self._faces

    def add_face(self,a,b,c,d=-1):
        """Adds a face to the mesh.
        
            :param a,b,c,d: Face to be added to the list of faces.
            :type a,b,c,d: int.
            :result: Modifies list of faces.
            :rtype: None
        """
        #TODO: add lists of faces just the same
        
        if max(a,b,c,d) < len(self.pts):
            if (d>=0) : self._faces.append([a,b,c,d])
            else: self._faces.append([a,b,c])
    
    def face_pts(self,index):
        """Returns the points of a given face.
        
            :param index: Face's index
            :type index: int
            :returns: Vertices.
            :rtype: Point
        """
        return [self.pts[i] for i in self.faces[index]]
    
    def face_centroid(self,index):
        """Returns the centroids of individual mesh faces.
        
            :param index: Index of a face.
            :type index: int
            :returns: The centroid of a face.
            :rtype: Point
        """
        return Point.centroid(self.face_pts(index))
        
    def face_normal(self,index):
        """Returns the normal vector of a face.
        
            :param index: Index of a face.
            :type index: int
            :returns: Normal vector.
            :rtype: Vec
        """
        verts = self.face_pts(index)
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
            :type: [Mesh]
        """
        exploded_meshes = []
        for face in msh.faces:
            pts = [msh.pts[v] for v in face]
            nface = [0,1,2] if len(face)==3 else [0,1,2,3]
            exploded_meshes.append(Mesh(pts,[nface]))
        return exploded_meshes
    
    
    