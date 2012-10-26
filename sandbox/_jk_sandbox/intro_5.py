import rhinoscriptsyntax as rs
import math

#Lists redux
# A list is a sequence of objects.
# We've now worked with lists of the same types of objects, like integers 
listInt = [1, 2, 4, 6, 3, 7, 12]

# or lists of points;  this is actually a list within a list and is said to be nested
p1 = [1, 2, 0]
p2 = [-2, 3, 0]
p3 = [-1, 2, 100]
listPoints = [p1, p2, p3]

#but lists can also comprise heterogeneous objects.
listMisc = ["time", 3.15, 10, [1, 4, 5]]

#notice that even though a list can contain another list, the length of this list is still 4
print len(listMisc)

# Lists with consectutive or evenly-spaced integers are so common that there is a built-in
# function that does exactly this
print range(17)
print range(3, 17)
print range(0, 21, 3)

# and of course there is always the empty list which is often used to assign a list
# variable that will be filled in the course of the program
listEmpty = []

# Lists are mutable, meaning that we can change any element within the list
#listInt = [1, 2, 4, 6, 3, 7, 12]
listInt[0] = 5
print listInt

# or change several elements using slicing
listInt[2:4] = [10, 20]
print listInt

# or change every element in the list;  for instance, scaling by a uniform scaling k
k = -2
listInt[:] = [k*x for x in listInt]
print listInt

# we can also delete an element from a list:
del listInt[1]
print listInt

# or several using slicing
del listInt[2:5]
print listInt


# Sometimes, it will be useful to modify a list but also to keep a copy of the original.
# This is called cloning
listIntClone = listInt[:]
#Now you can work with listIntClone and this won't affect listInt.
listIntClone.append(0)
print listIntClone
print listInt

# Notice that this is different if you were to just assign a list to another.
# This is called aliasing
listIntAlias = listInt
listIntAlias.append(0)
print listIntAlias
print listInt
	
	
# Lists and Loops
# The general syntax for lists and while is given by
# i = 0
# while i < len(LIST):
#	VARIABLE = LIST[i]
#	STATEMENTS
#	i = i + 1
#
# This is equivalent to the syntax for lists and for loops (slightly more concise)
# for VARIABLE in LIST:
#	STATEMENTS
#
# This is useful if we wanted to assign a sequence of N points spaced at equal
# intervals along the x-axis, for example
N = 17
interval = 2.5

pointsX = []
for i in range(N):
	curPoint = [i*interval, 0, 0]
	pointsX.append(curPoint)

# if we now want to draw out a subset of these points (like every other point), we can as
# easily do this by accessing every other index
for i in range(0, N, 2):
	rs.AddPoint(pointsX[i])

# pointsX is now a nested list, since each point is expressed as a list of 3 numbers itself.
print pointsX[2]
# to access the y-coordinate of this point, we can write this as
print pointsX[2][1]

# If you want to translate each point up by 1 unit in the y direction, we can do this
# by changing the value at the appropriate index
for i in range(len(pointsX)):
	pointsX[i][1] = pointsX[i][1] + 1
	
print pointsX


# Double lists
# It is often useful to be able to generate a grid of points in which case we need to
# have a loop within a loop.  Let's generate a grid on a canvas dimensioned 40(h) x 60(w)
# which has N points equally spaced horizontally and M points equally spaced vertically.

#N = 17
M = 7

# to store all of these points, we need to employ a double list
pointsXY = []
for i in range(N):
	pointsXY.append([])
	for j in range(M):
		curPoint = [i*60/float(N), j*40/float(M), 0]
		pointsXY[i].append(curPoint)

# Now you have a double list where you can access pointsXY[i][j] as an individual point
print pointsXY[1][3]
# Notice what applying len() to a double list does
print len(pointsXY)
print len(pointsXY[3])

# Since the first index references columns, we can easily draw out a list of points at column i
rs.AddPoints(pointsXY[3])



# Lists and Functions
# Lists can be an input as well as an output of a function

# This function gets equally spaced points along an ellipse drawn in the plane,
# centered at the orign where a and b are the semimajor and semiminor axes, resp.
# Remember: this ellipse can be parametrized as r(t) = (acos(t), bsin(t)), t in [0, 2pi]
def getPointsEllipse(a, b, numPoints):
	pOut = []
	for i in range(numPoints):
		t = i*2*math.pi/numPoints
		x = a*math.cos(t)
		y = b*math.sin(t)
		pOut.append([x,y,0])
	return pOut

rs.AddPoints(getPointsEllipse(10, 20, 30))

# Now if we wanted to draw these points at different heights, we can use two lists--
# one representing points along any curve drawn in plane and the other holding the
# list of heights -- as an input
def drawPointsAtHeights(listPointsCurve, listHeights):
	for height in listHeights:
		for curPoint in listPointsCurve:
			x = curPoint[0]
			y = curPoint[1]
			rs.AddPoint([x, y, height])
		

ellipse0 = getPointsEllipse(10, 20, 30)
floors = range(0, 200, 8)

drawPointsAtHeights(ellipse0, floors)


# Inputting a double list is also often done.  Here we have a function that takes as
# input a grid of points lying in plane and a light source position, and draws vertical
# lines along the grid with heights varying by its position.  In this case, heights
# are proportional to cos(theta) where theta is the angle of incidence
def drawHeightsGrid(pSource, gridPoints):
	for i in range(len(gridPoints)):
		for j in range(len(gridPoints[i])):
			start = gridPoints[i][j]
			v1 = rs.VectorUnitize(rs.VectorCreate(start, pSource))
			theta = rs.VectorDotProduct(v1, [0, 0, 1])
			end = [start[0],start[1], 20*abs(theta)]
			rs.AddLine(start, end)
		
drawHeightsGrid([0, 0, 10], pointsXY)


#print rs.Distance(v1,v2)
#print rs.VectorAdd(v1,v2)
#print rs.VectorScale(v1, 5)
#print rs.VectorSubtract(v1,v2)



#AddVector(v1, origin)
#AddVector(v2, origin)
#AddVector(rs.VectorSubtract(v1,v2), v2)
