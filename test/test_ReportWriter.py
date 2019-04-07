#! /usr/bin/python3
import unittest
import json
import sys
import os
sys.path.insert(0, '../')

from report_writer import ReportWriter
from constants import *

class TestReportWriter(unittest.TestCase):

    def test_write_JSON_report(self):
        flywheel_array = []
        flywheel_array.append('0:00:00.800000')
        flywheel_array.append('0:00:00.810000')
        flywheel_array.append('0:00:00.820000')
        flywheel_array.append('0:00:00.830000')
        ir_array = []
        ir_array.append(['0:00:00.800000',1])
        ir_array.append(['0:00:00.810000',2])
        ir_array.append(['0:00:00.820000',3])
        trial_time = 20
        rw = ReportWriter(flywheel_array, ir_array, trial_time, './')
        data_filename = rw.write_json_report()

        f = open(data_filename, "r")
        data = f.read()
        json_data = json.loads(data)
        f.close()
        timestamp_ary = []
        timestamp_ary = json_data['flywheel_times']
        ir_timestamp_ary = []
        ir_timestamp_ary = json_data['ir_times']

        self.assertEquals(timestamp_ary,flywheel_array)
        self.assertEquals(ir_timestamp_ary,ir_array)

        os.remove(data_filename)

if __name__ == "__main__":
    unittest.main()
