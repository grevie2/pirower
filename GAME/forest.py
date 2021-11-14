import pygame
import random
from terrain_utils import *
from screen import *
from constants import WIN_WIDTH, VIEWABLE_WIDTH_R

class Forest:
	def __init__(self, color, height, horiz_spacing_min, horiz_spacing_max, vert_spacing_min, vert_spacing_max, layer_multiplier):
		self.color = color
		self.height = height
		self.horiz_spacing_min = horiz_spacing_min
		self.horiz_spacing_max = horiz_spacing_max
		self.vert_spacing_min = vert_spacing_min
		self.vert_spacing_max = vert_spacing_max		
		self.trees = []
		self.layer_multiplier = layer_multiplier
		            
	def load_tree_image(self, tree_image_filename):    
		self.image = pygame.image.load(tree_image_filename).convert_alpha()
		
	def add_trees(self):
		if len(self.trees) == 0:
			#add tree						
			x = 0
			y = random.randint(self.height + self.vert_spacing_min, self.height + self.vert_spacing_max)
			self.trees.append([x, convert_height(y)])
		
		#while the x coord of the last tree is < stage right then add another tree		
		while self.trees[-1][0] < 800:			
			x = self.trees[-1][0] + random.randint(self.horiz_spacing_min, self.horiz_spacing_max)									
			y = random.randint(self.height + self.vert_spacing_min, self.height + self.vert_spacing_max)
			self.trees.append([x, convert_height(y)])    
		
	def remove_trees(self):
		if len(self.trees) > 0:
			#while the x coords of the first tree is < stage left then remove tree
			while self.trees[0][0] + self.image.get_rect().width < 0:				
				del(self.trees[0])
		
	def update(self):
		self.add_trees()
		self.remove_trees()
	
	def shift_left(self, r_change):
		pixel_chg = self.get_new_r_in_pixels(r_change, self.layer_multiplier)
		for t in self.trees:
			t[0] -= pixel_chg
	
	def get_new_r_in_pixels(self, r_change, layer_multiplier):
		num_pixels = (WIN_WIDTH/VIEWABLE_WIDTH_R * layer_multiplier) * r_change
		return int(round(num_pixels)) #rounding should not be needed
						
	def draw(self, screen):
		for t in self.trees:
			self.blit(screen, t[0], t[1])			
		
	def blit(self, screen, x, y):
		screen.blit(self.image, (x, y))	
