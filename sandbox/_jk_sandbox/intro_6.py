#BASIC I/O

# Opening a file creates a file object.  You will need to open a file before you
# can either read or write into a file.
# open() takes two arguments:  the first is the name of the data file that you want to open.
# The second is the mode -  "w" = write, "r" = read

# for writing, once you open a file, it will either create a file of that name if it doesn't
# exist or it will replace a file by that name (be careful not to open a file that you don't
# want to replace)
f = open("test.dat", "w")
# to put data into the file, use the write command
f.write("Welcome to my mod columns\n")
f.write("i \t %2 \t %3 \t %4 \n")
for i in range(20):
	f.write(str(i) + "\t" + str(i%2) + "\t" + str(i%3) +"\t" + str(i%4)+"\n")
# closing the file indicates that we are done writing and can be made available for reading
f.close()

# you can now open it again if we want to read the file
# (it will give you an error if you try to open a file that doesn't exist)
f = open ("test.dat", "r") 

# we can use the read method to read data from the file
# it can take an argument of the number of characters to be read
content = f.read(5)
print "First 5 characters are:", content

# now notice that if I keep on reading, it will only start at the place I just left off
content = f.read(10)
print "Next 10 characters are:", content

# if you want to start all over and read from the beginning, you have to close the file and
# reopen it
f.close()
f = open("test.dat", "r")
# Now if no arguments are supplied, then the entire text is read
contentAll = f.read()
print contentAll


# Parsing a Tabular Data File
# Ex. PCD File, EPW file - show examples of these

# We will be reading in dirNormal.dat 

# let's try reading in just the first couple lines of the file
file = open("dirNormals.txt", "r") # open the file
print file.readline()
print file.readline()
file.close()

# let's store just the directNormals into a list

#number of lines in the header
number_of_header_lines = 2

file = open("dirNormals.txt", "r") # open the file
lineno = 0 # keeps track of how many lines have been parsed
dirNormalIrad = []
for line in file:
	if lineno > number_of_header_lines-1 : # only parse this line if past the header
		data = [int(n) for n in line.split()]
		dirNormalNow = data[3]
		if dirNormalNow is not None:
			dirNormalIrad.append(dirNormalNow)
	lineno += 1 # keep track of how many lines have been parsed

file.close()

print len(dirNormalIrad)


def parseEx_file(filename, skip, col):
	file = open(filename)
	lineno = 0 # keeps track of how many lines have been parsed
	dataOut = []
	for line in file:
		if lineno > skip-1 : # only parse this line if past the header
			dataCol = parseEx_line(line, col)
			if dataCol is not None:
				dataOut.append(dataCol)
		lineno += 1 # keep track of how many lines have been parsed
	file.close()
	return dataOut

def parseEx_line(string, col):
  #split this string using whitespace as delimiter
  data = [int(n) for n in string.split()] 
  return data[col-1] #return only the first three values


fileName = "dirNormals.txt"
number_of_header_lines = 2
columnNumber = 4 #the column that we want to extract
dirNormalData = parseEx_file(fileName, number_of_header_lines, columnNumber)


# Since I've chosen a file that has complete data, i.e. 8760 hours in a year, I can easily
# extract out the direct normal for any (whole) hour of the year
import solarGeom as sg

date = "3/23"
h = "13:00"
day = sg.calc_dayOfYear(date)
hour = sg.calc_hourDecimal(h)
hourYear = (day-1)*24 + int(hour)-1
print "Direct Normal Irradiation on "+date+" at "+h+" is "+str(dirNormalData[hourYear])+" w/m^2"

# we don't have data that gives us continuous measurement between hours.  You can either decide
# to just take the data on the whole hour -- i.e. 13:30 has the same data as at 13:00 -- or
# you can interpolate the data

