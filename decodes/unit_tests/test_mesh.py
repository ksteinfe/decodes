import unittest
import decodes.core as dc
from decodes.core import *


class Tests(unittest.TestCase):

    tet_pts = [
        Point(0.0       , 0.0	      , 0.0),
        Point(0.9510565 , 0.0	      , 0.0),
        Point(0.6881910 , 1.3763819 , 0.0),
        Point(0.5257311 , 0.6881910	, 0.5)
    ]
    tet_faces = [[0,1,2],[0,2,3],[2,3,0],[3,0,1]]

    def test_empty_constructor(self):
        msh = Mesh()
        self.assertEqual(len(msh.pts),0,"mesh has an empty list of verts")

    def test_simple_constructor(self):
        msh = Mesh(self.tet_pts,self.tet_faces)
        for n in range(len(self.tet_pts)): self.assertEqual(msh[n],self.tet_pts[n],"a mesh constructed with a basis understands the given points in local coordinates")
        for n in range(len(self.tet_pts)): self.assertEqual(msh.pts[n],self.tet_pts[n],"a mesh constructed with no basis uses the world coords of the given points")
        
        cs = CS(Point(0,0),Vec(1,0),Vec(0,-1))
        msh = Mesh(self.tet_pts,self.tet_faces,basis=cs)
        for n in range(len(self.tet_pts)): self.assertEqual(msh[n],self.tet_pts[n],"a mesh constructed with a basis understands the given points in local coordinates")
        for n in range(len(self.tet_pts)): self.assertEqual(msh.pts[n],cs.eval(self.tet_pts[n]),"a mesh constructed with a basis understands the given points in local coordinates")

    def test_face_access(self):
        msh = Mesh(self.tet_pts,self.tet_faces)

        for n in range(len(self.tet_faces)): self.assertEqual(msh.faces[n],self.tet_faces[n],"basic face access")
        msh.add_face(1,2,3)
        self.assertEqual(msh.faces[-1],[1,2,3],"added face")

        self.assertEqual( msh.face_centroid(0) , Point.centroid([self.tet_pts[i] for i in self.tet_faces[0]]) , "face centroid")

        self.assertEqual( msh.face_normal(0) , Point(0,0,1), "face normal")


    def test_explode(self):
        msh = Mesh(self.tet_pts,self.tet_faces)
        meshes = Mesh.explode(msh)
        
        for n in range(len(meshes)):
            for m in range(3):
                self.assertEqual( self.tet_pts[self.tet_faces[n][m]] , meshes[n].pts[m] , "explode")

'''
m1 = dc.Mesh()
m1.add_vert(Vec(0.0,0.0,1.0)) #0
m1.add_vert(Vec(1.0,0.0,1.0)) #1
m1.add_vert(Vec(2.0,0.0,1.0)) #2
m1.add_vert(Vec(3.0, 0.0, 0.0)) #3
m1.add_vert(Vec(0.0, 1.0, 1.0)) #4
m1.add_vert(Vec(1.0, 1.0, 2.0)) #5
m1.add_vert(Vec(2.0, 1.0, 1.0)) #6
m1.add_vert(Vec(3.0, 1.0, 0.0)) #7
m1.add_vert(Vec(0.0, 2.0, 1.0)) #8
m1.add_vert(Vec(1.0, 2.0, 1.0)) #9
m1.add_vert(Vec(2.0, 2.0, 1.0)) #10
m1.add_vert(Vec(3.0, 2.0, 1.0)) #11
m1.add_face(0, 1, 5, 4)
m1.add_face(1, 2, 6, 5)
m1.add_face(2, 3, 7, 6)
m1.add_face(4, 5, 9, 8)
m1.add_face(5, 6, 10, 9)
m1.add_face(6, 7, 11, 10)


print "a simple mesh"
verts = [
  Point(0.0       , 0.0	      , 0.0),
  Point(0.9510565 , 0.0	      , 0.0),
  Point(0.6881910 , 1.3763819 , 0.0),
  Point(0.5257311 , 0.6881910	, 0.5)
]
faces = [[0,1,2],[0,2,3],[2,3,0],[3,0,1]]
m1 = dc.Mesh(verts,faces)
m1.set_color(Color.HSB(0.75,0.5,1.0))
m1.add_vert(Point(0,0,2))
m1.add_face(3,4,1)



print "working with face normals of meshes and colors"
normals = [Ray(mymesh.face_centroid(i),mymesh.face_normal(i)) for i in range(len(mymesh.faces))]
colorA = Color.HSB(0.0) #saturation and brightness of HSB colors default to 1.0
colorB = Color.HSB(0.75) #saturation and brightness of HSB colors default to 1.0

for ray in normals:
  angle = ray.vec.angle(Vec(0,0,1)) # constrained to 0 to PI
  t = angle / math.pi # constrained to 0 to 1
  color = Color.interpolate(colorA,colorB,t)
  ray.set_color(color)
 



print "mesh with defined basis"
m2 = dc.Mesh(faces=faces)
cs = CS(Point(2,1,1),Vec(0,1),Vec(0,0,1)) * Xform.rotation(center=Point(), angle=math.pi/2, axis=Vec(0,0,1))
m2.basis = cs
# verts with no basis will be added in basis space
m2.add_vert(Point(0.0       , 0.0	      , 0.0)) 
m2.add_vert(Point(0.9510565	, 0.0   	  , 0.0))
# verts that share a basis will be added in basis space
m2.add_vert(Point(0.6881910 , 1.3763819 , 0.0, basis=cs))
# verts with some other basis cannot be added to a mesh with a basis, 
# you should strip or apply the point's basis before adding to a mesh
bad_pt = Point(0.5257311 , 0.6881910	, 0.0, basis=CS(Point(0,0,0.5)))
m2.add_vert(bad_pt.basis_applied())


print "we can redefine the basis of the mesh, and everything follows"
cs2 = CylCS(Point(-1,-1))
m2.basis = cs2


print "manipulating the mesh vertices directly requires using the _verts reference"
m2._verts[3] += Vec(0,0,1)


print "transformations on the mesh points happen relative to the basis"
m2.verts = [v * 2 for v in m2.verts]
xf = Xform.mirror()
m2.verts = [v * xf for v in m2.verts]


print "transformations on the basis happen relative to the world"
m2.basis = m2.basis * xf

'''