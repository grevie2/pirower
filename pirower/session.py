import datetime
from constants import RESET_SESSION, STOP_SESSION, SESSION_COMPLETED
from constants import NUM_SECONDS_BEFORE_END_SESSION_WARNING
from constants import NUM_SECONDS_TIMEOUT, NUM_SECONDS_BEFORE_TIMEOUT_WARNING
from constants import NUM_SECONDS_BEFORE_TIMEOUT_CRITICAL_WARNING
from constants import STOPWATCH_COLOUR, RED, GREEN, WHITE
from constants import STOPWATCH_UPT, SCREEN_MSG, GHOST_UPT, STROKE_UPT, PLAYER_UPT, FISH_UPT
from time_utils import timedelta_milliseconds, convert_ms_to_elapsed
from sample import Sample
from global_variables import IRq, user_event_q

class session(object):
    def __init__(self):
        global IRq
        global user_event_q
        self.session_start_time = 0
        self.session_end_time = 0
        self.sess_complete = 0
        self.timestamp_ary = []
        self.ir_ary = []
        self.elapsed_time = 0
        self.update_lst = []
        self.sample_cnt = 0
        self.speed_sample_cnt = 0
        self.display_sample = 0
        self.timeout_time = ""

    def update_time_remaining(self, remaining_ms):
        remaining_sec = remaining_ms/1000
        stopwatch = convert_ms_to_elapsed(remaining_ms)
        if remaining_sec <= NUM_SECONDS_BEFORE_END_SESSION_WARNING:
            return [STOPWATCH_UPT, stopwatch, RED]
        else:
            return [STOPWATCH_UPT, stopwatch, STOPWATCH_COLOUR]

    def run(self, q, gui_q, session_start_time, session_end_time, display_sample):
        self.sess_complete = False
        remaining_ms = 0
        self.session_start_time = session_start_time        
        self.session_end_time = session_end_time
        self.sample_cnt = 1
        self.speed_sample_cnt = 0
        self.timeout_time = ""
        self.display_sample = display_sample
        sample = Sample()
        self.sample = 0
        while not self.sess_complete:
            sample_end_time = self.get_next_sample_end_time()
            sample.collect_sample(q, self.session_start_time, self.session_end_time, sample_end_time)
            self.update_lst = []

            if datetime.datetime.now() < self.session_end_time:
                remaining_ms = timedelta_milliseconds(self.session_end_time - datetime.datetime.now())

                #apply time remaining GUI update
                self.update_lst.append(self.update_time_remaining(remaining_ms))
                sp_change = sample.get_stroke_pos_change()
                r_change = sample.get_flywheel_change()

                #apply stroke pos change GUI update and data update
                self.update_lst.append([STROKE_UPT, sp_change])
                stroke_updates = sample.get_sample_ir_updates()
                if len(stroke_updates) > 0:
                    self.ir_ary.extend(stroke_updates)

                #apply flywheel GUI update and data update
                self.update_lst.append([PLAYER_UPT, r_change])
                flywheel_updates = sample.get_sample_flywheel_updates()
                if len(flywheel_updates) > 0:
                    self.timestamp_ary.extend(flywheel_updates)

                sample.reset()

                if r_change == 0:
                    if self.timeout_time == "":
                        self.timeout_time = datetime.datetime.now() + datetime.timedelta(seconds=NUM_SECONDS_TIMEOUT)
                    else:
                        timedelta = self.timeout_time - datetime.datetime.now()
                        to_seconds_remaining = int(timedelta.total_seconds())
                        if to_seconds_remaining <= 0:
                            self.update_lst.append([STOPWATCH_UPT, "TIMEOUT", RED])
                            self.update_lst.append([SCREEN_MSG, "TIMEOUT", RED])
                            self.sess_complete = True
                        elif to_seconds_remaining < NUM_SECONDS_BEFORE_TIMEOUT_CRITICAL_WARNING:
                            msg = "TIMEOUT IN " + str(to_seconds_remaining)
                            self.update_lst.append([SCREEN_MSG, msg, RED])
                        elif to_seconds_remaining < NUM_SECONDS_BEFORE_TIMEOUT_WARNING:
                            msg = "TIMEOUT IN " + str(to_seconds_remaining)
                            self.update_lst.append([SCREEN_MSG, msg, WHITE])
                else:
                    self.timeout_time = ""
                    #clear warning
                    self.update_lst.append([SCREEN_MSG, "", WHITE])

                self.update_lst.append([GHOST_UPT, True])
                self.update_lst.append([FISH_UPT, True])
            else:
                self.update_lst.append([STOPWATCH_UPT, "FINISH", GREEN])
                self.sess_complete = True

            gui_q.put(self.update_lst)

            if not user_event_q.empty():
                item_list = user_event_q.get_nowait()
                for item in item_list:
                    if item[0] == RESET_SESSION:
                        return RESET_SESSION
                    elif item[0] == STOP_SESSION:
                        return STOP_SESSION
        return SESSION_COMPLETED

    def get_ts_ary(self):
        return self.timestamp_ary

    def get_ir_ary(self):
        return self.ir_ary

    def get_next_sample_end_time(self):
        current_sample_end_time = self.session_start_time + (self.sample_cnt * datetime.timedelta(milliseconds=self.display_sample))
        self.sample_cnt += 1

        return current_sample_end_time
