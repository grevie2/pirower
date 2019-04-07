#! /usr/bin/python3
import unittest
import sys
sys.path.insert(0, '../')

from timestampbatcher import TimestampBatcher

class TestTimestampBatcher(unittest.TestCase):

    def test_no_revolutions_in_a_sample(self):
        session_mins = 1
        flywheel_array = []
        tsb = TimestampBatcher(flywheel_array)
        converted_ary = tsb.convert_ts_array_to_display_array(session_mins, 1000)
        self.assertEquals(converted_ary[0], 0)

    def test_one_revolution_in_a_sample(self):
        session_mins = 1
        flywheel_array = []
        flywheel_array.append('800')
        tsb = TimestampBatcher(flywheel_array)
        converted_ary = tsb.convert_ts_array_to_display_array(session_mins, 1000)
        self.assertEquals(converted_ary[0], 1)

    def test_multiple_revolutions_in_a_sample(self):
        session_mins = 1
        flywheel_array = []
        flywheel_array.append('800')
        flywheel_array.append('810')
        flywheel_array.append('820')
        tsb = TimestampBatcher(flywheel_array)
        converted_ary = tsb.convert_ts_array_to_display_array(session_mins, 1000)
        self.assertEquals(converted_ary[0], 3)

    def test_multiple_samples(self):
        session_mins = 1
        flywheel_array = []
        flywheel_array.append('800')
        flywheel_array.append('810')
        flywheel_array.append('1800')
        flywheel_array.append('1810')
        tsb = TimestampBatcher(flywheel_array)
        converted_ary = tsb.convert_ts_array_to_display_array(session_mins, 1000)
        self.assertEquals(converted_ary[0], 2)
        self.assertEquals(converted_ary[1], 2)

    def test_no_activity_between_samples(self):
        session_mins = 1
        flywheel_array = []
        flywheel_array.append('100')
        flywheel_array.append('5100')
        tsb = TimestampBatcher(flywheel_array)
        converted_ary = tsb.convert_ts_array_to_display_array(session_mins, 1000)
        #self.assertEquals([1,0,0,0,0,1],converted_ary)
        self.assertEquals(converted_ary[0], 1)
        self.assertEquals(converted_ary[1], 0)
        self.assertEquals(converted_ary[2], 0)
        self.assertEquals(converted_ary[3], 0)
        self.assertEquals(converted_ary[4], 0)
        self.assertEquals(converted_ary[5], 1)

if __name__ == "__main__":
    unittest.main()
