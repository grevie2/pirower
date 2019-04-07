#! /usr/bin/python3
import unittest
import json

import sys
import os
sys.path.insert(0, '../')

from settings_writer import SettingsWriter
from constants import PERSONAL_BESTS, PRE_BATCH, OVERHEAD


class TestSettingsWriter(unittest.TestCase):

    def test_write_read_JSON_settings(self):
        session_time = 20
        num_ghost_players = 4
        num_fish = 20
        refresh_rate = 10
        selector = PERSONAL_BESTS
        batch_mode = PRE_BATCH
        settings_filename = './test_settings.json'
        sw = SettingsWriter(settings_filename)
        game_view = OVERHEAD

        sw.write_json_settings(session_time, num_ghost_players, num_fish, refresh_rate, selector, batch_mode, game_view)
        settings = sw.read_json_settings()
        os.remove(settings_filename)

        self.assertEquals(settings['session_time'], session_time)
        self.assertEquals(settings['num_ghost_players'], num_ghost_players)
        self.assertEquals(settings['num_fish'], num_fish)
        self.assertEquals(settings['refresh_rate'], refresh_rate)
        self.assertEquals(settings['selector'], selector)
        self.assertEquals(settings['batch_mode'], batch_mode)
        
if __name__ == "__main__":
    unittest.main()
