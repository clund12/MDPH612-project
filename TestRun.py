import sys
from time import sleep
import numpy
import RPi.GPIO as GPIO # Can ONLY be run on a RPi!
import pigpio

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

velrot = 1 # define this as 1 rps

dutycycle = 128 # 50% dutycycle

#frequency = number of pulses per s
frequency = velrot*400
#if one full pulse moves by 1 step, then 200 pulses move by 1 full rotation
#if one half pulse moves by 1/2 step, then 400 pulses move by 1 full rotation
#thus frequency (pulse/s) = velrot (rps) * 400 (pulse/rotation)

pi.write(DIR,numpy.sign(velrot)) #set direction to be sign of velrot
#pi.hardware_PWM(18,frequency,dutycycle) 
pi.set_PWM_dutycycle(STEP,dutycycle)
pi.set_PWM_frequency(STEP,frequency)
sleep(1)
pi.set_PWM_dutycycle(STEP,0)
pi.set_PWM_frequency(STEP,frequency)
pi.stop()
#pi.hardware_PWM(18,frequency,0)  