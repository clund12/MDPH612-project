import sys
import numpy as np
import csv
import itertools
import RPi.GPIO as GPIO
from time import time,sleep
import matplotlib.pyplot as plt

#### This file must be run with a data file 
#### e.g. >> python FiletypeInputTest.py example.txt

##############################################################################
#### Set up GPIO pins and microstep resolution

# Convert direction from +/- to 1/0 for clockwise/counter-clockwise
def rot_direct(x):

    if np.sign(x) == 1:
        return 1
    else:
        return 0


DIR = 20          # Direction GPIO Pin
STEP = 21         # Step GPIO Pin
MODE = (14,15,18) # Microstep Resolution GPIO pins

GPIO.setmode(GPIO.BCM)      # Broadcom memory
GPIO.setup(DIR, GPIO.OUT)   # Sets direction pin to an output
GPIO.setup(STEP, GPIO.OUT)  # Sets step pin to an output
GPIO.setup(MODE, GPIO.OUT)


RESOLUTION = {'1': (0,0,0),
        '0.5': (1,0,0),
        '0.25': (0,1,0),
        '0.125': (1,1,0),
        '0.0625': (0,0,1),
        '0.03125': (1,0,1)}
RES = '0.25'

GPIO.output(MODE,RESOLUTION[RES])

################################################################################
# Read in data file, ensures it is a 2 column csv or txt file with equal lengths
# Import the data if it matches the criteria, raise an error otherwise
# PLEASE DELETE ANY AND ALL HEADERS

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
        # Go back to beginning of file
        f.seek(0)

        # The file gives a list of values like ['t1,z1\n','t2,z2\n',etc.]
        # Where t = time (s), z = cranial-caudal displacement (cm)
        # Create new list of (t1,z1),(t2,z2), etc. tuples
        tz = []
        for line in f:
            thistz = line.split(d)
            tz.append(thistz)


        # Make sure that itertools does not hold rows in memory
        del rows


    else:
        raise ValueError("This file is not 2 columns")


# Try to convert t, z into lists of numbers and replace commas with periods
# Otherwise, raise an error
try:
    # First, separate list of tuples into lists of just t, z
    t, z = zip(*tz)
    
    # Now replace ',' with '.' and convert to float
    t = list(map(lambda i: float(i.replace(',', '.')), t))
    z = list(map(lambda i: float(i.replace(',', '.')), z))

except:
    raise ValueError("This file contains non-numerical data and/or blank spaces")


################################################################################
### Calculate displacements from trace position data

# Create list of displacements and time intervals (simplest method)
displacements = []
delta_t = []

for i, val in enumerate(z[0:-1]):

    dis = z[i+1] - z[i]
    del_t = t[i+1] - t[i]
    displacements.append(dis)
    delta_t.append(del_t)

spr = 200                 # steps per revolution = 200 - from NEMA 17 spec sheet
micro = 1/float(RES)      # Number of microsteps per full step
step_count = micro*spr    # Total number of microstep per revolutions


# Rotation angle (microsteps) = step count (microsteps/rev) * linear displ. (cm) / (0.8 cm/rev)
theta = list(map(lambda i: step_count*i/0.8, displacements))

# Also need the directions: clockwise (1) if positive, counterclockwise (0) if negative
directions = list(map(rot_direct, theta))

# Can only input positive frequencies, so take absolute value of every omega
mag_theta = list(map(lambda i: abs(int(round(i))),theta))

# Define max position to be 8 cm in either direction, so platform isn't overextended
max_pos = step_count*8/0.8

# Finally, need positive or negative direction info to keep track of position
sign = list(map(np.sign, theta))

# Define delay to be (half, see below) the time taken to rotate a microstep
delay = []

# If next time interval requires 0 step, delay is simply set to be equal to the
# full time interval  
for i, val in enumerate(mag_theta):
    if val == 0:
        delay.append(delta_t[i])
    else:
        delay.append(delta_t[i]/val)


# Divide delay by 2 because delays are set twice per step
delay = np.divide(delay,2)

################################################################################
#### For plotting

# Keep track of programmed position
step_position = list(sum(theta[0:x+1]) for x in range(len(theta)))

timesincestart=[]
current_position=[]


try:
    # Temporal accuracy is imperfect, track it with timelost variable 
    timestart = time()

    # Keep track of total time elapsed
    t_cum_list = []

    i = 0

    # pos is the current position of the nut with respect to the center in
    # number of microsteps
    pos = 0
    
    # t_cum is the cumulative delay
    t_cum = 0

    # Loop through the trace and ensure total displacement from the center is 
    # smaller than max_pos 
    while (i<len(displacements) and abs(pos)<max_pos):

        # Set rotational direction to match step direction
        GPIO.output(DIR,directions[i])

        # Step through the calculated rotation angle
        # Motor rotates by 1 microstep per iteration of the 'for' loop
        # sleep() between GPIO.HIGH and GPIO.LOW sets the time taken by the 
        # motor to rotate by 1 microstep. sleep() after GPIO.low sets the delay
        # between each microstep
        if mag_theta[i] == 0:
            sleep(2*delay[i])

        else:
            for s in range(mag_theta[i]):
                GPIO.output(STEP, GPIO.HIGH)
                sleep(delay[i])
                GPIO.output(STEP, GPIO.LOW)
                sleep(delay[i])
                
                # Update position of platform
                pos += sign[i]
    

        # Update cumulative time
        t_cum += delta_t[i]
        t_cum_list.append(t_cum)

        timelost = time() - timestart - t_cum
        timesincestart.append(timelost + t_cum)
        current_position.append(pos)

        i += 1

# In case something goes wrong..
except KeyboardInterrupt:
    print("Stopping GPIO and exiting...")

# When the trace has finished, shut down the motor
finally:
    sleep(3)

    print "percent error in time =",100*timelost/t_cum,"%"

    # Make sure pin is set to low first
    GPIO.output(STEP, GPIO.LOW)

    # Set direction to account for current position
    GPIO.output(DIR, rot_direct(-pos))

    # Return platform to centre
    for x in range(int(abs(pos))):

        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.00125)
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.00125)
    
    # Shut down GPIO module
    GPIO.cleanup()

    step_position = list(map(lambda i: i*float(RES)*0.8/200, step_position))
    current_position = list(map(lambda i: i*float(RES)*0.8/200, current_position))

    plt.plot(t_cum_list,step_position,'b',label='programmed position vs. programmed time')
    plt.plot(timesincestart,current_position,'k',label='actual position vs. actual time')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (cm)')
    plt.legend(loc='upper right')
    plt.show()
