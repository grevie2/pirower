"""This class collects numeric button presses and """
import time
import RPi.GPIO as GPIO
from constants import MATRIX, ROW, COL

class ButtonPanel(object):
    def __init__(self):
        self.button_string = ""
        self.helpDisplayed = False
       
    def check_for_button_input(self):
        self.button_press = ""
        for j in range(4):
            GPIO.output(COL[j], 0)

            for i in range(4):
                if GPIO.input(ROW[i]) == 0:
                    self.button_press = MATRIX[i][j]
                    time.sleep(0.2)
                    while GPIO.input(ROW[i]) == 0:
                        pass
            GPIO.output(COL[j], 1)
        
        if self.button_press >= 0 and self.button_press <= 9:
            return str(self.button_press)
        else:
            return self.button_press
