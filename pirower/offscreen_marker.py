from constants import OFFSCREEN_MARKER_FONT_SIZE
from constants import WIN_HEIGHT, WIN_WIDTH
from constants import WHITE, GREEN
from constants import POINT_UP, POINT_DOWN, POINT_LEFT, POINT_RIGHT, POINT_AHEAD, POINT_BACK
from constants import OVERHEAD, SIDE
import pygame as pg

class OffscreenMarker(object):
    def __init__(self):
        pass
	
    def draw(self, screen, direction, viewable_min_r, viewable_max_r, x, y, r_y, game_view):
		myfont = pg.font.SysFont("Roboto Condensed", OFFSCREEN_MARKER_FONT_SIZE)
		midscreen_r_point = viewable_min_r + ((viewable_max_r - viewable_min_r)/2)
        
		if game_view == OVERHEAD:
			if direction == POINT_AHEAD:
				distance_ahead = r_y - midscreen_r_point
				label = myfont.render("+" + str(distance_ahead), 1, WHITE)
				label2 = myfont.render("++" + str(distance_ahead), 1, WHITE)
				label_x = x - label2.get_rect().width/2
				label_y = (WIN_HEIGHT/2) + 35
				screen.blit(label, (label_x, label_y))
				
				pt1_x = x - 40
				pt1_y = (WIN_HEIGHT/2) + 30								
				pt2_x = x
				pt2_y = (WIN_HEIGHT/2) + 0				
				pt3_x = x + 40
				pt3_y = (WIN_HEIGHT/2) + 30				
				tri = [(pt1_x, pt1_y), (pt2_x, pt2_y), (pt3_x, pt3_y)]
				pg.draw.polygon(screen, GREEN, tri)
				
			elif direction == POINT_BACK:
				distance_behind = midscreen_r_point - r_y
				label = myfont.render("-" + str(distance_behind), 1, WHITE)
				label2 = myfont.render("--" + str(distance_behind), 1, WHITE)
				label_x = x - label2.get_rect().width/2
				label_y = (WIN_HEIGHT/2) + 35
				screen.blit(label, (label_x, label_y))
				
				pt1_x = x - 40
				pt1_y = (WIN_HEIGHT/2) + 70
				pt2_x = x
				pt2_y = (WIN_HEIGHT/2) + 100
				pt3_x = x + 40
				pt3_y = (WIN_HEIGHT/2) + 70
				tri = [(pt1_x, pt1_y), (pt2_x, pt2_y), (pt3_x, pt3_y)]
				pg.draw.polygon(screen, GREEN, tri)
				       
		elif game_view == SIDE:      
			if direction == POINT_AHEAD:				
				distance_ahead = r_y - midscreen_r_point
				label = myfont.render("+" + str(distance_ahead), 1, WHITE)
				label2 = myfont.render("++" + str(distance_ahead), 1, WHITE)				
				label_x = WIN_WIDTH/2
				label_y = y + 15
				
				pt1_x = (WIN_WIDTH/2) + 0
				pt1_y = y - 15
				pt2_x = (WIN_WIDTH/2) + 15
				pt2_y = y
				pt3_x = (WIN_WIDTH/2) + 0
				pt3_y = y + 15
				tri = [(pt1_x, pt1_y), (pt2_x, pt2_y), (pt3_x, pt3_y)]                              
				pg.draw.polygon(screen, GREEN, tri)												
				screen.blit(label, (label_x, label_y))
								
			elif direction == POINT_BACK:
				distance_behind = midscreen_r_point - r_y
				label = myfont.render("-" + str(distance_behind), 1, WHITE)
				label2 = myfont.render("--" + str(distance_behind), 1, WHITE)
				label_x = WIN_WIDTH/2
				label_y = y + 15
				screen.blit(label, (label_x, label_y))
				
				pt1_x = (WIN_WIDTH/2) - 0
				pt1_y = y - 15
				pt2_x = (WIN_WIDTH/2) - 15
				pt2_y = y
				pt3_x = (WIN_WIDTH/2) - 0
				pt3_y = y + 15
				tri = [(pt1_x, pt1_y), (pt2_x, pt2_y), (pt3_x, pt3_y)]                              
				pg.draw.polygon(screen, GREEN, tri)                       
