# FGC Part 4
# parseEPW.py
# parses a EPW file and returns a nicely formatted dataset
import collections
import fieldpack as fp
from fieldpack import *

# number of lines in the header
# holds true for ALL EPW files
number_of_epw_header_lines = 8
# a dictionary that maps keystrings to column positions
# not a comprehensive list. for a complete listing, see
# apps1.eere.energy.gov/buildings/energyplus/
#     pdfs/weatherdatainformation.pdf
epw_keycols = {
  "DirNormIrad": 14, #direct normal irradiance (w/m2)
  "DifHorzIrad": 15, #diffuse horizontal irradiance (w/m2)
  "OpqSkyCvr": 23 , #opaque sky cover (tenths of sky)
  "DryBulbTemp": 6 , #dry bulb temperature (deg C)
  "DewPtTemp": 7 , #dew point temperature (deg C)
  "RelHumid": 8 , #relative humidity (%)
  "Pressure": 9 , #atmospheric station pressure (Pa)
  "WindDir": 20 , #wind direction (degrees)
  "WindSpd": 21 , #wind speed (m/s)
  "PreciptWater": 28 , #precipitable water (mm)
  "AeroDepth": 29 , #aerosol depth (1000ths)
  "SnowDepth": 30 , #snow depth (cm)
  "YearOfSample": 0 , #year of sample data
}

def main():
  # the path to your EPW file
  filepath = "p4/parseEPW/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
  # if you're not sure what path you're currently working in,
  # uncomment the next line
  # print "WORKING PATH: "+ os.getcwd()

  # a list of the keys we want to extract from the EPW
  keys = ["DryBulbTemp", "RelHumid", "DirNormIrad"]

  hours = parse_epw_file(filepath, keys)
  for i, hr in enumerate(hours):
    print ("for hour "+str(i)
        +", db="+hr["DryBulbTemp"]
        +", rh="+hr["RelHumid"]
        )
  


def parse_epw_file(path, desired_keys):
  skip = number_of_epw_header_lines
  file = open(path) # open the file
  lineno = 0 # keeps track of how many lines have been parsed
  hours = [] #initalize an empty list where we'll store our dicts
  for line in file:
    if lineno >= skip : # only parse this line if past the header
      hourdict = parse_epw_line(line, desired_keys) # parse line
      if hourdict is not None : 
        hours.append(hourdict)
    lineno += 1 # keep track of how many lines have been parsed
    if lineno > 8760+skip : break
  return hours

def parse_epw_line(string, desired_keys):
  vals = string.split(",")
  dict = {k:vals[epw_keycols[k]] for k in desired_keys}
  return dict #return the dictionary of values



# Here we check to see if this file is being executed as the "main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if __name__ == '__main__' : 
  main()