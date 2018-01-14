from decodes import *
from decodes.core import *
from decodes.core import dc_base, dc_color

if VERBOSE_FS: print("outie loaded")
import copy, collections

class Outie(object):
    """base outie class"""
    
    def __init__(self):
        self.iconscale = 1.0 # a scale factor for icons
        self.geom = [] # a simple list of geometry
        self._allow_foreign = False

    def __iadd__(self, other): 
        #todo: outie += other_outie should combine these outies
        self.put(other)
        return self
    
    def put(self,ngeom):
        
        if self._allow_foreign : 
            self.geom.append(copy.deepcopy(ngeom)) # if we allow foreigners, just put in whatever they gave us
        else:
            if ngeom is None : return
            if isinstance(ngeom, (Geometry) ) :
                if isinstance(ngeom, (HasBasis) ) and ngeom.do_translate : 
                    try:
                        ngeom = ngeom.basis_applied()
                        # self.geom.append(copy.deepcopy(ngeom))
                        self.geom.append(ngeom)
                    except:
                        self.geom.append(ngeom)
                else:
                    self.geom.append(ngeom)
            elif isinstance(ngeom, collections.Iterable) : 
                for g in ngeom : self.put(g)
            else : 
                raise NotImplementedError("This doesn't look like Decodes Geometry!\nThis outie doesn't allow foreigners!\n{0}".format(ngeom))
        
        
    def draw(self):
        #iterates over the geom list, 
        #calls the (hopefully overridden) draw function for each geometric object
        #returns a list of successful writes
        self._startDraw()
        try:
            results = list(map(self._drawGeom, self.geom))
            if False in results:
                print("dump not completely successful, the following geometry was not written:")
                i = -1
                try:
                    while 1:
                        i = results.index(False, i+1)
                        print(str(i) , self.geom[i])
                except ValueError:
                    pass
        
            self._endDraw() #finish up anything we need to in our drawing context
            self.clear() #empty the outie after each draw
            return results
        except:
            self._endDraw()
            raise
        
        
    def clear(self):
        self.geom = []
        
    def set_color(self,a,b=None,c=None):
        if not hasattr(self, 'props') : self.props = {}
        if isinstance(a, (Color) ) : self.props['color'] = a
        else : self.props['color'] = Color(a,b,c)
        
    def _startDraw(self):
        pass
        
    def _endDraw(self):
        pass