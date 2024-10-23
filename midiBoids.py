# midiBoids.py
#
# Author:  Chi Nguyen
# Email:   nguyenct1@g.cofc.edu
# Class:   CITA 284 
# Assignment: Homework #6
# Due Date:  1 April 2024
#
# Purpose: Control Boids with MIDI keyboard, which in turns, 
#          controls AudioSamples
#
# Input:   MIDI keyboard and AudioSample
#
# Output:  Cool stuff
#
# Notes:   Adjusted original comments for aesthetic purposes.
#          You also mispelled Threshold.
  
from gui import *
from math import *
from random import *
from midi import *
from music import *
  
# universe parameters
universeWidth  = 1000   # how wide the display
universeHeight = 650    # how high the display

# boid generation parameters

### <BEGIN CHANGE> ******************************************************
#numBoids   = 200        # from 2 to as much as your CPU can handle
#boidRadius = 2          # radius of boids
#boidColor  = Color.BLUE # color of boids

numBoids   = 1           # CPU cannot handle many
boidRadius = 2           # radius of boids
boidColor  = Color.BLUE  # color of boids

### <END CHANGE> *********************************************************

# boid distance parameters
minSeparation  = 30      # min comfortable distance between two boids
flockThreshold = 100     # boids closer than this are in a local flock
  
# boid behavior parameters (higher means quicker/stronger)
separationFactor = 0.01  # how quickly to separate
alignmentFactor  = 0.16  # how quickly to align with local flockmates
cohesionFactor   = 0.0   # how quickly to converge to attraction point
frictionFactor   = 1.1   # how hard it is to move - the more, the harder
                         # (1.0 means no friction)

### <CHI'S CODE BEGINS> ***************************************************

# 3audio generation
midi = MidiIn("Unknown vendor MPK mini 3")
audio1 = AudioSample("\Users\cn917\COFC\CITA284\midiBoids\piano.wav", D4)
audio2 = AudioSample("\Users\cn917\COFC\CITA284\midiBoids\sine.wav", D4, 10)

# loop the 2 voices
audio1.loop(times = -1, start = 0, size = -1, voice = 0)
audio2.loop(times = -1, start = 0, size = -1, voice = 1)

# extra parameters for later
alpha      = 255        # added for customization   
pitchStart = 150        # preferred frequency range
pitchStop  = 850         
data1Start = 48         # data 1 ranges for the keys
data1Stop  = 84          
data2Start = 0          # data 2 ranges for volume
data2Stop  = 127        # I want it starting at 8   

# midi knob control channel numbers
boidRadiusMidi     = 70 
alphaControlMidi   = 71
minSeparationMidi  = 72
flockThresholdMidi = 73

separationMidi     = 74
alignmentMidi      = 75
cohesionMidi       = 76
frictionMidi       = 77

# adjustment knobs for distance parameters & radius
def updateParameters(eventType, channel, data1, data2):
   global minSeparation, flockThreshold, boidRadius, alpha
   if   data1 == boidRadiusMidi:
      boidRadius     = mapValue(data2, data2Start, data2Stop, 1, 15)
   elif data1 == alphaControlMidi:
      alpha          = mapValue(data2, data2Start, data2Stop, 0, 255)
   elif data1 == minSeparationMidi:
      minSeparation  = mapValue(data2, data2Start, data2Stop, 5, 100)
   elif data1 == flockThresholdMidi:
      flockThreshold = int(mapValue(data2, data2Start, data2Stop, 10, 200))

# adjustment knobs for behavior parameters
def updateBehaviors(eventType, channel, data1, data2):
   global separationFactor, alignmentFactor, cohesionFactor, frictionFactor
   global data2Start, data2Stop # can't figure out the indent to not get '\n' error
   if   data1 == separationMidi:
      separationFactor  = mapValue(data2, data2Start, data2Stop, 0.0, 2)
   elif data1 == alignmentMidi:
      alignmentFactor   = mapValue(data2, data2Start, data2Stop, 0.0, 2)
   elif data1 == cohesionMidi:
      cohesionFactor    = mapValue(data2, data2Start, data2Stop, 0.0, 2)
   elif data1 == frictionMidi:
      frictionFactor    = mapValue(data2, data2Start, data2Stop, 1.0, 2)

# each pad adds a boid of different color, works in
# conjunction with boidRadiusMidi and alphaControlMidi 
# knobs to change size and transparency of each new boid
def addBoidsInColor(eventType, channel, data1, data2):
   global universe, numBoids, boidRadius, universeWidth, alpha
   if   data1 == 36:
      boidColor = Color(0, 255, 0, alpha)           # GREEN
      boid = Boid(x, y, boidRadius, boidColor, 1, 1)
      universe.add(boid)
   elif data1 == 37:
      boidColor = Color(255, 0, 0, alpha)           # RED
      boid = Boid(x, y, boidRadius, boidColor, 1, 1)
      universe.add(boid)
   elif data1 == 38:
      boidColor = Color(255, 128, 0, alpha)         # ORANGE
      boid = Boid(x, y, boidRadius, boidColor, 1, 1)
      universe.add(boid)
   elif data1 == 39:
      boidColor = Color(255, 255, 255, alpha)       # WHITE
      boid = Boid(x, y, boidRadius, boidColor, 1, 1)
      universe.add(boid)
   elif data1 == 40:
      boidColor = Color(0, 255, 255, alpha)         # CYAN
      boid = Boid(x, y, boidRadius, boidColor, 1, 1)
      universe.add(boid)
   elif data1 == 41:
      boidColor = Color(0, 0, 255, alpha)           # BLUE
      boid = Boid(x, y, boidRadius, boidColor, 1, 1)
      universe.add(boid)
   elif data1 == 42:                               
      boidColor = Color(255, 0, 255, alpha)         # VIOLET
      boid = Boid(x, y, boidRadius, boidColor, 1, 1)
      universe.add(boid)

# moves x and y points based on keyboard pitch and volume
# quieter value at the top of the display, louder at bottom
# constraint for 50 less than width and height so attraction 
# point stays relatively in the display
def moveAttractionPoint(eventType, channel, data1, data2):
   global universe, data1Start, data1Stop, data2Start, data2Stop
   data1_x = mapValue(data1, data1Start, data1Stop, 50, universe.display.getWidth()-50)
   data2_y = mapValue(data2, data2Start, data2Stop, 50, universe.display.getHeight()-50)
   universe.attractPoint = complex(data1_x, data2_y)

# works with minSeparationMidi knob
# higher separation = higher frequency   
def changeAudioKnob(eventType, channel, data1, data2):
   global audio, data2Start, data2Stop, pitchStart, pitchStop
   if data1 == minSeparationMidi:
      voice0Frequency = mapValue(data2, data2Start, data2Stop, pitchStart, pitchStop)
      audio1.setFrequency(voice0Frequency, 0)
      voice1Frequency = mapValue(data2, data2Start, data2Stop, pitchStart, pitchStop)
      audio2.setFrequency(voice0Frequency, 1)
   

# works with the keys
# higher pitch = higher frequency 
def changeAudioKey(eventType, channel, data1, data2):
   global audio, data1Start, data1Stop, pitchStart, pitchStop
   voice0Frequency = mapScale(data1, data1Start, data1Stop, pitchStart, pitchStop, MINOR_SCALE, 2)
   audio1.setFrequency(voice1Frequency, 0)
   voice1Frequency = mapScale(data1, data1Start, data1Stop, pitchStart, pitchStop, MINOR_SCALE, 2)
   audio2.setFrequency(voice1Frequency, 1)
 
# reset behavior parameters and audio
# frequencies, as a failsafe  
def resetPad(eventType, channel, data1, data2):
   global separationFactor, alignmentFactor, cohesionFactor 
   global frictionFactor, minSeparationMidi, audio
   
   if data1 == 43:
      separationFactor  = 0.01
      alignmentFactor   = 0.16
      cohesionFactor    = 0.01
      frictionFactor    = 1.1
      audio1.setFrequency(293.66, 0)
      audio2.setFrequency(293.66, 1)
   
# all function calls
midi.onNoteOn(moveAttractionPoint)
midi.onNoteOn(addBoidsInColor)
midi.onNoteOn(resetPad)
midi.onNoteOn(changeAudioKey)
midi.onInput(176, changeAudioKnob)
midi.onInput(176, updateParameters)
midi.onInput(176, updateBehaviors)

### <CHI'S CODE ENDS> *****************************************************

### define boid universe, a place where boids exist and interact ####
class BoidUniverse:
   """This is the boid universe..."""
  
   def __init__(self, title = "", width = 600, height = 400,
                frameRate=30):
  
      self.display = Display(title, width, height, 0, 0, Color.BLACK) # universe display
  
      self.boids = []                              # list of boids
  
      # holds attraction point for boids (initially, universe center)
      self.attractPoint = complex(width/2, height/2)  
  
      # create timer
      delay = 1000 / frameRate     # convert frame rate to delay (ms)
      self.timer = Timer(int(delay), self.animate)       # animation timer
  
      
      # when mouse is dragged, call this function to set the
      # attraction point for boids
      self.display.onMouseDrag( self.moveAttractionPoint )
   
   def start(self):
      """Starts animation."""
      self.timer.start()   # start movement!
  
   def stop(self):
      """Stops animation."""
      self.timer.stop()    # stop movement
  
   def add(self, boid):
      """Adds another boid to the system."""
  
      self.boids.append( boid )          # remember this boid
      self.display.add( boid.circle )    # add a circle for this boid
  
   def animate(self):
      """Makes boids come alive."""
  
      ### sensing and acting loop for all boids in the universe !!!
      for boid in self.boids:   # for every boid
  
         # first observe other boids and decide how to adjust movement
         boid.sense(self.boids, self.attractPoint)   
  
         # and then, make it so (move)!
         boid.act(self.display)                      
  
   def moveAttractionPoint(self, x, y):
      """Update the attraction point for all boids."""
      self.attractPoint = complex(x, y)
   
### define the boids, individual agents who can sense and act #######
class Boid:
   """This a boid..."""
  
   def __init__(self, x, y, radius, color,
                initVelocityX=1, initVelocityY=1 ):
      """Initialize boid's position, size, and initial velocity (x, y)."""
  
      # a boid is a filled circle
      self.circle = Circle(x, y, radius, color, True) 
  
      # set boid size, position
      self.radius = radius                # boid radius
      self.coordinates = complex(x, y)    # boid coordinates (x, y)
  
      # NOTE: We treat velocity in a simple way, i.e., as the
      # x, y displacement to add to the current boid coordinates,
      # to find where to move its circle next.  This moving is done
      # once per animation frame.
  
      # initialize boid velocity (x, y)
      self.velocity = complex(initVelocityX, initVelocityY)  
  
   def sense(self, boids, center):
      """Sense other boids' positions, etc., and adjust velocity
      (i.e., the displacement of where to move next)."""
  
      # use individual rules of thumb, to decide where to move next
  
      # 1. Rule of Separation - move away from other flockmates
      #                         to avoid crowding them
      self.separation = self.rule1_Separation(boids)
  
      # 2. Rule of Alignment - move towards the average heading
      #                        of other flockmates
      self.alignment = self.rule2_Alignment(boids)
  
      # 3. Rule of Cohesion - move toward the center of the universe
      self.cohesion = self.rule3_Cohesion(boids, center)
  
      # 4. Rule of Avoidance: move to avoid any obstacles
      #self.avoidance = self.rule4_Avoidance(boids)
  
      # create composite behavior
      self.velocity = (self.velocity / frictionFactor) + \
                      self.separation + self.alignment + \
                      self.cohesion            
  
   def act(self, display):
      """Move boid to a new position using current velocity."""
  
      # Again, we treat velocity in a simple way, i.e., as the
      # x, y displacement to add to the current boid coordinates,
      # to find where to move its circle next.
  
      # update coordinates
      self.coordinates = self.coordinates + self.velocity
  
      # get boid (x, y) coordinates
      x = self.coordinates.real  # get the x part
      y = self.coordinates.imag  # get the y part
  
      # act (i.e., move boid to new position)
      display.move( self.circle, int(x), int(y) )
  
   ##### steering behaviors ####################
   def rule1_Separation(self, boids):
      """Return proper velocity to keep separate from other boids,
         i.e., avoid collisions."""
  
      newVelocity = complex(0, 0)  # holds new velocity
  
      # get distance from every other boid in the flock, and as long
      # as we are too close for comfort, calculate direction to
      # move away (remember, velocity is just an x, y distance
      # to travel in the next animation/movement frame)
      for boid in boids:           # for each boid
  
         separation = self.distance(boid)   # how far are we?
  
         # too close for comfort (excluding ourself)?
         if separation < minSeparation and boid != self:
            # yes, so let's move away from this boid
            newVelocity = newVelocity - \
                          (boid.coordinates - self.coordinates)
  
      return newVelocity * separationFactor  # return new velocity
  
   def rule2_Alignment(self, boids):
      """Return proper velocity to move in the same general direction
         as local flockmates."""
   
      totalVelocity = complex(0, 0) # holds sum of boid velocities
      numLocalFlockmates = 0        # holds count of local flockmates
   
      # iterate through all the boids looking for local flockmates,
      # and accumulate all their velocities
      for boid in boids:
   
         separation = self.distance(boid)    # get boid distance
   
         # if this a local flockmate, record its velocity
         if separation < flockThreshold and boid != self:                      
            totalVelocity = totalVelocity + boid.velocity             
            numLocalFlockmates = numLocalFlockmates + 1     
           
      # average flock velocity (excluding ourselves)       
      if numLocalFlockmates > 0:
         avgVelocity = totalVelocity / numLocalFlockmates
      else:
         avgVelocity = totalVelocity
   
      # adjust velocity by how quickly we want to align
      newVelocity = avgVelocity - self.velocity
   
      return newVelocity * alignmentFactor  # return new velocity
  
   def rule3_Cohesion(self, boids, center):
      """Return proper velocity to bring us closer to center of the
         universe."""
  
      newVelocity = center - self.coordinates
  
      return newVelocity * cohesionFactor  # return new velocity
  
   ##### helper function ####################
   def distance(self, other):
      """Calculate the Euclidean distance between this and
         another boid."""
  
      xDistance = (self.coordinates.real - other.coordinates.real)
      yDistance = (self.coordinates.imag - other.coordinates.imag)
  
      return sqrt( xDistance*xDistance + yDistance*yDistance )
  
# start boid simulation
universe = BoidUniverse(title="Boid Flocking Behavior",
                        width=universeWidth, height=universeHeight,
                        frameRate=30)
  
# create and place boids
for i in range(0, numBoids):
  
   # get random position for this boid
   x = randint(0, universeWidth)
   y = randint(0, universeHeight)
  
   # create a boid with random position and velocity
   boid = Boid(x, y, boidRadius, boidColor, 1, 1)
   universe.add( boid )
  
# animate boids
universe.start()