import pygame
from fish import Fish
from constants import FISH_IMAGE_PATH

#this class requires pygame to be initialised
class OverheadStage:
	def __init__(self):			
		self.fishes = []
								
		#TODO: lane buoys could be processed by this class too	
		
		self.bg = pygame.Surface((32,32))
		self.bg.convert()		
		self.bg.fill(pygame.Color("#2A99EA"))
				
	#the number of fish must be reset before every race session
	def reset(self, num_fish, viewable_min_r, viewable_max_r):
		self.fishes = []
		for i in range(0, num_fish):
			f = Fish(FISH_IMAGE_PATH, viewable_min_r, viewable_max_r)
			self.fishes.append(f)
												
	def update(self, r_change, viewable_min_r, viewable_max_r, updateFish):				
		#print "updating fish"
		if updateFish:
			for f in self.fishes:
				f.update(viewable_min_r, viewable_max_r)
				
		#TODO: do other updates
		
	def draw(self, screen, viewable_max_r):
		# draw background
		for y in range(32):
			for x in range(64):
				screen.blit(self.bg, (x * 32, y * 32))

		#print "len is ", len(self.fishes)
		for f in self.fishes:
			f.blit(screen, viewable_max_r)
