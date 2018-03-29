import numpy as np
from time import sleep
import RPi.GPIO as GPIO # Can ONLY be run on a RPi!

DIR = 20     # Direction GPIO Pin
STEP = 21    # Step GPIO Pin
CW = 1       # Clockwise Rotation
CCW = 0      # Counterclockwise Rotation
SPR = 48     # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)      # Broadcom memory
GPIO.setup(DIR, GPIO.OUT)   # Sets direction pin to an output
GPIO.setup(STEP, GPIO.OUT)  # Sets step pin to an output
GPIO.output(DIR, CW)        # Sets initial direction to clockwise

step_count = SPR    # Set initial test to a single rotation
delay = 0.0208      # (1s / 48) - rotation will take 1 second if no delay

for x in range(step_count):     # Counts the 48 steps
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

###### This is from the first half of the tutorial - microstepping not included because I want to get everything set up in the simplest way before we play around with it. I'm going to focus on the velocity file now.
