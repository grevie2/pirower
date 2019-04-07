#! /usr/bin/python3
import unittest
import thread

import sys
import datetime
sys.path.insert(0, '../')


from global_variables import *
from constants import *
from time_utils import *
from player import *
import time

FLAGS = pygame.FULLSCREEN
screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)

class TestPlayer(unittest.TestCase):

    def test_part_drive_and_back_to_start(self):
        num_required_samples = 50
        player = Player('../' + OVERHEAD_PLAYER_IMAGE_PATH, BUFFER + (BUOY_AREA_WIDTH * 0.5), num_required_samples, OVERHEAD, 1)
        for i in range(0, 3):
            player.update(0, (-1))
        for i in range(0, 3):
            player.update(0, (1))

        self.assertEqual(player.current_stroke_type, RECOVERY_STROKE)
        self.assertEqual(player.stroke_pos_current, 0)
        self.assertEqual(player.part_stroke, False)
        self.assertEqual(player.stroke_count, 1)

    def test_full_drive_full_recovery(self):
        num_required_samples = 50
        player = Player('../' + OVERHEAD_PLAYER_IMAGE_PATH, BUFFER + (BUOY_AREA_WIDTH * 0.5), num_required_samples, OVERHEAD, 1)
        for i in range(0, 13):
            player.update(0, (-1))
        for i in range(0, 13):
            player.update(0, (1))

        self.assertEqual(player.current_stroke_type, RECOVERY_STROKE)
        self.assertEqual(player.stroke_pos_current, 0)
        self.assertEqual(player.part_stroke, False)
        self.assertEqual(player.stroke_count, 1)

    def test_part_drive_part_recovery_part_drive(self):
        num_required_samples = 50
        player = Player('../' + OVERHEAD_PLAYER_IMAGE_PATH, BUFFER + (BUOY_AREA_WIDTH * 0.5), num_required_samples, OVERHEAD, 1)
        for i in range(0, 5):
            player.update(0, (-1))
        for i in range(0, 3):
            player.update(0, (1))
        for i in range(0, 2):
            player.update(0, (-1))

        self.assertEqual(player.current_stroke_type, DRIVE_STROKE)
        self.assertEqual(player.stroke_pos_current, -4)
        self.assertEqual(player.part_stroke, True)
        self.assertEqual(player.stroke_count, 0)

    def test_part_recovery_part_drive_part_recovery(self):
        num_required_samples = 50
        player = Player('../' + OVERHEAD_PLAYER_IMAGE_PATH, BUFFER + (BUOY_AREA_WIDTH * 0.5), num_required_samples, OVERHEAD, 1)
        for i in range(0, 5):
            player.update(0, (-1))
        for i in range(0, 2):
            player.update(0, (1))
        for i in range(0, 2):
            player.update(0, (-1))
        for i in range(0, 3):
            player.update(0, (1))

        self.assertEqual(player.current_stroke_type, RECOVERY_STROKE)
        self.assertEqual(player.stroke_pos_current, -2)
        self.assertEqual(player.part_stroke, True)
        self.assertEqual(player.stroke_count, 0)

    def test_part_recovery_and_back_to_end(self):
        num_required_samples = 50
        player = Player('../' + OVERHEAD_PLAYER_IMAGE_PATH, BUFFER + (BUOY_AREA_WIDTH * 0.5), num_required_samples, OVERHEAD, 1)
        for i in range(0, 10):
            player.update(0, (-1))
        for i in range(0, 2):
            player.update(0, (1))
        for i in range(0, 4):
            player.update(0, (-1))

        self.assertEqual(player.current_stroke_type, DRIVE_STROKE)
        self.assertEqual(player.stroke_pos_current, -12)
        self.assertEqual(player.part_stroke, False)
        self.assertEqual(player.stroke_count, 0)

    def test_multiple_rowing_strokes_in_a_single_update(self):
        num_required_samples = 50
        player = Player('../' + OVERHEAD_PLAYER_IMAGE_PATH, BUFFER + (BUOY_AREA_WIDTH * 0.5), num_required_samples, OVERHEAD, 1)
        for i in range(0, 1):
            player.update(0, (-5))
        for i in range(0, 1):
            player.update(0, (5))

        self.assertEqual(player.current_stroke_type, RECOVERY_STROKE)
        self.assertEqual(player.stroke_pos_current, 0)
        self.assertEqual(player.part_stroke, False)
        self.assertEqual(player.stroke_count, 1)

    def test_multiple_rowing_strokes(self):
        num_required_samples = 50
        player = Player('../' + OVERHEAD_PLAYER_IMAGE_PATH, BUFFER + (BUOY_AREA_WIDTH * 0.5), num_required_samples, OVERHEAD, 1)
        for i in range(0, 12):
            player.update(0, (-1))
        for i in range(0, 12):
            player.update(0, (1))
        for i in range(0, 12):
            player.update(0, (-1))
        for i in range(0, 12):
            player.update(0, (1))

        self.assertEqual(player.current_stroke_type, RECOVERY_STROKE)
        self.assertEqual(player.stroke_pos_current, 0)
        self.assertEqual(player.part_stroke, False)
        self.assertEqual(player.stroke_count, 2)

    def test_spm(self):
        num_required_samples = 50
        player = Player('../' + OVERHEAD_PLAYER_IMAGE_PATH, BUFFER + (BUOY_AREA_WIDTH * 0.5), num_required_samples, OVERHEAD, 1)
        for i in range(0, 3):
            player.update(0, (-1))
        time.sleep(1)
        for i in range(0, 3):
            player.update(0, (1))

        self.assertEqual(player.current_stroke_type, RECOVERY_STROKE)
        self.assertEqual(player.stroke_pos_current, 0)
        self.assertEqual(player.part_stroke, False)
        self.assertEqual(player.stroke_count, 1)
        self.assertEqual(player.spm, 59)


if __name__ == "__main__":
    unittest.main()
