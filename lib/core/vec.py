import fieldpack as fp
import math, random
if fp.VERBOSE_FS: print "vec.py loaded"


class Vec(fp.Geometry):
  
  def __init__(self, a=0, b=0, c=0):
    if all( hasattr(a,i) and hasattr(b,i) for i in ['x','y','z'] ) :
      # we've been passed two things that act like points
      self._x = a.x - b.x
      self._y = a.y - b.y
      self._z = a.z - b.z  
    elif all([hasattr(a,'x'),hasattr(a,'y'),hasattr(a,'z')]):
      # we've been passed one thing that acts like a vec
      self._x = a.x
      self._y = a.y
      self._z = a.z
    else :
      self._x = a
      self._y = b
      self._z = c

  @property
  def x(self): return self._x
  @x.setter
  def x(self,value): self._x = value
  
  @property
  def y(self): return self._y
  @y.setter
  def y(self,value): self._y = value
  
  @property
  def z(self): return self._z
  @z.setter
  def z(self,value): self._z = value

  def __add__(self, vec): return Vec(self.x+vec.x , self.y+vec.y, self.z+vec.z)
  def __sub__(self, vec): return Vec(self.x-vec.x , self.y-vec.y, self.z-vec.z)
  def __div__(self, other): return Vec(self.x/float(other), self.y/float(other), self.z/float(other))
  def __invert__(self): return self.inverted()
  def __mul__(self, other):
    if isinstance(other, fp.Xform) :
      return other*self
    else : 
      #TODO: confim that other is a scalar
      return Vec(self.x * other, self.y * other, self.z * other)



  def __repr__(self): return "vec[{0},{1},{2}]".format(self.x,self.y,self.z)
  def to_tuple(self): return (self.x,self.y,self.z)

  def __lt__(self, other): return self.length2 < other.length2
  def __le__(self, other): return self.length2 <= other.length2
  def __eq__(self, other): return self.length2 == other.length2
  def __ne__(self, other): return self.length2 != other.length2
  def __gt__(self, other): return self.length2 > other.length2
  def __ge__(self, other): return self.length2 >= other.length2
  
  def is_identical(self,other): return all([self.x==other.x,self.y==other.y,self.z==other.z])
  def is_coincident(self,other): return self.normalized().is_identical( other.normalized() )
  
  @property
  def is_2d(self): return True if (self.z==0) else False
  
  @property
  def length(self): return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
  
  '''Length squared. Cheaper to calculate.'''
  @property 
  def length2(self):
      return self.x ** 2 + self.y ** 2 + self.z ** 2
  
  '''Length setter. Resizes vector.'''
  @length.setter
  def length(self,value): 
    factor = value / self.length
    self.x *= factor
    self.y *= factor
    self.z *= factor
  
  '''Linearly interpolates between vectors v1 and v2 at param t'''
  @staticmethod
  def interpolate(v0,v1,t=0.5):
    x = (1-t) * v0.x + t * v1.x
    y = (1-t) * v0.y + t * v1.y
    z = (1-t) * v0.z + t * v1.z
    return Vec(x,y,z)

  @staticmethod
  def random(rnge=[-1.0,1.0],normalize=True,constrain2d=False):
    x = random.uniform(rnge[0],rnge[1])
    y = random.uniform(rnge[0],rnge[1])
    z = random.uniform(rnge[0],rnge[1])
    v = Vec(x,y) if constrain2d else Vec(x,y,z)
    if normalize : return v.normalized()
    return v

  '''Returns the average of a list of vectors'''
  @staticmethod
  def average(vecs):
    return Vec( 
      sum([float(v.x) for v in vecs])/len(vecs) , 
      sum([float(v.y) for v in vecs])/len(vecs) , 
      sum([float(v.z) for v in vecs])/len(vecs) 
    )

  '''Returns the normalized bisector of two vectors'''
  @staticmethod
  def bisector(v0,v1): return Vec.average([v0.normalized(),v1.normalized()])      

  '''Return a new vector in the same direction, but given length (default 1.0)'''
  def normalized(self, length=1.0):
      factor = length / self.length
      return Vec(self.x * factor, self.y * factor, self.z * factor)    

  '''Return a new vector pointing in the opposite direction'''
  def inverted(self): return Vec(-self.x,-self.y,-self.z)
  
  '''Returns a new vector with coords rounded to n-digits (defaults to 0 digits (nearest int) )'''
  def rounded(self,n=0): return Vec(round(self.x,n),round(self.y,n),round(self.z,n))
  
  '''Returns a new vector limited to a given length'''
  def limited(self,n=1.0): 
    if self.length2 < n**2 : return Vec(self.x,self.y,self.z)
    return self.normalized(n)  
  
  '''Computes the dot product of this vector and the other vector'''
  def dot(self,other): return (self.x * other.x + self.y * other.y + self.z * other.z)

  '''Returns the length of the vector which results from the projection of this onto other'''
  def projected_length(self,other): return self.dot(other.normalized)

  '''Returns a new vector projected onto a destination vector'''
  def projected(self,other): return other * ( self.dot(other) / other.dot(other) )

  def cross(self, other):
      '''
      Return a new vector, the cross product.
      a x b = (a2b3 - a3b2, a3b1 - a1b3, a1b2 - a2b1)
      This will be at right angles to both self and other, with a length::
          len(self) * len(other) * sin(angle_between_them)
      '''
      return Vec(
          self.y * other.z - self.z * other.y,
          self.z * other.x - self.x * other.z,
          self.x * other.y - self.y * other.x
      )

  '''
  Returns the angle in radians between this vector and the other vector 
  return value is constrained to the range [-PI,PI].
  '''
  def angle(self,other):
    vdot = self.dot(other) / (self.length * other.length)
    if vdot>1.0 : vdot = 1.0
    if vdot<-1.0 : vdot = -1.0
    return math.acos(vdot)
    
  def angle_deg(self,other): return math.degrees(self.angle(other))


