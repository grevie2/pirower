#! /usr/bin/python3
import unittest
import sys
import os
import time
import datetime
sys.path.insert(0, '../')


from global_variables import *
from constants import *
from ghost_selector import *

class TestGhostSelector(unittest.TestCase):

    def test_5players_3files_diffflywheel_pa(self):
        f1 = "session_01min_000300_20180219195252.json"
        f2 = "session_01min_000400_20180219195252.json"
        f3 = "session_01min_000200_20180219195252.json"
        files = []
        files.append(f1)
        files.append(f2)
        files.append(f3)
        trial_length = 1
        max_players = 5
        selector = PERSONAL_AVERAGES
        filepath = '.'
        for filename in files:
            f = open(filename, "w")
            f.close()

        s = GhostSelector()
        sorted_files = s.select_ghost_files(trial_length, max_players, selector, filepath)

        for filename in files:
            os.remove(filename)

        self.assertEquals(sorted_files, [f2, f1, f3], 0)

    def test_5players_6files_diffflywheel_pa(self):
        f1 = "session_01min_000400_20170219120500.json"
        f2 = "session_01min_000300_20170219120500.json"
        f3 = "session_01min_000200_20170219120500.json"
        f4 = "session_01min_000100_20170219120500.json"
        f5 = "session_01min_000600_20170219120500.json"
        f6 = "session_01min_000601_20170219120500.json"
        files = []
        files.append(f1)
        files.append(f2)
        files.append(f3)
        files.append(f4)
        files.append(f5)
        files.append(f6)
        trial_length = 1
        max_players = 5
        selector = PERSONAL_AVERAGES
        filepath = '.'
        for filename in files:
            f = open(filename, "w")
            f.close()

        s = GhostSelector()
        sorted_files = s.select_ghost_files(trial_length, max_players, selector, filepath)

        for filename in files:
            os.remove(filename)

        self.assertEquals(sorted_files, [f5, f1, f2, f3], 0)

    def test_3players_6files_diffflywheel_pa(self):
        f1 = "session_01min_000400_20170219120500.json"
        f2 = "session_01min_000300_20170219120500.json"
        f3 = "session_01min_000200_20170219120500.json"
        f4 = "session_01min_000100_20170219120500.json"
        f5 = "session_01min_000600_20170219120500.json"
        f6 = "session_01min_000601_20170219120500.json"
        files = []
        files.append(f1)
        files.append(f2)
        files.append(f3)
        files.append(f4)
        files.append(f5)
        files.append(f6)
        trial_length = 1
        max_players = 3
        selector = PERSONAL_AVERAGES
        filepath = '.'
        for filename in files:
            f = open(filename, "w")
            f.close()

        s = GhostSelector()
        sorted_files = s.select_ghost_files(trial_length, max_players, selector, filepath)

        for filename in files:
            os.remove(filename)

        self.assertEquals(sorted_files, [f1, f2], 0)

    def test_3players_2files_diffflywheel_pa(self):
        f1 = "session_01min_000400_20170219120500.json"
        f2 = "session_01min_000300_20170219120500.json"
        files = []
        files.append(f1)
        files.append(f2)
        trial_length = 1
        max_players = 3
        selector = PERSONAL_AVERAGES
        filepath = '.'
        for filename in files:
            f = open(filename, "w")
            f.close()

        s = GhostSelector()
        sorted_files = s.select_ghost_files(trial_length, max_players, selector, filepath)

        for filename in files:
            os.remove(filename)

        self.assertEquals(sorted_files, [f1, f2], 0)

    def test_3players_2files_sameflywheel_pa(self):
        f1 = "session_01min_000400_20170219120500.json"
        f2 = "session_01min_000400_20180219120500.json"
        files = []
        files.append(f1)
        files.append(f2)
        trial_length = 1
        max_players = 3
        selector = PERSONAL_AVERAGES
        filepath = '.'
        for filename in files:
            f = open(filename, "w")
            f.close()

        s = GhostSelector()
        sorted_files = s.select_ghost_files(trial_length, max_players, selector, filepath)

        for filename in files:
            os.remove(filename)

        self.assertEquals(sorted_files, [f2, f1], 0)

    def test_1player_2files_sameflywheel_pa(self):
        f1 = "session_01min_000500_20170219120500.json"
        f2 = "session_01min_000400_20180219120500.json"
        files = []
        files.append(f1)
        files.append(f2)
        trial_length = 1
        max_players = 2
        selector = PERSONAL_BESTS
        filepath = '.'
        for filename in files:
            f = open(filename, "w")
            f.close()

        s = GhostSelector()
        sorted_files = s.select_ghost_files(trial_length, max_players, selector, filepath)

        for filename in files:
            os.remove(filename)

        self.assertEquals(sorted_files, [f1], 0)
if __name__ == "__main__":
    unittest.main()
