MDPH612 TERM PROJECT
====================

## Using a Raspberry Pi to translate breathing traces (from a Varian RPM system) into mechanical motion via a stepper motor.

### Aims:
- Extend to 2D if there is time
- Clean up github
- Fix temporal accuracy problem
- Reduce friction along the rail

### Completed:
- Stepper Motor script is now based on displacements and microsteps for better positional accuracy
- Interface with a DRV-8825 stepper driver and a NEMA 17 stepper motor
- Obtain breathing trace (maybe surface trace) data
- Update global variable with each iteration to track platform position
- Get the track 3D printed, assemble with the stepper motor
- Stepper motor script with microstepping
- Become familiar with a Raspberry Pi 3 (PIXEL for now)

- Conversion of general trace into instantaneous velocites
	- demonstrated with a simple sine wave
	- writes the results to a new csv
- Simple stepper motor script to test whether the set-up is correct when the parts arrive
- Convert these velocities into the rotation speed of the motor needed to induce the desired linear motion