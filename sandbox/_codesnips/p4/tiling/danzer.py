import fieldpack as fp
from fieldpack import *
import fieldpack.extensions.danzerTile as dt


maxRecursion = 5
def recurse(tiles,rlvl=0):
  if rlvl < maxRecursion : 
    return [recurse(tile.inflate(),rlvl+1) for tile in tiles]
  else :
    #for tile in tiles : outie.put(tile.draw()) 
    return [tile.draw() for tile in tiles]

outie = fp.make_out(fp.outies.Rhino, "tiles")
outie.put( recurse([dt.DzTileK()]) ) 
outie.draw()


