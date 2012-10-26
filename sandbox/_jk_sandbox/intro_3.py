# Functions

#an example you've seen before - type
print type("17")

#1. Basic math functions
#Python has a math module that provides most of the familiar mathematical functions. 
#A module is a file that contains a collection of related functions grouped together.  
#You need to import a module before you can use it
import math
print math.pi
print math.sqrt(2)
print math.sin(math.pi/2)
pi = math.pi
angleDegrees = 17
angleRadians = angleDegrees*2*pi/360
print math.sin(angleRadians)

#2. Function construction
#def NAME (LIST OF PARAMETERS):
#	STATEMENTS

def sinDegrees(angleIn):
    angleRad = angleIn*2*pi/360
    return math.sin(angleRad)

#statements inside the function are not executed until the function is called
print sinDegrees(10)

#notice all variables assigned within the body of the function are not 'seen' outside;  
#they are local
#print angleRad

#another function that prints anything that is input twice.  This can take any type
def printTwice(whateverIn):
	print whateverIn, whateverIn

printTwice(7)
printTwice('Hi Joy')

#3.  Encapsulation and Generalization
# Encapsulation is the process of wrapping a piece of code in a function, allowing you to
# take advantage of all the things functions are good for.  Generalization means taking 
# something specific, such as printing the multiples of 2, and making it more general, 
#such as printing the multiples of any integer.

# Let's revisit some of the examples that we did in Intro_2 and wrap these into functions.  As good coding practice, remember that variables within the body of a function are local so let's just use different names to highlight that and (hopefully) lessen any confusion
 
def printEvenOdd(numberIn):
	if numberIn%2 == 0:
		print numberIn, "is even"
	else:
		print numberIn, "is odd"
	
printEvenOdd(8)
printEvenOdd(29)

#if-elif-else
def compare(xIn, yIn):
	if (xIn < yIn):
		print xIn, "is smaller than", yIn
	elif (xIn > yIn):
		print xIn, "is larger than", yIn
	else:
		print xIn, "is equal to", yIn
		
compare(20, 15)
compare(15, 20)


#4.  Composition
# This is the very useful ability to call on another function from within a function

#ex
printTwice(sinDegrees(17))

# ex. let's take two points in 2D given by (xC, yC) and (xP, yP) which
# represents the center of a circle and a point on the perimeter of the circle and
# write a function that returns the area of this circle.
xC = 0
yC = 0
xP = 2
yP = 5

#Let's do this one step at a time for these specific points and then organize the resulting
#statements into functions.  
# Step 1:  calculate the distance bween (xC,yC) and (xP, yP) to get the radius of the circle

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

#5.  Recursion
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



