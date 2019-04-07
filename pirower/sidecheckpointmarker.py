from entity import Entity
from constants import WIN_WIDTH, CHECKPOINT_MARKER_FONT_SIZE, CHECKPOINT_INTERVAL
from constants import WHITE
from screen import get_r_in_pixels
import pygame

class SideCheckpointMarker(Entity):
    def __init__(self, marker_level_r):
        Entity.__init__(self)
        self.y = 0
        self.marker_level_r = marker_level_r

    def update(self, screen, viewable_min_r, viewable_max_r):
        #if it's onscreen then draw it
        if self.marker_level_r >= viewable_min_r and self.marker_level_r <= viewable_max_r:
            temp = viewable_max_r - self.marker_level_r
            self.y = get_r_in_pixels(temp)
            pygame.draw.line(screen, WHITE, (0, self.y), (WIN_WIDTH, self.y))

            myfont = pygame.font.SysFont("Roboto Condensed", CHECKPOINT_MARKER_FONT_SIZE)
            if self.marker_level_r == 0:
                label = myfont.render("START", 1, WHITE)
            else:
                label = myfont.render(str(self.marker_level_r) + "R", 1, WHITE)
            screen.blit(label, (WIN_WIDTH - 50, self.y))

        else:
            #get the next checkpoint to the nearest CHECKPOINT_INTERVAL
            m = viewable_max_r % CHECKPOINT_INTERVAL
            self.marker_level_r = viewable_max_r - m

        return self.marker_level_r
