from entity import Entity
from offscreen_marker import OffscreenMarker
import pygame as pg
import json
from constants import RECOVERY_STROKE, DRIVE_STROKE
from constants import OFFSCREEN_MARKER_FONT_SIZE, POINT_UP, POINT_DOWN, POINT_LEFT, POINT_RIGHT, POINT_AHEAD, POINT_BACK
from constants import GREEN, WHITE, BLUE, ORANGE
from constants import WIN_HEIGHT, GHOST_JSON_PATH
from constants import GAME_VIEW, OVERHEAD, SIDE
from constants import WIN_WIDTH, WIN_HEIGHT

from constants import VIEWABLE_WIDTH_R
import pygame
import datetime

class Ghost(Entity):
    def __init__(self, img_path, data_filename, x, layer_multiplier=1):
        #print "Ghost constructor"		
        Entity.__init__(self)
        
        #self.stroke_pos_current = 1 #shouldn't this be zero?
        #TODO: change the name of x - it's more aofa spacing var than an x value
        self.x = x
        self.y = x
        self.data_filename = data_filename
        fname = self.data_filename
        self.date_label = fname[27:29] + "/" + fname[25:27] + "/" + fname[21:25]
        self.time_label = fname[29:31] + ":" + fname[31:33] + ":" + fname[33:35]
        f = open(GHOST_JSON_PATH + '/' + self.data_filename, "r")
        data = f.read()
        json_data = json.loads(data)
        f.close()
        self.timestamp_ary = []
        self.timestamp_ary = json_data['flywheel_times']
        self.ir_timestamp_ary = []
        self.ir_timestamp_ary = json_data['ir_times']

        self.stroke_pos_current = 0 
        self.stroke_pos_change = 0               
        self.current_stroke_type = RECOVERY_STROKE
        self.stroke_count = 0
        self.part_stroke = False
        self.stroke_complete = False
        self.stroke_count = 0
        self.full_extent = False
        self.drive_complete = True
        self.recovery_complete = True
        self.stroke_attempted = False        
        #self.spm = 0
        self.current_stroke_start_time = ""
        self.current_stroke_end_time = ""
        self.layer_multiplier = layer_multiplier
        
        self.img_drive_0 = pygame.image.load(img_path + "/drive/rower_pos0.png").convert_alpha()
        self.img_drive_1 = pygame.image.load(img_path + "/drive/rower_pos1.png").convert_alpha()
        self.img_drive_2 = pygame.image.load(img_path + "/drive/rower_pos2.png").convert_alpha()        
        self.img_drive_3 = pygame.image.load(img_path + "/drive/rower_pos3.png").convert_alpha()
        self.img_drive_4 = pygame.image.load(img_path + "/drive/rower_pos4.png").convert_alpha()
        self.img_drive_5 = pygame.image.load(img_path + "/drive/rower_pos5.png").convert_alpha()
        self.img_drive_6 = pygame.image.load(img_path + "/drive/rower_pos6.png").convert_alpha()
        self.img_drive_7 = pygame.image.load(img_path + "/drive/rower_pos7.png").convert_alpha()
        self.img_drive_8 = pygame.image.load(img_path + "/drive/rower_pos8.png").convert_alpha()
        self.img_drive_9 = pygame.image.load(img_path + "/drive/rower_pos9.png").convert_alpha()
        self.img_drive_10 = pygame.image.load(img_path + "/drive/rower_pos10.png").convert_alpha()
        self.img_drive_11 = pygame.image.load(img_path + "/drive/rower_pos11.png").convert_alpha()
        self.img_drive_12 = pygame.image.load(img_path + "/drive/rower_pos12.png").convert_alpha()
        
        self.img_recovery_0 = pygame.image.load(img_path + "/recovery/rower_pos0.png").convert_alpha()
        self.img_recovery_1 = pygame.image.load(img_path + "/recovery/rower_pos1.png").convert_alpha()
        self.img_recovery_2 = pygame.image.load(img_path + "/recovery/rower_pos2.png").convert_alpha()
        self.img_recovery_3 = pygame.image.load(img_path + "/recovery/rower_pos3.png").convert_alpha()
        self.img_recovery_4 = pygame.image.load(img_path + "/recovery/rower_pos4.png").convert_alpha()
        self.img_recovery_5 = pygame.image.load(img_path + "/recovery/rower_pos5.png").convert_alpha()
        self.img_recovery_6 = pygame.image.load(img_path + "/recovery/rower_pos6.png").convert_alpha()
        self.img_recovery_7 = pygame.image.load(img_path + "/recovery/rower_pos7.png").convert_alpha()
        self.img_recovery_8 = pygame.image.load(img_path + "/recovery/rower_pos8.png").convert_alpha()
        self.img_recovery_9 = pygame.image.load(img_path + "/recovery/rower_pos9.png").convert_alpha()
        self.img_recovery_10 = pygame.image.load(img_path + "/recovery/rower_pos10.png").convert_alpha()
        self.img_recovery_11 = pygame.image.load(img_path + "/recovery/rower_pos11.png").convert_alpha()
        self.img_recovery_12 = pygame.image.load(img_path + "/recovery/rower_pos12.png").convert_alpha()
        
        self.img = self.img_drive_0
        
        self.offscreen_marker = OffscreenMarker()

    def update(self, viewable_min_r, viewable_max_r):                                	    
        if self.current_stroke_type == DRIVE_STROKE:			
            if self.stroke_pos_current >= 0:
                self.img = self.img_drive_0
            elif self.stroke_pos_current == -1:
                self.img = self.img_drive_1
            elif self.stroke_pos_current == -2:
                self.img = self.img_drive_2
            elif self.stroke_pos_current == -3:
                self.img = self.img_drive_3
            elif self.stroke_pos_current == -4:	        
                self.img = self.img_drive_4
            elif self.stroke_pos_current == -5:
                self.img = self.img_drive_5
            elif self.stroke_pos_current == -6:
                self.img = self.img_drive_6
            elif self.stroke_pos_current == -7:
                self.img = self.img_drive_7
            elif self.stroke_pos_current == -8:
                self.img = self.img_drive_8
            elif self.stroke_pos_current == -9:
                self.img = self.img_drive_9
            elif self.stroke_pos_current == -10:
                self.img = self.img_drive_10
            elif self.stroke_pos_current == -11:
                self.img = self.img_drive_11
            elif self.stroke_pos_current <= -12:
        	    self.img = self.img_drive_12        										
        elif self.current_stroke_type == RECOVERY_STROKE:			
            if self.stroke_pos_current >= 0:
                self.img = self.img_recovery_0
            elif self.stroke_pos_current == -1:
                self.img = self.img_recovery_1
            elif self.stroke_pos_current == -2:
                self.img = self.img_recovery_2
            elif self.stroke_pos_current == -3:
                self.img = self.img_recovery_3
            elif self.stroke_pos_current == -4:	        
                self.img = self.img_recovery_4
            elif self.stroke_pos_current == -5:
                self.img = self.img_recovery_5
            elif self.stroke_pos_current == -6:
                self.img = self.img_recovery_6
            elif self.stroke_pos_current == -7:
                self.img = self.img_recovery_7
            elif self.stroke_pos_current == -8:
                self.img = self.img_recovery_8
            elif self.stroke_pos_current == -9:
                self.img = self.img_recovery_9
            elif self.stroke_pos_current == -10:
                self.img = self.img_recovery_10
            elif self.stroke_pos_current == -11:
                self.img = self.img_recovery_11
            elif self.stroke_pos_current <= -12:
        	    self.img = self.img_recovery_12
        
        self.update_stroke_data(self.stroke_pos_change)       
        return self.r_y

    def update_stroke_data(self, stroke_pos_change):
        if stroke_pos_change != 0:
            if stroke_pos_change <= -1:
                self.current_stroke_type = DRIVE_STROKE
            else:
                self.current_stroke_type = RECOVERY_STROKE

            if self.current_stroke_type == DRIVE_STROKE and self.full_extent:
                self.part_stroke = True
            elif self.current_stroke_type == RECOVERY_STROKE and not self.full_extent:
                self.part_stroke = True

            if self.stroke_pos_current <= -12:
                self.full_extent = True
                self.part_stroke = False

            if self.stroke_pos_current <= -1:
                if not self.stroke_attempted:
                    self.stroke_attempted = True
                    #setting start time here is a bit weak as we have already completed one revolution of the sensor by this point
                    self.current_stroke_start_time = datetime.datetime.now()

            if self.stroke_pos_current >= 0:
                if self.stroke_attempted:
                    self.current_stroke_end_time = datetime.datetime.now()
                    self.stroke_count += 1                    
                    self.stroke_attempted = False
                self.full_extent = False
                self.part_stroke = False
                    			
    def render_ghost(self, screen, viewable_max_r, game_view):                
        if game_view == OVERHEAD:            
            temp = viewable_max_r - self.r_y        
            r_in_pix = self.get_new_r_in_pixels(temp, 1, OVERHEAD) 
            img_x = self.x - 50
            img_y = r_in_pix           
            screen.blit(self.img, (img_x, img_y))
            
            myfont = pg.font.SysFont("Roboto Condensed", 18)
            label = myfont.render(self.date_label, 1, GREEN)
            date_label_x = self.x - 45
            date_label_y = r_in_pix + 150
            screen.blit(label, (date_label_x, date_label_y))

            label = myfont.render(self.time_label, 1, WHITE)
            time_label_x = self.x - 35
            time_label_y = r_in_pix + 170            
            screen.blit(label, (time_label_x, time_label_y))
        
        elif game_view == SIDE:            
            temp = viewable_max_r - self.r_y        
            r_in_pix = self.get_new_r_in_pixels(temp, 1, SIDE)            
            img_width = self.img.get_rect().width                                                    
            img_height = self.img.get_rect().height                                                 
            img_x = r_in_pix - (img_width/2)
            #img_x = r_in_pix - 300
            img_y = self.y
            screen.blit(self.img, (img_x, img_y))
                        
            myfont = pg.font.SysFont("Roboto Condensed", 15)
            label = myfont.render(self.date_label, 1, BLUE)
            date_label_x = r_in_pix - ((img_width/2) + 80)
            date_label_y = self.y            
            #date_label_y = self.y + ((img_height) * 0.2)            
            screen.blit(label, (date_label_x, date_label_y))
            
            label = myfont.render(self.time_label, 1, ORANGE)
            time_label_x = r_in_pix - ((img_width/2) + 75)
            time_label_y = self.y + 20
            #time_label_y = self.y + ((img_height * 0.6) + 4)
            screen.blit(label, (time_label_x, time_label_y))
     
    def is_offscreen_and_behind_player(self, viewable_min_r, viewable_max_r, game_view):        
        if game_view == OVERHEAD:
            return self.r_y < viewable_min_r
        elif game_view == SIDE:
            if self.r_y < viewable_min_r:            
                offscreen_diff = self.r_y - viewable_min_r            
                min_onscreen_point = 0 - (self.img.get_width()/2)                                              
                r_in_pix = WIN_WIDTH - self.get_new_r_in_pixels(offscreen_diff, 1, SIDE)
          
                return r_in_pix < min_onscreen_point                
            else:
                return False            
                
    def is_offscreen_and_ahead_of_player(self, viewable_min_r, viewable_max_r, game_view):        
        if self.r_y > viewable_max_r:            
            #okay, it's at least partly offscreen so check further to see if all of the image is offscreen
            offscreen_diff = viewable_max_r - self.r_y            
            if game_view == OVERHEAD:
                return self.get_new_r_in_pixels(offscreen_diff, 1, OVERHEAD) < (0 - self.img.get_height())
            elif game_view == SIDE:                                                
                max_onscreen_point = WIN_WIDTH + (self.img.get_width()/2)                 
                r_in_pix = self.get_new_r_in_pixels(offscreen_diff, 1, SIDE)
                return r_in_pix > max_onscreen_point                                                             
        else:
            return False        
            
    def blit(self, screen, viewable_min_r, viewable_max_r, game_view):        
        if self.is_offscreen_and_behind_player(viewable_min_r, viewable_max_r, game_view):                        
            self.offscreen_marker.draw(screen, POINT_BACK, viewable_min_r, viewable_max_r, self.x, self.y, self.r_y, game_view)                            
        elif self.is_offscreen_and_ahead_of_player(viewable_min_r, viewable_max_r, game_view):            
            self.offscreen_marker.draw(screen, POINT_AHEAD, viewable_min_r, viewable_max_r, self.x, self.y, self.r_y, game_view)                            
        else:
            self.render_ghost(screen, viewable_max_r, game_view)
