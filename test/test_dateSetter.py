#! /usr/bin/python3
import unittest

import time
import sys
sys.path.insert(0, '../')

from dateSetter import DateSetter

class TestDateSetter(unittest.TestCase):


    def test_MonthName(self):
        ds = DateSetter()
        MonNameLookup = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', \
                         '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec', \
                         'rubbish':-1}
        for key, value in MonNameLookup.iteritems():
            mon = ds.get_month_name(key)
            self.assertEqual(mon, value)

if __name__ == "__main__":
    unittest.main()
