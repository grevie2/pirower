from mountain import Mountain
from terrain_utils import *
import random             
import pygame

from screen import *
from constants import WIN_WIDTH, VIEWABLE_WIDTH_R
	
class MountainRange:
	def __init__(self, color, start_height, end_height, vertical_displacement, layer_multiplier):		
		self.color = color
		self.mountains = []
		self.width = 0
		self.start_height = start_height
		self.end_height = end_height
		self.vertical_displacement = vertical_displacement
		self.layer_multiplier = layer_multiplier
		
	def add_mountain(self, start, end, roughness, vertical_displacement=None, num_of_iterations=16):
		m = Mountain(self.color)
		m.midpoint_displacement(start, end, roughness, vertical_displacement, num_of_iterations)
		self.mountains.append(m)
		
	def remove_mountain(self):
		pass
		
	def update(self):				
		width = 100  # Terrain width
		start_height = 390  # Terrain height start
		end_height = 390 # Terrain height end		
		width_min = 100
		width_max = 400
		
		if len(self.mountains) == 0:
			#add mountain						
			width = random.randint(width_min, width_max)			
			x_start = 0
			x_end = x_start + width		
			self.add_mountain([x_start, convert_height(self.start_height)], [x_end, convert_height(self.end_height)], 0.8, self.vertical_displacement, 5)    
		
		#while the x coord of the first point of the last mointain is < stage right then add another mountain		
		while self.mountains[-1].points[0][0] < 800:
			#x_start is the x of the last point of the last mountain						
			x_start = self.mountains[-1].points[-1][0]
			width = random.randint(width_min, width_max)									
			x_end = x_start + width		
			self.add_mountain([x_start, convert_height(self.start_height)], [x_end, convert_height(self.end_height)], 0.8, self.vertical_displacement, 5)     

		if len(self.mountains) > 0:
			#while the x coords of the last point of first mountain is < stage left then remove mointain								
			while self.mountains[0].points[-1][0] < 0:
				#remove mountain
				del(self.mountains[0])
															
	def draw(self, screen):		
		for m in self.mountains:
			m.draw(screen)
		
		#join first and last points with the bottom two corners
		pt1_x = self.mountains[0].points[0][0]
		pt1_y = 480
		pt2_x = self.mountains[-1].points[-1][0]
		pt2_y = 480
				
		temp = []		
		temp += [[pt1_x, pt1_y]]
		for m in self.mountains:
			temp += m.points
		temp += [[pt2_x, pt2_y]]				
		pygame.draw.polygon(screen, self.color, temp, 0)
	
	def shift_left(self, r_change):		     		
		pixel_chg = self.get_new_r_in_pixels(r_change, self.layer_multiplier)
		for m in self.mountains:
			for p in m.points:
				p[0] -= pixel_chg

	def get_new_r_in_pixels(self, r_change, layer_multiplier):
		num_pixels = (WIN_WIDTH/VIEWABLE_WIDTH_R * layer_multiplier) * r_change
		return int(round(num_pixels)) #rounding should not be needed
		
	def calc_left_edge(self, r):
		pass
		
	def calc_right_edge(self, r):
		pass
