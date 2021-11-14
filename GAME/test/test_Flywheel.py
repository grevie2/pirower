#! /usr/bin/python3
import unittest
import thread
import time
import sys
import datetime
sys.path.insert(0, '../')

from flywheel import Flywheel
from global_variables import *
from constants import *
from time_utils import *

#NUM_SECONDS_INACTIVITY_PERIOD must be set to 6 for this test TODO: fix this

def flywheel_simulated_input(num_spins,delay_between_spins):
    for i in range(0,num_spins):
        time.sleep(delay_between_spins)
        flywheel_q.put(datetime.datetime.now())

class TestFlywheel(unittest.TestCase):

    def test_no_activity(self):
        f = Flywheel()
        start_waiting = datetime.datetime.now()
        second_count = f.wait_for_flywheel_to_stop(gui_q)
        finish_waiting = datetime.datetime.now()
        time_spent_waiting = timedelta_milliseconds(finish_waiting - start_waiting)
        self.assertAlmostEquals(time_spent_waiting/1000, NUM_SECONDS_INACTIVITY_PERIOD, 0)
        self.assertEqual(second_count, NUM_SECONDS_INACTIVITY_PERIOD)
        #TODO: assert gui_q contains stopwatch update and screen update

    def add_n_spins_with_n_seconds_between_spins(self, num_spins, delay_between_spins):
        f = Flywheel()
        #start new thread that adds n flywheel spins with n seconds between spins
        try:
            thread.start_new_thread(flywheel_simulated_input,(num_spins,delay_between_spins,))
        except:
            print "Error: Unable to start thread"

        start_waiting = datetime.datetime.now()
        second_count = f.wait_for_flywheel_to_stop(gui_q)
        finish_waiting = datetime.datetime.now()
        time_spent_waiting = timedelta_milliseconds(finish_waiting - start_waiting)/1000
        reset_time = NUM_SECONDS_INACTIVITY_PERIOD + (num_spins * delay_between_spins)
        self.assertAlmostEquals(time_spent_waiting, reset_time, 1)
        self.assertEquals(second_count, NUM_SECONDS_INACTIVITY_PERIOD, 0)

    def test_add_3_spins_with_1_seconds_between_spins(self):
        self.add_n_spins_with_n_seconds_between_spins(3, 1)

    def test_add_4_spins_with_1_seconds_between_spins(self):
        self.add_n_spins_with_n_seconds_between_spins(4, 1)

if __name__ == "__main__":
    unittest.main()
