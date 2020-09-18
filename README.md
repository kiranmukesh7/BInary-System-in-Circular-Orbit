# BInary-System-in-Circular-Orbit

This repository contains the code(s) for animating binary systems with user defined masses. The simulation was performed using Python 3.6.9 with help of libraries - numpy, matplotlib and pylab. The simulation results are displayed in both polar and Cartesian coordinates. Log proportionality was used to compress the difference in magnitude of variation of masses to be visually represented (so that both the components are visible, at least). This was also helpful in simulating systems in which the components have non-identical characteristics (hence, different mass density, physical and chemical properties which influence their sizes.

The code can be run from the terminal by providing the input arguments along with the execution command. The below command can be used to get the list of input arguments and a brief description of the same. It also prints the guide to usage on the terminal.

$python3 orbit.py -m1 1 -m2 2 -key 1 -a 3 -ms 10 -plot polar -prop log

For example, the above command asks the system to execute the code with mass of the binary components being 1 and 2 units (some common base unit, say M_sun) with marker scale factor of 10, separation between them 3 units (say pc, A, etc.,) with the marker size proportional to logarithm of their masses and finally save the simulation (animation) as a ".gif" file.

# Bibliography

https://github.com/zaman13/Three-Body-Problem-Gravitational-System
