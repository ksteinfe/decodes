import decodes.core as dc
from decodes.core import *

def main():
    outie = dc.makeOut(dc.outies.Rhino, "wayout")
    epw = fake_epw_data()
    minHr = 0
    maxHr = 8760
    origin = Point(10.0, 10.0, 0.0)
    recWidth = 10
    recHeight = 50
    
    for h in range(minHr, maxHr):
        db = epw[h]["DryBulbTemp"]
        rh = epw[h]["RelHumid"]
        recColor = Color.RGB(mapVal(db,0,365,0,1), mapVal(rh, 0,365, 0,1), .5)
        outie.put(rec(origin, recWidth, recHeight, recColor)) 
        origin=origin+Vec(0, recHeight)
        if h%24 ==0: origin=origin+Vec(recWidth, recHeight*-24)
    outie.draw()
    
    
def mapVal(inVal, inMin, inMax, outMin, outMax):
    outRange = outMax - outMin
    inRange = inMax - inMin
    inVal = inVal - inMin
    val=(float(inVal)/inRange)*outRange
    outVal = outMin+val
    return outVal
    
#draws a rectangle at the passed origin with the passed dimensions and color
def rec(origin=Point(0.0, 0.0, 0.0), width=1, height=1, color=Color.HSB(0.75,0.5,1.0)):
    verts = [
      Point(origin.x , origin.y, 0.0),
      Point(origin.x+width , origin.y , 0.0),
      Point(origin.x+width , origin.y+height, 0.0),
      Point(origin.x, origin.y+height, 0.0)
    ]
    faces = [[0,1,2,3]]
    m1 = dc.Mesh(verts,faces)
    m1.set_color(color)
    return m1

def fake_epw_data():
  """ returns fake data of an EPW file
  out: a list (8760 long) of dicts containing EPW data values
  """
  ret = []
  for h in range(8760):
    dict = {}
    dict['DryBulbTemp'] = h%24
    dict['RelHumid'] = h%365
    ret.append(dict)
    
  return ret


if __name__=="__main__": main()


