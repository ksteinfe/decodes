import fieldpack as fp
from fieldpack import *
import fieldpack.extensions.pinwheelTile as pt



def main():
 #simpleTiling()
 attractorTiling()

def attractorTiling():
  outie = fp.make_out(fp.outies.Rhino, "tiles")
  attPt = Point(0.666,0.333)
  
  maxRecursion = 6
  baseDist = 0.9 # totally arbitrary
  falloff = 1.2 # also totally arbitrary
  def recurse(tiles,rlvl=0):
    if rlvl >= maxRecursion : return tiles
    moreTiles = []
    for tile in tiles :
      if attPt.distance(tile.centroid()) < baseDist/math.pow((rlvl+1),falloff) : 
        for t in recurse(tile.inflate(),rlvl+1) : moreTiles.append(t)
      else : moreTiles.append(tile)
    return moreTiles

  tiles = recurse([pt.PwTile()])
  print tiles
  for tile in tiles : 
    if attPt.distance(tile.centroid()) < baseDist/2 : outie.put(tile.draw()) 
  outie.draw()



def simpleTiling():
  outie = fp.make_out(fp.outies.Rhino, "tiles")
  
  maxRecursion = 3
  def recurse(tiles,rlvl=0):
    if rlvl >= maxRecursion : return [tile.draw() for tile in tiles]
    return [recurse(tile.inflate(),rlvl+1) for tile in tiles]
  
  cs = CS(Point(1,1),Vec(1,-1))
  outie.put( recurse([pt.PwTile(xf=cs.xform)]) ) 
  outie.draw()



if __name__=="__main__": main()
