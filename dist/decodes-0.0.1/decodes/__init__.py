print "http://decod.es"

"""A Platform-Agnostic Computational Geometry Environment 

.. moduleauthor:: Kyle Steinfeld <ksteinfe@gmail.com>

"""

class Outies:
  # list here all the outies we currently support
  Rhino, Grasshopper, SVG = range(3)


# keep this up to date with what outies we support
def makeOut(outtype, name="untitled", path=False):
  """This function constructs a new outie of the given type.
  
    :param outtype: The type of outie to create
    :type outtype: int (enumerated from Outies class)
    :param name: The name of the outie to create.  This name is used in different ways, depending on the context to which we will be drawing geometry
    :type name: string or "untitled"
    :param path: If an outie creates a file, the filepath to save to.
    :type path: string
    :rtype: child of decodes.outies.outie
  """
  import io.outie

  if outtype == Outies.Rhino:
    import io.rhino_out
    return io.rhino_out.RhinoOut(name)
  elif outtype == Outies.Grasshopper:
    import io.gh_out
    return io.gh_out.GrasshopperOut(name)
  elif outtype == Outies.SVG:
    import io.svg_out
    if path : return io.svg_out.SVGOut(name, path)
    else : return io.svg_out.SVGOut(name)
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
