import pygame
from forest import Forest
from mountain_range import MountainRange
from side_checkpoint_marker import SideCheckPointMarker
from constants import SIDE

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
#SKY = (255,229,193)
SKY = (220,200,255)

CLOUDS = (255,255,255)
HIGHLIGHT = (242,146,83)
MOUNTAIN = (235,99,21)
BACKGROUND_TREES = (184,106,0)
MIDGROUND_TREES = (123,69,0)
FOREGROUND_TREES  = (79,46,0)
LAKE = (200,180,255) #purple
LAKE = (255,229,193) #sky
LAKE = (220,200,255) #purple
LAKE = (120,180,255) #purple
LAKE = (145,207,255) #purple

#this class requires pygame to be initialised
class Stage:
	def __init__(self):			
		self.mr = MountainRange(MOUNTAIN, 330, 330, 60, 0.25)
		self.bgd = MountainRange(BACKGROUND_TREES, 310, 310, 10, 0.5)
		self.bg_trees = Forest(BACKGROUND_TREES, 310, 10, 40, 40, 50, 0.5)
		self.lake = MountainRange(LAKE, 290, 290, 0, 0)
		self.mg = MountainRange(MIDGROUND_TREES, 60, 60, 10, 1.5)		
		self.mg_trees = Forest(MIDGROUND_TREES, 60, 5, 40, 55, 75, 1.5)		
		self.fg = MountainRange(FOREGROUND_TREES, 0, 0, 10, 2.5)		
		self.fg_trees = Forest(FOREGROUND_TREES, 10, 30, 90, 90, 170, 2.5)
		self.side_checkpoint_marker = SideCheckPointMarker(0)	        
		
		#these could be done after construction of the Stage object
		self.bg_trees.load_tree_image('./resources/trees/small_trees_bg.png')
		self.mg_trees.load_tree_image('./resources/trees/med_trees_mg.png')
		self.fg_trees.load_tree_image('./resources/trees/large_trees_fg.png')	
		
		#lane buoys could be processed by this class too	
		
		self.bg = pygame.Surface((32,32))
		self.bg.convert()		
		self.bg.fill(pygame.Color("#FFE5C1"))
		self.bg.fill(pygame.Color("#dff1ff"))
		#self.bg.fill(pygame.Color("#dcc8ff"))
		
	def reset(self):
		self.side_checkpoint_marker = SideCheckPointMarker(0)	        
		
	def update(self, r_change):				
		self.mr.shift_left(r_change)			 
		self.bgd.shift_left(r_change) 
		self.bg_trees.shift_left(r_change)  
		#no lake change 
		self.mg.shift_left(r_change)  
		self.mg_trees.shift_left(r_change)  
		self.fg.shift_left(r_change)  
		self.fg_trees.shift_left(r_change)  
							
	def draw(self, screen, viewable_min_r, viewable_max_r, ghosts, player):						
        # draw background
		for y in range(32):
			for x in range(64):
				screen.blit(self.bg, (x * 32, y * 32))
                
		self.mr.update()
		self.mr.draw(screen)
		self.bgd.update()
		self.bgd.draw(screen)				
		self.bg_trees.update()
		self.bg_trees.draw(screen)				
		self.lake.update()
		self.lake.draw(screen)				
		checkpoint_r = self.side_checkpoint_marker.update(screen, viewable_min_r, viewable_max_r)
		
		for g in ghosts:
			g.blit(screen, viewable_min_r, viewable_max_r, SIDE)
        
		player.blit(screen, viewable_min_r, viewable_max_r, SIDE)
            
		self.mg.update()
		self.mg.draw(screen)						
		self.mg_trees.update()
		self.mg_trees.draw(screen)
		self.fg.update()
		self.fg.draw(screen)						
		self.fg_trees.update()
		self.fg_trees.draw(screen)			
