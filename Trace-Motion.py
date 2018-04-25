import sys
import numpy as np
import csv
import itertools
import pigpio
from time import sleep

#### This file must be run with a data file 
#### e.g. >> python FiletypeInputTest.py example.txt

# Start pigpio daemon
import subprocess
subprocess.Popen("sudo pigpiod")

################################################################################
# Read in data file, ensures it is a 2 column csv or txt file with equal lengths
# Import the data if it matches the criteria, raise an error otherwise

# First, read in data file entered during function call
f = open(sys.argv[1],'r')


# Check file extension in a case-insensitive manner
if sys.argv[1].lower().endswith('.csv'):
        
    # If .csv, use commas to split values and lines
    d = ','


elif sys.argv[1].lower().endswith('txt'):

    # If .txt, use tabs to split values and lines
    d = '\t'

    # Remove blank lines
    lines = f.readlines()

    with open(sys.argv[1],'w') as f:
        lines = filter(str.strip, lines)
        f.writelines(lines)


else: 
    raise ValueError("This is not a .csv or .txt file")

with open(sys.argv[1],'r') as f:

    # Use csv reader tool to make sure the number of columns is 2
    # Itertools.tee splits the single iterable output by csv reader into
    # multiple iterables
    rows, columns = itertools.tee(csv.reader(f, delimiter=d,
        skipinitialspace=True))


    # Read first line and count columns 
    if len(next(rows)) == 2:

        # Make sure the columns are the same length
        if len(next(columns)) == len(next(columns)):
                
            # Go back to beginning of file
            f.seek(0)

            # The file gives a list of values like ['t1,z1\n','t2,z2\n',etc.]
            # Where t = time (s), z = cranial-caudal displacement (cm)
            # Create new list of (t1,z1),(t2,z2), etc. tuples
            tz = []
            for line in f:
                thistz = line.split(d)
                tz.append(thistz)


        else:
            raise ValueError("Please ensure the columns are the same length")

        # Make sure that itertools does not hold rows in memory
        del rows


    else:
        raise ValueError("This file is not 2 columns")


# Separate list of tuples into lists of just t, z
t, z = zip(*tz)

# Convert t, z into lists of numbers
t = list(map(lambda i: float(i.replace(',', '.')), t))
z = list(map(lambda i: float(i.replace(',', '.')), z))

################################################################################
### Calculate velocities from trace position data


# Define step size for finite differences
h = (t[-1] - t[0])/len(t)

# Create list of velocities (simplest method)
velocities = []

for i, val in enumerate(z):

    if i == 0:
        vel = (z[i+1] - z[i])/h
        velocities.append(vel)

    elif i == len(z)-1:
        vel = (z[i] - z[i-1])/h
        velocities.append(vel)

    else:
        vel = (z[i+1] - z[i-1])/(2*h)
        velocities.append(vel)

# angular freq (steps/s) = 200 (steps/rev) * linear velocity (cm/s) / (0.8 cm/rev)
omega = list(map(lambda i: 200*i/0.8, velocities))

# Can only input positive frequencies, so take absolute value of every omega
magomega = list(map(abs,omega))

# Also need the directions: clockwise (1) if positive, counterclockwise (0) if negative
directions = list(map(lambda i: 1 if i>0 else 0, omega))

# Connect to pigpio daemon
pi = pigpio.pi()

DIR = 20     # Direction GPIO Pin
STEP = 18    # Step GPIO Pin

dutycycle = 500000 # 50% dutycycle (bipolar motor)

try:
    i = 0

    while (i<len(velocities)):

        # Set rotational direction to match instantaneous angular frequency
        pi.write(DIR,directions[i])

        # Set frequency to the instantaneous angular frequency
        pi.hardware_PWM(18, magomega[i], dutycycle)

        # Wait for current movement to finish before continuing
        sleep(2*h)

        i += 1

# In case something goes wrong..
except KeyboardInterrupt:
    print("Stopping PIGPIO and exiting...")

# When the trace has finished, shut down the motor
finally:
    pi.hardware_PWM(STEP,0,0) # PWM Off
    pi.stop()
