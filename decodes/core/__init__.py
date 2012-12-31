print "decodes core loaded"

VERBOSE_FS = True # determines if we verify file system loaded right
VERBOSE = True

#__all__ = ["base", "color"]

#from outies import *
#from innies import *
from color import *

from base import *
from vec import *
from point import *
from cs import *

from line import *

from mesh import *
from pgon import *

from xform import *
from intersection import *



# keep this up to date with what outies we support
def makeOut(outtype, name="untitled", path=False):
  """This function constructs a new outie of the given type.
  
    :param outtype: The type of outie to create
    :type outtype: decodes.outies.outie.XXX
    :param name: The name of the outie to create.  This name is used in different ways, depending on the context to which we will be drawing geometry
    :type name: string or "untitled"
    :param path: If an outie creates a file, the filepath to save to.
    :type path: string
    :rtype: child of decodes.outies.outie
  """

  if outtype == outies.Rhino:
    return outies.RhinoOut(name)
  elif outtype == outies.Grasshopper:
    return outies.GrasshopperOut(name)
  elif outtype == outies.SVG:
    if path : return outies.SVGOut(name, path)
    else : return outies.SVGOut(name)
  else :
    print "!!! hey, i don't have an outie of type foo !!!"
    return False

# keep this up to date with what outies we support
def makeIn(intype):
  if intype == innies.Rhino:
    return innies.RhinoIn()
  if intype == innies.Foo:
    if VERBOSE : print "!!! hey, i don't have an innie of type foo !!!"
    return False
