"""This class batches the ir entries according to interval"""
from datetime import datetime, timedelta
from strokesensorrecorder import StrokeSensorRecorder

class IRBatcher(object):
    def __init__(self, ts_array):
        self.ts_ary = ts_array

    def convert_stroke_array_to_display_array(self, interval):
        stroke_ary = []
        max_boundary = interval
        count = 0
        j = 0
        ss = StrokeSensorRecorder()

        if len(self.ts_ary) > 0:
            while j < len(self.ts_ary):
                current_element = self.ts_ary[j]
                current_elapsed = int(current_element[0])

                if current_elapsed < max_boundary:
                    ir_id = current_element[1]
                    count += ss.update(current_elapsed, ir_id)
                    j = j + 1
                    ss.reset_change()
                elif current_elapsed >= max_boundary:
                    stroke_ary.append(count)
                    count = 0
                    max_boundary += interval

            ss.reset_change()
            ir_id = current_element[1]
            count += ss.update(current_elapsed, ir_id)
            stroke_ary.append(count)
        return stroke_ary
