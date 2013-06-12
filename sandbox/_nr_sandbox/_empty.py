import decodes as dc
from decodes.core import *
from decodes.extensions.cellular_automata import CA
import random

import os
path = os.path.expanduser("~") + os.sep + "_decodes_export"
f_prefix = "maze_"
random.seed(0.1)


# Function to be used to initialize a random boolean field
def random_values():
    return (random.choice([0,1]) == 0)

# Function to create a maze out of an random boolean field
# based on algorithm published by Kostas Terzidis,"Algorithms for Visual Design", pp. 168-171
def maze_rules(cur_val,nei_vals):
    nxt_val = cur_val
    count = 0
    for i in nei_vals:
        if i : count += 1
    if count == 3 : nxt_val = True
    if count > 4: nxt_val = False
    return nxt_val

# Function to perform Conway's Game of Life
def life_rules(home,neighbors):
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

width = 100
height = 100
my_CA = CA(Interval(width,height),True,False)
my_CA.set_rule(maze_rules)

# Create a starting position
init = []
for i in range(width*height):
    init.append(random_values())
my_CA.set_cells(init)
my_CA.record()


#img = my_CA.cells.to_image()
#img.save("test", path, True)



# Run the CA
gen = 25
stepsize = 1

for n in range(gen):
    print "step",n
    for m in range(stepsize): my_CA.step()
    my_CA.record()

# create output
for n in range(len(my_CA.hist)):
    img = my_CA.hist[n].to_image()
    img.save(f_prefix+str(n), path, True)


raw_input("press enter...")