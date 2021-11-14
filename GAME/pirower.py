#! /usr/bin/python3

#sudo python pirower.py

import datetime
import threading
import RPi.GPIO as GPIO
from array import array
import pygame
from math import ceil

from global_variables import num_lanes, flywheel_q, IRq, gui_q, user_event_q, button_panel_event_q 

from fish import Fish
from checkpointmarker import CheckpointMarker
from buoy import Buoy
from prebatchghost import PreBatchGhost
from ontheflybatchghost import OnTheFlyBatchGhost

from player import Player


from ir_callbacks import ir
from flywheel_callbacks import increaserev
from flywheel import Flywheel
from report_writer import ReportWriter
from buttonpanel import ButtonPanel
from session import session
from settings_writer import SettingsWriter
from dateSetter import DateSetter
from ghost_selector import GhostSelector

from stage import *
from overhead_stage import OverheadStage

import sys
import time
import os

from constants import FANWHEEL_CHANNEL
from constants import IR_ONE_CHANNEL, IR_TWO_CHANNEL, IR_THREE_CHANNEL
from constants import IR_ONE_LED_CHANNEL, IR_TWO_LED_CHANNEL, IR_THREE_LED_CHANNEL
from constants import ROW, COL, DISPLAY, DEPTH

from constants import NO_GHOST_FILES_PRESENT, GHOST_JSON_PATH

from constants import OVERHEAD_PLAYER_IMAGE_PATH, OVERHEAD_GHOST_IMAGE_PATH, FISH_IMAGE_PATH, SETTINGS_JSON_FILE
from constants import SIDE_PLAYER_IMAGE_PATH, SIDE_GHOST_IMAGE_PATH

from constants import STOPWATCH_UPT, BUFFER, BUOY_AREA_WIDTH, VIEWABLE_HEIGHT_R 
from constants import SELECTOR, RESET, SYSTEM_DATE, SESSION_COMPLETED, MAX_PLAYERS
from constants import TRIAL_TIME, REFRESH_RATE, FISH, SELECTOR, RESET_SESSION, STOP_SESSION, SHUTDOWN
from constants import MULTILINE_MSG, BUTTON_MSG, SCREEN_MSG
from constants import BUOY_SIZE, BUOY_AREA_WIDTH, BUOY_AREA_MIN_X
from constants import EXIT, RESET
from constants import STOPWATCH_UPT, PLAYER_UPT, GHOST_UPT, FISH_UPT, STROKE_UPT
from constants import SYSTEM_DATE, SELECTOR, VIEWABLE_HEIGHT_R, NUM_ROWS
from constants import HELP_FONT_SIZE, STOPWATCH_FONT_SIZE, STOPWATCH_COLOUR, SYSTEM_TIME_FONT_SIZE, SCREEN_MSG_FONT_SIZE, BUTTON_MSG_FONT_SIZE
from constants import WHITE, GREEN, BLUE, RED, GREY, BLACK
from constants import PERSONAL_BESTS, PERSONAL_AVERAGES, PERSONAL_WORSTS
from constants import LABLE_FONT_SIZE_SML, LABEL_ORIGIN_X_BOTTOM, LABEL_SPACER_HORIZONTAL, LABEL_SPACER_VERTICAL_MIDDLE, LABEL_SPACER_VERTICAL_BOTTOM
from constants import WIN_WIDTH, WIN_HEIGHT
from constants import PRE_BATCH, ON_THE_FLY_BATCH
from constants import LEFT, MID
from constants import GAME_VIEW, OVERHEAD, SIDE, VIEWABLE_WIDTH_R



#flywheel
GPIO.setmode(GPIO.BOARD)
GPIO.setup(FANWHEEL_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(FANWHEEL_CHANNEL,GPIO.RISING, callback=increaserev)

#ir beams
GPIO.setup(IR_ONE_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(IR_ONE_CHANNEL,GPIO.FALLING, callback=ir)
GPIO.setup(IR_TWO_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(IR_TWO_CHANNEL,GPIO.FALLING, callback=ir)
GPIO.setup(IR_THREE_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(IR_THREE_CHANNEL,GPIO.FALLING, callback=ir)

#leds
GPIO.setup(IR_ONE_LED_CHANNEL, GPIO.OUT)
GPIO.setup(IR_TWO_LED_CHANNEL, GPIO.OUT)
GPIO.setup(IR_THREE_LED_CHANNEL, GPIO.OUT)

GPIO.output(IR_ONE_LED_CHANNEL,GPIO.LOW)
GPIO.output(IR_TWO_LED_CHANNEL,GPIO.LOW)
GPIO.output(IR_THREE_LED_CHANNEL,GPIO.LOW)

GPIO.output(IR_ONE_LED_CHANNEL,GPIO.HIGH)
GPIO.output(IR_TWO_LED_CHANNEL,GPIO.HIGH)
GPIO.output(IR_THREE_LED_CHANNEL,GPIO.HIGH)

#button panel
for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j],1)

for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

class sessionManager():
    def __init__(self):
        self.refresh_ghosts = True
        self.keep_looping = True
        self.wait_for_flywheel = True
        self.trial_time = 10
        self.old_datetime = datetime.datetime.now()
        self.new_datetime = datetime.datetime.now()
        self.num_fish = 20
        self.selector = PERSONAL_BESTS
        self.batch_mode = PRE_BATCH

    #1. Get a listing of all files that meet the ghost criteria (trial_length)
    #2. Find n number of ghosts that meet selector criteria, or the most we can get
    #3. Load those ghosts into the global ghosts array
    def load_ghosts(self, trial_length, max_players, selector, display_sample, filepath):
        global ghosts
        global gui_q
        ghosts = []

        s = GhostSelector()
        selected_ghost_files = s.select_ghost_files(trial_length, max_players, selector, filepath)

        if selected_ghost_files != NO_GHOST_FILES_PRESENT:
            #if GAME_VIEW == OVERHEAD:
            if self.game_view == OVERHEAD:
                for i in range(0, len(selected_ghost_files)):
                    filename = selected_ghost_files[i]
					
                    ghost_x = self.get_lane_pos_x(i, max_players)					
                    if self.batch_mode == PRE_BATCH:
                        g = PreBatchGhost(OVERHEAD_GHOST_IMAGE_PATH, filename, ghost_x, trial_length, display_sample)
                    else:
                        g = OnTheFlyBatchGhost(OVERHEAD_GHOST_IMAGE_PATH, filename, ghost_x, trial_length, display_sample)  
                    ghosts.append(g)
            #elif GAME_VIEW == SIDE:
            elif self.game_view == SIDE:
                if len(selected_ghost_files) >= 2:
                    spacing = 130               
                    filename = selected_ghost_files[0]
                    spacing += 55
                    if self.batch_mode == PRE_BATCH:
                        g = PreBatchGhost(SIDE_GHOST_IMAGE_PATH + "/150", filename, spacing, trial_length, display_sample, 1)
                    else:
                        g = OnTheFlyBatchGhost(SIDE_GHOST_IMAGE_PATH + "/150", filename, spacing, trial_length, display_sample, 1)  
                    ghosts.append(g)
                
                    filename = selected_ghost_files[1]
                    spacing += 55
                    if self.batch_mode == PRE_BATCH:
                        g = PreBatchGhost(SIDE_GHOST_IMAGE_PATH + "/250", filename, spacing, trial_length, display_sample, 1)
                    else:
                        g = OnTheFlyBatchGhost(SIDE_GHOST_IMAGE_PATH + "/250", filename, spacing, trial_length, display_sample, 1)  
                    ghosts.append(g)
					 
		
    def get_lane_pos_x(self, lane_num, num_tot_players):
        lane_width = BUOY_AREA_WIDTH/num_tot_players
        middle_lane = ceil(float(num_tot_players/2))

        if lane_num < middle_lane:
            #lower than middle lane number
            offset_x = (lane_width * lane_num) + (0.5 * lane_width)
        else:
            #higher than middle lane number
            offset_x = (lane_width * lane_num) + (1.5 * lane_width)

        ghost_x = BUFFER + offset_x
        return ghost_x

    def set_trial_time(self, gui_q, trial_time):
        update_lst = []
        update_lst.append([STOPWATCH_UPT, self.getFormattedTrialTime(trial_time), STOPWATCH_COLOUR])
        gui_q.put(update_lst)

    def getFormattedTrialTime(self, trial_time):
        d = datetime.timedelta(minutes=trial_time)
        return str(d) + ':0'

    def run(self):
        global flywheel_q
        global gui_q
        global num_rows
        global player        
        global num_lanes
        global user_event_q
        sw = SettingsWriter(SETTINGS_JSON_FILE)

        while self.keep_looping:
            if self.refresh_ghosts:
                settings = sw.read_json_settings()
                self.trial_time = settings['session_time']
                self.max_players = settings['num_ghost_players']
                num_lanes = self.max_players
                self.num_fish = settings['num_fish']
                self.refresh_rate_hz = settings['refresh_rate']
                self.display_sample = 1000/self.refresh_rate_hz
                self.selector = settings['selector']
                self.batch_mode = settings['batch_mode']
                #TODO: fix this
                num_required_samples = 2000/self.display_sample                
                self.game_view = settings['game_view']
                
                self.load_ghosts(self.trial_time, self.max_players, self.selector, self.display_sample, GHOST_JSON_PATH)
                
                if self.game_view == OVERHEAD:
                    player = Player(OVERHEAD_PLAYER_IMAGE_PATH, BUFFER + (BUOY_AREA_WIDTH * 0.5), num_required_samples, self.game_view, 1)
                elif self.game_view == SIDE:                               
                    player = Player(SIDE_PLAYER_IMAGE_PATH, BUFFER + (BUOY_AREA_WIDTH * 0.5), num_required_samples, self.game_view, 1)
                                              
                #resets everything - not just the number of fish
                gui_q.put([[RESET, self.num_fish, self.game_view]])
                
                #set the label to selector
                gui_q.put([[SELECTOR, self.selector]])
                
                if self.wait_for_flywheel:
                    f = Flywheel()
                    f.wait_for_flywheel_to_stop(gui_q)
                    self.wait_for_flywheel = False
                    #clear the IRq too!!!!
                    while not IRq.empty():
                        IRq.get()

                self.set_trial_time(gui_q, self.trial_time)
                self.refresh_ghosts = False

            elif not flywheel_q.empty() or not IRq.empty():
                self.run_session()
                gui_q.put([[RESET, self.num_fish, self.game_view]])

            self.refresh_date()
            self.process_user_events()

    def refresh_date(self):
        self.new_datetime = datetime.datetime.now()
        timedelta = self.new_datetime - self.old_datetime
        if int(timedelta.total_seconds()) > 1 or int(timedelta.total_seconds()) < -1:
            str_now = self.new_datetime.strftime("%d/%m/%Y %H:%M")
            self.old_datetime = self.new_datetime
            gui_q.put([[SYSTEM_DATE, str_now, WHITE]])

    def run_session(self):
        s = session()

        if not flywheel_q.empty():
            session_start_time = flywheel_q.get_nowait()
            flywheel_q.put(session_start_time)
        elif not IRq.empty():
            IRItem = IRq.get_nowait()
            session_start_time = IRItem[0]
            IRq.put(IRItem)

        session_end_time = session_start_time + datetime.timedelta(minutes = self.trial_time)
        retval = s.run(flywheel_q, gui_q, session_start_time, session_end_time, self.display_sample)

        if retval == SESSION_COMPLETED:
            ts_ary = s.get_ts_ary()
            ir_ary = s.get_ir_ary()
            r = ReportWriter(ts_ary, ir_ary, self.trial_time, GHOST_JSON_PATH)
            r.write_json_report()
            #new
            gui_q.put([[SELECTOR, 0]])
            self.refresh_ghosts = True
            self.wait_for_flywheel = True
        elif retval == RESET_SESSION:
            #the user stopped the session
            self.refresh_ghosts = True
            self.wait_for_flywheel = True
            self.switch_off_LEDs()
        elif retval == STOP_SESSION:
            self.switch_off_LEDs()
            self.keep_looping = False

    def process_user_events(self):
        if not user_event_q.empty():
            item_list = user_event_q.get_nowait()
            for item in item_list:
                if item[0] == MAX_PLAYERS:
                    self.max_players = item[1]
                    self.num_lanes = self.max_players
                    self.write_settings()
                    gui_q.put([[SELECTOR, 0]])
                    self.refresh_ghosts = True
                elif item[0] == TRIAL_TIME:
                    self.trial_time = item[1]
                    self.write_settings()
                    gui_q.put([[SELECTOR, 0]])
                    self.refresh_ghosts = True
                elif item[0] == FISH:
                    self.num_fish = item[1]
                    self.write_settings()
                    gui_q.put([[SELECTOR, 0]])
                    self.refresh_ghosts = True
                elif item[0] == STOP_SESSION:
                    self.keep_looping = False
                elif item[0] == RESET_SESSION:
                    self.write_settings()
                    gui_q.put([[SELECTOR, 0]])
                    self.refresh_ghosts = True
                elif item[0] == REFRESH_RATE:
                    self.refresh_rate_hz = item[1]
                    self.display_sample = 1000/self.refresh_rate_hz
                    self.write_settings()
                    gui_q.put([[SELECTOR, 0]])
                    self.refresh_ghosts = True
                elif item[0] == SELECTOR:
                    self.selector = item[1]
                    self.write_settings()
                    gui_q.put([[SELECTOR, 0]])
                    self.refresh_ghosts = True
                elif item[0] == PRE_BATCH:
                    self.batch_mode = PRE_BATCH
                    self.write_settings()
                    gui_q.put([[SELECTOR, 0]])
                    self.refresh_ghosts = True
                elif item[0] == ON_THE_FLY_BATCH:				
                    self.batch_mode = ON_THE_FLY_BATCH
                    self.write_settings()
                    gui_q.put([[SELECTOR, 0]])
                    self.refresh_ghosts = True
                elif item[0] == GAME_VIEW:
                    self.game_view = item[1]
                    self.write_settings()
                    self.refresh_ghosts = True									    
                    
    def write_settings(self):
        sw = SettingsWriter(SETTINGS_JSON_FILE)
        sw.write_json_settings(self.trial_time, self.max_players, self.num_fish, self.refresh_rate_hz, self.selector, self.batch_mode, self.game_view)

    def switch_off_LEDs(self):
        GPIO.output(IR_ONE_LED_CHANNEL,GPIO.LOW)
        GPIO.output(IR_TWO_LED_CHANNEL,GPIO.LOW)
        GPIO.output(IR_THREE_LED_CHANNEL,GPIO.LOW)

class userEventSubmitter():
    def run(self):
        global num_lanes
        global user_event_q

        helpDisplayed = False
        bp = ButtonPanel()
        keep_looping = True
                                                    
        while keep_looping:
            #only used if user presses ctrl+c
            if not button_panel_event_q.empty():
                item_list = button_panel_event_q.get_nowait()
                for item in item_list:
                    if item[0] == EXIT:
                        keep_looping = False

            buttonPressed = bp.check_for_button_input()
            if buttonPressed != "":
                if buttonPressed == 'A':
                    gui_q.put([[BUTTON_MSG, "", GREEN]])
                    if len(bp.button_string) > 0:
                        ds = DateSetter()
                        ds.set_system_date(bp.button_string)
                        bp.button_string = ""
                elif buttonPressed == 'B':
                    gui_q.put([[BUTTON_MSG, "", GREEN]])
                    if len(bp.button_string) > 0:
                        trial_time = int(bp.button_string)
                        user_event_q.put([[TRIAL_TIME, trial_time]])
                        bp.button_string = ""
                elif buttonPressed == 'C':
                    if len(bp.button_string) > 0:
                        key = int(bp.button_string)
                        bp.button_string = ""
                        gui_q.put([[BUTTON_MSG, "", GREEN]])
                        if key == 1:
                            user_event_q.put([[REFRESH_RATE, 10]])
                        elif key == 2:
                            gui_q.put([[BUTTON_MSG, "", GREEN]])
                            user_event_q.put([[REFRESH_RATE, 20]])
                        elif key == 4:
                            num_fish = 0
                            user_event_q.put([[FISH, num_fish]])                            
                        elif key == 5:
                            num_fish = 5
                            user_event_q.put([[FISH, num_fish]])                            
                        elif key == 6:
                            num_fish = 20
                            user_event_q.put([[FISH, num_fish]])                            
                        elif key == 7:
                            max_players = 1
                            num_lanes = max_players
                            user_event_q.put([[MAX_PLAYERS, max_players]])
                        elif key == 8:
                            max_players = 3
                            num_lanes = max_players
                            user_event_q.put([[MAX_PLAYERS, max_players]])
                        elif key == 9:
                            max_players = 5
                            num_lanes = max_players
                            user_event_q.put([[MAX_PLAYERS, max_players]])
                        elif key == 10:
                            user_event_q.put([[SELECTOR, PERSONAL_BESTS]])
                        elif key == 11:
                            user_event_q.put([[SELECTOR, PERSONAL_AVERAGES]])
                        elif key == 12:
                            user_event_q.put([[SELECTOR, PERSONAL_WORSTS]])
                elif buttonPressed == 'D':
                    if len(bp.button_string) > 0:
                        key = int(bp.button_string)
                        bp.button_string = ""
                        gui_q.put([[BUTTON_MSG, "", GREEN]])
                        if key == 1:
                            user_event_q.put([[RESET_SESSION],])
                        elif key == 2:
                            user_event_q.put([[STOP_SESSION],])
                            keep_looping = False
                            gui_q.put([[EXIT]])
                        elif key == 3:
                            user_event_q.put([[STOP_SESSION],])
                            keep_looping = False
                            gui_q.put([[SHUTDOWN]])
                        elif key == 4:
                            user_event_q.put([[PRE_BATCH],])
                        elif key == 5:
                            user_event_q.put([[ON_THE_FLY_BATCH],])
                        elif key == 6:                         
                            max_players = 5
                            num_lanes = max_players
                            #game view is only sent to the event queue so that it can be saved to the settings json file                            
                            user_event_q.put([[MAX_PLAYERS, max_players], [GAME_VIEW, OVERHEAD],[REFRESH_RATE, 20]]) #overhead view supports 5 players, and 20hz on Pi3 or Pi3b+
                            gui_q.put([[GAME_VIEW,OVERHEAD],])
                        elif key == 7:            
                            max_players = 3 #side view only supports 3 players
                            num_lanes = max_players                                                        
                            user_event_q.put([[MAX_PLAYERS, max_players], [GAME_VIEW, SIDE],[REFRESH_RATE, 10]]) #side view supports 3 players, and only 10hz on Pi3 or Pi3b+
                            gui_q.put([[GAME_VIEW, SIDE],])
                               
                elif buttonPressed == '*':
                    bp.button_string = bp.button_string[:-1]
                    gui_q.put([[BUTTON_MSG, bp.button_string, GREEN]])
                elif buttonPressed == '#':
                    if not helpDisplayed:
                        msgs = [['yyyymmddhhmm, A : Manually set clock', RED, MID],
                                        ['<numeric>, B : Set race period', RED, MID],
                                        ['1, C : Set refresh to 10Hz', RED, MID],
                                        ['2, C : Set refresh to 20Hz (Pi 3 only)', RED, MID],
                                        ['4, C : Set fish to 0', RED, MID],
                                        ['5, C : Set fish to 5', RED, MID],
                                        ['6, C : Set fish to 20', RED, MID],
                                        ['7, C : Set ghost players to 0', RED, MID],
                                        ['8, C : Set ghost players to 2', RED, MID],
                                        ['9, C : Set ghost players to 4', RED, MID],
                                        ['10, C : Select personal bests', RED, MID],
                                        ['11, C : Select personal averages', RED, MID],
                                        ['12, C : Select personal worsts', RED, MID],
                                        ['1, D : Reset', WHITE, MID],
                                        ['2, D : Exit to desktop', WHITE, MID],
                                        ['3, D : Exit and shutdown Pi', WHITE, MID],
                                        ['# : Help', WHITE, MID],
                                        ['* : Backspace', WHITE, MID],
                                        ['4, D : Set batch mode to pre-batch', RED, LEFT],
                                        ['5, D : Set batch mode to on-the-fly', RED, LEFT],
                                        ['6, D : Set view to overhead', RED, LEFT],
                                        ['7, D : Set view to side', RED, LEFT]]
                        gui_q.put([[MULTILINE_MSG, msgs]])
                        helpDisplayed = True
                    else:
                        gui_q.put([[MULTILINE_MSG,[['', WHITE, MID]]]])
                        helpDisplayed = False
                else:
                    bp.button_string += buttonPressed
                    gui_q.put([[BUTTON_MSG, bp.button_string, GREEN]])

            time.sleep(0.05)

def shutdown():
    cmd = "sudo halt"
    #print cmd
    os.system(cmd)

def main():
    g = GUIManager()
    g.run()

class GUIManager:
    def __init__(self):
        global gui_q
        global num_lanes
        global num_rows
        global player
        global user_event_q
        global button_panel_event_q

        self.selector = 0
        self.updateGhosts = False
        
    def run(self):
        position = 0,0
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

        pygame.init()
        #FLAGS = 0
        #FLAGS = NOFRAME
        FLAGS = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
        pygame.mouse.set_visible(False)
        try:
            sm = sessionManager()
            self.t = threading.Thread(target=sm.run, args=())
            self.t.start()

            ues = userEventSubmitter()
            self.t1 = threading.Thread(target=ues.run, args=())
            self.t1.start()
        except:
            print ("Error: Unable to start threads")

        pygame.display.set_caption("Pi-Rower")        
        self.checkpoint_marker = CheckpointMarker(0)        
        self.stage = Stage()
        self.overhead_stage = OverheadStage()
        
        self.run_main_loop()

    def run_main_loop(self):
        while 1:
            try:                
                #reset player r value
                self.r_change = 0
                self.stroke_pos_change = 0

                #respond to player input
                self.extract_updates()
                self.apply_updates()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        #any key press will exit the program                           
                        gui_q.put([[EXIT]])
                        user_event_q.put([[STOP_SESSION],])
                        button_panel_event_q.put([[EXIT]])

            except KeyboardInterrupt:
                #this is only relevant in windowed mode                
                gui_q.put([[EXIT]])
                user_event_q.put([[STOP_SESSION],])
                button_panel_event_q.put([[EXIT]])
            except:
                raise

    #TODO: I don't like this method, it should be part of something else
    def setup_buoys(self, num_lanes, num_rows):
        x=BUOY_AREA_MIN_X
        y=0-BUOY_SIZE/2
        buoys = []
        i=0
        j=0
        for i in range(0, num_rows):
            for j in range(0, num_lanes+1):
                b = Buoy(x, y)
                buoys.append(b)
                x += (BUOY_AREA_WIDTH / num_lanes)
                j += 1
            y += (VIEWABLE_HEIGHT_R / num_rows)
            x = BUOY_AREA_MIN_X
            i += 1
        return buoys

    def extract_updates(self):
		#NOTE: If the GUI thread takes too long then the event queue will keep getting bigger
        #print "gui_q.qsize() is ", gui_q.qsize()        
        update_lst = gui_q.get()
        for item in update_lst:
            if item[0] == SHUTDOWN:
                while self.t.isAlive():
                    pass
                while self.t1.isAlive():
                    pass                
                GPIO.cleanup()
                
                shutdown()
            if item[0] == EXIT:
                while self.t.isAlive():
                    pass
                while self.t1.isAlive():
                    pass
                GPIO.cleanup()
                sys.exit(0)
            elif item[0] == RESET:
                self.num_fish = item[1]
                self.game_view = item[2]  
                self.reset_values()
            elif item[0] == SCREEN_MSG:
                self.screen_msg = item[1]
                self.screen_msg_colour = item[2]
            elif item[0] == BUTTON_MSG:
                self.button_msg = item[1]
                self.button_msg_colour = item[2]
            elif item[0] == STOPWATCH_UPT:
                self.stopwatch = item[1]
                self.stopwatch_colour = item[2]
            elif item[0] == PLAYER_UPT:
                self.r_change = item[1]
                self.viewable_min_r += self.r_change
                self.viewable_max_r += self.r_change
            elif item[0] == GHOST_UPT:
                self.updateGhosts = True
            elif item[0] == FISH_UPT:
                self.updateFish = True
            elif item[0] == STROKE_UPT:
                self.stroke_pos_change = item[1]
            elif item[0] == MULTILINE_MSG:
                self.msgs = item[1]
            elif item[0] == SYSTEM_DATE:
                self.now = item[1]
            elif item[0] == SELECTOR:
                self.selector = item[1]
            elif item[0] == GAME_VIEW:
				self.game_view = item[1]
             
    def reset_values(self):        
        if self.game_view == OVERHEAD:
            self.viewable_min_r = 0 - (VIEWABLE_HEIGHT_R/2)
            self.viewable_max_r = 0 + (VIEWABLE_HEIGHT_R/2)
        else:
            self.viewable_min_r = 0 - (VIEWABLE_WIDTH_R/2)
            self.viewable_max_r = 0 + (VIEWABLE_WIDTH_R/2)
            
        self.r_total = 0
        self.loop_count = 0
        self.stroke_pos_current = 0
        self.selector = 0
        self.stopwatch = '0:00:00:0'
        self.stopwatch_colour = STOPWATCH_COLOUR
        self.buoys = self.setup_buoys(num_lanes, NUM_ROWS)
        self.button_msg = ""
        self.button_msg_colour = WHITE
        self.screen_msg = ""
        self.screen_msg_colour = WHITE
        self.msgs = ""
        self.now = ""
        self.updateGhosts = False
        self.updateFish = False
        self.overhead_stage.reset(self.num_fish, self.viewable_min_r, self.viewable_max_r)
        self.stage.reset()
                
    #this method also blits
    def apply_updates(self):
        if self.updateGhosts:
            for g in ghosts:
                g.update(self.viewable_min_r, self.viewable_max_r)                
            self.updateGhosts = False

        self.r_total = player.update(self.r_change, self.stroke_pos_change)        
                
        if self.game_view == OVERHEAD:
            self.overhead_stage.update(self.r_change, self.viewable_min_r, self.viewable_max_r, self.updateFish)
            self.updateFish = False
            self.overhead_stage.draw(self.screen, self.viewable_max_r)

            for b in self.buoys:
                result = b.update(self.screen, self.r_change)        
            checkpoint_r = self.checkpoint_marker.update(self.screen, self.viewable_min_r, self.viewable_max_r)
            
            for g in ghosts:                
                g.blit(self.screen, self.viewable_min_r, self.viewable_max_r, self.game_view)
                                                       
            player.blit(self.screen, self.viewable_min_r, self.viewable_max_r, self.game_view)
        
        elif self.game_view == SIDE:	
            self.stage.update(self.r_change)
            self.stage.draw(self.screen, self.viewable_min_r, self.viewable_max_r, ghosts, player)
            		                                                                                   						                               
        self.loop_count += 1

        self.display_button_msg()
        self.display_stopwatch()
        self.display_screen_msg()
        self.display_help_msgs()
        self.display_system_time()
        self.display_selector()
        pygame.display.update()

    def display_help_msgs(self):
        #each msg must have a colon
        myfont = pygame.font.SysFont("XXX",HELP_FONT_SIZE)
        y=WIN_HEIGHT*0.23
        for msg in self.msgs:            		
            text = msg[0]
            colour = msg[1]
            alignment = msg[2]
            if alignment == MID:	
                label = myfont.render(text, 1, colour)
                short_width = self.get_width_of_rendered_text_up_to_colon(myfont, text)
                x = (WIN_WIDTH / 2) - short_width				
                y+= WIN_HEIGHT * 0.035
                self.screen.blit(label, (x, y))
        
        #measuring up to the colon is redundant here - might want to change this        
        y=WIN_HEIGHT*0.23        
        for msg in self.msgs:            		
            text = msg[0]
            colour = msg[1]
            alignment = msg[2]
            if alignment == LEFT:	
                label = myfont.render(text, 1, colour)
                short_width = self.get_width_of_rendered_text_up_to_colon(myfont, text)
                x = 5			
                y+= WIN_HEIGHT * 0.035
                self.screen.blit(label, (x, y))

    def display_stopwatch(self):
        myfont = pygame.font.SysFont("Roboto Condensed",STOPWATCH_FONT_SIZE)
        label = myfont.render(self.stopwatch, 1, WHITE)
        offset_x = (WIN_WIDTH/2) - (label.get_rect().width/2)
        #TODO: fix this
        offset_x -= 3
        pt1 = (offset_x, LABEL_SPACER_VERTICAL_MIDDLE)
        pt2 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_MIDDLE)
        pt3 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_MIDDLE + label.get_rect().height)
        pt4 = (offset_x, LABEL_SPACER_VERTICAL_MIDDLE + label.get_rect().height)
        polygon = [pt1,pt2,pt3,pt4]
        pygame.draw.polygon(self.screen,BLUE,polygon)
        self.screen.blit(label, (offset_x, LABEL_SPACER_VERTICAL_MIDDLE))

    def display_system_time(self):
        myfont = pygame.font.SysFont("Roboto Condensed",SYSTEM_TIME_FONT_SIZE)
        #label = myfont.render(self.now, 1, (145,207,255))
        label = myfont.render(self.now, 1, (0,0,0))
        self.screen.blit(label,(30,70))

    def display_selector(self):

        if self.selector == PERSONAL_BESTS:
            pb_colour = GREEN
            pa_colour = GREY
            pw_colour = GREY
        elif self.selector == PERSONAL_AVERAGES:
            pb_colour = GREY
            pa_colour = GREEN
            pw_colour = GREY
        elif self.selector == PERSONAL_WORSTS:
            pb_colour = GREY
            pa_colour = GREY
            pw_colour = GREEN
        else:
            pb_colour = GREY
            pa_colour = GREY
            pw_colour = GREY

        myfont = pygame.font.SysFont("Roboto Condensed",LABLE_FONT_SIZE_SML)

        #pb
        offset_x = LABEL_ORIGIN_X_BOTTOM
        label = myfont.render("BST", 1, BLACK)
        pt1 = (offset_x, LABEL_SPACER_VERTICAL_BOTTOM)
        pt2 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_BOTTOM)
        pt3 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_BOTTOM + label.get_rect().height)
        pt4 = (offset_x, LABEL_SPACER_VERTICAL_BOTTOM + label.get_rect().height)
        polygon = [pt1,pt2,pt3,pt4]
        pygame.draw.polygon(self.screen,pb_colour,polygon)
        self.screen.blit(label, (offset_x, LABEL_SPACER_VERTICAL_BOTTOM))

        #pa
        offset_x = offset_x + label.get_rect().width + LABEL_SPACER_HORIZONTAL
        label = myfont.render("AVG", 1, BLACK)
        pt1 = (offset_x, LABEL_SPACER_VERTICAL_BOTTOM)
        pt2 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_BOTTOM)
        pt3 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_BOTTOM + label.get_rect().height)
        pt4 = (offset_x, LABEL_SPACER_VERTICAL_BOTTOM + label.get_rect().height)
        polygon = [pt1,pt2,pt3,pt4]
        pygame.draw.polygon(self.screen,pa_colour,polygon)
        self.screen.blit(label, (offset_x, LABEL_SPACER_VERTICAL_BOTTOM))

        #pw
        offset_x = offset_x + label.get_rect().width + LABEL_SPACER_HORIZONTAL
        label = myfont.render("WST", 1, BLACK)
        pt1 = (offset_x, LABEL_SPACER_VERTICAL_BOTTOM)
        pt2 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_BOTTOM)
        pt3 = (offset_x + label.get_rect().width, LABEL_SPACER_VERTICAL_BOTTOM + label.get_rect().height)
        pt4 = (offset_x, LABEL_SPACER_VERTICAL_BOTTOM + label.get_rect().height)
        polygon = [pt1,pt2,pt3,pt4]
        pygame.draw.polygon(self.screen,pw_colour,polygon)
        self.screen.blit(label, (offset_x, LABEL_SPACER_VERTICAL_BOTTOM))

    def display_screen_msg(self):
        myfont = pygame.font.SysFont("Roboto Condensed",SCREEN_MSG_FONT_SIZE)
        label = myfont.render(self.screen_msg, 1, self.screen_msg_colour)
        self.screen.blit(label,(WIN_WIDTH/2-label.get_rect().width/2,150))

    def display_button_msg(self):
        myfont = pygame.font.SysFont("Roboto Condensed",BUTTON_MSG_FONT_SIZE)
        label = myfont.render(self.button_msg, 1, self.button_msg_colour)
        self.screen.blit(label,(WIN_WIDTH/2-label.get_rect().width/2,WIN_HEIGHT*0.25))

    def get_width_of_rendered_text_up_to_colon(self, font, text):
        colon_pos = text.find(':')
        short_label = font.render(text[:colon_pos], 1, WHITE)
        return short_label.get_rect().width

if __name__ == "__main__":
    main()
