import numpy as np
import sys
import matplotlib.pyplot as plt

#### Call this file via the command line, passing the desired csv file as an argument: >> python TracetoVelocities.py sometrace.csv

# Read in the file -> gives a list of values like [x1,y1\n,x2,y2\n,etc.]
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

# Double check that the data has been transferred correctly. Uncomment when you're sure.
plt.plot(x,y)
plt.show()

# Only need to work with the y data, as the x data will keep the correct indexing and doesn't need to be altered
