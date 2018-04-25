import sys
import numpy as np
from time import sleep
import pigpio
# Make sure to run "sudo pigpiod" in the command line

# Read in the file -> gives a list of values like ['t1,z1\n','t2,z2\n',etc.]
# Where t = time (s), z = cranial-caudal displacement (cm)
data = open(sys.argv[1],'r')
data = data.readlines()

# Create new list of (t1,z1),(t2,z2), etc. tuples
tz = []
for line in data:
    line = line.strip('\n')
    thistz = line.split(',')
    tz.append(thistz)

# Separate list of tuples into lists of just t, z
t, z = zip(*tz)

# Convert x, y into lists of numbers
t = list(map(float,t))
z = list(map(float,z))

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
