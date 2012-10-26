# Variables, Expressions, Statements

# 1. Values and types

# <- any line that begins with the pound symbol is a comment
#int
print 17
print type(17)

#string - double or single quotation is fine, so long as they match
print "Hi Joy"
print 'Hi Joy'
print type("Hi Joy")

#float
print 3.14159
print type(3.14159)

# !- this may look like an int but is a string
print type('17')

# !- this is not a legal integer.  This is interpreted as a comma-separated list of 3 integers
print 1,000,000


# 2. Variables

n = 17

# print out the value of the variable
print n

# variables can be assigned another value and type
n = "Hi Joy"
# variables will always inherit the last value and type it was assigned
print n

#make sure to keep track (and differentiate) your variable names
x = 17
pi = 3.14159
greeting = "Hi Joy"

print type(x)
print type(pi)
print type(greeting)

# A variable name contains letters and numbers and must begin with a letter.  
# By convention, a variable does not start with a capital letters.  
# Also, must avoid the default keywords that are already 'taken'
#Illegal variable names
#7x = 7*x
#print 7x
#pi~ = 3.14159
#print pi~
#def = "Hi Joy"
#print def

# A statement is an instruction that can be executed.  
# So far we've seen two kinds: print and assignment
# A script is just a sequence of statements

# statements can be combined with commas to print a single line
print "x is a", type(x), " and has a value of", x

#3.  Expressions - a combination of values, variables and operators
print 2+8
print 2-8
print 2*8
print 8/2
print 2**8
#be careful with division.  Sometimes to be safe, do 2.0/8.0
print 2/8
#or you can do type conversion; 
#if either top or bottom is a float then automatically the result is a float
top = 2
bot = 8
print float(top)/float(bot)
#usual rules of precedence:  parantheses, exponent, mult and divide, add and substact
print (5-2)**3*2-5

#expressions involving strings
print greeting + " Ko"
print greeting*3