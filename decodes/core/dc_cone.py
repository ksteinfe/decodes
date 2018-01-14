#!python

from decodes.core import *
# from . import dc_base, dc_interval, dc_vec, dc_point, dc_plane, dc_cs, dc_circle
if VERBOSE_FS: print("dc_cone.py loaded")
import math

class Cone(Circle):
    """
    A 3d right circular cone class
    
    In the Cartesian coordinate system, an elliptic cone is the locus of an equation of the form:
    x2   y2   z2
    -- + -- = --
    a2   b2   c2

    """
    def __init__(self, plane, radius, height):
        self.height = height
        super().__init__(plane, radius)
    
    def __repr__(self): return "cone[{0},{1},{2},{3},{4},{5} r:{6} h:{7}]".format(self.x,self.y,self.z,self._vec.x,self._vec.y,self._vec.z,self.rad,self.height)

    def contains(self, pt):
        # the axis vector, pointing from the base to the tip
        cone_axis = self.normal * self.height
        # project pt onto axis to find the point's distance along the axis:
        cone_dist = math.sqrt(cone_axis.dot(pt - self.origin))
        if cone_dist < 0 or cone_dist > self.height:
            # point is above or below cone
            return False

        # Then you calculate the cone radius at that point along the axis:
        cone_radius = (cone_dist / self.height) * self.rad
        # And finally calculate the point's orthogonal distance from the axis to compare against the cone radius:
        orth_distance = (pt - self.origin) - self.normal * cone_dist

        if orth_distance > cone_radius:
            # point is to the side of the cone
            return False
        return True

    def volume(self):
        """
        V = 1/3 * Ab * h
        """
        return((math.pi * self.rad * 2.0 * self.height) / 3)

# entry point
if __name__ == "__main__":
  print("main")
  o = Cone(Plane(), 5.0, 10.0)

  print(o)
  print("contains %d" % (o.contains(Point(0.0, 0.0, 5.0))))
  print("volume %f" % (o.volume()))

