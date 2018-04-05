from time import sleep
import RPi.GPIO as GPIO
import pigpio

## START THE PIGPIO DEAMON! - sudo pigpiod
# Default sampling rate (defines allowable frequencies) is 5. This can be
# changed using the -s tag when calling pigpiod

DIR = 20     # Direction GPIO Pin
STEP = 21    # Step GPIO Pin
SWITCH = 16  # GPIO Pin of Switch

# Connect to pigpio daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)

# Set up input switch
pi.set_mode(SWITCH, pigpio.INPUT)
pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)

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
RES = 'Full'
for i in range(3):
    pi.write(MODE[i],RESOLUTION[RES][i])

# Set duty cycle and frequency
pi.set_PWM_dutycycle(STEP,128) # PWM 1/2 On 1/2 Off - 50% duty cycle
pi.set_PWM_frequency(STEP,500) # 500 pulses per second - 500 Hz

# For specific frequencies not in table PiStepperFreq.png, use pin 18 and:
# pi.hardware_PWM(18,frequency,dutycycle)

try:
    while True:
        pi.write(DIR,pi.read(SWITCH)) # Set direction
        sleep(.1)

except KeyboardInterrupt:
    print("Stopping PIGPIO and exiting...")
finally:
    pi.set_PWM_dutycycle(STEP,0) # PWM Off
    pi.stop()
