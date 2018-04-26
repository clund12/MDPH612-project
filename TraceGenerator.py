import numpy as np
import scipy.constants as sc
import matplotlib.pyplot as plt
import csv

# Define a sine wave
x = np.linspace(0, 4*sc.pi, 100)
xy = list(map(lambda i: [10*i/(2*sc.pi), 3*np.sin(i)], x))

##### Place any other function you want to test here:


# Plot whatever trace you want to verify it's of the right form, is sufficiently smooth, etc.

#plt.plot(*zip(*xy))
#plt.show()

# If it's good, comment out the plot and uncomment the lines below to write it to a csv file

with open('trace.csv','w') as output:
    writer = csv.writer(output)
    writer.writerows(xy)
