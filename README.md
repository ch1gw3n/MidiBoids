## Overview
Project for Digital Media Programming

Assignment: Write a Jython program that creates a simple chaos synthesizer. Use the AKAI Mini MIDI controller to control different aspects of the boids movement. Then, map boids movement to control the frequency (or other parameters) in different voices of an AudioSample.

This project does require a MIDI keyboard, preferably the “Akai MPK Mini MK3 25-Key Keyboard Controller” since the program was specifically mapped to that keyboard, and the two .wav files uploaded.

## Using A Boids Simulation Code
  Knobs controlled:
    1. radius of boids
    2. alpha value of boids
    3. minimum separation 
    4. flock threshold
    5. separation factor
    6. alignment factor
    7. cohesion factor
    8. friction factor
  Seven pads added boids in colors:
    1. green
    2. red
    3. orange
    4. white
    5. cyan
    6. blue
    7. violet
   One pad acts as a program reset.

The color pads work in conjunction with radius and alpha knobs to control what a new boid looks like.
The boids’ attraction point updates according to a key’s pitch and volume, they will move accordingly.
Audio frequency and separation knob work in conjunction → higher separation = higher frequency
Keys can also change frequency → higher pitch = higher frequency.

Contact Me: c.n91702@gmail.com
