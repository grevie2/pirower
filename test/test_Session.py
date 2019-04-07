#! /usr/bin/python3
import unittest
import thread
import time
import datetime
import sys
sys.path.insert(0, '../')

from session import session
from global_variables import *
from constants import *
from time_utils import *

def flywheel_simulated_input(num_spins,delay_between_spins):
    for i in range(0,num_spins):
        time.sleep(delay_between_spins)
        flywheel_q.put(datetime.datetime.now())

def ir_simulated_input(num_strokes, delay_between_ir):
    for i in range(0,num_strokes):
        for j in range(1, 4):
            time.sleep(delay_between_ir)
            IRq.put([datetime.datetime.now(),j])

class TestSession(unittest.TestCase):
    def add_n_spins_with_n_seconds_between_spins(self, num_spins, delay_between_spins):
        #start new thread that adds n flywheel spins with n seconds between spins
        try:
            thread.start_new_thread(flywheel_simulated_input,(num_spins,delay_between_spins,))
        except:
            print "Error: Unable to start thread"

    def add_n_strokes_with_n_seconds_between_ir(self, num_spins, delay_between_ir):
        #start new thread that adds n flywheel spins with n seconds between spins
        try:
            thread.start_new_thread(ir_simulated_input,(num_spins,delay_between_ir,))
        except:
            print "Error: Unable to start thread"

    def test_add_10_spins_with_0pt1_seconds_between_spins(self):
        s = session()
        self.add_n_spins_with_n_seconds_between_spins(10, 0.1)

        session_start_time = datetime.datetime.now()
        session_end_time = session_start_time + datetime.timedelta(seconds = 2)
        display_sample = 50
        retval = s.run(flywheel_q, gui_q, session_start_time, session_end_time, display_sample)
        self.assertEquals(retval,SESSION_COMPLETED)
        self.assertEquals(len(s.get_ts_ary()),10)

    def test_add_200_spins_with_0pt02_seconds_between_spins(self):
        s = session()
        self.add_n_spins_with_n_seconds_between_spins(200, 0.02)

        session_start_time = datetime.datetime.now()
        session_end_time = session_start_time + datetime.timedelta(seconds = 5)
        display_sample = 50
        retval = s.run(flywheel_q, gui_q, session_start_time, session_end_time, display_sample)
        self.assertEquals(retval,SESSION_COMPLETED)
        self.assertEquals(len(s.get_ts_ary()),200)

    def test_complete_20_strokes_with_0pt01_seconds_between_each_ir(self):
        s = session()
        self.add_n_strokes_with_n_seconds_between_ir(20, 0.01)

        session_start_time = datetime.datetime.now()
        session_end_time = session_start_time + datetime.timedelta(seconds = 1)
        display_sample = 50
        retval = s.run(flywheel_q, gui_q, session_start_time, session_end_time, display_sample)
        self.assertEquals(retval,SESSION_COMPLETED)
        self.assertEquals(len(s.get_ir_ary()),60)


if __name__ == "__main__":
    unittest.main()
