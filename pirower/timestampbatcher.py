"""This class batches the flywheel timestamps according to interval"""
import datetime

def round_down(num, divisor):
    return num - (num%divisor)

NUM_MS_IN_A_MIN = 60000

class TimestampBatcher(object):
    def __init__(self, ts_array):
        self.ts_ary = ts_array

    def convert_ts_array_to_display_array(self, session_mins, interval):
        #create display array of required length which contains all zeroes
        display_ary = [0] * (session_mins * NUM_MS_IN_A_MIN)

        for t in self.ts_ary:
            #round down the milliseconds to nearest 50
            t_rounded = round_down(int(t), interval)
            element = int(t_rounded/interval)
            #increment element at the specified location by one
            display_ary[element] += 1

        return display_ary
