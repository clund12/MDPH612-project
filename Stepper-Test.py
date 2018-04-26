import sys
import numpy as np
import csv
import itertools
import RPi.GPIO as GPIO
from time import sleep

#### This file must be run with a data file 
#### e.g. >> python FiletypeInputTest.py example.txt

##############################################################################
#### Set up GPIO pins and microstep resolution

# Directions need to be converted from +/- to 1/0 for clockwise/counter-clockwise
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

# Create list of velocities (simplest method)
displacements = []
delta_t = []

for i, val in enumerate(z[0:-1]):

    dis = z[i+1] - z[i]
    del_t = t[i+1] - t[i]
    displacements.append(dis)
    delta_t.append(del_t)

spr = 200              # steps per revolution = 200 - from NEMA 17 spec sheet
micro = 1/float(RES)     # Number of microsteps per full step
step_count = micro*spr # Total number of microstep per revolutions


# Rotation angle (steps) = step count (microsteps/rev) * linear displ. (cm) / (0.8 cm/rev)
theta = list(map(lambda i: float(step_count*i/0.8), displacements))

# Can only input positive frequencies, so take absolute value of every omega
mag_theta = list(map(lambda i: abs(int(round(i))),theta))

# Also need the directions: clockwise (1) if positive, counterclockwise (0) if negative
directions = list(map(rot_direct, theta))

# Finally, need positive or negative direction info to keep track of position
sign = list(map(np.sign, theta))

# Define maximum position to be 8 cm in either direction, so platform is not overextended
max_pos = step_count*8/0.8

# Define delay between pulses so that movement can finish
delay = np.divide(delta_t,mag_theta)

# Divide delay by 2 because delays are set twice per step
delay = np.divide(delay,2)


try:
    i = 0
    pos = 0

    while (i<len(displacements) and abs(pos)<max_pos):

        # Set rotational direction to match step direction
        GPIO.output(DIR,directions[i])

        # Step through the calculated rotation angle
        for s in range(mag_theta[i]):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay[i])
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay[i])

            # Update position of platform
            pos += sign[i]

        i += 1
    print pos
# In case something goes wrong..
except KeyboardInterrupt:
    print("Stopping PIGPIO and exiting...")

# When the trace has finished, shut down the motor
finally:
    sleep(5)

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
