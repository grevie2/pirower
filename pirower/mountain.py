import os                             # path resolving and image saving
import random                         # midpoint displacement
from PIL import Image, ImageDraw      # image creation and drawing
import bisect                         # working with the sorted list of points
import pygame

class Mountain:
	def __init__(self, color):
		self.start = 0
		self.points = []
		self.color=color
        
	def midpoint_displacement(self, start, end, roughness, vertical_displacement=None, num_of_iterations=16):
		"""
		Given a straight line segment specified by a starting point and an endpoint
		in the form of [starting_point_x, starting_point_y] and [endpoint_x, endpoint_y],
		a roughness value > 0, an initial vertical displacement and a number of
		iterations > 0 applies the  midpoint algorithm to the specified segment and
		returns the obtained list of points in the form
		points = [[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
		"""
		# Final number of points = (2^iterations)+1
		if vertical_displacement is None:
			# if no initial displacement is specified set displacement to:
			#  (y_start+y_end)/2
			vertical_displacement = (start[1]+end[1])/2
		# Data structure that stores the points is a list of lists where
		# each sublist represents a point and holds its x and y coordinates:
		# points=[[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
		#              |          |              |
		#           point 0    point 1        point n
		# The points list is always kept sorted from smallest to biggest x-value
		self.points = [start, end]
		iteration = 1
		while iteration <= num_of_iterations:
			# Since the list of points will be dynamically updated with the new computed
			# points after each midpoint displacement it is necessary to create a copy
			# of the state at the beginning of the iteration so we can iterate over
			# the original sequence.
			# Tuple type is used for security reasons since they are immutable in Python.
			points_tup = tuple(self.points)
			for i in range(len(points_tup)-1):
				# Calculate x and y midpoint coordinates:
				# [(x_i+x_(i+1))/2, (y_i+y_(i+1))/2]
				midpoint = list(map(lambda x: (points_tup[i][x]+points_tup[i+1][x])/2,
									[0, 1]))
				# Displace midpoint y-coordinate				
				midpoint[1] += random.choice([-vertical_displacement,
											  0])
								
				# Insert the displaced midpoint in the current list of points         
				bisect.insort(self.points, midpoint)
				# bisect allows to insert an element in a list so that its order
				# is preserved.
				# By default the maintained order is from smallest to biggest list first
				# element which is what we want.
			# Reduce displacement range
			vertical_displacement *= 2 ** (-roughness)
			# update number of iterations
			iteration += 1		
                           
	def convert_height(self, current_height):
		return 480 - current_height
		    
	def draw(self, screen):
		prev = self.points[0]
		for p in self.points:			
			#pygame.draw.line(screen, self.color, (prev[0], self.convert_height(prev[1])), (p[0], self.convert_height(p[1])))
			pygame.draw.line(screen, self.color, (prev[0], prev[1]), (p[0], p[1]))
			prev = p
