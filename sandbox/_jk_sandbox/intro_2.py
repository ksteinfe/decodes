#Conditional statements

#1.  More operators and expressions

#The modulus.  x%y gives the remainder after x divides y
#checks to see whether something is odd(1) or even(0)
print 5%2
print 14%2
#checks to see whether something is a multiple of another;  if it is, returns 0
print 14%6
print 48%6
#extracts the rightmost digit of a number
print 531%10
#or the rightmost 2 digits
print 531%100

#Boolean expressions - an expression that is either true or false
x =5
y = 6
print x==y  	#True if x equals y.  False otherwise
print x!=y	#True if x is not equal to y.  False otherwise
print x < y	#True if x is less than y.  False otherwise
print x > y	#True if x is greater than y.  False otherwise
print x<=y	#True if x is less than or equal to y.  False otherwise
print x >=y	#True if x is greater than or equal to y.  False otherwise

#Logical operators - and, or, not
n = 7
print n%2 or n%3  	#True if either statement is true
print n%2 and n>5 	#True if both statements are true
print not(n>5)		#Opposite of the expression.  Since n>5 is True, then not(n>5) is False

#2.  Conditional statements
# if CONDITION(S):
#		FIRST STATEMENT
#		...
#		LAST STATEMENT
x = 8
if x%2 == 0:
	print x, "is even"

#if-else construction	
if x%2 == 0:
	print x, "is even"
else:
	print x, "is odd"

#if-elif-else
x = 240
y = 120
if (x < y):
	print x, "is smaller than", y
elif (x > y):
	print x, "is larger than", y
else:
	print x, "is equal to", y
	

