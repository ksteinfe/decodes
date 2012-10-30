import fieldpack as fp
from fieldpack import *


def main():
 outie = fp.makeOut(fp.outies.Rhino, "wayout")
 
 epw = fake_epw_data()
 print epw
 
 outie.draw()


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


