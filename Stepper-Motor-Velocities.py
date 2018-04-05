import sys
import numpy as np
from time import sleep
#import RPi.GPIO as GPIO # Can ONLY be run on a RPi!

DIR = 20     # Direction GPIO Pin
STEP = 21    # Step GPIO Pin
CW = 1       # Clockwise Rotation
CCW = 0      # Counterclockwise Rotation
SPR = 200     # Steps per Revolution (Checked according to NEMA 17 spec sheet)

#GPIO.setmode(GPIO.BCM)      # Broadcom memory
#GPIO.setup(DIR, GPIO.OUT)   # Sets direction pin to an output
#GPIO.setup(STEP, GPIO.OUT)  # Sets step pin to an output
#GPIO.output(DIR, CW)        # Sets initial direction to clockwise

step_count = SPR    # Set initial test to a single rotation
delay = 0.005      # (1s / 200) - rotation will take 1 second if no delay

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
velocities = list(map(float,y))

# Convert velocities into rotational velocities (rpm)
velrot = velocities # We can get to this later
nmicro = 1 # Number of microsteps per step

fstep = velrot*SPR*nmicro/60 # microsteps per second

