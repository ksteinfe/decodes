#!python

from decodes.core import *
# from . import dc_base, dc_interval, dc_vec, dc_point, dc_plane, dc_cs, dc_circle
if VERBOSE_FS: print("dc_cylinder.py loaded")



class Cylinder(Circle):
    """
    right circular cylinder
    CircleGeometry(radius, segments, thetaStart, thetaLength)
    PlaneGeometry(width, height, widthSegments, heightSegments)
    CylinderGeometry(radiusTop, radiusBottom, height, radiusSegments, heightSegments, openEnded, thetaStart, thetaLength)

    """
    def __init__(self, plane, radius, height):
        self.height = height
        super().__init__(plane, radius)
    
    def __repr__(self): return "cylinder[{0},{1},{2},{3},{4},{5} r:{6} h:{7}]".format(self.x,self.y,self.z,self._vec.x,self._vec.y,self._vec.z,self.rad,self.height)

    def contains(self, pt):
        if(self.near_pt(pt).dist(self) >= self.rad):
            return False
        return super().contains(pt, self.height * 0.5)

# entry point
if __name__ == "__main__":
  print("main")
  o = Cylinder(Plane(), 5, 10)

  print(o)
  print("contains %d" % (o.contains(Point(4.5,0,4.9))))
