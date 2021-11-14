from constants import IR_ONE, IR_ONE_CHANNEL, IR_ONE_LED_CHANNEL
from constants import IR_TWO, IR_TWO_CHANNEL, IR_TWO_LED_CHANNEL
from constants import IR_THREE, IR_THREE_CHANNEL, IR_THREE_LED_CHANNEL
from global_variables import IRq
import RPi.GPIO as GPIO
import datetime

def ir(channel):
    global IRq
    if channel == IR_ONE_CHANNEL:
        IRq.put([datetime.datetime.now(), IR_ONE])
        GPIO.output(IR_ONE_LED_CHANNEL,GPIO.HIGH)
        GPIO.output(IR_TWO_LED_CHANNEL,GPIO.LOW)
        GPIO.output(IR_THREE_LED_CHANNEL,GPIO.LOW)

    elif channel == IR_TWO_CHANNEL:
        IRq.put([datetime.datetime.now(), IR_TWO])
        GPIO.output(IR_ONE_LED_CHANNEL,GPIO.LOW)
        GPIO.output(IR_TWO_LED_CHANNEL,GPIO.HIGH)
        GPIO.output(IR_THREE_LED_CHANNEL,GPIO.LOW)

    elif channel == IR_THREE_CHANNEL:
        IRq.put([datetime.datetime.now(),IR_THREE])
        GPIO.output(IR_ONE_LED_CHANNEL,GPIO.LOW)
        GPIO.output(IR_TWO_LED_CHANNEL,GPIO.LOW)
        GPIO.output(IR_THREE_LED_CHANNEL,GPIO.HIGH)

    else:
        #something has gone wrong
        pass
