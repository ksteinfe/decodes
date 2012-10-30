print "decodes core loaded"
VERBOSE_FS = False # determines if we verify file system loaded right
VERBOSE = True



#ERASE ME
#from thingo import *
#from thato import *

from outies import *
#from innies import *
from color import *

from base import *
from vec import *
from point import *
from mesh import *
from cs import *
from xform import *
from line import *
from intersection import *



# keep this up to date with what outies we support
def makeOut(outtype, name):
  if outtype == outies.Rhino:
    return outies.RhinoOut(name)
  if outtype == outies.Foo:
    if VERBOSE : print "!!! hey, i don't have an outie of type foo !!!"
    return False

# keep this up to date with what outies we support
def makeIn(intype):
  if intype == innies.Rhino:
    return innies.RhinoIn()
  if intype == innies.Foo:
    if VERBOSE : print "!!! hey, i don't have an innie of type foo !!!"
    return False
