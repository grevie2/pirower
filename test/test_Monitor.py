#! /usr/bin/python3
import unittest
import sys
sys.path.insert(0, '../')

from monitor import Monitor

class TestMonitor(unittest.TestCase):
    def test_one_pulses_per_update(self):
        num_required_samples = 40
        m = Monitor(num_required_samples)
        for i in range(0, num_required_samples):
            m.update(1)
        self.assertEqual(m.current_speed, 41.2)

    def test_two_pulses_per_update(self):
        num_required_samples = 40
        m = Monitor(num_required_samples)
        for i in range(0, num_required_samples):
            m.update(2)
        self.assertEqual(m.current_speed, 82.4)

    def test_not_enough_samples(self):
        num_required_samples = 40
        m = Monitor(num_required_samples)
        for i in range(0, num_required_samples-1):
            m.update(2)
        self.assertEqual(m.current_speed, 0)

    def test_speed_calculated_but_not_not_enough_samples_to_refresh(self):
        num_required_samples = 40
        m = Monitor(num_required_samples)
        for i in range(0, num_required_samples):
            m.update(1)
        for i in range(0, num_required_samples-1):
            m.update(5)
        self.assertEqual(m.current_speed, 41.2)

if __name__ == "__main__":
    unittest.main()
