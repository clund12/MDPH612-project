import numpy as np
import csv

x = np.linspace(0,2,100)
xy = list(map(lambda i: [5*i, i**2], x)) 

with open('spintrace.csv','w') as output:
    writer = csv.writer(output)
    writer.writerows(xy)
