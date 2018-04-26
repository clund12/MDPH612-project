import numpy as np
import csv
from scipy import signal

x = np.linspace(0,10,100)
xy = list(map(lambda i: [i, signal.square(2*i/(2*np.pi))], x))

with open('squaretrace.csv','w') as output:
    writer = csv.writer(output)
    writer.writerows(xy)


