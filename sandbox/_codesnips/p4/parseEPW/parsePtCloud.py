# FGC Part 4
# parsePtCloud.py
# parses a PCD file and returns a collection of points
import fieldpack as fp
from fieldpack import *

#TODO: update this to most current fieldpack version

# number of lines in the header
number_of_header_lines = 10 

def parse_pcd_file(path, skip):
  file = open(path) # open the file
  lineno = 0 # keeps track of how many lines have been parsed
  ptcloud = [] #initalize an empty list of points
  for line in file:
    if lineno > skip : # only parse this line if past the header
      pt = parse_pcd_line(line) # parse line and get array of vals
      if pt is not None : 
        ptcloud.append(Vec3d(pt[0],pt[1],pt[2]))
    lineno += 1 # keep track of how many lines have been parsed
  return ptcloud

def parse_pcd_line(string):
  #split this string using whitespace as delimiter
  #and convert to float... all in one line!
  pt = [float(n) for n in string.split()] 
  return pt[:3] #return only the first three values


# thepath to your PCD file
filepath = "p4/parseEPW/pointcloud.txt"
# if you're not sure what path you're currently working in,
# uncomment the next line
# print "WORKING PATH: "+ os.getcwd()

points = parse_pcd_file(filepath, number_of_header_lines)
for pt in points:
  pt.draw()
