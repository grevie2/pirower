from entity import Entity
import pygame
from screen import get_r_in_pixels
from constants import BUOY_COLOUR, BUOY_SIZE, VIEWABLE_HEIGHT_R

class Buoy(Entity):    
    def __init__(self, x, r_y):
        Entity.__init__(self)                
        self.r_y = r_y
        self.y = 0
        self.x = x        
        self.color = BUOY_COLOUR
                        
    def update(self, screen, r_change):                
        self.r_y += r_change

        if self.r_y > VIEWABLE_HEIGHT_R:
            #it's not neccessarily zero, it depends how much it has gone offscreen
            self.r_y = 0 + (self.r_y - VIEWABLE_HEIGHT_R)
                                
        #convert to pixels
        self.y = get_r_in_pixels(self.r_y)                                        
        pygame.draw.circle(screen, self.color, (self.x-(BUOY_SIZE/2), \
											   get_r_in_pixels(self.r_y)-(BUOY_SIZE/2)), \
											   BUOY_SIZE)
                                                   
        return self.r_y
                    
