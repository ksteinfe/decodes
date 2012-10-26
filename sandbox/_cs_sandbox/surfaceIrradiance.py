#surfaceIrradiance: this visualizes surface irradiance on an elliptical tower for a fixed time
#and a normal irradiaton I_n calculated using a placeholder function

import math
import rhinoscriptsyntax as rs
import fieldpack.extensions.solarGeom as sg


#1. Capturing the buiding geometry
# This example takes an elliptical plan for each floor and generates a set of
# points where each floor have a point distribution that is a rotated version
# of the floor before.  This is captured as a double list, with the first index
# cycling over the number of floors, and second index capturing the points
# on each floor


def getPointsTower(numFloors, numPoints):
	interval = 2*math.pi/numPoints
	rot = interval/7
	height = 200/numFloors
	pOut = []
	for floor in range(numFloors):
		pOut.append([])
		for i in range(numPoints):
			t = i*2*math.pi/numPoints+floor*rot
			x = 32.5*math.cos(t)
			y = 55*math.sin(t)
			z = floor*height
			pOut[floor].append([x,y,z])
	return pOut

	
# 2. Performing a solar incidence analysis on the geometry
# A. Use placeholder function which returns a normal irradiation for an input of day
#    in the year and hour of the day 
def dirNormalIrad_Placeholder(day, hour):
	return 1000*max(0, -math.cos(hour*math.pi/12) + 1/8.0 - (day-171)**2/115600)

# B. Read in from a file (dirNormals.txt) which has already stripped the normal
#    column from an EPW file and puts it in the 4th column
def dirNormalIrad_fromFile(fileIn):
    number_of_header_lines=2
    #declare list
    dirNormalIradList=[]
    lineno=0
    #loop through lines
    for line in file:
        #skip header
	if lineno > number_of_header_lines - 1 :
	    #for a generic line, data is an array of four numbers
	    #delimiter is white space
	    data = [int(n) for n in line.split()]
	    #extract data from 4th column and append to direct irradiance list initiated earlier
	    dirNormalIradList.append(data[3])
	lineno = lineno + 1
    return dirNormalIradList



def AddVector(vecdir, base_point):
	if base_point==None:
		base_point = [0,0,0]
	tip_point = rs.PointAdd(base_point, vecdir)
	line = rs.AddLine(base_point, tip_point)
	if line:
		return rs.CurveArrows(line, 2)

# surfaceIrradiance_fixed:  takes a sun vector and a fixed value intensityIn (corresponding to a fixed time)
# and generates a vector at each plane on the tower that is proportional to the surface irradiance on each plane.
def surfaceIrradiance_fixed(towerIn, sunIn, intensityIn):
	sunUnit = rs.VectorUnitize(sunIn)
	for floor in range(len(towerIn)):
		numPoints = len(towerIn[floor])
		for i in range(numPoints):
			p1 = towerIn[floor][i]
			p2 = towerIn[floor][(i+1)%numPoints]
			v1 = rs.VectorSubtract(p2, p1)
			v2 = [0,0,1]		
			n = rs.VectorCrossProduct(v1, v2)
			if rs.VectorLength(n) > rs.UnitAbsoluteTolerance(10**(-3), True):
				cosTheta = rs.VectorDotProduct(rs.VectorUnitize(n), sunUnit)
				if cosTheta > 0:
					factor = intensityIn*cosTheta/200  #200 is just to shorten the vector to something manageable
					v = rs.VectorScale(n, factor)
					AddVector(v, p1)


# surfaceIrradiance_aggregate:  takes a list of sun vectors in sunIn and normal irradiance values in intensityIn
# (sunIn and intensityIn corresponds to the same time period - no checks currently done) and generates
# a vector at each plane on the tower that is proportional to the max aggregated surface irradiance on each plane.
def surfaceIrradiance_aggregateMax(towerIn, sunIn, intensityIn):
	N = len(sunIn)
	for floor in range(len(towerIn)):
		numPoints = len(towerIn[floor])
		for i in range(numPoints):
			p1 = towerIn[floor][i]
			p2 = towerIn[floor][(i+1)%numPoints]
			v1 = rs.VectorSubtract(p2, p1)
			v2 = [0,0,1]		
			n =  rs.VectorCrossProduct(v1, v2)
			if rs.VectorLength(n) > rs.UnitAbsoluteTolerance(10**(-3), True):
				factors = []
				for j in range(N):
					sunUnit = rs.VectorUnitize(sunIn[j])
					cosTheta = rs.VectorDotProduct(rs.VectorUnitize(n), sunUnit)
					if cosTheta > 0:
						factors.append(intensityIn[j]*cosTheta)
			factor = max(factors)/200  #200 is just to shorten the vector to something manageable
			v = rs.VectorScale(n, factor)
			AddVector(v, p1)



# Get the points of the tower 
tower = getPointsTower(30, 10)
print tower
# Fix a location 
latitude = 40.75
longitude = -73.5
timezone = -5.0

#----------------------------------------------------------------------------------------------------------------
# First calculate surface irradiance on the tower for a fixed hour of a given day
day = sg.calc_dayOfYear("03/16")
hour = sg.calc_hourDecimal("13:00")
sun = rs.VectorUnitize(sg.calc_sunVector(latitude, longitude, timezone, day, hour))

#define the direct normal data file to use for irradiance values 
file = open("c:\dirNormals.txt", "r")
dirNormalIrad=dirNormalIrad_fromFile(file)

#retrieve the corresponding value of I_n for the particular hour that we're interested in;

#I_n = dirNormalIrad_Placeholder(day, h)
I_n = dirNormalIrad[int((day-1)*24 + hour -1)]  #currently rounds to the nearest hour if reading from file
surfaceIrradiance_fixed(tower, sun, I_n)

#----------------------------------------------------------------------------------------------------------------
#Next, let's calculate an aggregated surface irradiance over a consecutive period of time 
dayStart = sg.calc_dayOfYear("03/21")
dayEnd = sg.calc_dayOfYear("06/21")

#create the lists for the sun vector and normal irradiance values during this time;  here,
#we only keep the values corresponding to a sun vector that has a positive z-value
sunList = []
dirNormalIradList = []

for day in range(dayStart, dayEnd+1):
	for h in range(24):
		sun = rs.VectorUnitize(sg.calc_sunVector(latitude, longitude, timezone, day, h))
		if sun[2] > 0:
			sunList.append(sun)
			dirNormalIradList.append(dirNormalIrad[int((day-1)*24 + h)])

						 
			
#surfaceIrradiance_aggregateMax(tower, sunList, dirNormalIradList)