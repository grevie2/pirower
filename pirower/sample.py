"""Collects a sample of size up to sample end time"""

#from datetime import datetime
from strokesensorrecorder import StrokeSensorRecorder
from flywheel_recorder import FlywheelRecorder
from global_variables import IRq
from time_utils import timedelta_milliseconds
import datetime

class Sample(object):
    def __init__(self):
        self.ssr = StrokeSensorRecorder()
        self.fwr = FlywheelRecorder()
        self.elapsed_time = 0

    def collect_sample(self, flywheel_q, session_start_time, session_end_time, sample_end_time):
        sample_current_time = datetime.datetime.now()
        while sample_current_time < sample_end_time and sample_current_time < session_end_time:
            if not flywheel_q.empty():
                flywheel_time = flywheel_q.get_nowait()
                self.elapsed_time = flywheel_time - session_start_time
                self.elapsed_time = timedelta_milliseconds(self.elapsed_time)
                self.fwr.update(self.elapsed_time)

            if not IRq.empty():
                item = IRq.get_nowait()
                ir_time = item[0]
                new_ir = item[1]
                self.elapsed_time = ir_time - session_start_time
                self.elapsed_time = timedelta_milliseconds(self.elapsed_time)
                self.ssr.update(self.elapsed_time, new_ir)

            sample_current_time = datetime.datetime.now()

    def get_sample_flywheel_updates(self):
        return self.fwr.flywheel_updates

    def get_sample_ir_updates(self):
        return self.ssr.get_ir_pos_updates()

    def get_stroke_pos_change(self):
        return self.ssr.get_stroke_pos_change()

    def get_flywheel_change(self):
        return self.fwr.get_change()

    def reset(self):
        self.fwr.reset_change()
        self.ssr.reset_change()
