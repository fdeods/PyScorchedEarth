### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
#
# Gravity objects

from math import sqrt
from libs.pyIgnition import keyframes, interpolate
import random

UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL = 1000.0  # Well, Newton got one to make it less stupidly large.


def RandomiseStrength(base, range):
	return base + (float(random.randrange(int(-range * 100), int(range * 100))) / 100.0)


class DirectedGravity:
	def __init__(self, strength = 0.0, strengthrandrange = 0.0, direction = [0, 1]):
		self.initstrength = strength
		self.strength = strength
		self.strengthrandrange = strengthrandrange
		directionmag = sqrt(direction[0]**2 + direction[1]**2)
		self.direction = [direction[0] / directionmag, direction[1] / directionmag]
		
		self.keyframes = []
		self.CreateKeyframe(0, self.strength, self.strengthrandrange, self.direction)
		self.curframe = 0
	
	def Update(self):
		newvars = interpolate.InterpolateKeyframes(self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'direction_x':self.direction[0], 'direction_y':self.direction[1]}, self.keyframes)
		self.initstrength = newvars['strength']
		self.strengthrandrange = newvars['strengthrandrange']
		self.direction = [newvars['direction_x'], newvars['direction_y']]
		
		if self.strengthrandrange != 0.0:
			self.strength = RandomiseStrength(self.initstrength, self.strengthrandrange)
		
		self.curframe = self.curframe + 1
	
	def GetForce(self, pos):
		force = [self.strength * self.direction[0], self.strength * self.direction[1]]
		
		return force
	
	def CreateKeyframe(self, frame, strength = None, strengthrandrange = None, direction = [None, None], interpolationtype = "linear"):
		keyframes.CreateKeyframe(self.keyframes, frame, {'strength':strength, 'strengthrandrange':strengthrandrange, 'direction_x':direction[0], 'direction_y':direction[1], 'interpolationtype':interpolationtype})
	
	def ConsolidateKeyframes(self):
		keyframes.ConsolidateKeyframes(self.keyframes, self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'direction_x':self.direction[0], 'direction_y':self.direction[1]})
	
	def SetStrength(self, newstrength):
		self.CreateKeyframe(self.curframe, strength = newstrength)
	
	def SetStrengthRandRange(self, newstrengthrandrange):
		self.CreateKeyframe(self.curframe, strengthrandrange = newstrengthrandrange)
	
	def SetDirection(self, newdirection):
		self.CreateKeyframe(self.curframe, direction = newdirection)


class PointGravity:
	def __init__(self, strength = 0.0, strengthrandrange = 0.0, pos = (0, 0)):
		self.initstrength = strength
		self.strength = strength
		self.strengthrandrange = strengthrandrange
		self.pos = pos
		
		self.keyframes = []
		self.CreateKeyframe(0, self.strength, self.strengthrandrange, self.pos)
		self.curframe = 0
	
	def Update(self):			
		newvars = interpolate.InterpolateKeyframes(self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'pos_x':self.pos[0], 'pos_y':self.pos[1]}, self.keyframes)
		self.initstrength = newvars['strength']
		self.strengthrandrange = newvars['strengthrandrange']
		self.pos = (newvars['pos_x'], newvars['pos_y'])
		
		if self.strengthrandrange != 0.0:
			self.strength = RandomiseStrength(self.initstrength, self.strengthrandrange)
		else:
			self.strength = self.initstrength
		
		self.curframe = self.curframe + 1
	
	def GetForce(self, pos):
		distsquared = (pow(float(pos[0] - self.pos[0]), 2.0) + pow(float(pos[1] - self.pos[1]), 2.0))
		if distsquared == 0.0:
			return [0.0, 0.0]
		
		forcemag = (self.strength * UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL) / (distsquared)
		
		# Calculate normal vector from pos to the gravity point and multiply by force magnitude to find force vector
		dist = sqrt(distsquared)
		dx = float(self.pos[0] - pos[0]) / dist
		dy = float(self.pos[1] - pos[1]) / dist
		
		force = [forcemag * dx, forcemag * dy]
		
		return force
	
	def GetMaxForce(self):
		return self.strength * UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL
	
	def CreateKeyframe(self, frame, strength = None, strengthrandrange = None, pos = (None, None), interpolationtype = "linear"):
		keyframes.CreateKeyframe(self.keyframes, frame, {'strength':strength, 'strengthrandrange':strengthrandrange, 'pos_x':pos[0], 'pos_y':pos[1], 'interpolationtype':interpolationtype})
	
	def ConsolidateKeyframes(self):
		keyframes.ConsolidateKeyframes(self.keyframes, self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'pos_x':self.pos[0], 'pos_y':self.pos[1]})
	
	def SetStrength(self, newstrength):
		self.CreateKeyframe(self.curframe, strength = newstrength)
	
	def SetStrengthRandRange(self, newstrengthrandrange):
		self.CreateKeyframe(self.curframe, strengthrandrange = newstrengthrandrange)
	
	def SetPos(self, newpos):
		self.CreateKeyframe(self.curframe, pos = newpos)
