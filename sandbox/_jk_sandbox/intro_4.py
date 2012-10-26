#Iterative Programs

#1.  Template for Iterative Programs:
#STEP 1  Choose a variable that "counts" (could be counting through integers, or a 
#				collection of data)
#STEP 2  Initialize outside the loop - where do I start?
#STEP 3  Set up end test - how do I know when loop is done?
#STEP 4  Construct block of code - set of instructions that will be followed each time 
#		       in the loop;  all that changes is the value of the variable
#STEP 5  Decide what to do when done

#2.  The while statement
#while CONDITION(S) (with an outcome of 0 or 1):
#STATEMENTS

#ex. Find the square root of a perfect square - without using math library!
x = 16
ans = 0
while ans*ans < x:
	ans = ans + 1
print ans
	
#The answer is right, so long as you give a perfect square that is positive.  Let's make 
#this a bit more general to accept any integer.  A good lesson in debugging is to 
#simulate the code using reasonable values (putting yourself in other people's shoes).
#Try this for x = 26.  What happens?  What happens with negative numbers?  
#Another good tactic to debug is to print out intermediate data that can tell you if 
#it matches your own simulation.

x = 189
ans = 0
if x >= 0:
	while ans*ans < x:
		ans = ans + 1
		print "ans = ", ans
	if ans*ans != x:
		print x, " is not a perfect square"
	else:
		print ans
else:
	print x, " is negative.  Please try a positive integer"


#3.  The for loop
# for VARIABLE in SOME COLLECTION:
#		STATEMENTS
#
#	One advantage of this over the while statment is that you do not need to explicity 
#update any variable which means that the loop will terminate so long as the collection 
#is finite
# A useful built-in Python function here is the function range()

#ex print out all divisors of a positive integer x.  
n = 270
for i in range (1, n):
	if n%i == 0:
		print i
#you could've also done this using a while loop (try it!) but you will have to explicity 
#initiialize or increment the variable i;  incrementing is automatic using a for loop

#as before, you can add in the condition that checks to see that n is positive when you've 
#checked that the code is behaving as you would expect for positive input
if n > 0:
	for i in range (1, n):
		if n%i == 0:
			print i
else:
		print x, " is negative.  Please try a positive integer"

#rewrite the square root example using a for loop


#Once you're sure that your program is working, it makes sense to take out the 
#debugging statements and wrap these into functions.  

def mySquareRoot(xIn):
	ansOut = 0;
	if xIn >= 0:
		while ansOut*ansOut < xIn:
			ansOut = ansOut + 1
		if ansOut*ansOut != xIn:
			print xIn, " is not a perfect square"
		else:
			return ansOut			
	else:
		print x, " is negative"
		
		
print mySquareRoot(211)
print mySquareRoot(121)


def myDivisors(xIn):
	if xIn > 0:
		for candidate in range(1, xIn):
			if xIn%candidate ==0:
				print candidate
	else:
		print xIn, " is negative.  Please try a positive integer"
		
myDivisors(270)
myDivisors(-5)

#Now suppose in this last example, that I didn't want to print out all of the divisors as
# soon as I called the function but that I just wanted to store them as an output (and possibly use all the elements or some of the elements later for another purpose)  The problem is that the output here isn't a single number but a collection of numbers.  

#4.  Introducing sequences
#A more detailed treatment of the properties and the manipulation of sequences will be given later, but here's a taste of why one might need a data type that holds more than one element in it

#A sequence is an ordered set of elements.  We've already seen one kind of sequence, the string, which is an ordered set of characters.  Here, we will be looking at ordered sets of numbers

#The basic representation of a sequence of numbers is
seq = [5, 3, 2, 1, 7, 20, -10]
print seq

#to get a handle on elements in this sequence, use the construction seq[i], 
#remembering that the index starts at 0. 
print seq[0]  #first element in sequence
print seq[2]  #third element in the sequence

#you can also find out how many elements are in a sequence using the 
#function len()
print len(seq)

#this way you can print out the last element of the sequence 
#(always remembering that the index starts at 0)
print seq[len(seq)-1]

#to get a partial list of elements in the sequence, use the construction 
#seq[i, k] which will extract the elements between the ith and kth index
# not including the element at the kth index -- this is called slicing
print seq[2:5]

#if no first index is supplied, this will give all elements up to but not 
#including the second index
print seq[:4]

#if no second index is supplied, this will give all elements after and 
#including the first index
print seq[4:] 

#you've also already seen a function that returns a sequence
print range(1, 7)

#you can also concatenate sequences together using +
seq1 = [1.1, 3, 7,1]
seq2 = [2,3.5]
print seq1+seq2

#or, if you start off with an empty list, you can add one one element at a time
seqList = []
seqList.append(4)
print seqList
seqList.append(101)
print seqList

#now revisit the divisors example so that instead of printing out all 
#the divisors, instead store all divisors as a sequence
xIn = 270

def myDivisorsStored(xIn):
	if xIn > 0:
		seqOut = []  #this initializes the sequence variable 
		for candidate in range(1, xIn):
			if xIn%candidate ==0:
				seqOut.append(candidate)
		return seqOut
	else:
		print xIn, " is negative.  Please try a positive integer"
	

print myDivisorsStored(270)
print myDivisorsStored(2711)
