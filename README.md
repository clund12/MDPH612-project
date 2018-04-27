MDPH612 TERM PROJECT
====================

# Towards a 4D breast phantom for CyberKnife QA
## Translation of breathing trace data into mechanical motion

### Project Outline

The goal of this work is to design an open-source, easy-to-construct 4D breast phantom model that could be constructed by medical physicists for motion-tracking and, potentially, dosimetry of CyberKnife treatments.  A list of materials required by any interested physicists is provided below, as are the scripts needed to interact with the equipment and the files needed for the 3D printing of some components.  Initially, the goal is to construct a proof-of-principle 2D model that accurately translates the time and spatial (1D) information of a Varian RPM breathing trace into mechanical motion.


### Equipment

- Raspberry Pi 3
- NEMA 17 Stepper motor
- Archimedes screw, washer, and connector to motor
- Bearing to hold screw at other end
- Texas Instruments DRV8825 Stepper Motor Controller IC
- 3D printer capable of printing parts up to approximately 30 cm in length
- Electrical components:
    - 10-12 V power supply
    - Multimetre
    - Breadboard, wires, etc.


### Aims

- Write a script to control the motor via the RPi
- Connect the electronics, RPi, and motor and test the script
- Design a 3D model of the support and rails needed to house the mechanical
  components
- Assemble mechanics/electronics with housing and connect motor to screw
- Improve script to handle errors and make it more user-friendly
- Extend principles to include a second spatial dimension
- Still to come..


### Progress

- All electronics, mechanical, and printed components assembled properly
- The script interfaces the RPi, driver, and motor correctly
    - Able to handle complex input behaviour
    - Spatial accuracy is very high
    - Platform cannot be extended past the physical bounds of the rails and is
      always returned to the centre
    - Useful errors are returned when users input improper files


### Issues

- Temporal accuracy must be addressed
- Friction along the rails must be reduced
- Errors should be returned when movements are beyond the capacity of the motor
- Next iteration of housing will need to be made more robust


### Authors

- Chris Lund
- Veng-Jean Heng

### Acknowledgements

- Dr. Francois DeBlois
- McGill MPU
