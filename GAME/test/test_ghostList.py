#! /usr/bin/python3
import unittest
import sys
import os
import time
import datetime
sys.path.insert(0, '../')

from ghostlist import GhostList
from global_variables import *
from constants import *

class TestGhostList(unittest.TestCase):

    def test_different_flywheel_values_present_pb_selected(self):
        f1 = "session_01min_000300_20180219195252.json"
        f2 = "session_01min_000400_20180219195252.json"
        f3 = "session_01min_000200_20180219195252.json"
        files = []
        files.append(f1)
        files.append(f2)
        files.append(f3)
        trial_length = 1
        for filename in files:
            f = open(filename, "w")
            f.close()

        s = GhostList(trial_length, '.')
        sorted_files = s.get_ghost_filelist(PERSONAL_BESTS)

        for filename in files:
            os.remove(filename)

        self.assertEquals(sorted_files, [f2, f1, f3], 0)

    def test_different_flywheel_values_present_pw_selected(self):
        f1 = "session_01min_000300_20180219195252.json"
        f2 = "session_01min_000400_20180219195252.json"
        f3 = "session_01min_000200_20180219195252.json"
        files = []
        files.append(f1)
        files.append(f2)
        files.append(f3)
        trial_length = 1
        for filename in files:
            f = open(filename, "w")
            f.close()

        s = GhostList(trial_length, '.')
        sorted_files = s.get_ghost_filelist(PERSONAL_WORSTS)

        for filename in files:
            os.remove(filename)

        self.assertEquals(sorted_files, [f3, f1, f2], 0)

    def test_same_flywheel_values_but_different_dates_pb_selected(self):
        f1 = "session_01min_000400_20160219120500.json"
        f2 = "session_01min_000400_20170219120500.json"
        f3 = "session_01min_000400_20180219120500.json"
        files = []
        files.append(f1)
        files.append(f2)
        files.append(f3)
        trial_length = 1
        for filename in files:
            f = open(filename, "w")
            f.close()

        s = GhostList(trial_length, '.')
        sorted_files = s.get_ghost_filelist(PERSONAL_BESTS)

        for filename in files:
            os.remove(filename)

        self.assertEquals(sorted_files, [f3, f2, f1], 0)

    def test_no_files_present(self):
        trial_length = 1
        s = GhostList(trial_length, '.')
        sorted_files = s.get_ghost_filelist(PERSONAL_WORSTS)

        self.assertEquals(sorted_files, [], 0)

    def test_same_flywheel_values_but_different_dates_pw_selected(self):
        f1 = "session_01min_000400_20160219120500.json"
        f2 = "session_01min_000400_20170219120500.json"
        f3 = "session_01min_000400_20180219120500.json"
        files = []
        files.append(f1)
        files.append(f2)
        files.append(f3)
        trial_length = 1
        for filename in files:
            f = open(filename, "w")
            f.close()

        s = GhostList(trial_length, '.')
        sorted_files = s.get_ghost_filelist(PERSONAL_WORSTS)

        for filename in files:
            os.remove(filename)

        self.assertEquals(sorted_files, [f1, f2, f3], 0)

    def test_different_flywheel_values_but_same_dates_pa_selected(self):
        f1 = "session_01min_000400_20170219120500.json"
        f2 = "session_01min_000300_20170219120500.json"
        f3 = "session_01min_000200_20170219120500.json"
        f4 = "session_01min_000100_20170219120500.json"
        files = []
        files.append(f1)
        files.append(f2)
        files.append(f3)
        files.append(f4)
        trial_length = 1
        for filename in files:
            f = open(filename, "w")
            f.close()

        s = GhostList(trial_length, '.')
        sorted_files = s.get_ghost_filelist(PERSONAL_AVERAGES)

        for filename in files:
            os.remove(filename)

        self.assertEquals(sorted_files, [f1, f2, f3, f4], 0)

if __name__ == "__main__":
    unittest.main()
