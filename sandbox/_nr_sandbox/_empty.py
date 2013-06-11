import decodes as dc
from decodes.core import *
from decodes.extensions.cellular_automata import CA
import random

import os
path = os.path.expanduser("~") + os.sep + "_decodes_export"
f_prefix = "maze_"
random.seed(0.2)


# Function to be used to initialize a random boolean field
def random_values():
    return (random.choice([0,1]) == 0)

# Function to create a maze out of an random boolean field
# based on algorithm published by Kostas Terzidis,"Algorithms for Visual Design", pp. 168-171
def maze(home,neighbors):
    count = 0
    for i in neighbors:
        if i : count += 1
    if count == 3 : return True
    if count > 4: return False
    return home

# Function to perform Conway's Game of Life
def life(home,neighbors):
    count = 0
    for i in neighbors:
        if i : count += 1
    if home:
        if (count < 2) or (count >3) :
            return False
        else:
            return True
    else:
        if (count == 3):
            return True
        else:
            return False

# Initialize CA model

width = 200
height = 200
my_CA = CA(Interval(width,height),True,False)
my_CA.set_rule(maze)

# Create a starting position
init = []
for i in range(width*height):
    init.append(random_values())
my_CA.start(init)

# Run the CA
gen = 40
stepsize = 1

for n in range(gen):
    print "step",n
    for m in range(stepsize): my_CA.step()
    my_CA.record()

# create output
for n in range(len(my_CA.hist_u)):
    img = my_CA.hist_u[n].to_image()
    img.save(f_prefix+str(n), path, True)


raw_input("press enter...")