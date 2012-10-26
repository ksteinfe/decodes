import fieldpack as fp
from fieldpack import *
innie = fp.makeIn(fp.innies.Rhino)
outie = fp.makeOut(fp.outies.Rhino, "wayout")



#outie.put(innie.get_point())

print "a user selected mesh"
innie = fp.makeIn(fp.innies.Rhino)
mymesh = innie.get_mesh()
mymesh *= Xform.translation(Vec(0,0,5))
outie.put(mymesh)


print "working with face normals of meshes and colors"
normals = [Ray(mymesh.face_centroid(i),mymesh.face_normal(i)) for i in range(len(mymesh.faces))]
colorA = Color.HSB(0.0) #saturation and brightness default to 1.0
colorB = Color.HSB(0.75) #saturation and brightness default to 1.0

for ray in normals:
  angle = ray.vec.angle(Vec(0,0,1)) # constrained to 0 to PI
  t = angle / math.pi # constrained to 0 to 1
  color = Color.interpolate(colorA,colorB,t)
  ray.set_color(color)
  
outie.put(normals)




outie.draw()