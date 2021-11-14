import random
import pygame
from entity import Entity
from constants import LEFT_TO_RIGHT, WIN_WIDTH
from screen import get_r_in_pixels

class Fish(Entity):
    def __init__(self, fish_image_path, viewable_min_r, viewable_max_r):
        Entity.__init__(self)
        self.fish_image_path = fish_image_path
        self.regenerate(viewable_min_r, viewable_max_r)
        self.fish_direction = LEFT_TO_RIGHT
        self.fish_num = 1
        self.fish_image_filename = ""
        self.y = 0

    def update(self, viewable_min_r, viewable_max_r):
        #if it's onscreen then update screen position
        if Entity.is_onscreen(self, viewable_min_r, viewable_max_r):
            temp = viewable_max_r - self.r_y
            self.y = get_r_in_pixels(temp)
            if self.fish_direction == LEFT_TO_RIGHT:
                self.x += self.fish_speed
            else:
                self.x -= self.fish_speed
        else:
            self.regenerate(viewable_min_r, viewable_max_r)

        return self.r_y

    def regenerate(self, viewable_min_r, viewable_max_r):
        self.fish_num = random.randint(1, 5)
        self.fish_image_filename = self.fish_image_path + "/fish" + str(self.fish_num) + "_small.png"
        self.image = pygame.image.load(self.fish_image_filename).convert_alpha()

        #the scaled images don't look very good
        #old_width = self.image.get_rect().width
        #new_width = int(old_width * 0.8)
        #old_height = self.image.get_rect().width
        #new_height = int(old_height * 0.8)
        #self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.r_y = random.randint(viewable_min_r, viewable_max_r)
        self.fish_direction = random.randint(1, 2)
        self.fish_speed = random.randint(5, 15)

        if self.fish_direction == LEFT_TO_RIGHT:
            self.x = 0 - self.image.get_width()
        else:
            self.x = WIN_WIDTH + self.image.get_width()
            #flip the image if fish is swimming right to left
            self.image = pygame.transform.flip(self.image, True, False)
            
    #TODO: I think the first two lines of this method are not needed
    def blit(self, screen, viewable_max_r):
        temp = viewable_max_r - self.r_y
        self.y = get_r_in_pixels(temp)
        screen.blit(self.image, (self.x - self.image.get_width(), self.y))
