# FGC Part 4
# parsePtCloudWIthCSVmodule.py
# parses a PCD file and returns a collection of points
import fieldpack as fp
from fieldpack import *
import csv #OOOPS!!! Looks like CSV module is not available in IronPython
        
# the path to your PCD file
filepath = "p4/parseEPW/pointcloud.txt" 
# number of lines in the header
number_of_header_lines = 10

def parse_pcd_file(path, skip):
  file = open(path) # open the file
  lineno = 0 # keeps track of how many lines have been parsed
  ptcloud = [] #initalize an empty list of points
  for row in csv.reader(file, delimiter='\t'):
    if lineno > skip : # only parse this line if past the header
      print row
    lineno += 1 # keep track of how many lines have been parsed
  return ptcloud


points = parse_pcd_file(filepath, number_of_header_lines)
for pt in points:
  pt.draw()
