import numpy as np
import sys
import matplotlib.pyplot as plt
import csv

#### Call this file via the command line, passing the desired csv file as an argument: >> python TracetoVelocities.py sometrace.csv

# Read in the file -> gives a list of values like ['x1,y1\n','x2,y2\n',etc.]
data = open(sys.argv[1],'r')
data = data.readlines()

# Create new list of (x1,y1),(x2,y2), etc. tuples
xy = []
for line in data:
    line = line.strip('\n')
    thisxy = line.split(',')
    xy.append(thisxy)

# Separate list of tuples into lists of just x, y
x, y = zip(*xy)

# Convert x, y into lists of numbers
x = list(map(float,x))
y = list(map(float,y))

# Double check that the data has been transferred correctly. Uncomment when you're sure.
#plt.plot(x,y)
#plt.show()

# Only need to work with the y data, as the x data will keep the correct indexing and doesn't need to be altered

# Define step size for finite differences
h = (x[-1] - x[0])/len(x)

# Create list of velocities (simplest method)
velocities = []
for i, val in enumerate(y):
    if i == 0:
        vel = (y[i+1] - y[i])/h
        velocities.append(vel)
    elif i == len(y)-1:
        vel = (y[i] - y[i-1])/h
        velocities.append(vel)
    else:
        vel = (y[i+1] - y[i-1])/(2*h)
        velocities.append(vel)

# Check that the output is correct. Comment out afterwards and then uncomment the write to file underneath.
plt.plot(x,velocities)
plt.show()

# Write to new csv file
#xvel = zip(x,velocities)
#with open('tracevelocities.csv','w') as output:
#    writer = csv.writer(output)
#    writer.writerows(xvel)


