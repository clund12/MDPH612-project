import numpy as np
from time import sleep
import RPi.GPIO as GPIO # Can ONLY be run on a RPi!

DIR = 20     # Direction GPIO Pin
STEP = 21    # Step GPIO Pin
CW = 1       # Clockwise Rotation
CCW = 0      # Counterclockwise Rotation
SPR = 200     # Steps per Revolution (Checked according to NEMA 17 spec sheet)

GPIO.setmode(GPIO.BCM)      # Broadcom memory
GPIO.setup(DIR, GPIO.OUT)   # Sets direction pin to an output
GPIO.setup(STEP, GPIO.OUT)  # Sets step pin to an output
GPIO.output(DIR, CW)        # Sets initial direction to clockwise

# For microstepping tests
# Note: current is 71% of maximum in full step mode, but this is not the case
# for microstepping! If the current has been increased past the maximum when
# we're working with full step, then we need to decrease it.
MODE = (14,15,18) # Microstep Resolution GPIO pins
#GPIO.setup(MODE, GPIO.OUT)

RESOLUTION = {'Full': (0,0,0),
        'Half': (1,0,0),
        '1/4': (0,1,0),
        '1/8': (1,1,0),
        '1/16': (0,0,1),
        '1/32': (1,0,1)}
#GPIO.output(MODE,Resolution['1/32'])

step_count = SPR    # Set initial test to a single rotation
delay = 0.005      # (1s / 200) - rotation will take 1 second if no delay

for x in range(step_count):     # Counts the 200 steps
    GPIO.output(STEP, GPIO.HIGH)# Toggles step pin high
    sleep(delay)                # Wait duration of step
    GPIO.output(STEP, GPIO.LOW) # Toggles step pin low
    sleep(delay)                # Wait again: Pulsed, 2s for full rotation

sleep(.5)            # delay for half of a second after rotation(s)
GPIO.output(DIR,CCW) # Set direction to counterclockwise

# Go through rotation loop again with the new direction
# This might be where we can condense the program -> placing the GPIO.output into a conditional for loop will allow a continuous change as we run through a data set - as long as the delays aren't too short! This would then mean that we will always have to run it in some sort of pulsed mode, depending on how fast the loop runs through -> probably not a problem
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

###### This is from the first half of the tutorial - microstepping not included because I want to get everything set up in the simplest way before we play around with it. I'm going to focus on the velocity file now. It might actually be worth leaving this file as is and making a new one, so we can just check the motor with this one, then with a microstepping file, and then have a more complex file ready to go.
