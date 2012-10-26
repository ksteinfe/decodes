#Function Composition and Recursion

#1.  Composition
# This is the very useful ability to call on another function from within a function
# As a first example, let's take two points in 2D given by (xC, yC) and (xP, yP) which
# represents the center of a circle and a point on the perimeter of the circle and
# write a function that returns the area of this circle.
xC = 0
yC = 0
xP = 2
yP = 5

#Let's do this one step at a time for these specific points and then organize the resulting
#statements into functions.  
# Step 1:  calculate the distance bween (xC,yC) and (xP, yP) to get the radius of the circle
import math
r = math.sqrt((xC-xP)**2 + (yC-yP)**2)
print r
# Step 2:  calculate the area of the circle
areaCircle = math.pi*r**2
print areaCircle

#it makes sense to write one function that calculates the distance betwen two points 
#given in 2D
def distance2D(x1, y1, x2, y2):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

#which is called within another function that calculates the area of a circle based on 
#two points given in 2D
def areaCircleTwoPoints2D(x1, y1, x2, y2):
	radius = distance2D(x1, y1, x2, y2)
	return math.pi*radius**2
	
#check that this gives the same answer as before	
print areaCircleTwoPoints2D(xC, yC, xP, yP)
#it is now just a 1-liner to to calculate this for any other pair of points
print areaCircleTwoPoints2D(5, 3, 2, 1)

#2  Recursion
# We've seen that a function can call another function.  It turns out that it can call on itself as well.
 
# A function that takes an integer and counts down to 0
def countdown(n):
	if n <= 0:
		print 'Happy New Year!'
	else:
		print n
		countdown(n-1)

countdown(4)

#A classic example of a recursion.  The FIbonacci sequence starts with 0, 1 and each subsequent 
# number in the sequence is defined by being the sum of the previous two

def fibonacci(n):
	if n == 0 or n == 1:
		return 1 
	else:
		return fibonacci(n-1) + fibonacci(n-2)
	
print fibonacci(30)

