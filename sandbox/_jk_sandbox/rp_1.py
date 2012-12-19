#Points in 2D

#Importing the rhinoscript package will give you access to a large number
#of objects and functions in Rhino
import rhinoscriptsyntax as rs

#Let's work in 2D first (in Rhino, only look at Top window).

#Points in 2D can be represented by a list of numbers [x, y, 0]
p1 = [1,12,0]
p2 = [-2,2,0]

#and drawn to the canvas by using a built-in function
rs.AddPoint(p1)
rs.AddPoint(p2)

#we can draw a collection of points, such as this zig-zag,
#based on user-inputted data
count = rs.GetInteger("Number of points")
height = rs.GetInteger("Height of zig-zag")

if count:
    for i in range(count):
    	x = i
    	if (i%(2*height) < height):
    		y = i%height
    	else:
    		y =height-(i%height)
    	rs.AddPoint([x,y,0])

#this is a collecton of points along a 'curve' defined by a
#mathematical function, y = |x|sin(5x),  for a specified range
#and a fixed stepsize in x (representing angle in degrees).
#For fixed intervals, the built-in function frange is very useful
import math

lower = -30
upper = 60
step = 1
#print rs.frange(lower, upper, step)

#remember this handy little function?  
def sinDegrees(angleIn):
	angleRad = angleIn*2*math.pi/360
	return math.sin(angleRad)

for x in rs.frange(lower, upper, step):
	y = math.fabs(x)*sinDegrees(10*x)
	rs.AddPoint([x,y,0])

#up to this point, every point in the collection is printed out one at a time.
#But suppose we wanted to save this collection of points so that this can be
#used later.  This can be done using a list of points, using the same operations
#on lists that we used when we were working with lists of numbers.
#(of course this is a list of points so initializing these is different,
#but less confusing to focus on the similarities at this stage)

listPoints = []
for x in rs.frange(lower, upper, step):
	y = math.fabs(x)*sinDegrees(10*x)
	listPoints.append([x,y,0])

#this collection can now be used as input for built-in functions
#such as AddInterpCurve which draws an interpolated curve based
#on input of a list of points
rs.AddInterpCurve(listPoints)
