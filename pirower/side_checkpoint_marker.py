from entity import Entity
from constants import WIN_WIDTH, SIDE_VIEW_CHECKPOINT_MARKER_FONT_SIZE, CHECKPOINT_INTERVAL
from constants import WHITE, RED, ORANGE
from constants import VIEWABLE_WIDTH_R, WIN_WIDTH, SIDE
from screen import get_r_in_pixels
import pygame

class SideCheckPointMarker(Entity):
    def __init__(self, marker_level_r):
        Entity.__init__(self)
        self.y = 200
        self.marker_level_r = marker_level_r
        self.marker_level_r = 0
    		                                    
    def update(self, screen, viewable_min_r, viewable_max_r):
        #if it's onscreen then draw it
        if self.marker_level_r >= viewable_min_r and self.marker_level_r <= viewable_max_r:                    
            r_change = viewable_max_r - self.marker_level_r                        
            r_in_pix = self.get_new_r_in_pixels(r_change, 1, SIDE)            
            pt1_x = r_in_pix + 60
            pt1_y = 190            
            pt2_x = r_in_pix + 260
            pt2_y = 480            
            pygame.draw.line(screen, RED, (pt1_x, pt1_y), (pt2_x, pt2_y))

            myfont = pygame.font.SysFont("Roboto Condensed", SIDE_VIEW_CHECKPOINT_MARKER_FONT_SIZE)
            if self.marker_level_r == 0:
                label = myfont.render("START", 1, RED)
            else:
                label = myfont.render(str(self.marker_level_r) + "R", 1, RED)                
            label_x = r_in_pix + 80
            label_y = 190 
            screen.blit(label, (label_x, label_y))            
        else:			
            #get the next checkpoint to the nearest CHECKPOINT_INTERVAL             
            m = viewable_max_r % CHECKPOINT_INTERVAL
            self.marker_level_r = viewable_max_r - m
                        
        return self.marker_level_r                        
