#! /usr/bin/python3
import unittest
import time
import sys
sys.path.insert(0, '../')
import threading

from buttonpanel import *
from global_variables import *
from constants import *
from time_utils import timedelta_milliseconds

GPIO.setmode(GPIO.BOARD)

#button panel
for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j],1)

for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_string = ""

def run_button_panel_thread(duration):
    global button_string
    bp = ButtonPanel()

    start_time = datetime.datetime.now()
    end_time = start_time + (datetime.timedelta(seconds = duration))
    remaining_ms = timedelta_milliseconds(end_time - datetime.datetime.now())
    now = datetime.datetime.now()
    while button_string == "" and now < end_time:
        button_string = bp.check_for_button_input()
        time.sleep(0.2)
        now = datetime.datetime.now()

class TestButtonPanel(unittest.TestCase):
    global button_string
    def test_HandleButtonPress(self):
        duration = 4
        try:
            t = threading.Thread(target=run_button_panel_thread, args=(duration,))
            t.start()
        except:
            print "Error: Unable to start thread"

        print "press 1 on keypad"
        time.sleep(5)
        self.assertEqual(button_string, '1')

if __name__ == "__main__":
    unittest.main()
