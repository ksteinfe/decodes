from decodes import core as dc
if dc.VERBOSE_FS: print "outie loaded"
import copy, collections

class Outie(object):
  """base outie class"""
  
  def __init__(self):
    self.iconscale = 1.0 # a scale factor for icons
    self.geom = [] # a simple list of geometry
    
  def put(self,ngeom):
    if isinstance(ngeom, (dc.HasBasis) ) :
      ngeom = ngeom.basis_applied()
    if isinstance(ngeom, (dc.Geometry) ) :
      self.geom.append(copy.deepcopy(ngeom))
    elif isinstance(ngeom, collections.Iterable):
        for g in ngeom : self.put(g)
    else :
      raise NotImplementedError("This doesn't look like Fieldpack Geometry!\nYou can't put that in an outie!\n{0}".format(ngeom))
    
  def draw(self):
    #iterates over the geom list, 
    #calls the (hopefully overridden) draw function for each geometric object
    #returns a list of successful writes
    self._startDraw()
    results = map(self._drawGeom, self.geom)
    if False in results:
      print "dump not completely successful, the following geometry was not written:"
      i = -1
      try:
        while 1:
          i = results.index(False, i+1)
          print str(i) , self.geom[i]
      except ValueError:
        pass
    
    self._endDraw() #finish up anything we need to in our drawing context
    self.clear() #empty the outie after each draw
    return results
    
  def as_drawn(self):
    #iterates over the geom list,
    #calls the overridden draw function for each geometric object
    #returns a list of whatever these draw functions return
    
    self._startDraw()
    results = map(self._drawGeom, self.geom)
    self._endDraw()
    self.clear() #empty the outie after each draw
    return results
    
  def clear(self):
    self.geom = []
    
  def set_color(self,a,b=None,c=None):
    if not hasattr(self, 'props') : self.props = {}
    if isinstance(a, (dc.Color) ) : self.props['color'] = a
    else : self.props['color'] = dc.Color(a,b,c)
    
  def _startDraw(self):
    pass
    
  def _endDraw(self):
    pass