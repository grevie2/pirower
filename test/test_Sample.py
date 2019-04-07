#! /usr/bin/python3
import unittest
import thread
import time
import datetime
import sys
sys.path.insert(0, '../')

from sample import Sample
from global_variables import *
from constants import *
from time_utils import *

ANTICLOCKWISE = 0
CLOCKWISE = 1

def flywheel_simulated_input(num_spins,delay_between_spins):
    for i in range(0,num_spins):
        time.sleep(delay_between_spins)
        flywheel_q.put(datetime.datetime.now())

def ir_simulated_input(num_irspins, delay_between_ir, direction):
    for i in range(0, num_irspins):
        if direction == ANTICLOCKWISE:
            for j in range(3, 0, -1):
                time.sleep(delay_between_ir)
                IRq.put([datetime.datetime.now(),j])
        elif direction == CLOCKWISE:
            for j in range(1, 4):
                time.sleep(delay_between_ir)
                IRq.put([datetime.datetime.now(),j])

class TestSample(unittest.TestCase):
    def add_n_spins_with_n_seconds_between_spins(self, num_spins, delay_between_spins):
    #start new thread that adds n flywheel spins with n seconds between spins
        try:
            thread.start_new_thread(flywheel_simulated_input,(num_spins,delay_between_spins,))
        except:
            print "Error: Unable to start thread"

    def add_n_irspins_with_n_seconds_between_ir(self, num_spins, delay_between_ir, direction):
        #start new thread that adds n flywheel spins with n seconds between spins
        try:
            thread.start_new_thread(ir_simulated_input,(num_spins,delay_between_ir,direction,))
        except:
            print "Error: Unable to start thread"

    def test_add_10_spins_with_0pt1_seconds_between_spins(self):
        s = Sample()
        session_start_time = datetime.datetime.now()
        session_end_time = session_start_time + datetime.timedelta(seconds = 3)
        sample_end_time = session_start_time + datetime.timedelta(seconds = 2)
        self.add_n_spins_with_n_seconds_between_spins(10, 0.1)
        s.collect_sample(flywheel_q, session_start_time, session_end_time, sample_end_time)
        self.assertEquals(s.get_flywheel_change(),10)
        self.assertEquals(len(s.get_sample_flywheel_updates()),10)

    def test_0_spins(self):
        s = Sample()
        session_start_time = datetime.datetime.now()
        session_end_time = session_start_time + datetime.timedelta(seconds = 3)
        sample_end_time = session_start_time + datetime.timedelta(seconds = 2)
        s.collect_sample(flywheel_q, session_start_time, session_end_time, sample_end_time)
        self.assertEquals(s.get_flywheel_change(),0)
        self.assertEquals(len(s.get_sample_flywheel_updates()),0)

    def test_complete_12_anticlockwise_irspins_with_0pt01_seconds_between_each_ir(self):
        s = Sample()
        session_start_time = datetime.datetime.now()
        session_end_time = session_start_time + datetime.timedelta(seconds = 3)
        sample_end_time = session_start_time + datetime.timedelta(seconds = 2)
        self.add_n_irspins_with_n_seconds_between_ir(12, 0.01, ANTICLOCKWISE)
        s.collect_sample(flywheel_q, session_start_time, session_end_time, sample_end_time)
        self.assertEquals(s.get_stroke_pos_change(),-12)
        self.assertEquals(len(s.get_sample_ir_updates()),36)

    def test_complete_11_anticlockwise_irspins_with_0pt01_seconds_between_each_ir(self):
        s = Sample()
        session_start_time = datetime.datetime.now()
        session_end_time = session_start_time + datetime.timedelta(seconds = 3)
        sample_end_time = session_start_time + datetime.timedelta(seconds = 2)
        self.add_n_irspins_with_n_seconds_between_ir(11, 0.01, ANTICLOCKWISE)
        s.collect_sample(flywheel_q, session_start_time, session_end_time, sample_end_time)
        self.assertEquals(s.get_stroke_pos_change(),-11)
        self.assertEquals(len(s.get_sample_ir_updates()),33)

    #note: the limit is 12
    def test_complete_20_anticlockwise_irspins_with_0pt01_seconds_between_each_ir(self):
        s = Sample()
        session_start_time = datetime.datetime.now()
        session_end_time = session_start_time + datetime.timedelta(seconds = 3)
        sample_end_time = session_start_time + datetime.timedelta(seconds = 2)
        self.add_n_irspins_with_n_seconds_between_ir(12, 0.01, ANTICLOCKWISE)
        s.collect_sample(flywheel_q, session_start_time, session_end_time, sample_end_time)
        self.assertEquals(s.get_stroke_pos_change(),-12)
        self.assertEquals(len(s.get_sample_ir_updates()),36)

    def test_complete_2_clockwise_irspins_with_0pt01_seconds_between_each_ir(self):
        s = Sample()
        #since this test starts at IR_ONE, we'll say the 'old' IR was IR_THREE
        s.ssr.old_ir = IR_THREE
        session_start_time = datetime.datetime.now()
        session_end_time = session_start_time + datetime.timedelta(seconds = 3)
        sample_end_time = session_start_time + datetime.timedelta(seconds = 2)
        self.add_n_irspins_with_n_seconds_between_ir(2, 0.01, CLOCKWISE)
        s.collect_sample(flywheel_q, session_start_time, session_end_time, sample_end_time)
        self.assertEquals(s.get_stroke_pos_change(),2)
        self.assertEquals(len(s.get_sample_ir_updates()),6)

if __name__ == "__main__":
    unittest.main()
