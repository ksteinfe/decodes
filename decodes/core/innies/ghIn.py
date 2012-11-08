from decodes import core as dc
from decodes.core import *


if dc.VERBOSE_FS: print "ghIn loaded"


class RhinoIn():
  """innie for pulling stuff from grasshopper"""
  
  def __init__(self):
    pass
    
  def get(self, gh_incoming):
    # main function for processing incoming data from Grasshopper into Decodes geometry
    # incoming may be a sigleton, a list, or a datatree
    # variable in GH script component will be replaced by whatever is returned here
    
    return False
    
