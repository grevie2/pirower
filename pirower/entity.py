import pygame
#from screen import get_r_in_pixels
#from screen import get_new_r_in_pixels
from constants import WIN_WIDTH, WIN_HEIGHT, VIEWABLE_HEIGHT_R, VIEWABLE_WIDTH_R, GAME_VIEW, OVERHEAD, SIDE

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #print "Entity constructor"
        self.r_y = 0
        self.x = 0
        

    def is_offscreen_left(self):
        return self.x >= 0 - self.image.get_width()

    def is_offscreen_right(self):
        return self.x <= WIN_WIDTH + self.image.get_width()

    def is_offscreen_and_ahead_of_player(self, viewable_max_r, game_view):
        if self.r_y > viewable_max_r:            
            #okay, it's at least partly offscreen so check further to see if all of the image is offscreen
            offscreen_diff = viewable_max_r - self.r_y            
            if game_view == OVERHEAD:
                return self.get_new_r_in_pixels(offscreen_diff, 1) < (0 - self.img.get_height())
            elif game_view == SIDE:
                #print "here"
                return self.get_new_r_in_pixels(offscreen_diff, 1) < (0 - self.img.get_width())            
        else:
            return False
	
    def get_new_r_in_pixels(self, r_change, layer_multiplier, game_view):
        if game_view == OVERHEAD:
            num_pixels = (WIN_HEIGHT/VIEWABLE_HEIGHT_R * layer_multiplier) * r_change
        elif game_view == SIDE:
            num_pixels = WIN_WIDTH - (WIN_WIDTH/VIEWABLE_WIDTH_R * layer_multiplier) * r_change           
        return int(round(num_pixels)) #rounding should not be needed
		        
    def is_offscreen_and_behind_player(self, viewable_min_r):
        return self.r_y < viewable_min_r
                  
    def is_offscreen(self, viewable_min_r):
        return self.is_offscreen_and_behind_player(viewable_min_r) and \
                self.is_offscreen_left() and \
                self.is_offscreen_right()

    def is_onscreen(self, viewable_min_r, viewable_max_r):
        return self.r_y >= viewable_min_r and self.r_y <= viewable_max_r and \
                self.x >= 0 - self.image.get_width() and \
                self.x <= WIN_WIDTH + self.image.get_width()
