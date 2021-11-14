from entity import Entity
from constants import RECOVERY_STROKE, DRIVE_STROKE
from constants import WIN_HEIGHT, WIN_WIDTH
from constants import LABEL_FONT_SIZE, LABEL_ORIGIN_X_TOP, LABEL_SPACER_VERTICAL_TOP, LABEL_SPACER_HORIZONTAL
from constants import YELLOW, GREEN, GREY, BLACK, PALE_RED, WHITE, PURPLE, PURPLE2, ORANGE
from constants import GAME_VIEW, OVERHEAD, SIDE
import datetime
import pygame
from monitor import Monitor
from screen import get_r_in_pixels

class Player(Entity):
    def __init__(self, player_image_path, x, num_required_samples, game_view, layer_multiplier=1):
        Entity.__init__(self)
        self.player_image_path = player_image_path        
        self.r_y = 0        
        self.x = x
        self.stroke_pos_current = 0
        self.r_change = 0
        self.y = 0
        self.current_stroke_type = RECOVERY_STROKE
        self.stroke_count = 0
        self.part_stroke = False
        self.stroke_complete = False
        self.stroke_count = 0
        self.full_extent = False
        self.drive_complete = True
        self.recovery_complete = True
        self.stroke_attempted = False
        self.layer_multiplier = layer_multiplier
                
        self.spm = 0
        self.current_stroke_start_time = ""
        self.current_stroke_end_time = ""
                
        self.img_drive_0 = pygame.image.load(player_image_path + "/drive/rower_pos0.png").convert_alpha()
        self.img_drive_1 = pygame.image.load(player_image_path + "/drive/rower_pos1.png").convert_alpha()
        self.img_drive_2 = pygame.image.load(player_image_path + "/drive/rower_pos2.png").convert_alpha()        
        self.img_drive_3 = pygame.image.load(player_image_path + "/drive/rower_pos3.png").convert_alpha()
        self.img_drive_4 = pygame.image.load(player_image_path + "/drive/rower_pos4.png").convert_alpha()
        self.img_drive_5 = pygame.image.load(player_image_path + "/drive/rower_pos5.png").convert_alpha()
        self.img_drive_6 = pygame.image.load(player_image_path + "/drive/rower_pos6.png").convert_alpha()
        self.img_drive_7 = pygame.image.load(player_image_path + "/drive/rower_pos7.png").convert_alpha()
        self.img_drive_8 = pygame.image.load(player_image_path + "/drive/rower_pos8.png").convert_alpha()
        self.img_drive_9 = pygame.image.load(player_image_path + "/drive/rower_pos9.png").convert_alpha()
        self.img_drive_10 = pygame.image.load(player_image_path + "/drive/rower_pos10.png").convert_alpha()
        self.img_drive_11 = pygame.image.load(player_image_path + "/drive/rower_pos11.png").convert_alpha()
        self.img_drive_12 = pygame.image.load(player_image_path + "/drive/rower_pos12.png").convert_alpha()
        
        self.img_recovery_0 = pygame.image.load(player_image_path + "/recovery/rower_pos0.png").convert_alpha()
        self.img_recovery_1 = pygame.image.load(player_image_path + "/recovery/rower_pos1.png").convert_alpha()
        self.img_recovery_2 = pygame.image.load(player_image_path + "/recovery/rower_pos2.png").convert_alpha()
        self.img_recovery_3 = pygame.image.load(player_image_path + "/recovery/rower_pos3.png").convert_alpha()
        self.img_recovery_4 = pygame.image.load(player_image_path + "/recovery/rower_pos4.png").convert_alpha()
        self.img_recovery_5 = pygame.image.load(player_image_path + "/recovery/rower_pos5.png").convert_alpha()
        self.img_recovery_6 = pygame.image.load(player_image_path + "/recovery/rower_pos6.png").convert_alpha()
        self.img_recovery_7 = pygame.image.load(player_image_path + "/recovery/rower_pos7.png").convert_alpha()
        self.img_recovery_8 = pygame.image.load(player_image_path + "/recovery/rower_pos8.png").convert_alpha()
        self.img_recovery_9 = pygame.image.load(player_image_path + "/recovery/rower_pos9.png").convert_alpha()
        self.img_recovery_10 = pygame.image.load(player_image_path + "/recovery/rower_pos10.png").convert_alpha()
        self.img_recovery_11 = pygame.image.load(player_image_path + "/recovery/rower_pos11.png").convert_alpha()
        self.img_recovery_12 = pygame.image.load(player_image_path + "/recovery/rower_pos12.png").convert_alpha()
        
        self.player_image = self.img_drive_0

        self.monitor = Monitor(num_required_samples)
        
        #NOTE: this line assumes all player images are the same width
        if game_view == OVERHEAD:
			self.image_offset_x = x
			img_height = self.player_image.get_rect().height                
			self.image_offset_y = (WIN_HEIGHT/2) - (img_height/2)
        elif game_view == SIDE:
            img_width = self.player_image.get_rect().width                
            self.image_offset_x = (WIN_WIDTH/2) - (img_width/2)
            self.image_offset_y = 300 # TODO: might want to pass this in        

    def update(self, r_change, stroke_pos_change):
        self.stroke_pos_current += stroke_pos_change

        if self.current_stroke_type == DRIVE_STROKE:			
            if self.stroke_pos_current >= 0:
                self.player_image = self.img_drive_0
            elif self.stroke_pos_current == -1:
                self.player_image = self.img_drive_1
            elif self.stroke_pos_current == -2:
                self.player_image = self.img_drive_2
            elif self.stroke_pos_current == -3:
                self.player_image = self.img_drive_3
            elif self.stroke_pos_current == -4:	        
                self.player_image = self.img_drive_4
            elif self.stroke_pos_current == -5:
                self.player_image = self.img_drive_5
            elif self.stroke_pos_current == -6:
                self.player_image = self.img_drive_6
            elif self.stroke_pos_current == -7:
                self.player_image = self.img_drive_7
            elif self.stroke_pos_current == -8:
                self.player_image = self.img_drive_8
            elif self.stroke_pos_current == -9:
                self.player_image = self.img_drive_9
            elif self.stroke_pos_current == -10:
                self.player_image = self.img_drive_10
            elif self.stroke_pos_current == -11:
                self.player_image = self.img_drive_11
            elif self.stroke_pos_current <= -12:
        	    self.player_image = self.img_drive_12        										
        elif self.current_stroke_type == RECOVERY_STROKE:			
            if self.stroke_pos_current >= 0:
                self.player_image = self.img_recovery_0
            elif self.stroke_pos_current == -1:
                self.player_image = self.img_recovery_1
            elif self.stroke_pos_current == -2:
                self.player_image = self.img_recovery_2
            elif self.stroke_pos_current == -3:
                self.player_image = self.img_recovery_3
            elif self.stroke_pos_current == -4:	        
                self.player_image = self.img_recovery_4
            elif self.stroke_pos_current == -5:
                self.player_image = self.img_recovery_5
            elif self.stroke_pos_current == -6:
                self.player_image = self.img_recovery_6
            elif self.stroke_pos_current == -7:
                self.player_image = self.img_recovery_7
            elif self.stroke_pos_current == -8:
                self.player_image = self.img_recovery_8
            elif self.stroke_pos_current == -9:
                self.player_image = self.img_recovery_9
            elif self.stroke_pos_current == -10:
                self.player_image = self.img_recovery_10
            elif self.stroke_pos_current == -11:
                self.player_image = self.img_recovery_11
            elif self.stroke_pos_current <= -12:
        	    self.player_image = self.img_recovery_12
                   
        #the scaled images don't look very good
        #old_width = self.player_image.get_rect().width
        #new_width = int(old_width * 2.0)
        #old_height = self.player_image.get_rect().width
        #new_height = int(old_height * 2.0)
        #self.player_image = pygame.transform.scale(self.player_image, (new_width, new_height))

        self.update_stroke_data(stroke_pos_change)
        self.monitor.update(r_change)
        self.r_y += r_change
        self.r_change = r_change
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
                    #NOTE: setting start time here is a bit weak as we have already completed one revolution of the sensor by this point
                    self.current_stroke_start_time = datetime.datetime.now()

            if self.stroke_pos_current >= 0:
                if self.stroke_attempted:
                    self.current_stroke_end_time = datetime.datetime.now()
                    self.stroke_count += 1
                    self.calculate_spm()
                    self.stroke_attempted = False
                self.full_extent = False
                self.part_stroke = False

    def calculate_spm(self):
        if self.current_stroke_end_time != self.current_stroke_start_time:
            timedelta = self.current_stroke_end_time - self.current_stroke_start_time
            self.spm = int(60/timedelta.total_seconds())

    def get_r_total(self):
        return self.r_y

    def get_r_change(self):
        return self.r_change

    #TODO: sort this mess out
    def blit(self, screen, viewable_min_r, viewable_max_r, game_view):
        if game_view == OVERHEAD:
			#if it's onscreen then draw it
            if self.r_y >= viewable_min_r and self.r_y <= viewable_max_r:
                temp = viewable_max_r - self.r_y                
                #TODO: the player does not move on the screen!!!
                self.y = self.get_new_r_in_pixels(temp, 1, OVERHEAD)
                screen.blit(self.player_image, (self.x - 50, self.y))
                #screen.blit(self.player_image, (self.image_offset_x, self.image_offset_y))
                
        elif game_view == SIDE:
            #if it's onscreen then draw it
            if self.r_y >= viewable_min_r and self.r_y <= viewable_max_r:
                temp = viewable_max_r - self.r_y                
                #TODO: the player does not move on the screen!!!
                self.y = self.get_new_r_in_pixels(temp, 1, SIDE)
                #screen.blit(self.player_image, (self.x - 50, self.y))
                screen.blit(self.player_image, (self.image_offset_x, self.image_offset_y))
            
        self.render_labels(screen)

    #TODO: All this label code could be in a separate class
    def render_labels(self, screen):
        myfont = pygame.font.SysFont("Roboto Condensed",LABEL_FONT_SIZE)

        #drive
        offset_x = LABEL_ORIGIN_X_TOP
        string = "DRIVE"
        label = myfont.render(string, 1, BLACK)
        pt1 = (offset_x, LABEL_SPACER_VERTICAL_TOP)
        pt2 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP)
        pt3 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        pt4 = (offset_x, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        polygon = [pt1,pt2,pt3,pt4]
        if self.current_stroke_type == DRIVE_STROKE:
            if self.part_stroke:
                pygame.draw.polygon(screen,YELLOW,polygon)
            else:
                pygame.draw.polygon(screen,GREEN,polygon)
        else:
            pygame.draw.polygon(screen,GREY,polygon)
        screen.blit(label, (offset_x, LABEL_SPACER_VERTICAL_TOP))

        #recovery
        #myfont.set_bold(True)
        offset_x = offset_x + label.get_rect().width + LABEL_SPACER_HORIZONTAL
        string = "RECOVERY"
        label = myfont.render(string, 1, BLACK)
        pt1 = (offset_x, LABEL_SPACER_VERTICAL_TOP)
        pt2 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP)
        pt3 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        pt4 = (offset_x, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        polygon = [pt1,pt2,pt3,pt4]
        if self.current_stroke_type == RECOVERY_STROKE:
            if self.part_stroke:
                pygame.draw.polygon(screen,YELLOW,polygon)
            else:
                pygame.draw.polygon(screen,GREEN,polygon)
        else:
            pygame.draw.polygon(screen,GREY,polygon)
        screen.blit(label, (offset_x, LABEL_SPACER_VERTICAL_TOP))

        #stk
        offset_x = offset_x + label.get_rect().width + LABEL_SPACER_HORIZONTAL
        padded_count = (str(self.stroke_count)).zfill(4)
        string = "STK " + padded_count
        label = myfont.render(string, 1, WHITE)
        pt1 = (offset_x, LABEL_SPACER_VERTICAL_TOP)
        pt2 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP)
        pt3 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        pt4 = (offset_x, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        polygon = [pt1, pt2, pt3, pt4]
        pygame.draw.polygon(screen, PURPLE, polygon)
        screen.blit(label, (offset_x, LABEL_SPACER_VERTICAL_TOP))

        #avg
        offset_x = offset_x + label.get_rect().width + LABEL_SPACER_HORIZONTAL
        padded_spm = (str(self.spm)).zfill(2)
        string = "STK/MIN " + padded_spm
        label = myfont.render(string, 1, WHITE)
        pt1 = (offset_x, LABEL_SPACER_VERTICAL_TOP)
        pt2 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP)
        pt3 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        pt4 = (offset_x, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        polygon = [pt1, pt2, pt3, pt4]
        pygame.draw.polygon(screen, PURPLE2, polygon)
        screen.blit(label, (offset_x, LABEL_SPACER_VERTICAL_TOP))

        #spd
        offset_x = offset_x + label.get_rect().width + LABEL_SPACER_HORIZONTAL
        formatted_str = self.format_value(self.monitor.current_speed)
        label = myfont.render("SPD " + formatted_str, 1, WHITE)
        pt1 = (offset_x, LABEL_SPACER_VERTICAL_TOP)
        pt2 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP)
        pt3 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        pt4 = (offset_x, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        polygon = [pt1,pt2,pt3,pt4]
        pygame.draw.polygon(screen,ORANGE,polygon)
        screen.blit(label, (offset_x, LABEL_SPACER_VERTICAL_TOP))

        #dist
        offset_x = offset_x + label.get_rect().width + LABEL_SPACER_HORIZONTAL
        formatted_dist = self.format_value(self.monitor.current_dist)
        label = myfont.render("DST " + formatted_dist, 1, WHITE)
        pt1 = (offset_x, LABEL_SPACER_VERTICAL_TOP)
        pt2 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP)
        pt3 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        pt4 = (offset_x, LABEL_SPACER_VERTICAL_TOP + label.get_rect().height)
        polygon = [pt1,pt2,pt3,pt4]
        pygame.draw.polygon(screen,PALE_RED,polygon)
        screen.blit(label, (offset_x, LABEL_SPACER_VERTICAL_TOP))

        #if it has a decimal point, split in two, prefix and postfix with zeroes, stick parts together
    def format_value(self, value):
        s = str(round(value,2))
        formatted_dist = ""
        if '.' in s:
            dec_pos = s.find('.')
            s1 = (s[:dec_pos]).zfill(2)
            s2 = (s[dec_pos+1:])
            if len(s2) == 1:
                s2 += '0'
            formatted_str = s1 + '.' + s2
        else:
            formatted_str = s.zfill(2) + '.00'
        return formatted_str
