import sys
from time import sleep
import numpy
import RPi.GPIO as GPIO # Can ONLY be run on a RPi!
import pigpio

## START THE PIGPIO DEAMON! - sudo pigpiod
# Default sampling rate (defines allowable frequencies) is 5. This can be
# changed using the -s tag when calling pigpiod

DIR = 20     # Direction GPIO Pin
STEP = 21    # Step GPIO Pin
#SWITCH = 16  # GPIO Pin of Switch [Not Needed: we won't use a switch]
CW = 1
CCW = 0
# Connect to pigpio daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)

# Set up input switch
#pi.set_mode(SWITCH, pigpio.INPUT)
#pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)

# Note: current is 71% of maximum in full step mode, but this is not the case
# for microstepping! If the current has been increased past the maximum when
# we're working with full step, then we need to decrease it.
MODE = (14,15,18) # Microstep Resolution GPIO pins
#GPIO.setup(MODE, GPIO.OUT)

RESOLUTION = {'1': (0,0,0),
        '1/2': (1,0,0),
        '1/4': (0,1,0),
        '1/8': (1,1,0),
        '1/16': (0,0,1),
        '1/32': (1,0,1)}
RES = '1'
for i in range(3):
    pi.write(MODE[i],RESOLUTION[RES][i])

#### Call this file via the command line, passing the desired csv file as an 
#### argument: >> python TracetoVelocities.py sometrace.csv

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
time, height = zip(*xy)

# Convert x, y into lists of numbers
time = list(map(float,time))
velocities = list(map(float,height)) #in cm/s

# Convert velocities into rotational velocities (rps)
#nmicro = int(1/float(RES))   # Number of microsteps per step
#SPR = 200                    # From Nema 17 doc
#fstep = velrot*SPR*nmicro/60 # microsteps per second


# Set duty cycle and frequency
#pi.set_PWM_dutycycle(STEP,128) # PWM 1/2 On 1/2 Off - 50% duty cycle
# I think this is where we can include the frequency. We'll have to feed this
# function in a loop
#pi.set_PWM_frequency(STEP,500) # 500 pulses per second - 500 Hz

dutycycle = 128

# For specific frequencies not in table PiStepperFreq.png, use pin 18 and:
for i in range(len(time)):
    pi.write(DIR,numpy.sign(velrot[i]))
    pi.hardware_PWM(18,velrot[i]*200,dutycycle)
    sleep(time[i+1]-time[i])

pi.hardware_PWM(18,frequency,0) 
