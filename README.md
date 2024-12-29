# Boid Simulation with MIDI Integration

The assignment: Write a Jython program that creates a simple chaos synthesizer. Use the AKAI Mini MIDI controller to control different aspects of the boids movement. Then, map boids movement to control the frequency (or other parameters) in different voices of an AudioSample.

This program does require a MIDI keyboard, preferably the “Akai MPK Mini MK3 25-Key Keyboard Controller” since the program was specifically mapped to that keyboard, and the two .wav files uploaded.

This program simulates flocking behavior of "boids" (autonomous agents) with MIDI-controlled audio and visual parameters. It combines visual dynamics with audio synthesis, creating an interactive and customizable experience.

## Features

### Boid Behavior
- **Separation:** Boids maintain a minimum comfortable distance from each other.
- **Alignment:** Boids align their direction with local flockmates.
- **Cohesion:** Boids move toward an attraction point, which can be influenced by user input.
- **Interactive Movement:** Attraction points can be dynamically updated via mouse drag or MIDI input.

### MIDI Integration

- **Keys Control:**
  - The boids’ attraction point updates according to a key’s pitch and volume, they will move accordingly.
  - Audio frequency and separation knob work in conjunction → higher separation = higher frequency
  - Keys can also change frequency → higher pitch = higher frequency.
- **Audio Playback:**
  - Two looped audio samples (`piano.wav` and `sine.wav`) with adjustable frequencies based on MIDI input.

## Setup

1. Ensure you have the necessary dependencies installed:
   - `gui`
   - `math`
   - `random`
   - `midi`
   - `music`

2. Place the audio files `piano.wav` and `sine.wav` in the appropriate directory specified in the program.

3. Connect a MIDI controller (e.g., MPK Mini) to your computer.

## MIDI Controls

| Knobs               | Channel | Description                                |
|---------------------|---------|--------------------------------------------|
| Boid Radius         | `70`    | Adjusts the size of the boids.             |
| Transparency        | `71`    | Adjusts the alpha value of the boids.      |
| Min Separation      | `72`    | Adjusts the minimum separation distance.   |
| Flock Threshold     | `73`    | Adjusts the flocking threshold.            |
| Separation Factor   | `74`    | Adjusts the separation behavior factor.    |
| Alignment Factor    | `75`    | Adjusts the alignment behavior factor.     |
| Cohesion Factor     | `76`    | Adjusts the cohesion behavior factor.      |
| Friction Factor     | `77`    | Adjusts the friction for boid movement.    |

| Pads     | Channel | Description           |
|----------|---------|-----------------------|
| Green    | `36`    | Adds a green boid.    |
| Red      | `37`    | Adds a red boid.      |
| Orange   | `38`    | Adds a orange boid.   |
| White    | `39`    | Adds a white boid     |
| Cyan     | `40`    | Adds a cyan boid      |
| Blue     | `41`    | Adds a blue boid      |
| Violet   | `42`    | Adds a violet boid    |
| Reset    | `43`    | Resets the program.   |

## Usage

1. Start the simulation by running the script.
2. Use your MIDI controller to interact with the simulation:
   - Play notes to move attraction points and adjust audio frequencies.
   - Use knobs to control boid behavior and parameters.
   - Press specific keys to add boids of various colors.
3. Observe the boids' flocking behavior and corresponding audio changes.

## Reset Functionality

To reset behavior parameters and audio frequencies, press the designated MIDI key (default: `43`).

## Customization

Feel free to modify the following parameters in the script:
- **Number of boids (`numBoids`)** for larger or smaller flocks.
- **Audio files** to use different sound samples.
- **MIDI channel numbers** to match your specific controller.

## Notes

- This program is CPU-intensive when handling a large number of boids. Adjust `numBoids` as needed for your system's performance.
- Ensure your MIDI controller is properly configured and connected before running the script.

## Contact Information
- **Author:** Chi Nguyen
- **Email:** c.n91702@gmail.com
